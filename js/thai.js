// Thai under the English. The Thai text comes from content/thXX.json (made by tools/build_unit05.py and checked there).
// The English is never changed: only an extra Thai line is added under it.

let TH_DICT = {};
const thaiOn = () => store.get("thai", true);

async function loadThai(uid) {
  try {
    const r = await fetch(`content/th${uid}.json`, { cache: "no-cache" });
    TH_DICT = r.ok ? await r.json() : {};
  } catch (e) { TH_DICT = {}; }
}

function thOf(s) { const t = thaiOn() && s ? (TH_DICT[s] || "") : ""; return t === s ? "" : t; }   // no repeat when Thai = English
function tb(s) { if (!s) return ""; const t = thOf(s); return t ? `${s}<span class="th">${t}</span>` : s; }   // text + Thai line
function U(en, th) { return thaiOn() ? `${en}<span class="th">${th}</span>` : en; }                        // buttons and headings

function thaiSwitch() {
  return `<button class="ubtn thsw ${thaiOn() ? "on" : ""}" id="thSw" title="Thai on or off">🇹🇭 ไทย ${thaiOn() ? "✓" : "✗"}</button>`;
}
