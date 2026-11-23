"""Shared helpers for tools/build_unit07.py and later units.

W = word card, L = teaching card, X = book/workbook question, Q = quiz question, B = test bank question.
Every English text goes through T() so its Thai is remembered (see checks.py).
If a word's Canva picture is not in img/unitXX/ yet, the word shows an emoji instead.
"""
import json
import os

from checks import TH, T, check_all, write_check_me

ROOT = os.path.join(os.path.dirname(__file__), "..")


class Kit:
    def __init__(self, unit, emoji):
        self.U = unit
        self.IMG = f"img/unit{unit}/"
        self.EMOJI = emoji

    def W(self, w, pos, th, d, dth, ex, exth, img=None, emoji=None, hl=None):
        T(d, dth)
        T(ex, exth)
        out = {"w": w, "pos": pos, "th": th, "def": d, "ex": ex}
        if img and os.path.exists(os.path.join(ROOT, self.IMG + img + ".jpg")):
            out["img"] = self.IMG + img + ".jpg"
        else:
            out["emoji"] = emoji or self.EMOJI.get(img, "📝")
        if hl:
            out["hl"] = hl
        return out

    def pic(self, w):
        """Match-game tile for a word: its picture, or a big emoji."""
        return f'<img src="{w["img"]}" alt="" loading="lazy">' if w.get("img") else f'<span style="font-size:2em">{w["emoji"]}</span>'

    def build(self, title, pages, sections, bank):
        unit = {"unit": self.U, "title": title, "pages": pages, "sections": sections}
        check_all(unit, bank, ROOT)
        out = os.path.join(ROOT, "content")
        dump = lambda name, data: json.dump(data, open(os.path.join(out, name), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
        dump(f"unit{self.U}.json", unit)
        dump(f"bank{self.U}.json", {"questions": bank})
        dump(f"th{self.U}.json", TH)
        write_check_me(unit, self.U, os.path.join(out, "CHECK-ME.md"))
        n_ex = sum(len(s.get("book", [])) + len(s.get("wb", [])) for s in sections)
        print(f"Unit {self.U}: {len(sections)} lessons, {n_ex} book and workbook questions, {len(bank)} test questions, {len(TH)} Thai lines. All checks passed ✅")


def L(tag, title, tth, lines=(), page=None, examples=(), note=None, table=None):
    c = {"tag": tag, "title": T(title, tth)}
    if page:
        c["page"] = page
    if lines:
        c["lines"] = [T(a, b) for a, b in lines]
    if examples:
        c["examples"] = [T(a, b) for a, b in examples]
    if note:
        c["note"] = T(*note)
    if table:
        c["table"] = table
    return c


def X(ex, page, q, answer=None, kind="write", inst=None, hint=None, steps=None, why=None,
      choices=None, right=None, box=None, classNote=None, say=True):
    item = {"ex": T(*ex), "page": page, "q": T(*q), "kind": kind}
    if inst:
        item["inst"] = T(*inst)
    if answer:
        item["answer"] = T(*answer)
    if hint:
        item["hint"] = T(*hint)
    if steps:
        item["steps"] = [T(a, b) for a, b in steps]
    if why:
        item["why"] = T(*why)
    if choices:
        item["choices"] = choices
        item["right"] = right
    if box:
        item["box"] = box
    if classNote:
        item["classNote"] = T(*classNote)
    if not say:
        item["say"] = False
    return item


def Q(q, qth, options, why=None):
    out = {"q": T(q, qth), "options": options}
    if why:
        out["why"] = T(*why)
    return out


def B(q, qth, options, why, whyth, src):
    return {"q": T(q, qth), "options": options, "why": T(why, whyth), "src": src}


def EX(n, en, th):
    return (f"Exercise {n}: {en}", f"แบบฝึกหัดที่ {n}: {th}")


def S(models, turns, tip=None):
    """Speak activity. models: [(en, th)], turns: [(q, qth, starter, sth, example, exth)]"""
    out = {"models": [T(a, b) for a, b in models],
           "turns": [{"q": T(q, qt), "starter": T(s, st), "example": T(e, et)} for q, qt, s, st, e, et in turns]}
    if tip:
        out["tip"] = T(*tip)
    return out


def sort(title, bins, items):
    return {"title": T(*title), "bins": [T(*b) for b in bins], "items": items}
