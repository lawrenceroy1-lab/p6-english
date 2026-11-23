// Unit page: loads content/unitXX.json. Each tab is one book lesson; each lesson has its own activities.

const params = new URLSearchParams(location.search);
const UNIT_ID = params.get("u") || "05";
let DATA = null;
let secIdx = 0;
let act = "learn";
let mode = "";               // "" = a lesson, "practice", "test" or "battle" = whole-unit modes
let cleanup = null;          // stops timers when leaving an activity

const ACTS = [
  { id: "learn", e: "📘", name: "Learn", th: "เรียนรู้", has: s => s.learn && s.learn.length },
  { id: "words", e: "🖼️", name: "Word Cards", th: "บัตรคำศัพท์", has: s => s.words && s.words.length },
  { id: "book",  e: "📖", name: "Student Book", th: "หนังสือเรียน", has: s => s.book && s.book.length },
  { id: "wb",    e: "📒", name: "Workbook", th: "แบบฝึกหัด", has: s => s.wb && s.wb.length },
  { id: "speak", e: "🗣️", name: "Speak", th: "ฝึกพูด", has: s => s.speak },
  { id: "spell", e: "🎧", name: "Listen and Spell", th: "ฟังแล้วสะกด", has: s => s.spell && s.spell.length },
  { id: "flash", e: "🃏", name: "Flashcards", th: "บัตรคำ", has: s => flashCards(s).length },
  { id: "match", e: "🧩", name: "Match Game", th: "เกมจับคู่", has: s => s.match && s.match.length },
  { id: "sort",  e: "🪣", name: "Sort It", th: "เกมแยกกลุ่ม", has: s => s.sort },
  { id: "build", e: "🧱", name: "Sentence Builder", th: "เกมเรียงประโยค", has: s => s.build && s.build.length },
  { id: "quiz",  e: "⚡", name: "Speed Quiz", th: "ตอบเร็ว", has: s => s.quiz && s.quiz.length },
  { id: "battle", e: "🏆", name: "Class Battle", th: "แข่งขันในห้อง", has: s => s.quiz && s.quiz.length && isTeacher() }
];

const view = () => document.getElementById("view");
// Units 5 to 8 have numbers; Review and Irregular Verbs do not.
const unitNo = () => isNaN(+DATA.unit) ? DATA.unit : Number(DATA.unit);
const unitName = d => isNaN(+d.unit) ? d.title : `Unit ${Number(d.unit)}: ${d.title}`;
const fig = () => "";                       // (maths diagrams: not used on the English site)
const img = (src, alt, cls) => src ? `<img class="${cls || "wimg"}" src="${src}" alt="${esc(alt || "")}" loading="lazy" decoding="async" onerror="this.style.display='none'">` : "";

// ---------- Load ----------
fetch(`content/unit${UNIT_ID}.json`, { cache: "no-cache" })
  .then(r => { if (!r.ok) throw new Error(); return r.json(); })
  .then(async d => {
    await loadThai(UNIT_ID);
    DATA = d;
    document.title = `${unitName(d)} | P.6 English with T. Roy`;
    document.getElementById("unitTitle").innerHTML = `${esc(unitName(d))} <span class="small">📖 ${esc(d.pages)}</span>`;
    readHash();
    renderTabs();
    go(true);
  })
  .catch(() => { document.getElementById("unitTitle").textContent = "This unit is coming soon 🙂"; });
askName(false);

function readHash() {
  const h = new URLSearchParams(location.hash.slice(1));
  const s = parseInt(h.get("s"), 10);
  if (!isNaN(s) && DATA.sections[s]) secIdx = s;
  if (ACTS.some(a => a.id === h.get("a"))) act = h.get("a");
  mode = ["practice", "test", "battle"].includes(h.get("m")) ? h.get("m") : "";
}
window.addEventListener("hashchange", () => { if (DATA && !window.TEST_RUNNING) { readHash(); renderTabs(); go(); } });
function writeHash() { history.replaceState(null, "", mode ? `#m=${mode}` : `#s=${secIdx}&a=${act}`); }

function renderTabs() {
  document.getElementById("unitBar").innerHTML = `
    <button class="ubtn practice ${mode === "practice" ? "on" : ""}" data-m="practice">${U("✏️ Practice", "ฝึกทำ")}</button>
    <button class="ubtn test ${mode === "test" ? "on" : ""}" data-m="test">${U("📝 Unit Test", "แบบทดสอบ")}</button>
    ${isTeacher() ? `<button class="ubtn battle ${mode === "battle" ? "on" : ""}" data-m="battle">🏆 Class Battle</button>` : ""}
    <a class="ubtn board" href="leaderboard.html?u=${UNIT_ID}">${U("🏅 Leaderboard", "อันดับคะแนน")}</a>${thaiSwitch()}`;
  document.getElementById("thSw").onclick = () => {
    if (window.TEST_RUNNING) return alert("Please finish the Unit Test first.");
    store.set("thai", !thaiOn()); BANK = null; renderTabs(); go();
  };
  const leaveOk = () => !window.TEST_RUNNING || confirm("Leave the Unit Test? Your answers will be lost.");
  document.querySelectorAll(".ubtn[data-m]").forEach(b => b.onclick = () => { if (!leaveOk()) return; mode = b.dataset.m; renderTabs(); go(); });
  document.getElementById("tabs").innerHTML = DATA.sections.map((s, i) =>
    `<button class="tab ${!mode && i === secIdx ? "on" : ""}" data-i="${i}">${esc(s.short || s.title)}${thOf(s.short || s.title) ? `<span class="th">${thOf(s.short || s.title)}</span>` : ""}</button>`).join("");
  document.querySelectorAll(".tab").forEach(b => b.onclick = () => { if (!leaveOk()) return; mode = ""; secIdx = +b.dataset.i; act = firstAct(); renderTabs(); go(); });
  const acts = document.getElementById("acts");
  acts.style.display = mode ? "none" : "";
  const sec = DATA.sections[secIdx];
  const list = ACTS.filter(a => a.has(sec));
  if (!list.some(a => a.id === act)) act = list[0].id;
  const seen = new Set(store.get(`seen_${UNIT_ID}`, []));
  acts.innerHTML = list.map(a =>
    `<button class="act ${a.id === act ? "on" : ""} ${seen.has(sec.id + ":" + a.id) ? "seen" : ""}" data-a="${a.id}"><span class="e">${a.e}</span>${U(a.name, a.th)}</button>`).join("");
  document.querySelectorAll(".act").forEach(b => b.onclick = () => { act = b.dataset.a; renderTabs(); go(); });
}
function firstAct() { return ACTS.find(a => a.has(DATA.sections[secIdx])).id; }
function actList() { return ACTS.filter(a => a.has(DATA.sections[secIdx])); }

