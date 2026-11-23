"""Shared helpers and checks for the unit build scripts (tools/build_unitXX.py)."""
import os
import re

TH = {}          # English text -> Thai text


def T(en, th):
    """Remember the Thai for this English text, and give back the English."""
    TH.setdefault(en, th)      # the same English used twice keeps its first Thai
    return en


WORDS = {w: str(i) for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}
WORDS.update({"thirty": "30", "forty": "40", "fifty": "50", "hundred": "100"})
TH_WORDS = {"หนึ่ง": "1", "เดียว": "1", "สอง": "2", "สาม": "3", "สี่": "4", "ห้า": "5", "หก": "6", "เจ็ด": "7", "แปด": "8", "เก้า": "9", "สิบ": "10", "ยี่สิบ": "20", "สี่สิบ": "40"}


def numerals(s):
    s = re.sub(r"<[^>]+>", " ", s).replace("กริยาช่องที่ 3", "").replace("กริยาช่องที่ 1", "").replace("กริยาช่องที่ 2", "")   # "verb form 3" is the Thai name for past participle
    s = re.sub(r"(?<=\d),(?=\d{3})", "", s)                        # 6,000 = 6000
    return set(re.findall(r"\d+(?:\.\d+)?", s))


def all_numbers(s, thai):
    out = numerals(s)
    if thai:
        out |= {v for k, v in TH_WORDS.items() if k in s}
    else:
        out |= {WORDS[m.lower()] for m in re.findall(r"\b(" + "|".join(WORDS) + r")\b", s, flags=re.I)}
    return out


def numbers_ok(en, th):
    """Every numeral (2014, 86, 5.1) must be in both texts. Number words (three / สาม) count as numbers too."""
    return numerals(en) <= all_numbers(th, True) and numerals(th) <= all_numbers(en, False)


def walk(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from walk(v)
    elif isinstance(x, list):
        for v in x:
            yield from walk(v)


def check_all(unit, bank, root):
    errors = []
    for en, th in TH.items():
        if not numbers_ok(en, th):
            errors.append(f"Numbers differ: {en!r} / {th!r}")
        if re.search(r"[A-Za-z]", en) and not th.strip():
            errors.append(f"Empty Thai: {en!r}")
    for s in list(walk(unit)) + list(walk(bank)) + list(TH.values()):
        if "—" in s:
            errors.append(f"Em dash found: {s!r}")
    for p in re.findall(r'img/unit\d+/[\w-]+\.jpg', " ".join(walk(unit))):
        if not os.path.exists(os.path.join(root, p)):
            errors.append(f"Missing picture: {p}")
    for sec in unit["sections"]:
        sid = sec["id"]
        for q in sec.get("quiz", []) + bank:
            if len(q["options"]) != 4 or len(set(q["options"])) != 4:
                errors.append(f"[{sid}] quiz needs 4 different options: {q['q']!r}")
        for k in ("book", "wb"):
            for q in sec.get(k, []):
                if q["kind"] != "class" and not q.get("answer"):
                    errors.append(f"[{sid}] {k} question has no answer: {q['q']!r}")
                if q.get("choices") and not (0 <= q["right"] < len(q["choices"])):
                    errors.append(f"[{sid}] bad right choice: {q['q']!r}")
        if sec.get("sort"):
            nb = len(sec["sort"]["bins"])
            for it in sec["sort"]["items"]:
                if not (0 <= it[1] < nb):
                    errors.append(f"[{sid}] sort item in a missing group: {it}")
        if "match" in sec and sec["match"] is not None and len(sec["match"]) and len(sec["match"]) < 3:
            errors.append(f"[{sid}] match game needs at least 3 pairs")
    if errors:
        raise SystemExit("❌ Problems found:\n" + "\n".join(errors))


def write_check_me(unit, u, path):
    """Writes (or replaces) this unit's part of content/CHECK-ME.md."""
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    lines = [f"<!-- UNIT {u} START -->", f"## Unit {int(u)}: {unit['title']}", "",
             "Every answer below was written by Claude (there is no answer key). Please tick ✅ or correct it.",
             "Items marked 🎧 need the class audio; no answer was written for them.", ""]
    for sec in unit["sections"]:
        rows = [(k, q) for k in ("book", "wb") for q in sec.get(k, [])]
        if not rows:
            continue
        lines.append(f"### {strip(sec['title'])}")
        lines.append("")
        for k, q in rows:
            where = f"{'Student Book' if k == 'book' else 'Workbook'} p.{q['page']}"
            if q["kind"] == "class":
                lines.append(f"- [ ] {where} · {strip(q['ex'])} · {strip(q['q'])} → 🎧 in class with audio (no answer written)")
            else:
                tag = " (example answer, open question)" if q["kind"] == "open" else ""
                lines.append(f"- [ ] {where} · {strip(q['ex'])} · {strip(q['q'])} → **{strip(q['answer'])}**{tag}")
        lines.append("")
    lines.append(f"<!-- UNIT {u} END -->")
    block = "\n".join(lines)
    head = "# CHECK-ME: answers for T. Roy to check\n\nThai text should also be checked by a Thai colleague.\n\n"
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else head
    pat = re.compile(rf"<!-- UNIT {u} START -->.*?<!-- UNIT {u} END -->", re.S)
    new = pat.sub(block, old) if pat.search(old) else old.rstrip() + "\n\n" + block + "\n"
    open(path, "w", encoding="utf-8").write(new)