function go(first) {
  if (cleanup) { cleanup(); cleanup = null; }
  if ("speechSynthesis" in window) speechSynthesis.cancel();
  writeHash();
  if (mode === "practice") Practice();
  else if (mode === "test") UnitTest();
  else if (mode === "battle") Battle({ title: "Whole unit", quiz: null }, true);
  else {
    const sec = DATA.sections[secIdx];
    const seen = new Set(store.get(`seen_${UNIT_ID}`, [])); seen.add(sec.id + ":" + act); store.set(`seen_${UNIT_ID}`, [...seen]);
    ({ learn: Learn, words: Words, book: s => Exercises(s, "book"), wb: s => Exercises(s, "wb"), speak: Speak, spell: Spell,
       flash: Flash, match: Match, sort: Sort, build: Build, quiz: Quiz, battle: Battle })[act](sec);
  }
  if (!first) window.scrollTo({ top: document.getElementById("unitBar").offsetTop - 10, behavior: "smooth" });
}

// "Next activity" button at the end of an activity (and "Next lesson" at the end of a lesson)
function nextActBtn() {
  const list = actList(), k = list.findIndex(a => a.id === act);
  if (k >= 0 && k < list.length - 1) return `<button class="bigbtn dark" id="nextAct">${U(`Next: ${list[k + 1].e} ${list[k + 1].name} ➡`, "กิจกรรมถัดไป")}</button>`;
  if (secIdx < DATA.sections.length - 1) return `<button class="bigbtn dark" id="nextAct">${U(`Next lesson: ${DATA.sections[secIdx + 1].short} ➡`, "บทเรียนถัดไป")}</button>`;
  return `<button class="bigbtn dark" id="nextAct">${U("✏️ Go to Practice ➡", "ไปฝึกทำ")}</button>`;
}
function wireNextAct() {
  const b = document.getElementById("nextAct");
  if (!b) return;
  b.onclick = () => {
    const list = actList(), k = list.findIndex(a => a.id === act);
    if (k >= 0 && k < list.length - 1) act = list[k + 1].id;
    else if (secIdx < DATA.sections.length - 1) { secIdx++; act = firstAct(); }
    else mode = "practice";
    renderTabs(); go();
  };
}

function header(sec, title, extra) {
  return `<div class="panel-title"><h2>${title}</h2>${extra || ""}</div>
          <p class="small" style="margin-top:-6px">${tb(sec.title)} · 📖 ${esc(sec.pages)}</p>`;
}

// A numbered list of every card / question, on the right (below on phones). Tap one to jump to it.
const plain = h => String(h || "").replace(/<span class="th">.*?<\/span>/g, "").replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
const short = (h, n = 46) => { const t = plain(h); return t.length > n ? t.slice(0, n - 1) + "…" : t; };
function sideList(title, names, cur, marks) {
  return `<nav class="sidelist no-print" aria-label="${esc(plain(title))}"><h3>${title}</h3>${names.map((nm, k) =>
    `<button class="${k === cur ? "on" : ""}" data-j="${k}"><span class="n">${k + 1}</span><span>${esc(nm)}${marks && marks[k] ? " " + marks[k] : ""}</span></button>`).join("")}</nav>`;
}
function withSide(main, side) { return `<div class="with-side"><div class="side-main">${main}</div>${side}</div>`; }
function onJump(f) {
  view().querySelectorAll(".sidelist button").forEach(b => b.onclick = () => { f(+b.dataset.j); });
  const on = view().querySelector(".sidelist button.on");
  if (on && on.parentElement.scrollHeight > on.parentElement.clientHeight) on.parentElement.scrollTop = on.offsetTop - 80;
}
function backNext(i, n, ids) {
  return `<div class="btnrow">
    <button class="bigbtn grey" id="${ids[0]}" ${i === 0 ? "disabled" : ""}>${U("⬅ Back", "ย้อนกลับ")}</button>
    ${i < n - 1 ? `<button class="bigbtn" id="${ids[1]}">${U("Next ➡", "ถัดไป")}</button>` : nextActBtn()}</div>`;
}
const on = (id, f) => { const el = document.getElementById(id); if (el) el.onclick = f; };

// =============== LEARN (teaching cards: blue) ===============
function Learn(sec) {
  let i = 0;
  const cards = sec.learn;
  function draw() {
    const c = cards[i];
    view().innerHTML = `<div class="panel">${header(sec, U("📘 Learn", "เรียนรู้"))}${withSide(`
      <div class="learn-card">
        <span class="tag ${c.tag === "Example" ? "ex" : ""}">${esc(c.tag || "Learn")}</span>
        ${c.page ? `<span class="badge pg">${c.page}</span>` : ""}
        <h3>${tb(c.title)}</h3>
        ${img(c.img, c.title, "limg")}
        ${(c.lines || []).map(l => `<p>${tb(l)}</p>`).join("")}
        ${c.table ? `<div class="tscroll"><table class="t">${c.table.map((r, k) => `<tr>${r.map(x => k === 0 ? `<th>${x}</th>` : `<td>${x}</td>`).join("")}</tr>`).join("")}</table></div>` : ""}
        ${c.examples ? `<div class="exlist">${c.examples.map(x => `<div class="exline">${sayBtns(x)}<span>${tb(x)}</span></div>`).join("")}</div>` : ""}
        ${c.note ? `<div class="hint-box">💡 ${tb(c.note)}</div>` : ""}
      </div>
      ${backNext(i, cards.length, ["lp", "ln"])}
      <div class="dots">Card ${i + 1} of ${cards.length}</div>`, sideList(U("📘 All cards", "ทุกบัตร"), cards.map(c => plain(c.title)), i))}</div>`;
    onJump(k => { i = k; draw(); });
    on("lp", () => { i--; draw(); });
    on("ln", () => { i++; draw(); });
    wireNextAct();
  }
  draw();
}

// =============== WORD CARDS (picture, word, Thai, meaning, example, listen) ===============
function Words(sec) {
  let i = 0;
  const ws = sec.words;
  function draw() {
    const w = ws[i];
    view().innerHTML = `<div class="panel">${header(sec, U("🖼️ Word Cards", "บัตรคำศัพท์"))}${withSide(`
      <div class="word-card">
        <div class="wpic">${w.img ? img(w.img, w.w) : `<div class="wemoji">${w.emoji || "📝"}</div>`}</div>
        <div class="wtext">
          <div class="wword">${esc(w.w)} ${sayBtns(w.w)}</div>
          <div class="wpos">${esc(w.pos)}</div>
          ${thaiOn() ? `<div class="wth">🇹🇭 ${esc(w.th)}</div>` : ""}
          <div class="wdef">${tb(w.def)}</div>
          <div class="wex">${sayBtns(w.ex)} <span>${tb(w.ex.replace(new RegExp(`\\b(${w.hl || w.w})\\b`, "i"), "<b>$1</b>"))}</span></div>
        </div>
      </div>
      ${backNext(i, ws.length, ["wp", "wn"])}
      <div class="dots">Word ${i + 1} of ${ws.length}</div>`, sideList(U("🖼️ All words", "คำศัพท์ทั้งหมด"), ws.map(x => x.w + (thaiOn() ? " · " + x.th : "")), i))}</div>`;
    onJump(k => { i = k; draw(); });
    on("wp", () => { i--; draw(); });
    on("wn", () => { i++; draw(); });
    wireNextAct();
  }
  draw();
}

// =============== BOOK AND WORKBOOK EXERCISES (orange question, yellow hint, green answer) ===============
function Exercises(sec, which) {
  const qs = sec[which];
  const isWB = which === "wb";
  let i = 0, hint = false, shown = 0, ans = false, picked = -1;
  const title = isWB ? U("📒 Workbook", "แบบฝึกหัด") : U("📖 Student Book", "หนังสือเรียน");
  function draw() {
    const q = qs[i];
    const cls = q.kind === "class";
    const steps = (q.steps || []).slice(0, shown).map((s, k) => `<div class="step${k === shown - 1 ? " new" : ""}"><b class="n">Step ${k + 1}${thaiOn() ? ` (ขั้นที่ ${k + 1})` : ""}:</b> ${tb(s)}</div>`).join("");
    let btns = "";
    if (q.hint && !hint) btns += `<button class="bigbtn yellow" id="gh">${U("💡 Hint", "คำใบ้")}</button>`;
    if (q.steps && shown < q.steps.length) btns += `<button class="bigbtn" id="gs">${shown === 0 ? U("Show Step 1", "ดูขั้นที่ 1") : U("Show next step", "ดูขั้นต่อไป")}</button>`;
    if (!cls && q.answer) btns += `<button class="bigbtn ansbtn ${ans ? "grey" : "green"}" id="ga">${ans ? U("🙈 Hide answer", "ซ่อนคำตอบ") : U("👀 Show answer", "ดูคำตอบ")}</button>`;
    const choices = q.choices ? `<div class="chrow">${q.choices.map((c, k) => {
      const st = picked < 0 ? "" : k === q.right ? "right" : k === picked ? "wrong" : "dim";
      return `<button class="chbtn ${st}" data-k="${k}" ${picked >= 0 ? "disabled" : ""}>${esc(c)}</button>`; }).join("")}</div>
      ${picked >= 0 ? `<div class="feedback ${picked === q.right ? "good" : "bad"}">${picked === q.right ? U("✅ Correct!", "ถูกต้อง") : U("❌ Not quite. Look at the green one.", "ยังไม่ถูก ดูคำตอบสีเขียว")}</div>` : ""}` : "";
    view().innerHTML = `<div class="panel">${header(sec, title)}${withSide(`
      <div class="q-card">
        <div class="q-head"><span>${tb(q.ex)}</span><span class="badge">${isWB ? "📒 Workbook" : "📖 Book"} p.${q.page}</span></div>
        <div class="q-body">
          ${q.inst ? `<div class="q-inst">${tb(q.inst)}</div>` : ""}
          ${q.box ? `<div class="wordbox">${q.box.map(w => `<span>${esc(w)}</span>`).join("")}</div>` : ""}
          <div class="q-text">${q.say !== false ? sayBtns(q.q) : ""} ${tb(q.q)}</div>
          ${choices}
          ${cls ? `<div class="class-box">🎧 ${tb(q.classNote || "Do this in class with the audio and T. Roy.")}</div>` : ""}
          ${hint && q.hint ? `<div class="hint-box">💡 ${tb(q.hint)}</div>` : ""}
          ${steps}
          ${ans ? `<div class="answer-box"><div>${q.kind === "open" ? U("Example answer:", "ตัวอย่างคำตอบ") : U("Answer:", "คำตอบ")} <span class="final">${tb(q.answer)}</span></div>
            ${q.why ? `<div class="why">✅ ${U("WHY", "เพราะอะไร")}: ${tb(q.why)}</div>` : ""}
            ${q.kind === "open" ? `<div class="small">${U("Your answer can be different. That's OK!", "คำตอบของนักเรียนอาจต่างได้ ไม่เป็นไร")}</div>` : ""}</div>` : ""}
          <div class="btnrow">${btns}</div>
        </div>
      </div>
      ${backNext(i, qs.length, ["gp", "gn"])}
      <div class="dots">Question ${i + 1} of ${qs.length}</div>`,
      sideList(isWB ? U("📒 All questions", "ทุกข้อ") : U("📖 All questions", "ทุกข้อ"), qs.map(x => `${plain(x.ex).replace(/:.*/, "")} · ${short(x.q, 30)}`), i))}</div>`;
    on("gh", () => { hint = true; draw(); });
    on("gs", () => { shown++; draw(); });
    on("ga", () => { ans = !ans; draw(); });
    on("gp", () => { i--; reset(); });
    on("gn", () => { i++; reset(); });
    view().querySelectorAll(".chbtn").forEach(b => b.onclick = () => { picked = +b.dataset.k; draw(); });
    onJump(k => { i = k; reset(); });
    wireNextAct();
  }
  function reset() { shown = 0; hint = false; ans = false; picked = -1; if (window.DrawPad) DrawPad.clear(); draw(); }
  draw();
}

// =============== SPEAK (model sentences, your turn, optional microphone check) ===============
const Rec = window.SpeechRecognition || window.webkitSpeechRecognition;
const words = s => plain(s).toLowerCase().replace(/[^a-z0-9' ]/g, " ").split(/\s+/).filter(Boolean);
function listen(target, box) {
  if (!Rec) { box.innerHTML = `<div class="pill">${U("This browser cannot listen. Try Chrome or Safari, or practise with a partner.", "เบราว์เซอร์นี้ฟังเสียงไม่ได้ ลองใช้ Chrome หรือ Safari หรือฝึกกับเพื่อน")}</div>`; return; }
  const r = new Rec();
  r.lang = "en-US"; r.interimResults = false; r.maxAlternatives = 3;
  box.innerHTML = `<div class="pill mic-on">🎤 ${U("Listening… speak now!", "กำลังฟัง… พูดได้เลย")}</div>`;
  r.onresult = e => {
    const alts = [...e.results[0]].map(a => a.transcript);
    if (!target) { box.innerHTML = `<div class="fb-box good">👂 ${U("I heard:", "ได้ยินว่า")} <b>${esc(alts[0])}</b></div>`; return; }
    const want = words(target);
    const best = alts.map(a => { const got = new Set(words(a)); return { a, hit: want.filter(w => got.has(w)).length }; }).sort((x, y) => y.hit - x.hit)[0];
    const pct = Math.round(best.hit / want.length * 100);
    const got = new Set(words(best.a));
    box.innerHTML = `<div class="fb-box ${pct >= 80 ? "good" : "bad"}">${pct >= 80 ? "🌟" : "💪"} <b>${pct}%</b> · ${U("I heard:", "ได้ยินว่า")} “${esc(best.a)}”
      <div class="heard">${want.map(w => `<span class="${got.has(w) ? "ok" : "miss"}">${esc(w)}</span>`).join(" ")}</div>
      <div class="small">${pct >= 80 ? U("Great speaking!", "พูดได้ดีมาก") : U("Listen again 🔊 and try once more.", "ฟังอีกครั้งแล้วลองใหม่")}</div></div>`;
  };
  r.onerror = () => { box.innerHTML = `<div class="pill">${U("I couldn't hear you. Allow the microphone and try again.", "ไม่ได้ยินเสียง กรุณาอนุญาตไมโครโฟนแล้วลองใหม่")}</div>`; };
  r.start();
}
function Speak(sec) {
  const sp = sec.speak;
  const items = sp.models.map(m => ({ t: "model", s: m })).concat(sp.turns.map(t => ({ t: "turn", ...t })));
  let i = 0, ex = false;
  function draw() {
    const it = items[i];
    const body = it.t === "model"
      ? `<div class="speak-card model"><div class="tag">🔊 ${U("Listen and repeat", "ฟังแล้วพูดตาม")}</div>
           <div class="speak-line">${tb(it.s)}</div>
           <div class="btnrow"><button class="bigbtn say" data-say="${esc(plain(it.s))}">🔊 ${U("Listen", "ฟัง")}</button><button class="bigbtn say grey" data-slow="1" data-say="${esc(plain(it.s))}">🐢 ${U("Slow", "ช้า")}</button>
           <button class="bigbtn orange" id="mic">🎤 ${U("Say it", "พูดเลย")}</button></div><div id="micBox"></div></div>`
      : `<div class="speak-card turn"><div class="tag">🙋 ${U("Your turn", "ตาของนักเรียน")}</div>
           <div class="speak-line">${sayBtns(it.q)} ${tb(it.q)}</div>
           ${it.starter ? `<div class="starter">✏️ ${tb(it.starter)}</div>` : ""}
           ${ex ? `<div class="answer-box">${U("Example answer:", "ตัวอย่างคำตอบ")} <b>${tb(it.example)}</b> ${sayBtns(it.example)}</div>` : ""}
           <div class="btnrow"><button class="bigbtn ${ex ? "grey" : "green"}" id="exb">${ex ? U("🙈 Hide example", "ซ่อนตัวอย่าง") : U("👀 Example answer", "ดูตัวอย่างคำตอบ")}</button>
           <button class="bigbtn orange" id="mic">🎤 ${U("Say my answer", "พูดคำตอบของฉัน")}</button></div><div id="micBox"></div></div>`;
    view().innerHTML = `<div class="panel">${header(sec, U("🗣️ Speak", "ฝึกพูด"))}${withSide(`
      ${sp.tip && i === 0 ? `<div class="hint-box">💡 ${tb(sp.tip)}</div>` : ""}
      ${body}
      <p class="small">🎤 ${U("The microphone check only works in some browsers. Nothing is recorded or saved.", "การตรวจด้วยไมโครโฟนใช้ได้ในบางเบราว์เซอร์ ไม่มีการบันทึกเสียง")}</p>
      ${backNext(i, items.length, ["sp", "sn"])}`,
      sideList(U("🗣️ All sentences", "ทุกประโยค"), items.map(x => (x.t === "model" ? "🔊 " : "🙋 ") + short(x.t === "model" ? x.s : x.q, 36)), i))}</div>`;
    on("mic", () => listen(it.t === "model" ? it.s : "", document.getElementById("micBox")));
    on("exb", () => { ex = !ex; draw(); });
    on("sp", () => { i--; ex = false; draw(); });
    on("sn", () => { i++; ex = false; draw(); });
    onJump(k => { i = k; ex = false; draw(); });
    wireNextAct();
  }
  draw();
}

// =============== LISTEN AND SPELL ===============
function Spell(sec) {
  const all = sec.spell;
  let list, i, right, tries, t0, done;
  function start() { list = shuffle(all).slice(0, Math.min(10, all.length)); i = 0; right = 0; t0 = Date.now(); ask(); }
  const norm = s => s.toLowerCase().replace(/[^a-z]/g, "");
  function ask() {
    const w = list[i]; tries = 0; done = false;
    view().innerHTML = `<div class="panel">${header(sec, U("🎧 Listen and Spell", "ฟังแล้วสะกด"))}
      <div class="quiz-top"><span>${i + 1} / ${list.length}</span><span>✅ ${right}</span></div>
      <div class="spell-box">
        <div class="btnrow"><button class="bigbtn say big" data-say="${esc(w.w)}">🔊 ${U("Listen", "ฟัง")}</button><button class="bigbtn say grey big" data-slow="1" data-say="${esc(w.w)}">🐢 ${U("Slow", "ช้า")}</button></div>
        <div class="spell-dash">${w.w.split("").map(ch => ch === " " ? "&nbsp;&nbsp;" : ch === "-" ? "-" : "_").join(" ")}</div>
        <input id="spIn" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="${U("Type the word", "พิมพ์คำที่ได้ยิน").replace(/<[^>]+>/g, " ")}">
        <div class="btnrow"><button class="bigbtn green" id="spGo">${U("Check ✔", "ตรวจ")}</button><button class="bigbtn yellow" id="spHint">${U("💡 Hint", "คำใบ้")}</button></div>
        <div id="spFb"></div></div></div>`;
    say(w.w);
    const inp = document.getElementById("spIn");
    inp.focus();
    inp.onkeydown = e => { if (e.key === "Enter") check(); };
    on("spGo", check);
    on("spHint", () => { document.getElementById("spFb").innerHTML = `<div class="hint-box">💡 ${U(`It starts with <b>${esc(w.w[0])}</b>.`, `ขึ้นต้นด้วย <b>${esc(w.w[0])}</b>`)}${w.th && thaiOn() ? ` · 🇹🇭 ${esc(w.th)}` : ""}</div>`; });
    function check() {
      if (done) return;
      const ok = norm(inp.value) === norm(w.w);
      tries++;
      const fb = document.getElementById("spFb");
      if (ok || tries >= 2) {
        done = true;
        if (ok && tries === 1) right++;
        fb.innerHTML = `<div class="fb-box ${ok ? "good" : "bad"}">${ok ? U("✅ Correct!", "ถูกต้อง") : U("The word is:", "คำที่ถูกคือ")} <b class="bigword">${esc(w.w)}</b>${w.th && thaiOn() ? ` · ${esc(w.th)}` : ""}</div>
          <div class="btnrow"><button class="bigbtn" id="spN">${i < list.length - 1 ? U("Next word ➡", "คำถัดไป") : U("See my score 🏁", "ดูคะแนน")}</button></div>`;
        on("spN", () => { i++; i < list.length ? ask() : end(); });
      } else fb.innerHTML = `<div class="fb-box bad">❌ ${U("Not quite. Listen again and try once more.", "ยังไม่ถูก ฟังอีกครั้งแล้วลองใหม่")}</div>`;
    }
  }
  function end() {
    const time = Math.round((Date.now() - t0) / 1000);
    saveScore({ unit: unitNo(), section: sec.title, activity: "Listen and Spell", score: right, total: list.length, time });
    view().innerHTML = `<div class="panel">${header(sec, U("🎧 Listen and Spell", "ฟังแล้วสะกด"))}
      <div class="bigscore">${right} / ${list.length}</div><p style="text-align:center">${U("Right on the first try", "ถูกตั้งแต่ครั้งแรก")}</p>
      <div class="btnrow"><button class="bigbtn green" id="spA">${U("Play again", "เล่นอีกครั้ง")}</button>${nextActBtn()}</div></div>`;
    on("spA", start); wireNextAct();
  }
  view().innerHTML = `<div class="panel">${header(sec, U("🎧 Listen and Spell", "ฟังแล้วสะกด"))}
    <p style="text-align:center">${U("Listen to the word. Type it. You have 2 tries.", "ฟังคำศัพท์ แล้วพิมพ์ให้ถูก มีโอกาส 2 ครั้ง")}<br>🔊 ${U("Turn on the sound!", "เปิดเสียงด้วย")}</p>
    <div class="btnrow"><button class="bigbtn green" id="spS">${U("Start ▶", "เริ่ม")}</button></div></div>`;
  on("spS", start);
}

// =============== FLASHCARDS (in order, Back/Next, list on the right) ===============
function flashCards(sec) {
  const fromWords = (sec.words || []).map(w => ({
    front: `${w.img ? img(w.img, w.w, "fimg") : `<div class="wemoji">${w.emoji || "📝"}</div>`}<div>${esc(w.w)}</div>`,
    back: `${thaiOn() ? `<div class="wth">${esc(w.th)}</div>` : ""}<div>${tb(w.def)}</div>`, say: w.w, name: w.w }));
  return fromWords.concat((sec.flash || []).map(f => ({ front: tb(f.front), back: tb(f.back), say: f.front, name: plain(f.front) })));
}
function Flash(sec) {
  const cards = flashCards(sec);
  let order = cards.map((_, k) => k), pos = 0, flipped = false;
  const mark = {};
  const icon = k => mark[k] === "know" ? "✅" : mark[k] === "learn" ? "🔁" : "";
  const count = m => Object.values(mark).filter(v => v === m).length;
  function draw() {
    if (pos >= order.length) {
      const learning = cards.map((_, k) => k).filter(k => mark[k] === "learn");
      view().innerHTML = `<div class="panel">${header(sec, U("🃏 Flashcards", "บัตรคำ"))}
        <div class="bigscore">🎉</div>
        <p style="text-align:center"><b class="pile-know">${U("I know it", "รู้แล้ว")}: ${count("know")}</b> · <b class="pile-learn">${U("Still learning", "ยังต้องฝึก")}: ${count("learn")}</b></p>
        <div class="btnrow"><button class="bigbtn grey" id="fb">${U("⬅ Back to the last card", "กลับไปบัตรสุดท้าย")}</button>
          ${learning.length ? `<button class="bigbtn orange" id="fl">${U(`Practise "Still learning" again (${learning.length})`, "ฝึกบัตรที่ยังไม่รู้อีกครั้ง")}</button>` : ""}
          <button class="bigbtn" id="fa">${U("Start again", "เริ่มใหม่")}</button>${nextActBtn()}</div></div>`;
      on("fb", () => { pos = order.length - 1; draw(); });
      on("fl", () => { order = learning; pos = 0; draw(); });
      on("fa", () => { order = cards.map((_, k) => k); Object.keys(mark).forEach(k => delete mark[k]); pos = 0; draw(); });
      wireNextAct();
      return;
    }
    const k = order[pos], c = cards[k];
    view().innerHTML = `<div class="panel">${header(sec, U("🃏 Flashcards", "บัตรคำ"))}${withSide(`
      <div class="piles"><span>Card ${pos + 1} of ${order.length}</span><span class="pile-know">✅ ${count("know")}</span><span class="pile-learn">🔁 ${count("learn")}</span></div>
      <div class="flash-area"><div class="flash ${flipped ? "flipped" : ""}" id="card">
        <div class="face front">${c.front}</div>
        <div class="face back">${c.back}</div>
      </div></div>
      <p class="tapnote">${U("Tap the card to flip it", "แตะบัตรเพื่อพลิก")} · ${sayBtns(plain(c.say))}</p>
      <div class="btnrow"><button class="bigbtn orange" id="fn">${U("🔁 Still learning", "ยังต้องฝึก")}</button><button class="bigbtn green" id="fk">${U("✅ I know it", "รู้แล้ว")}</button></div>
      <div class="btnrow"><button class="bigbtn grey" id="fp" ${pos === 0 ? "disabled" : ""}>${U("⬅ Back", "ย้อนกลับ")}</button>
        <button class="bigbtn" id="fx">${pos === order.length - 1 ? U("Finish 🏁", "จบ") : U("Next ➡", "ถัดไป")}</button></div>`,
      sideList(U("🃏 All cards", "บัตรทั้งหมด"), order.map(j => short(cards[j].name, 36) + (icon(j) ? " " + icon(j) : "")), pos))}</div>`;
    document.getElementById("card").onclick = () => { flipped = !flipped; document.getElementById("card").classList.toggle("flipped", flipped); };
    const move = p => { pos = p; flipped = false; draw(); };
    on("fk", () => { mark[k] = "know"; move(pos + 1); });
    on("fn", () => { mark[k] = "learn"; move(pos + 1); });
    on("fp", () => move(pos - 1));
    on("fx", () => move(pos + 1));
    onJump(move);
  }
  draw();
}

// =============== MATCH GAME ===============
function Match(sec) {
  const key = `best_${DATA.unit}_${sec.id}`;
  let timer = null;
  cleanup = () => clearInterval(timer);
  const T = U("🧩 Match Game", "เกมจับคู่");
  function start() {
    const pairs = shuffle(sec.match).slice(0, 6);
    const tiles = shuffle(pairs.flatMap((p, k) => [{ k, s: p[0] }, { k, s: p[1] }]));
    let sel = null, left = pairs.length, t0 = Date.now(), penalty = 0;
    view().innerHTML = `<div class="panel">${header(sec, T)}
      <div class="timer" id="mt">0.0 s</div>
      <p class="tapnote">${U("Tap two cards that go together. A wrong match adds 1 second.", "แตะ 2 ใบที่เข้าคู่กัน ถ้าผิดจะบวกเวลา 1 วินาที")}</p>
      <div class="match-grid">${tiles.map((t, i) => `<button class="tile" data-i="${i}">${t.s}</button>`).join("")}</div></div>`;
    const mt = document.getElementById("mt");
    timer = setInterval(() => { mt.textContent = (((Date.now() - t0) / 1000) + penalty).toFixed(1) + " s"; }, 100);
    view().querySelectorAll(".tile").forEach(b => b.onclick = () => {
      const i = +b.dataset.i;
      if (b.classList.contains("gone")) return;
      if (sel === null) { sel = i; b.classList.add("sel"); return; }
      if (sel === i) { b.classList.remove("sel"); sel = null; return; }
      const a = view().querySelector(`.tile[data-i="${sel}"]`);
      if (tiles[sel].k === tiles[i].k) {
        a.classList.add("gone"); b.classList.add("gone"); left--;
        if (!left) finish(((Date.now() - t0) / 1000) + penalty, pairs.length);
      } else {
        penalty += 1;
        a.classList.add("bad"); b.classList.add("bad");
        setTimeout(() => { a.classList.remove("bad", "sel"); b.classList.remove("bad"); }, 400);
      }
      a.classList.remove("sel"); sel = null;
    });
  }
  function finish(s2, n) {
    clearInterval(timer);
    const time = Math.round(s2 * 10) / 10;
    const best = store.get(key, null);
    const isBest = best === null || time < best;
    if (isBest) store.set(key, time);
    saveScore({ unit: unitNo(), section: sec.title, activity: "Match Game", score: n, total: n, time });
    view().innerHTML = `<div class="panel">${header(sec, T)}
      <div class="bigscore">⏱️ ${time} s</div>
      <p style="text-align:center;font-weight:800">${isBest ? U("🎉 New best time!", "ทำเวลาดีที่สุดใหม่") : `${U("Your best time", "เวลาที่ดีที่สุด")}: ${best} s`}</p>
      <div class="btnrow"><button class="bigbtn green" id="ma">${U("Play again", "เล่นอีกครั้ง")}</button>${nextActBtn()}</div></div>`;
    on("ma", start); wireNextAct();
  }
  const best = store.get(key, null);
  view().innerHTML = `<div class="panel">${header(sec, T)}
    <p style="text-align:center">${U("Match each pair as fast as you can!", "จับคู่ให้เร็วที่สุด")}</p>
    ${best !== null ? `<p style="text-align:center;font-weight:800">🏅 ${U("Your best time", "เวลาที่ดีที่สุด")}: ${best} s</p>` : ""}
    <div class="btnrow"><button class="bigbtn green" id="ms">${U("Start ▶", "เริ่ม")}</button></div></div>`;
  on("ms", start);
}

// =============== SORT IT (put each card in the right group) ===============
function Sort(sec) {
  const S = sec.sort;
  const T = U("🪣 Sort It", "เกมแยกกลุ่ม");
  let items, i, right, wrongOnce, bins, t0;
  function start() { items = shuffle(S.items); i = 0; right = 0; wrongOnce = false; bins = S.bins.map(() => []); t0 = Date.now(); draw(); }
  function draw(msg) {
    const it = items[i];
    view().innerHTML = `<div class="panel">${header(sec, T)}
      <p class="q-inst" style="text-align:center">${tb(S.title)}</p>
      <div class="quiz-top"><span>${i + 1} / ${items.length}</span><span>✅ ${right}</span></div>
      <div class="sort-item">${esc(it[0])} ${sayBtns(it[0])}</div>
      <div class="sort-bins">${S.bins.map((b, k) => `<button class="sort-bin b${k}" data-k="${k}"><b>${tb(b)}</b><span class="in">${bins[k].map(esc).join(" · ")}</span></button>`).join("")}</div>
      <div id="soFb">${msg || ""}</div></div>`;
    view().querySelectorAll(".sort-bin").forEach(b => b.onclick = () => {
      const k = +b.dataset.k;
      if (k === it[1]) {
        if (!wrongOnce) right++;
        bins[k].push(it[0]); wrongOnce = false; i++;
        if (i < items.length) draw(`<div class="feedback good">✅ ${U("Yes!", "ใช่แล้ว")}</div>`); else end();
      } else {
        wrongOnce = true;
        b.classList.add("bad"); setTimeout(() => b.classList.remove("bad"), 400);
        document.getElementById("soFb").innerHTML = `<div class="feedback bad">❌ ${U("Try another group.", "ลองกลุ่มอื่น")}</div>${it[2] ? `<div class="hint-box">💡 ${tb(it[2])}</div>` : ""}`;
      }
    });
  }
  function end() {
    const time = Math.round((Date.now() - t0) / 1000);
    saveScore({ unit: unitNo(), section: sec.title, activity: "Sort It", score: right, total: items.length, time });
    view().innerHTML = `<div class="panel">${header(sec, T)}
      <div class="bigscore">${right} / ${items.length}</div>
      <div class="sort-bins">${S.bins.map((b, k) => `<div class="sort-bin b${k}"><b>${tb(b)}</b><span class="in">${bins[k].map(esc).join(" · ")}</span></div>`).join("")}</div>
      <div class="btnrow"><button class="bigbtn green" id="soA">${U("Play again", "เล่นอีกครั้ง")}</button>${nextActBtn()}</div></div>`;
    on("soA", start); wireNextAct();
  }
  view().innerHTML = `<div class="panel">${header(sec, T)}
    <p style="text-align:center">${tb(S.title)}</p>
    <p style="text-align:center">${U("Tap the right group for each card.", "แตะกลุ่มที่ถูกต้องสำหรับแต่ละบัตร")}</p>
    <div class="btnrow"><button class="bigbtn green" id="soS">${U("Start ▶", "เริ่ม")}</button></div></div>`;
  on("soS", start);
}

// =============== SENTENCE BUILDER (tap the words in the right order) ===============
function Build(sec) {
  const T = U("🧱 Sentence Builder", "เกมเรียงประโยค");
  let list, i, right, t0;
  function start() { list = shuffle(sec.build).slice(0, Math.min(8, sec.build.length)); i = 0; right = 0; t0 = Date.now(); ask(); }
  function ask() {
    const target = list[i];
    const parts = target.split("|").map(s => s.trim());
    let pool = shuffle(parts.map((p, k) => ({ p, k })));
    while (parts.length > 1 && pool.every((x, j) => x.k === j)) pool = shuffle(pool);
    let line = [], checks = 0, done = false;
    const full = parts.join(" ");
    function draw(msg) {
      view().innerHTML = `<div class="panel">${header(sec, T)}
        <div class="quiz-top"><span>${i + 1} / ${list.length}</span><span>✅ ${right}</span></div>
        <p class="tapnote">${U("Tap the cards to make a sentence. Tap a card in the line to take it back.", "แตะบัตรเพื่อเรียงประโยค แตะบัตรในแถวเพื่อนำกลับ")}</p>
        <div class="build-line ${done ? "done" : ""}">${line.map((x, j) => `<button class="btile in" data-j="${j}">${esc(x.p)}</button>`).join("") || "&nbsp;"}</div>
        <div class="build-pool">${pool.map((x, j) => `<button class="btile" data-j="${j}">${esc(x.p)}</button>`).join("")}</div>
        <div id="bFb">${msg || ""}</div>
        <div class="btnrow">${done ? `<button class="bigbtn" id="bN">${i < list.length - 1 ? U("Next ➡", "ถัดไป") : U("See my score 🏁", "ดูคะแนน")}</button>`
          : `<button class="bigbtn green" id="bC" ${pool.length ? "disabled" : ""}>${U("Check ✔", "ตรวจ")}</button>${checks ? `<button class="bigbtn grey" id="bS">${U("👀 Show answer", "ดูคำตอบ")}</button>` : ""}`}</div></div>`;
      if (!done) {
        view().querySelectorAll(".build-pool .btile").forEach(b => b.onclick = () => { line.push(pool.splice(+b.dataset.j, 1)[0]); draw(); });
        view().querySelectorAll(".build-line .btile").forEach(b => b.onclick = () => { pool.push(line.splice(+b.dataset.j, 1)[0]); draw(); });
      }
      on("bC", () => {
        checks++;
        const ok = line.map(x => x.p).join(" ") === full;
        if (ok) { done = true; if (checks === 1) right++; say(full); draw(`<div class="feedback good">✅ ${U("Great sentence!", "ประโยคถูกต้อง")}</div>`); }
        else draw(`<div class="feedback bad">❌ ${U("Not quite. Move some cards and check again.", "ยังไม่ถูก ลองสลับบัตรแล้วตรวจอีกครั้ง")}</div>`);
      });
      on("bS", () => { done = true; line = parts.map((p, k) => ({ p, k })); pool = []; say(full); draw(`<div class="answer-box">${U("Answer:", "คำตอบ")} <b>${tb(full)}</b></div>`); });
      on("bN", () => { i++; i < list.length ? ask() : end(); });
    }
    draw();
  }
  function end() {
    const time = Math.round((Date.now() - t0) / 1000);
    saveScore({ unit: unitNo(), section: sec.title, activity: "Sentence Builder", score: right, total: list.length, time });
    view().innerHTML = `<div class="panel">${header(sec, T)}
      <div class="bigscore">${right} / ${list.length}</div><p style="text-align:center">${U("Right on the first check", "ถูกตั้งแต่ตรวจครั้งแรก")}</p>
      <div class="btnrow"><button class="bigbtn green" id="bA">${U("Play again", "เล่นอีกครั้ง")}</button>${nextActBtn()}</div></div>`;
    on("bA", start); wireNextAct();
  }
  view().innerHTML = `<div class="panel">${header(sec, T)}
    <p style="text-align:center">${U("Put the words in the right order to make a sentence.", "เรียงคำให้ถูกต้องเป็นประโยค")}</p>
    <div class="btnrow"><button class="bigbtn green" id="bSt">${U("Start ▶", "เริ่ม")}</button></div></div>`;
  on("bSt", start);
}

// =============== SPEED QUIZ (Kahoot style) ===============
function Quiz(sec) {
  const SHAPES = ["▲", "◆", "●", "■"];
  const LIMIT = 20;
  const T = U("⚡ Speed Quiz", "ตอบเร็ว");
  let timer = null;
  cleanup = () => clearInterval(timer);
  let qs, i, points, correct, streak, t0Quiz;
  function start() {
    qs = shuffle(sec.quiz).slice(0, 10).map(q => ({ ...q, opts: shuffle(q.options.map((o, k) => ({ o, ok: k === 0 }))) }));
    i = 0; points = 0; correct = 0; streak = 0; t0Quiz = Date.now();
    ask();
  }
  function ask() {
    const q = qs[i];
    const t0 = Date.now();
    let answered = false;
    view().innerHTML = `<div class="panel">
      <div class="quiz-top"><span>${i + 1} / ${qs.length}</span><span>⭐ ${points}</span><span id="qt">${LIMIT}</span></div>
      <div class="timebar"><div id="tb" style="width:100%"></div></div>
      <div class="quiz-q">${tb(q.q)}</div>
      <div class="opts">${q.opts.map((o, k) => `<button class="opt c${k}" data-k="${k}"><span class="shape">${SHAPES[k]}</span><span>${esc(o.o)}</span></button>`).join("")}</div>
      <div id="fb"></div></div>`;
    const tbar = document.getElementById("tb"), qt = document.getElementById("qt");
    timer = setInterval(() => {
      const el = (Date.now() - t0) / 1000;
      tbar.style.width = Math.max(0, 100 - el / LIMIT * 100) + "%";
      qt.textContent = Math.max(0, Math.ceil(LIMIT - el));
      if (el >= LIMIT && !answered) answer(-1);
    }, 100);
    view().querySelectorAll(".opt").forEach(b => b.onclick = () => { if (!answered) answer(+b.dataset.k); });
    function answer(k) {
      answered = true;
      clearInterval(timer);
      const el = (Date.now() - t0) / 1000;
      const ok = k >= 0 && q.opts[k].ok;
      let gained = 0;
      if (ok) {
        streak++; correct++;
        gained = Math.round(500 + 500 * Math.max(0, (LIMIT - el) / LIMIT)) + (streak >= 2 ? Math.min(500, (streak - 1) * 100) : 0);
        points += gained;
      } else streak = 0;
      view().querySelectorAll(".opt").forEach((b, j) => { b.classList.add(q.opts[j].ok ? "right" : "dim"); b.disabled = true; });
      const right = q.opts.find(o => o.ok).o;
      document.getElementById("fb").innerHTML = `
        <div class="feedback ${ok ? "good" : "bad"}">${ok ? `✅ +${gained}${streak >= 2 ? ` 🔥 ${streak}` : ""}` : (k < 0 ? "⏰ Time's up!" : "❌ Not quite.")}</div>
        ${ok ? "" : `<p style="text-align:center">${U("The answer is", "คำตอบคือ")} <b>${esc(right)}</b></p>`}
        ${q.why ? `<div class="hint-box">💡 ${tb(q.why)}</div>` : ""}
        <div class="btnrow"><button class="bigbtn" id="qn">${i < qs.length - 1 ? U("Next ➡", "ถัดไป") : U("See my score 🏁", "ดูคะแนน")}</button></div>`;
      on("qn", () => { i++; i < qs.length ? ask() : end(); });
    }
  }
  function end() {
    const time = Math.round((Date.now() - t0Quiz) / 1000);
    saveScore({ unit: unitNo(), section: sec.title, activity: "Speed Quiz", score: correct, total: qs.length, time });
    const msg = correct === qs.length ? "Perfect! 🌟" : correct >= qs.length * 0.7 ? "Great job! 🎉" : correct >= qs.length * 0.4 ? "Good try! Keep practising 💪" : "Look at Learn and Word Cards again, then play again 💪";
    view().innerHTML = `<div class="panel">${header(sec, T)}
      <div class="bigscore">${correct} / ${qs.length}</div>
      <p style="text-align:center;font-weight:900;font-size:1.3em">⭐ ${points} points</p>
      <p style="text-align:center">${msg}</p>
      <div class="btnrow"><button class="bigbtn green" id="qa">${U("Play again", "เล่นอีกครั้ง")}</button>${nextActBtn()}</div></div>`;
    on("qa", start); wireNextAct();
  }
  view().innerHTML = `<div class="panel">${header(sec, T)}
    <p style="text-align:center">${U(`${Math.min(10, sec.quiz.length)} questions · 20 seconds each<br>Answer fast for more points. Get them right in a row for a 🔥 streak bonus!`, "ตอบเร็วได้คะแนนมาก ตอบถูกติดกันได้โบนัส")}</p>
    <div class="btnrow"><button class="bigbtn green" id="qs">${U("Start ▶", "เริ่ม")}</button></div></div>`;
  on("qs", start);
}

// =============== CLASS BATTLE (teacher, projector) ===============
async function Battle(sec, whole) {
  let pool;
  if (whole) {
    try { pool = (await loadBank()).map(q => ({ q: q.q, a: q.options[0] })); } catch (e) { return noBank(); }
    sec = { title: "Whole unit", pages: DATA.pages };
  } else pool = sec.quiz.map(q => ({ q: tb(q.q), a: esc(q.options[0]) }));
  const DEFAULT = ["Red Team", "Blue Team", "Yellow Team", "Green Team"];
  let n = 2, names = DEFAULT.slice(), scores, qs, i, revealed;
  function setup() {
    view().innerHTML = `<div class="panel team-setup">${header(sec, "🏆 Class Battle")}
      <p>For the projector. Teams answer, then T. Roy clicks the team that got it right.</p>
      <p><b>How many teams?</b></p>
      <div class="cls-row">${[2, 3, 4].map(k => `<button class="clsbtn ${k === n ? "on" : ""}" data-n="${k}">${k}</button>`).join("")}</div>
      <div>${names.slice(0, n).map((nm, k) => `<div><input data-k="${k}" value="${esc(nm)}" maxlength="18"></div>`).join("")}</div>
      <div class="btnrow"><button class="bigbtn green" id="bs">Start battle ▶</button></div></div>`;
    view().querySelectorAll(".clsbtn").forEach(b => b.onclick = () => { n = +b.dataset.n; setup(); });
    view().querySelectorAll("input").forEach(inp => inp.oninput = () => { names[+inp.dataset.k] = inp.value || DEFAULT[+inp.dataset.k]; });
    on("bs", () => { scores = new Array(n).fill(0); qs = shuffle(pool).slice(0, 10); i = 0; revealed = false; draw(); });
  }
  function board(clickable) {
    return `<div class="scoreboard">${scores.map((s, k) => `<div class="team t${k}"><div>${esc(names[k])}</div><div class="pts">${s}</div>
      ${clickable ? `<button data-k="${k}">✅ Got it!</button>` : ""}</div>`).join("")}</div>`;
  }
  function draw() {
    const q = qs[i];
    view().innerHTML = `<div class="panel">
      <div class="quiz-top"><span>🏆 Question ${i + 1} / ${qs.length}</span></div>
      <div class="battle-q">${q.q}</div>
      ${revealed ? `<div class="battle-a">✅ ${q.a}</div>` : ""}
      ${board(revealed)}
      <div class="btnrow">${revealed ? `<button class="bigbtn grey" id="bnone">Nobody got it ➡</button>` : `<button class="bigbtn orange" id="brev">Show answer 👀</button>`}
        <button class="bigbtn dark" id="bend">End battle 🏁</button></div></div>`;
    const next = () => { i++; revealed = false; i < qs.length ? draw() : end(); };
    on("brev", () => { revealed = true; draw(); });
    on("bnone", next); on("bend", end);
    view().querySelectorAll(".team button").forEach(b => b.onclick = () => { scores[+b.dataset.k]++; next(); });
  }
  function end() {
    const top = Math.max(...scores);
    const winners = names.slice(0, n).filter((_, k) => scores[k] === top);
    view().innerHTML = `<div class="panel"><div class="winner">🎉🏆🎉<br>${winners.length > 1 ? "It's a tie!<br>" + winners.map(esc).join(" & ") : esc(winners[0]) + " wins!"}</div>
      ${board(false)}<div class="btnrow"><button class="bigbtn green" id="bagain">New battle</button></div></div>`;
    on("bagain", setup);
  }
  setup();
}
