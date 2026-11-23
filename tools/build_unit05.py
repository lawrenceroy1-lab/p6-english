"""Builds Unit 5 (Exciting Sports) for the P.6 English website.

Run:  python3 tools/build_unit05.py

It writes:
  content/unit05.json   the lessons (English)
  content/bank05.json   Practice and Unit Test questions
  content/th05.json     the Thai line for each English text
  content/CHECK-ME.md   every answer Claude wrote, for T. Roy to check (Unit 5 part)

T("English", "Thai") gives the English text and remembers its Thai.
The script stops with an error if a Thai line has different numbers from the English,
if an em dash is used, if a picture file is missing, or if a quiz question is broken.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from checks import TH, T, check_all, write_check_me  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
U = "05"
IMG = "img/unit05/"


def W(w, pos, th, d, dth, ex, exth, img=None, emoji=None, hl=None):
    """A vocabulary word: word, part of speech, Thai meaning, meaning, example sentence."""
    T(d, dth)
    T(ex, exth)
    out = {"w": w, "pos": pos, "th": th, "def": d, "ex": ex}
    if img:
        out["img"] = IMG + img + ".jpg"
    if emoji:
        out["emoji"] = emoji
    if hl:
        out["hl"] = hl
    return out


def L(tag, title, tth, lines=(), page=None, examples=(), note=None, table=None, img=None):
    """A teaching card. lines/examples are (English, Thai) pairs."""
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
    if img:
        c["img"] = img
    return c


def X(ex, page, q, answer=None, kind="write", inst=None, hint=None, steps=None, why=None,
      choices=None, right=None, box=None, classNote=None, say=True):
    """One exercise item. Every text is an (English, Thai) pair, except box and choices (English only)."""
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
    """Quiz question: options[0] is the right answer."""
    out = {"q": T(q, qth), "options": options}
    if why:
        out["why"] = T(*why)
    return out


# ------------------------------------------------------------------ common instructions
EX = lambda n, en, th: (f"Exercise {n}: {en}", f"แบบฝึกหัดที่ {n}: {th}")

# ================================================================== 0. UNIT OPENER
opener = {
    "id": "opener", "title": T("Unit Opener: Exciting Sports", "เปิดบทเรียน: กีฬาที่น่าตื่นเต้น"),
    "short": T("Start", "เริ่มต้น"), "pages": "Book p.50 to 51",
    "learn": [
        L("Welcome", "Welcome to Unit 5: Exciting Sports!", "ยินดีต้อนรับสู่บทที่ 5: กีฬาที่น่าตื่นเต้น", [
            ("In this unit you will:", "ในบทนี้นักเรียนจะ:"),
            ("🏂 learn words for extreme sports and safety equipment", "🏂 เรียนคำศัพท์เกี่ยวกับกีฬาผาดโผนและอุปกรณ์ความปลอดภัย"),
            ("⏳ use the present perfect with <b>for</b> and <b>since</b>", "⏳ ใช้ Present Perfect กับ for และ since"),
            ("💥 make adjectives stronger with <b>so, very, really, extremely</b>", "💥 ทำให้คำคุณศัพท์มีความหมายหนักขึ้นด้วย so, very, really, extremely"),
            ("🎵 sing a song, 📖 read about brave athletes, 🌳 connect with nature, ✍️ write a biography", "🎵 ร้องเพลง 📖 อ่านเรื่องนักกีฬาที่กล้าหาญ 🌳 ใกล้ชิดธรรมชาติ ✍️ เขียนชีวประวัติ"),
        ], page="📖 p.50"),
        L("Look", "Look at the big photo", "ดูภาพใหญ่ในหนังสือ", [
            ("Open your book to pages 50 and 51.", "เปิดหนังสือหน้า 50 และ 51"),
            ("A man is in a small green boat called a <b>kayak</b>. He is going down a big waterfall!", "ชายคนหนึ่งอยู่ในเรือเล็กสีเขียวที่เรียกว่า เรือคายัค เขากำลังล่องลงน้ำตกขนาดใหญ่"),
            ("The photo is from Amazonas, Brazil.", "ภาพนี้ถ่ายที่รัฐอามาโซนัส ประเทศบราซิล"),
            ("This sport is called <b>kayaking</b>. It is an <b>extreme sport</b>: exciting and dangerous.", "กีฬานี้เรียกว่า การพายเรือคายัค เป็นกีฬาผาดโผน คือ น่าตื่นเต้นและอันตราย"),
        ], page="📖 p.50 to 51"),
        L("Feelings", "How does he feel?", "เขารู้สึกอย่างไร", [
            ("We can describe feelings with a strong word before the adjective.", "เราบอกความรู้สึกได้ โดยใส่คำที่เน้นความหมายไว้หน้าคำคุณศัพท์"),
        ], examples=[
            ("He feels <b>really</b> happy.", "เขารู้สึกมีความสุขมาก"),
            ("He feels <b>very</b> worried.", "เขารู้สึกกังวลมาก"),
            ("He feels <b>totally</b> excited.", "เขารู้สึกตื่นเต้นสุด ๆ"),
        ], note=("You will learn more about really, very and totally in Grammar 2.", "นักเรียนจะได้เรียน really, very และ totally เพิ่มเติมในไวยากรณ์ 2"), page="📖 p.50"),
    ],
    "book": [
        X(("Look, check, and write: Question 1", "ดู เลือก และเขียน: ข้อ 1"), 50,
          ("How do you think this person feels? Really happy, very worried, or totally excited?", "นักเรียนคิดว่าคนนี้รู้สึกอย่างไร มีความสุขมาก กังวลมาก หรือตื่นเต้นสุด ๆ"),
          ("I think he feels totally excited.", "ฉันคิดว่าเขารู้สึกตื่นเต้นสุด ๆ"), kind="open",
          hint=("Look at his face and the big waterfall. Start with: I think he feels…", "ดูใบหน้าของเขาและน้ำตกใหญ่ เริ่มประโยคว่า I think he feels…")),
        X(("Look, check, and write: Question 2", "ดู เลือก และเขียน: ข้อ 2"), 50,
          ("Would you ever do this sport?", "นักเรียนจะลองเล่นกีฬานี้ไหม"),
          ("Yes, I would! It looks super exciting. / No, I wouldn't. It looks extremely dangerous.", "ใช่ ฉันจะลอง มันดูน่าตื่นเต้นสุด ๆ / ไม่ ฉันไม่ลอง มันดูอันตรายมาก"), kind="open",
          hint=("Answer Yes, I would or No, I wouldn't. Then give a reason.", "ตอบว่า Yes, I would หรือ No, I wouldn't แล้วบอกเหตุผล")),
        X(("Look, check, and write: Question 3", "ดู เลือก และเขียน: ข้อ 3"), 50,
          ("Write a caption for the photo.", "เขียนคำบรรยายใต้ภาพ"),
          ("Down the waterfall: totally exciting!", "ล่องลงน้ำตก: ตื่นเต้นสุด ๆ"), kind="open",
          hint=("A caption is a short title for a photo. Use only a few words.", "คำบรรยายใต้ภาพคือชื่อสั้น ๆ ของภาพ ใช้คำเพียงไม่กี่คำ")),
    ],
    "speak": {
        "models": [T("This sport looks really exciting.", "กีฬานี้ดูน่าตื่นเต้นมาก"),
                   T("I think he feels totally excited.", "ฉันคิดว่าเขารู้สึกตื่นเต้นสุด ๆ"),
                   T("Would you ever go kayaking?", "นักเรียนจะลองพายเรือคายัคไหม")],
        "turns": [
            {"q": T("What is your favorite sport?", "กีฬาที่นักเรียนชอบที่สุดคืออะไร"), "starter": T("My favorite sport is…", "กีฬาที่ฉันชอบที่สุดคือ…"),
             "example": T("My favorite sport is badminton.", "กีฬาที่ฉันชอบที่สุดคือแบดมินตัน")},
            {"q": T("Would you ever go kayaking down a waterfall?", "นักเรียนจะลองพายเรือคายัคลงน้ำตกไหม"), "starter": T("Yes, I would. / No, I wouldn't, because…", "ใช่ ฉันจะลอง / ไม่ ฉันไม่ลอง เพราะว่า…"),
             "example": T("No, I wouldn't, because it looks very dangerous!", "ไม่ ฉันไม่ลอง เพราะมันดูอันตรายมาก")},
        ],
    },
}

# ================================================================== 1. VOCABULARY 1
v1_words = [
    W("extreme sports", "noun", "กีฬาผาดโผน", "exciting and dangerous sports", "กีฬาที่น่าตื่นเต้นและอันตราย",
      "Many young people love extreme sports.", "คนหนุ่มสาวหลายคนชอบกีฬาผาดโผน", "extreme-sports"),
    W("land", "verb", "ลงสู่พื้น", "to come down to the ground after being in the air", "ลงมาถึงพื้นหลังจากลอยอยู่ในอากาศ",
      "The BMX rider jumps and then lands on the ground.", "นักปั่น BMX กระโดดแล้วลงสู่พื้น", "land", hl="lands"),
    W("length", "noun", "ความยาว", "how long something is", "บอกว่าสิ่งของยาวเท่าไร",
      "The length of the jump was two football fields!", "ความยาวของการกระโดดเท่ากับสนามฟุตบอลสองสนาม", "length"),
    W("flip", "verb", "ตีลังกา", "to turn over in the air", "หมุนตัวกลับหัวกลางอากาศ",
      "BMX riders can flip in the air.", "นักปั่น BMX ตีลังกากลางอากาศได้", "flip"),
    W("skiing", "noun", "การเล่นสกี", "moving fast over snow on two long boards", "การเคลื่อนที่เร็วบนหิมะด้วยแผ่นยาวสองแผ่น",
      "Skiing is popular in cold countries.", "การเล่นสกีเป็นที่นิยมในประเทศที่มีอากาศหนาว", "skiing"),
    W("kitesurfing", "noun", "การเล่นไคท์เซิร์ฟ", "surfing on a board while a big kite pulls you", "การโต้คลื่นบนกระดานโดยมีว่าวใหญ่ดึงไป",
      "Kitesurfing is a new kind of surfing.", "ไคท์เซิร์ฟเป็นการโต้คลื่นแบบใหม่", "kitesurfing"),
    W("crash", "verb", "ชน", "to hit something hard by accident", "พุ่งชนสิ่งของอย่างแรงโดยไม่ได้ตั้งใจ",
      "Be careful, or you will crash into the wall!", "ระวังนะ ไม่อย่างนั้นจะชนกำแพง", "crash"),
    W("strength", "noun", "ความแข็งแรง", "the power of being strong", "พลังของความแข็งแรง",
      "Kitesurfers need a lot of strength in their arms.", "นักไคท์เซิร์ฟต้องมีแขนที่แข็งแรงมาก", "strength"),
    W("hang-gliding", "noun", "การเล่นเครื่องร่อน", "flying with a big wing, like a bird", "การบินด้วยปีกขนาดใหญ่ เหมือนนก",
      "Hang-gliding is a very popular extreme sport.", "การเล่นเครื่องร่อนเป็นกีฬาผาดโผนที่นิยมมาก", "hang-gliding"),
    W("accident", "noun", "อุบัติเหตุ", "something bad that happens when you don't plan it", "เหตุร้ายที่เกิดขึ้นโดยไม่ได้ตั้งใจ",
      "Tom had a bike accident last year.", "ทอมประสบอุบัติเหตุจักรยานเมื่อปีที่แล้ว", "accident"),
    W("injury", "noun", "การบาดเจ็บ", "a hurt part of your body", "ส่วนของร่างกายที่ได้รับบาดเจ็บ",
      "Emma has an injury on her arm.", "เอ็มม่ามีแผลบาดเจ็บที่แขน", "injury"),
    W("equipment", "noun", "อุปกรณ์", "the things you need for an activity", "สิ่งของที่ต้องใช้ในการทำกิจกรรม",
      "You need special equipment for hang-gliding.", "การเล่นเครื่องร่อนต้องใช้อุปกรณ์พิเศษ", "equipment"),
    W("height", "noun", "ความสูง", "how high something is", "บอกว่าสิ่งของสูงเท่าไร",
      "The bird is flying at a great height.", "นกกำลังบินอยู่ที่ความสูงมาก", "height"),
    W("travel", "verb", "เดินทาง เคลื่อนที่", "to move from one place to another", "เคลื่อนที่จากที่หนึ่งไปอีกที่หนึ่ง",
      "The kitesurfer travels fast across the water.", "นักไคท์เซิร์ฟเคลื่อนที่เร็วข้ามผิวน้ำ", "travel", hl="travels"),
]

vocab1 = {
    "id": "vocab1", "title": T("Vocabulary 1: Extreme Sports", "คำศัพท์ 1: กีฬาผาดโผน"), "short": T("Vocabulary 1", "คำศัพท์ 1"),
    "pages": "Book p.52 to 53 · Workbook p.40 to 41",
    "learn": [
        L("Learn", "What are extreme sports?", "กีฬาผาดโผนคืออะไร", [
            ("Extreme sports are <b>dangerous</b> and <b>exciting</b>.", "กีฬาผาดโผนเป็นกีฬาที่อันตรายและน่าตื่นเต้น"),
            ("🪂 In the air: hang-gliding", "🪂 ในอากาศ: การเล่นเครื่องร่อน"),
            ("🌊 In the water: kitesurfing", "🌊 ในน้ำ: ไคท์เซิร์ฟ"),
            ("🚲 On land: BMX biking, skiing", "🚲 บนบก: การปั่นจักรยาน BMX การเล่นสกี"),
        ], page="📖 p.52"),
        L("Reading", "The text on page 52 (short summary)", "บทอ่านหน้า 52 (สรุปสั้น ๆ)", [
            ("Read the full text in your book. Here is a short summary.", "อ่านเนื้อเรื่องเต็มในหนังสือ นี่คือสรุปสั้น ๆ"),
            ("⛷️ Extreme skiers go super fast (240 km an hour) and fly a long way before they land.", "⛷️ นักสกีผาดโผนไปเร็วมาก (240 กิโลเมตรต่อชั่วโมง) และลอยไปไกลก่อนลงสู่พื้น"),
            ("🚲 In skiing and BMX biking, people flip in the air.", "🚲 ในการเล่นสกีและ BMX ผู้เล่นตีลังกากลางอากาศ"),
            ("🌊 Kitesurfers travel across the water at 55 km an hour or more. They need strong arms. People call them \"Charlie Browners.\"", "🌊 นักไคท์เซิร์ฟเคลื่อนที่บนน้ำ 55 กิโลเมตรต่อชั่วโมงหรือมากกว่า ต้องมีแขนแข็งแรง คนเรียกพวกเขาว่า \"ชาร์ลี บราวเนอร์ส\""),
            ("🪂 Hang-gliders can fly like birds, as high as 6,000 m.", "🪂 นักเล่นเครื่องร่อนบินได้เหมือนนก สูงได้ถึง 6,000 เมตร"),
            ("⚠️ Bad accidents are not common, but sometimes people get injuries.", "⚠️ อุบัติเหตุร้ายแรงไม่ค่อยเกิดขึ้น แต่บางครั้งก็มีคนบาดเจ็บ"),
        ], page="📖 p.52"),
        L("Word families", "long → length, strong → strength, high → height", "long → length, strong → strength, high → height", [
            ("Some adjectives have a noun partner.", "คำคุณศัพท์บางคำมีคำนามที่เป็นคู่กัน"),
        ], table=[["Adjective", "Noun"], ["long ยาว", "length ความยาว"], ["strong แข็งแรง", "strength ความแข็งแรง"], ["high สูง", "height ความสูง"]],
          examples=[("The bike is very <b>long</b>. What is its <b>length</b>?", "จักรยานยาวมาก ความยาวของมันเท่าไร"),
                    ("The boy is <b>strong</b>. He has a lot of <b>strength</b>.", "เด็กชายแข็งแรง เขามีความแข็งแรงมาก"),
                    ("The hill is very <b>high</b>. What is its <b>height</b>?", "เนินเขาสูงมาก ความสูงของมันเท่าไร")],
          note=("Spelling: lenGTH, strenGTH, but heiGHT.", "การสะกด: length, strength ลงท้ายด้วย gth แต่ height ลงท้ายด้วย ght"), page="📒 p.40"),
        L("Action words", "Actions: fly, flip, land, crash, travel", "คำกริยาแสดงการกระทำ: fly, flip, land, crash, travel", [
            ("These verbs describe what athletes do.", "คำกริยาเหล่านี้บอกว่านักกีฬาทำอะไร"),
        ], table=[["Now", "Past"], ["fly", "flew"], ["flip", "flipped"], ["land", "landed"], ["crash", "crashed"], ["travel", "traveled"]],
          examples=[("The rider <b>flipped</b> in the air and <b>landed</b> safely.", "นักปั่นตีลังกากลางอากาศแล้วลงสู่พื้นอย่างปลอดภัย"),
                    ("James <b>crashed</b> into a tree, but he was OK.", "เจมส์ชนต้นไม้ แต่เขาไม่เป็นไร")],
          note=("American spelling: traveled (one l), like in your book.", "การสะกดแบบอเมริกัน: traveled (l ตัวเดียว) เหมือนในหนังสือ"), page="📖 p.52"),
    ],
    "words": v1_words,
    "book": [
        X(EX(1, "Listen and read.", "ฟังและอ่าน"), 52, ("Listen to the text on page 52 and read it in your book.", "ฟังบทอ่านหน้า 52 และอ่านตามในหนังสือ"),
          kind="class", classNote=("Do this in class with the audio (TR: 5.1). Then look at the Learn summary.", "ทำในห้องเรียนพร้อมฟังเสียง (TR: 5.1) แล้วดูสรุปในส่วน Learn")),
        X(EX(2, "Listen and repeat.", "ฟังและพูดตาม"), 52, ("Listen and repeat the new words.", "ฟังและพูดคำศัพท์ใหม่ตาม"),
          kind="class", classNote=("Do this in class with the audio (TR: 5.2), or use the 🔊 buttons in Word Cards.", "ทำในห้องเรียนพร้อมฟังเสียง (TR: 5.2) หรือกดปุ่ม 🔊 ในบัตรคำศัพท์")),
        X(EX(3, "Ask and answer.", "ถามและตอบ"), 53, ("What are kitesurfers called?", "นักไคท์เซิร์ฟถูกเรียกว่าอะไร"),
          ("They're called \"Charlie Browners.\"", "พวกเขาถูกเรียกว่า \"ชาร์ลี บราวเนอร์ส\""), inst=("Work with a partner. What did you learn?", "ทำกับเพื่อน นักเรียนได้เรียนรู้อะไร"),
          hint=("Look at the kitesurfing part of the text on page 52.", "ดูย่อหน้าเรื่องไคท์เซิร์ฟในหน้า 52")),
        X(EX(3, "Ask and answer.", "ถามและตอบ"), 53, ("How fast can extreme skiers go?", "นักสกีผาดโผนไปได้เร็วเท่าไร"),
          ("They can go 240 km (150 mi.) an hour.", "ไปได้ 240 กิโลเมตร (150 ไมล์) ต่อชั่วโมง"),
          hint=("Find the word \"speeds\" in the first part of the text.", "หาคำว่า speeds ในส่วนแรกของเนื้อเรื่อง")),
        X(EX(3, "Ask and answer.", "ถามและตอบ"), 53, ("What do kitesurfers need in their arms?", "นักไคท์เซิร์ฟต้องมีอะไรที่แขน"),
          ("They need lots of strength.", "ต้องมีความแข็งแรงมาก"), hint=("It is a noun from \"strong.\"", "เป็นคำนามที่มาจากคำว่า strong")),
        X(EX(3, "Ask and answer.", "ถามและตอบ"), 53, ("In which two sports do people flip in the air?", "กีฬาสองชนิดไหนที่ผู้เล่นตีลังกากลางอากาศ"),
          ("In skiing and BMX biking.", "การเล่นสกีและการปั่นจักรยาน BMX"), hint=("Find the word \"flip\" on page 52.", "หาคำว่า flip ในหน้า 52")),
        X(EX(3, "Ask and answer.", "ถามและตอบ"), 53, ("How high can you fly when you go hang-gliding?", "เล่นเครื่องร่อนบินได้สูงเท่าไร"),
          ("You can fly at a height of 6,000 m (20,000 ft.).", "บินได้ที่ความสูง 6,000 เมตร (20,000 ฟุต)"), hint=("Find the word \"height.\"", "หาคำว่า height")),
        X(EX(3, "Ask and answer.", "ถามและตอบ"), 53, ("Are serious accidents common in hang-gliding?", "อุบัติเหตุร้ายแรงในการเล่นเครื่องร่อนเกิดบ่อยไหม"),
          ("No, they aren't. But sometimes people have injuries when they land.", "ไม่บ่อย แต่บางครั้งผู้เล่นได้รับบาดเจ็บตอนลงสู่พื้น"), hint=("Read the hang-gliding part again.", "อ่านส่วนที่เกี่ยวกับเครื่องร่อนอีกครั้ง")),
    ],
    "wb": [
        X(EX(1, "Find the secret message.", "หาข้อความลับ"), 40, ("Cross out the names of three sports.", "ขีดฆ่าชื่อกีฬา 3 ชนิด"),
          ("hang-gliding, kitesurfing, skiing", "การเล่นเครื่องร่อน ไคท์เซิร์ฟ การเล่นสกี"),
          box=["accident", "are", "cool", "equipment", "extreme sports", "hang-gliding", "height", "injury", "kitesurfing", "length", "skiing", "strength", "to crash", "to flip", "to land", "to travel"],
          hint=("\"Extreme sports\" is a group of sports, not the name of one sport.", "\"extreme sports\" เป็นกลุ่มของกีฬา ไม่ใช่ชื่อกีฬาชนิดเดียว"), say=False),
        X(EX(1, "Find the secret message.", "หาข้อความลับ"), 40, ("Cross out four actions.", "ขีดฆ่าคำกริยาแสดงการกระทำ 4 คำ"),
          ("to crash, to flip, to land, to travel", "ชน ตีลังกา ลงสู่พื้น เดินทาง"),
          hint=("Actions are verbs. They often have \"to\" in front.", "คำแสดงการกระทำคือคำกริยา มักมี to อยู่ข้างหน้า"), say=False),
        X(EX(1, "Find the secret message.", "หาข้อความลับ"), 40, ("Cross out the nouns formed from long, strong, and high.", "ขีดฆ่าคำนามที่มาจาก long, strong และ high"),
          ("length, strength, height", "ความยาว ความแข็งแรง ความสูง"), hint=("Look at the Word families card in Learn.", "ดูบัตร Word families ในส่วน Learn"), say=False),
        X(EX(1, "Find the secret message.", "หาข้อความลับ"), 40, ("Cross out all the words with three syllables (for example, e-quip-ment).", "ขีดฆ่าคำที่มี 3 พยางค์ทั้งหมด (เช่น e-quip-ment)"),
          ("accident (ac-ci-dent), equipment (e-quip-ment), injury (in-ju-ry)", "accident, equipment, injury"),
          steps=[("Clap the words that are left: ac-ci-dent = 3 claps.", "ปรบมือตามพยางค์ของคำที่เหลือ: ac-ci-dent = ปรบ 3 ครั้ง"),
                 ("are = 1, cool = 1. Keep them.", "are = 1 พยางค์ cool = 1 พยางค์ เก็บไว้")],
          hint=("Clap your hands for each part of the word.", "ปรบมือหนึ่งครั้งต่อหนึ่งพยางค์"), say=False),
        X(EX(1, "Find the secret message.", "หาข้อความลับ"), 40, ("Read the words that you didn't cross out. Write the message.", "อ่านคำที่ไม่ได้ขีดฆ่า แล้วเขียนข้อความ"),
          ("Extreme sports are cool!", "กีฬาผาดโผนเจ๋งมาก"),
          steps=[("Three words are left: extreme sports, are, cool.", "เหลือ 3 คำ: extreme sports, are, cool"),
                 ("Put them in an order that makes a sentence.", "เรียงให้เป็นประโยค")],
          hint=("Three words are not crossed out. Make a sentence with them.", "มี 3 คำที่ไม่ถูกขีดฆ่า นำมาแต่งเป็นประโยค"), say=False),
        X(EX(2, "Look and write.", "ดูและเขียน"), 40, ("The ____ of this bike is 86 cm (34 inches).", "____ ของจักรยานคันนี้คือ 86 ซม. (34 นิ้ว)"),
          ("height", "ความสูง"), inst=("Complete the sentences. Look at the picture of the boy and the bike.", "เติมประโยคให้สมบูรณ์ ดูภาพเด็กชายและจักรยาน"),
          why=("86 cm goes from the ground up to the top of the bike, so it is the height. (This one is the example in the book.)", "86 ซม. วัดจากพื้นขึ้นไปถึงด้านบนของจักรยาน จึงเป็นความสูง (ข้อนี้เป็นตัวอย่างในหนังสือ)")),
        X(EX(2, "Look and write.", "ดูและเขียน"), 40, ("If you buy a BMX bike, you should always check the ____ of the \"top tube.\"", "ถ้าซื้อจักรยาน BMX ควรตรวจดู ____ ของ \"ท่อบน\" เสมอ"),
          ("length", "ความยาว"), hint=("The top tube goes from the handlebars to the seat. Is it long or high?", "ท่อบนยาวจากแฮนด์ไปถึงเบาะ มันยาวหรือสูง"),
          why=("We measure how long the top tube is, so the answer is length.", "เราวัดว่าท่อบนยาวเท่าไร คำตอบคือ length")),
        X(EX(2, "Look and write.", "ดูและเขียน"), 40, ("The ____ of this bike's top tube is ____.", "____ ของท่อบนจักรยานคันนี้คือ ____"),
          ("The length of this bike's top tube is 38 cm (15 inches).", "ความยาวของท่อบนจักรยานคันนี้คือ 38 ซม. (15 นิ้ว)"),
          hint=("Find the number on the bar between the handlebars and the seat.", "หาตัวเลขบนท่อระหว่างแฮนด์กับเบาะ")),
        X(EX(2, "Look and write.", "ดูและเขียน"), 40, ("The boy's ____ is ____. He's the tallest boy in my class.", "____ ของเด็กชายคือ ____ เขาเป็นเด็กที่สูงที่สุดในห้อง"),
          ("The boy's height is 137 cm (54 inches).", "ความสูงของเด็กชายคือ 137 ซม. (54 นิ้ว)"),
          hint=("Look at the number next to the boy.", "ดูตัวเลขข้างตัวเด็กชาย")),
        X(EX(3, "Describe the pictures.", "บรรยายภาพ"), 41, ("Picture 2: a skier upside down in the air.", "ภาพที่ 2: นักสกีกลับหัวอยู่กลางอากาศ"),
          ("He's skiing. He's flipping in the air. He'll land in the snow.", "เขากำลังเล่นสกี เขากำลังตีลังกากลางอากาศ เขาจะลงสู่หิมะ"), kind="open",
          inst=("Use the words in the box.", "ใช้คำในกรอบ"),
          box=["go hang-gliding", "go kitesurfing", "go skiing", "flip", "land", "travel", "along the water", "in a field", "in the air", "equipment", "accident", "strength"],
          hint=("Example 1 in the book: He's riding his motorcycle. He's crashing into a rock. He may have an injury.", "ตัวอย่างข้อ 1 ในหนังสือ: He's riding his motorcycle. He's crashing into a rock. He may have an injury.")),
        X(EX(3, "Describe the pictures.", "บรรยายภาพ"), 41, ("Picture 3: a person hanging under a big wing.", "ภาพที่ 3: คนห้อยอยู่ใต้ปีกขนาดใหญ่"),
          ("He's going hang-gliding. He's flying in the air. He'll land in a field.", "เขากำลังเล่นเครื่องร่อน เขากำลังบินอยู่ในอากาศ เขาจะลงจอดในทุ่ง"), kind="open",
          box=["go hang-gliding", "go kitesurfing", "go skiing", "flip", "land", "travel", "along the water", "in a field", "in the air", "equipment", "accident", "strength"],
          hint=("Use: go hang-gliding, in the air, land, in a field.", "ใช้คำว่า go hang-gliding, in the air, land, in a field")),
        X(EX(3, "Describe the pictures.", "บรรยายภาพ"), 41, ("Picture 4: a girl on a board with a kite.", "ภาพที่ 4: เด็กผู้หญิงบนกระดานพร้อมว่าว"),
          ("She's going kitesurfing. She's traveling along the water. She needs a lot of strength.", "เธอกำลังเล่นไคท์เซิร์ฟ เธอกำลังเคลื่อนที่ไปตามผิวน้ำ เธอต้องใช้ความแข็งแรงมาก"), kind="open",
          box=["go hang-gliding", "go kitesurfing", "go skiing", "flip", "land", "travel", "along the water", "in a field", "in the air", "equipment", "accident", "strength"],
          hint=("Use: go kitesurfing, travel, along the water, strength.", "ใช้คำว่า go kitesurfing, travel, along the water, strength")),
        X(EX(4, "Read. Then match the questions and answers.", "อ่าน แล้วจับคู่คำถามกับคำตอบ"), 41, ("1. My favorite sport is surfing. What about you?", "1. กีฬาที่ฉันชอบที่สุดคือโต้คลื่น แล้วเธอล่ะ"),
          ("e. I like skateboarding best of all, but I'm not very good at it!", "e. ฉันชอบสเก็ตบอร์ดที่สุด แต่ฉันเล่นไม่ค่อยเก่ง"), choices=["a", "b", "c", "d", "e"], right=4,
          hint=("\"What about you?\" asks about YOUR favorite sport.", "What about you? ถามถึงกีฬาที่เธอชอบ")),
        X(EX(4, "Read. Then match the questions and answers.", "อ่าน แล้วจับคู่คำถามกับคำตอบ"), 41, ("2. Have you ever had an accident while playing sports?", "2. เธอเคยประสบอุบัติเหตุขณะเล่นกีฬาไหม"),
          ("b. Yes, a year ago. I crashed into a rock on my bike and broke my arm.", "b. เคย เมื่อปีที่แล้ว ฉันขี่จักรยานชนหินและแขนหัก"), choices=["a", "b", "c", "d", "e"], right=1,
          hint=("Look for an answer that starts with Yes and tells a story.", "หาคำตอบที่ขึ้นต้นด้วย Yes และเล่าเหตุการณ์")),
        X(EX(4, "Read. Then match the questions and answers.", "อ่าน แล้วจับคู่คำถามกับคำตอบ"), 41, ("3. What kind of equipment do you need for swimming?", "3. ว่ายน้ำต้องใช้อุปกรณ์อะไรบ้าง"),
          ("d. Nothing expensive, just a swimsuit.", "d. ไม่มีอะไรแพง แค่ชุดว่ายน้ำ"), choices=["a", "b", "c", "d", "e"], right=3,
          hint=("Which answer talks about a thing you wear?", "คำตอบไหนพูดถึงสิ่งที่สวมใส่")),
        X(EX(4, "Read. Then match the questions and answers.", "อ่าน แล้วจับคู่คำถามกับคำตอบ"), 41, ("4. I love to watch extreme sports on TV. Those athletes are so amazing.", "4. ฉันชอบดูกีฬาผาดโผนทางทีวี นักกีฬาเหล่านั้นสุดยอดมาก"),
          ("a. I agree. I like how some of them flip in the air before landing.", "a. ฉันเห็นด้วย ฉันชอบตอนที่บางคนตีลังกากลางอากาศก่อนลงสู่พื้น"), choices=["a", "b", "c", "d", "e"], right=0,
          hint=("When someone gives an opinion, you can say \"I agree.\"", "เมื่อมีคนแสดงความคิดเห็น เราตอบได้ว่า I agree")),
        X(EX(4, "Read. Then match the questions and answers.", "อ่าน แล้วจับคู่คำถามกับคำตอบ"), 41, ("5. What's the worst injury you've ever had?", "5. การบาดเจ็บที่แย่ที่สุดที่เธอเคยเป็นคืออะไร"),
          ("c. I've broken a finger, but that's all. I've been very lucky!", "c. ฉันเคยนิ้วหัก แค่นั้นเอง ฉันโชคดีมาก"), choices=["a", "b", "c", "d", "e"], right=2,
          hint=("Look for an injury: a part of the body.", "หาคำตอบที่พูดถึงการบาดเจ็บของร่างกาย")),
        X(EX(5, "Listen and speak.", "ฟังและพูด"), 41, ("Check your answers to Activity 4. Then listen and repeat.", "ตรวจคำตอบกิจกรรมที่ 4 แล้วฟังและพูดตาม"),
          kind="class", classNote=("Do this in class with the audio (TR: 5.1). At home, practise the five conversations in the Speak activity.", "ทำในห้องเรียนพร้อมฟังเสียง (TR: 5.1) ที่บ้านฝึกบทสนทนาทั้ง 5 ในกิจกรรมฝึกพูด")),
    ],
    "speak": {
        "tip": T("Listen 🔊, then say it. Press 🎤 to check your speaking (Chrome or Safari).", "ฟัง 🔊 แล้วพูดตาม กด 🎤 เพื่อตรวจการพูด (Chrome หรือ Safari)"),
        "models": [
            T("My favorite sport is surfing. What about you?", "กีฬาที่ฉันชอบที่สุดคือโต้คลื่น แล้วเธอล่ะ"),
            T("I like skateboarding best of all.", "ฉันชอบสเก็ตบอร์ดที่สุด"),
            T("Have you ever had an accident while playing sports?", "เธอเคยประสบอุบัติเหตุขณะเล่นกีฬาไหม"),
            T("Yes, a year ago. I crashed into a rock on my bike.", "เคย เมื่อปีที่แล้ว ฉันขี่จักรยานชนหิน"),
            T("What kind of equipment do you need for swimming?", "ว่ายน้ำต้องใช้อุปกรณ์อะไรบ้าง"),
            T("What's the worst injury you've ever had?", "การบาดเจ็บที่แย่ที่สุดที่เธอเคยเป็นคืออะไร"),
        ],
        "turns": [
            {"q": T("What extreme sport would you like to try?", "นักเรียนอยากลองกีฬาผาดโผนชนิดไหน"), "starter": T("I'd like to try… because it looks…", "ฉันอยากลอง… เพราะมันดู…"),
             "example": T("I'd like to try kitesurfing because it looks exciting.", "ฉันอยากลองไคท์เซิร์ฟเพราะมันดูน่าตื่นเต้น")},
            {"q": T("What equipment do you need for hang-gliding?", "การเล่นเครื่องร่อนต้องใช้อุปกรณ์อะไร"), "starter": T("You need…", "ต้องใช้…"),
             "example": T("You need a hang-glider and a helmet.", "ต้องใช้เครื่องร่อนและหมวกกันน็อก")},
            {"q": T("Have you ever had an injury?", "นักเรียนเคยบาดเจ็บไหม"), "starter": T("Yes, I have. I… / No, I haven't.", "เคย ฉัน… / ไม่เคย"),
             "example": T("Yes, I have. I hurt my knee when I fell off my bike.", "เคย ฉันเจ็บเข่าตอนตกจักรยาน")},
        ],
    },
    "spell": [{"w": w["w"], "th": w["th"]} for w in v1_words],
    "match": [[w["w"], f'<img src="{w["img"]}" alt="" loading="lazy">'] for w in v1_words[:13]] + [["travel", "เดินทาง เคลื่อนที่"]],
    "sort": {"title": T("Is it a sport, an action, or a size word?", "เป็นชื่อกีฬา คำกริยา หรือคำบอกขนาด"),
             "bins": [T("Sport", "กีฬา"), T("Action (verb)", "การกระทำ (คำกริยา)"), T("Size or power (noun)", "ขนาดหรือพลัง (คำนาม)")],
             "items": [["skiing", 0], ["kitesurfing", 0], ["hang-gliding", 0], ["BMX biking", 0], ["flip", 1], ["land", 1], ["crash", 1], ["travel", 1],
                       ["length", 2], ["height", 2], ["strength", 2]]},
    "build": ["Extreme sports | are | cool!", "The skier | flies | and then | lands.", "Kitesurfers need | a lot of | strength | in their arms.",
              "You need | special equipment | for hang-gliding.", "BMX riders | flip | in the air.", "Tom had | a bad accident | on his bike."],
    "quiz": [
        Q("Which word means \"to turn over in the air\"?", "คำไหนแปลว่า \"ตีลังกากลางอากาศ\"", ["flip", "land", "crash", "travel"]),
        Q("Which word means \"how high something is\"?", "คำไหนแปลว่า \"ความสูง\"", ["height", "length", "strength", "injury"]),
        Q("Which word means \"how long something is\"?", "คำไหนแปลว่า \"ความยาว\"", ["length", "height", "strength", "equipment"]),
        Q("Kitesurfers need a lot of ____ in their arms.", "นักไคท์เซิร์ฟต้องมี ____ ที่แขนมาก", ["strength", "height", "length", "accident"]),
        Q("A helmet and knee pads are sports ____.", "หมวกกันน็อกและสนับเข่าเป็น ____ กีฬา", ["equipment", "injuries", "accidents", "heights"]),
        Q("After the jump, the rider ____ on the ground.", "หลังกระโดด นักปั่น ____ บนพื้น", ["lands", "flips", "travels", "crashes"]),
        Q("Which sport uses a big kite and a board on the water?", "กีฬาไหนใช้ว่าวใหญ่และกระดานบนน้ำ", ["kitesurfing", "skiing", "hang-gliding", "BMX biking"]),
        Q("Which sport do you do on snow?", "กีฬาไหนเล่นบนหิมะ", ["skiing", "kitesurfing", "hang-gliding", "surfing"]),
        Q("Emma broke her arm. It was a bad ____.", "เอ็มม่าแขนหัก มันเป็น ____ ที่ร้ายแรง", ["injury", "height", "equipment", "flip"]),
        Q("Be careful! Don't ____ into the tree!", "ระวัง! อย่า ____ ต้นไม้", ["crash", "land", "flip", "travel"]),
        Q("What are kitesurfers called in the book?", "ในหนังสือ นักไคท์เซิร์ฟถูกเรียกว่าอะไร", ["Charlie Browners", "Sky Riders", "Wave Kings", "Kite Flyers"]),
        Q("Which noun comes from \"strong\"?", "คำนามไหนมาจาก strong", ["strength", "strongth", "stronger", "strongness"]),
    ],
}

# ================================================================== 2. GRAMMAR 1
grammar1 = {
    "id": "grammar1", "title": T("Grammar 1: Present perfect with for and since", "ไวยากรณ์ 1: Present Perfect กับ for และ since"),
    "short": T("Grammar 1", "ไวยากรณ์ 1"), "pages": "Book p.54 · Workbook p.42",
    "learn": [
        L("Rule 1", "The present perfect: from the past up to now", "Present Perfect: จากอดีตจนถึงตอนนี้", [
            ("We use the present perfect for something that <b>started in the past</b> and is <b>still true now</b>.", "ใช้ Present Perfect กับสิ่งที่เริ่มในอดีตและยังเป็นจริงอยู่ตอนนี้"),
            ("⏪ 2015 ─────────────▶ now ✅", "⏪ 2015 ─────────────▶ ตอนนี้ ✅"),
        ], examples=[("I <b>have lived</b> here for ten years. (I still live here.)", "ฉันอาศัยอยู่ที่นี่มา 10 ปีแล้ว (ตอนนี้ยังอยู่)"),
                     ("Kitesurfing <b>has been</b> popular since 2000.", "ไคท์เซิร์ฟเป็นที่นิยมตั้งแต่ปี 2000")], page="📖 p.54"),
        L("Rule 2", "How to make it: have / has + past participle", "วิธีสร้าง: have / has + กริยาช่องที่ 3", [
            ("I, you, we, they → <b>have</b> ('ve)", "I, you, we, they → have ('ve)"),
            ("he, she, it, one sport → <b>has</b> ('s)", "he, she, it, กีฬาหนึ่งชนิด → has ('s)"),
            ("Not: haven't = have not, hasn't = has not", "ปฏิเสธ: haven't = have not, hasn't = has not"),
        ], table=[["Who", "have / has", "past participle", ""], ["I", "have ('ve)", "worked", "here for ten years."], ["I", "haven't", "taken", "a vacation since 2016."],
                  ["Snowboarding", "has", "been", "popular since the Olympics."], ["Skiing", "hasn't", "been", "popular for many years."]], page="📒 p.42"),
        L("Rule 3", "FOR + a period of time ⏳", "FOR + ช่วงเวลา ⏳", [
            ("Use <b>for</b> to say HOW LONG.", "ใช้ for เพื่อบอกว่านานเท่าไร"),
            ("for ten years · for five days · for a month · for an hour · for a long time", "for ten years (เป็นเวลาสิบปี) · for five days · for a month · for an hour · for a long time"),
        ], examples=[("Surfing has been my favorite sport <b>for</b> many years.", "การโต้คลื่นเป็นกีฬาที่ฉันชอบที่สุดมาหลายปีแล้ว"),
                     ("Lily has had her bike <b>for</b> three years.", "ลิลลี่มีจักรยานมา 3 ปีแล้ว")],
          note=("Ask: Can I count it? (ten years, two weeks) → for", "ถามตัวเองว่า นับได้ไหม (10 ปี 2 สัปดาห์) → ใช้ for"), page="📖 p.54"),
        L("Rule 4", "SINCE + a point in time 📍", "SINCE + จุดเริ่มต้นของเวลา 📍", [
            ("Use <b>since</b> to say WHEN it started.", "ใช้ since เพื่อบอกว่าเริ่มเมื่อไร"),
            ("since 2016 · since June · since Monday · since last year · since the 1970s · since I was born", "since 2016 (ตั้งแต่ปีนั้น) · since June · since Monday · since last year · since the 1970s · since I was born"),
        ], examples=[("Many people have had accidents <b>since</b> last year.", "หลายคนประสบอุบัติเหตุตั้งแต่ปีที่แล้ว"),
                     ("He has wanted to go skiing <b>since</b> he was a boy.", "เขาอยากไปเล่นสกีตั้งแต่ยังเป็นเด็ก")],
          note=("Ask: Is it a start date or moment? (2016, Monday, I was born) → since", "ถามตัวเองว่า เป็นวันหรือเวลาที่เริ่มต้นไหม (2016 วันจันทร์ ตอนฉันเกิด) → ใช้ since"), page="📖 p.54"),
        L("Verbs", "Past participles you need", "กริยาช่องที่ 3 ที่ต้องใช้", [
            ("Regular verbs add -ed. Irregular verbs change. Learn them!", "กริยาปกติเติม -ed กริยาผิดปกติเปลี่ยนรูป ต้องจำ"),
        ], table=[["Verb", "Past participle"], ["be", "been"], ["have", "had"], ["do", "done"], ["take", "taken"], ["ride", "ridden"], ["know", "known"],
                  ["want", "wanted"], ["work", "worked"], ["enjoy", "enjoyed"], ["try", "tried"], ["play", "played"], ["live", "lived"]], page="📖 p.54"),
        L("Questions", "Asking: How long have you…?", "การถาม: How long have you…? (นานเท่าไรแล้ว)", [
            ("How long + have/has + person + past participle?", "How long + have/has + ผู้กระทำ + กริยาช่องที่ 3"),
        ], examples=[("How long <b>have</b> you <b>had</b> a bicycle?", "เธอมีจักรยานมานานเท่าไรแล้ว"),
                     ("I've had a bike <b>for</b> five years.", "ฉันมีจักรยานมา 5 ปีแล้ว"),
                     ("I've had one <b>since</b> I was six.", "ฉันมีมาตั้งแต่อายุ 6 ขวบ")], page="📖 p.54"),
        L("Trick", "Change since to for: do the math!", "เปลี่ยน since เป็น for: คิดเลข", [
            ("Count the years from the start until now (2026).", "นับจำนวนปีจากจุดเริ่มต้นจนถึงตอนนี้ (2026)"),
        ], examples=[("since 2014 → 2026 minus 2014 = 12 → for 12 years", "since 2014 → 2026 ลบ 2014 = 12 → for 12 years"),
                     ("since 2000 → 2026 minus 2000 = 26 → for 26 years", "since 2000 → 2026 ลบ 2000 = 26 → for 26 years")],
          note=("Your workbook was written some years ago, so its example says \"more than six years.\" Use this year for your answers.", "แบบฝึกหัดเขียนไว้หลายปีก่อน ตัวอย่างจึงบอกว่า more than six years ให้ใช้ปีปัจจุบันในการตอบ"), page="📒 p.42"),
    ],
    "book": [
        X(EX(1, "Read. Write and underline.", "อ่าน เขียน และขีดเส้นใต้"), 54, ("Kitesurfing ____ popular for/since I was a kid.", "ไคท์เซิร์ฟ ____ เป็นที่นิยม for/since ฉันยังเป็นเด็ก"),
          ("Kitesurfing has been popular since I was a kid.", "ไคท์เซิร์ฟเป็นที่นิยมตั้งแต่ฉันยังเป็นเด็ก"),
          inst=("Use the words in the box. Write the verb, then underline for or since.", "ใช้คำในกรอบ เขียนกริยา แล้วขีดเส้นใต้ for หรือ since"), box=["be", "be", "be", "have", "want"],
          why=("This is the example. \"I was a kid\" is a point in time, so since.", "ข้อนี้เป็นตัวอย่าง I was a kid เป็นจุดเริ่มต้นของเวลา จึงใช้ since")),
        X(EX(1, "Read. Write and underline.", "อ่าน เขียน และขีดเส้นใต้"), 54, ("Surfing ____ my favorite sport for/since many years.", "การโต้คลื่น ____ กีฬาที่ฉันชอบที่สุด for/since หลายปี"),
          ("Surfing has been my favorite sport for many years.", "การโต้คลื่นเป็นกีฬาที่ฉันชอบที่สุดมาหลายปีแล้ว"), choices=["for", "since"], right=0,
          hint=("Surfing = it, so use has. \"Many years\" is a period of time.", "Surfing = it ใช้ has ส่วน many years เป็นช่วงเวลา"),
          why=("be → has been. Many years = how long → for.", "be → has been ส่วน many years บอกว่านานเท่าไร → for")),
        X(EX(1, "Read. Write and underline.", "อ่าน เขียน และขีดเส้นใต้"), 54, ("Many people ____ accidents for/since last year.", "หลายคน ____ อุบัติเหตุ for/since ปีที่แล้ว"),
          ("Many people have had accidents since last year.", "หลายคนประสบอุบัติเหตุตั้งแต่ปีที่แล้ว"), choices=["for", "since"], right=1,
          hint=("Many people = they, so use have. Which verb from the box goes with accidents?", "Many people = they ใช้ have กริยาไหนในกรอบใช้กับ accidents"),
          why=("have → have had. Last year = when it started → since.", "have → have had ส่วน last year คือจุดเริ่มต้น → since")),
        X(EX(1, "Read. Write and underline.", "อ่าน เขียน และขีดเส้นใต้"), 54, ("Skiing ____ my dad's favorite sport for/since the last twenty years.", "การเล่นสกี ____ กีฬาที่พ่อชอบที่สุด for/since 20 ปีที่ผ่านมา"),
          ("Skiing has been my dad's favorite sport for the last twenty years.", "การเล่นสกีเป็นกีฬาที่พ่อชอบที่สุดมาตลอด 20 ปีที่ผ่านมา"), choices=["for", "since"], right=0,
          hint=("\"The last twenty years\" is how long.", "the last twenty years บอกว่านานเท่าไร"),
          why=("be → has been. Twenty years = a period of time → for.", "be → has been ส่วน 20 ปีเป็นช่วงเวลา → for")),
        X(EX(1, "Read. Write and underline.", "อ่าน เขียน และขีดเส้นใต้"), 54, ("He ____ to go skiing for/since he was a boy.", "เขา ____ ไปเล่นสกี for/since เขายังเป็นเด็กชาย"),
          ("He has wanted to go skiing since he was a boy.", "เขาอยากไปเล่นสกีตั้งแต่ยังเป็นเด็กชาย"), choices=["for", "since"], right=1,
          hint=("Only \"want\" is left in the box. He → has.", "ในกรอบเหลือแค่ want ส่วน He → has"),
          why=("want → has wanted. \"He was a boy\" is a point in time → since.", "want → has wanted ส่วน he was a boy เป็นจุดเริ่มต้น → since")),
        X(EX(2, "Play a game.", "เล่นเกม"), 54, ("Use the game board in the back of the book. Take turns. Ask the person on your left a question.", "ใช้กระดานเกมท้ายเล่ม ผลัดกันถามคำถามคนที่อยู่ทางซ้าย"),
          ("How long have you had a bicycle? I've had one for three years.", "เธอมีจักรยานมานานเท่าไรแล้ว ฉันมีมา 3 ปีแล้ว"), kind="open",
          hint=("Heads = move 1 space. Tails = move 2 spaces. Ask: How long have you…?", "ออกหัว = เดิน 1 ช่อง ออกก้อย = เดิน 2 ช่อง ถามว่า How long have you…?")),
    ],
    "wb": [
        X(EX(1, "Read and write.", "อ่านและเขียน"), 42, ("My friends / be / fans of hang-gliding / 2014.", "เพื่อนของฉัน / เป็น / แฟนของการเล่นเครื่องร่อน / 2014"),
          ("My friends have been fans of hang-gliding since 2014.", "เพื่อนของฉันเป็นแฟนการเล่นเครื่องร่อนตั้งแต่ปี 2014"),
          inst=("Look at the timeline. Write the sentences with since.", "ดูเส้นเวลา เขียนประโยคโดยใช้ since"),
          why=("This is the example in the workbook.", "ข้อนี้เป็นตัวอย่างในแบบฝึกหัด")),
        X(EX(1, "Read and write.", "อ่านและเขียน"), 42, ("People / enjoy / kitesurfing / 2000.", "ผู้คน / สนุกกับ / ไคท์เซิร์ฟ / 2000"),
          ("People have enjoyed kitesurfing since 2000.", "ผู้คนสนุกกับไคท์เซิร์ฟมาตั้งแต่ปี 2000"),
          steps=[("People = they → have.", "People = they → ใช้ have"), ("enjoy → enjoyed.", "enjoy → enjoyed"), ("2000 is a point in time → since.", "2000 เป็นจุดเริ่มต้น → since")]),
        X(EX(1, "Read and write.", "อ่านและเขียน"), 42, ("Surfing / be popular / around the world / the 1970s.", "การโต้คลื่น / เป็นที่นิยม / ทั่วโลก / ทศวรรษ 1970"),
          ("Surfing has been popular around the world since the 1970s.", "การโต้คลื่นเป็นที่นิยมทั่วโลกตั้งแต่ทศวรรษ 1970"),
          steps=[("Surfing = it → has.", "Surfing = it → ใช้ has"), ("be → been.", "be → been"), ("the 1970s is a point in time → since.", "ทศวรรษ 1970 เป็นจุดเริ่มต้น → since")]),
        X(EX(1, "Read and write.", "อ่านและเขียน"), 42, ("1960s / more than 10 million people / try / skateboarding.", "ทศวรรษ 1960 / คนมากกว่า 10 ล้านคน / ลอง / สเก็ตบอร์ด"),
          ("More than 10 million people have tried skateboarding since the 1960s.", "คนมากกว่า 10 ล้านคนได้ลองเล่นสเก็ตบอร์ดตั้งแต่ทศวรรษ 1960"),
          hint=("Start with the people. try → tried (y changes to i).", "เริ่มประโยคด้วยผู้คน try → tried (เปลี่ยน y เป็น i)")),
        X(EX(2, "Read and write.", "อ่านและเขียน"), 42, ("Rewrite sentence 1 with for: My friends have been fans of hang-gliding since 2014.", "เขียนประโยคที่ 1 ใหม่โดยใช้ for: เพื่อนของฉันเป็นแฟนการเล่นเครื่องร่อนตั้งแต่ปี 2014"),
          ("My friends have been fans of hang-gliding for 12 years.", "เพื่อนของฉันเป็นแฟนการเล่นเครื่องร่อนมา 12 ปีแล้ว"),
          inst=("Read the sentences in Activity 1 and do the math! Rewrite the sentences.", "อ่านประโยคในกิจกรรมที่ 1 แล้วคิดเลข เขียนประโยคใหม่"),
          steps=[("2026 minus 2014 = 12.", "2026 ลบ 2014 = 12")],
          why=("The workbook example says \"for more than six years\" because the book is older. In 2026 it is 12 years.", "ตัวอย่างในแบบฝึกหัดบอกว่า for more than six years เพราะหนังสือพิมพ์นานแล้ว ในปี 2026 คือ 12 ปี")),
        X(EX(2, "Read and write.", "อ่านและเขียน"), 42, ("Rewrite sentence 2 with for: People have enjoyed kitesurfing since 2000.", "เขียนประโยคที่ 2 ใหม่โดยใช้ for: ผู้คนสนุกกับไคท์เซิร์ฟมาตั้งแต่ปี 2000"),
          ("People have enjoyed kitesurfing for 26 years.", "ผู้คนสนุกกับไคท์เซิร์ฟมา 26 ปีแล้ว"), steps=[("2026 minus 2000 = 26.", "2026 ลบ 2000 = 26")]),
        X(EX(2, "Read and write.", "อ่านและเขียน"), 42, ("Rewrite sentence 3 with for: Surfing has been popular around the world since the 1970s.", "เขียนประโยคที่ 3 ใหม่โดยใช้ for: การโต้คลื่นเป็นที่นิยมทั่วโลกตั้งแต่ทศวรรษ 1970"),
          ("Surfing has been popular around the world for about 50 years.", "การโต้คลื่นเป็นที่นิยมทั่วโลกมาประมาณ 50 ปีแล้ว"),
          steps=[("The 1970s means 1970 to 1979.", "ทศวรรษ 1970 คือปี 1970 ถึง 1979"), ("2026 minus 1970 = 56, and 2026 minus 1979 = 47. So about 50 years.", "2026 ลบ 1970 = 56 และ 2026 ลบ 1979 = 47 จึงประมาณ 50 ปี")]),
        X(EX(2, "Read and write.", "อ่านและเขียน"), 42, ("Rewrite sentence 4 with for: More than 10 million people have tried skateboarding since the 1960s.", "เขียนประโยคที่ 4 ใหม่โดยใช้ for: คนมากกว่า 10 ล้านคนได้ลองเล่นสเก็ตบอร์ดตั้งแต่ทศวรรษ 1960"),
          ("More than 10 million people have tried skateboarding for more than 50 years.", "คนมากกว่า 10 ล้านคนได้ลองเล่นสเก็ตบอร์ดมานานกว่า 50 ปีแล้ว"),
          steps=[("The 1960s means 1960 to 1969.", "ทศวรรษ 1960 คือปี 1960 ถึง 1969"), ("2026 minus 1969 = 57. So more than 50 years.", "2026 ลบ 1969 = 57 จึงมากกว่า 50 ปี")]),
    ],
    "speak": {
        "tip": T("Ask a friend \"How long…?\" questions. Answer with for or since.", "ถามเพื่อนด้วยคำถาม How long…? แล้วตอบด้วย for หรือ since"),
        "models": [
            T("How long have you had a bicycle?", "เธอมีจักรยานมานานเท่าไรแล้ว"),
            T("I've had one for three years.", "ฉันมีมา 3 ปีแล้ว"),
            T("I've studied English since I was six.", "ฉันเรียนภาษาอังกฤษตั้งแต่อายุ 6 ขวบ"),
            T("Kitesurfing has been popular since 2000.", "ไคท์เซิร์ฟเป็นที่นิยมตั้งแต่ปี 2000"),
        ],
        "turns": [
            {"q": T("How long have you been at this school?", "เธออยู่โรงเรียนนี้มานานเท่าไรแล้ว"), "starter": T("I've been at this school for… / since…", "ฉันอยู่โรงเรียนนี้มา… / ตั้งแต่…"),
             "example": T("I've been at this school for six years.", "ฉันอยู่โรงเรียนนี้มา 6 ปีแล้ว")},
            {"q": T("How long have you known your best friend?", "เธอรู้จักเพื่อนสนิทมานานเท่าไรแล้ว"), "starter": T("I've known my best friend for… / since…", "ฉันรู้จักเพื่อนสนิทมา… / ตั้งแต่…"),
             "example": T("I've known my best friend since Grade 1.", "ฉันรู้จักเพื่อนสนิทตั้งแต่ ป.1")},
            {"q": T("How long have you lived in your house?", "เธออาศัยอยู่ในบ้านหลังนี้มานานเท่าไรแล้ว"), "starter": T("I've lived in my house for… / since…", "ฉันอาศัยอยู่ในบ้านมา… / ตั้งแต่…"),
             "example": T("I've lived in my house since I was born.", "ฉันอาศัยอยู่ในบ้านนี้ตั้งแต่เกิด")},
            {"q": T("How long have you played your favorite sport?", "เธอเล่นกีฬาที่ชอบมานานเท่าไรแล้ว"), "starter": T("I've played… for… / since…", "ฉันเล่น… มา… / ตั้งแต่…"),
             "example": T("I've played football for four years.", "ฉันเล่นฟุตบอลมา 4 ปีแล้ว")},
        ],
    },
    "sort": {"title": T("Does it go with FOR or SINCE?", "ใช้กับ FOR หรือ SINCE"),
             "bins": [T("for ⏳", "for ⏳"), T("since 📍", "since 📍")],
             "items": [["ten years", 0], ["a month", 0], ["an hour", 0], ["five days", 0], ["a long time", 0], ["two weeks", 0], ["many years", 0],
                       ["2016", 1], ["June", 1], ["last year", 1], ["Monday", 1], ["I was born", 1], ["the 1970s", 1], ["8 o'clock", 1]]},
    "build": ["I have | lived here | for | ten years.", "Kitesurfing | has been | popular | since 2000.", "How long | have you | had | a bicycle?",
              "Emma has | played tennis | for | three years.", "He has wanted | to go skiing | since | he was a boy.", "We haven't | taken a vacation | since | 2016."],
    "match": [["be", "been"], ["have", "had"], ["do", "done"], ["take", "taken"], ["ride", "ridden"], ["know", "known"], ["want", "wanted"], ["try", "tried"], ["enjoy", "enjoyed"]],
    "quiz": [
        Q("I have lived here ____ ten years.", "ฉันอาศัยอยู่ที่นี่ ____ 10 ปี", ["for", "since", "at", "in"]),
        Q("She has been a surfer ____ 2018.", "เธอเป็นนักโต้คลื่น ____ ปี 2018", ["since", "for", "at", "on"]),
        Q("Kitesurfing ____ popular since 2000.", "ไคท์เซิร์ฟ ____ เป็นที่นิยมตั้งแต่ปี 2000", ["has been", "have been", "was been", "is been"]),
        Q("My friends ____ fans of hang-gliding since 2014.", "เพื่อนของฉัน ____ แฟนการเล่นเครื่องร่อนตั้งแต่ปี 2014", ["have been", "has been", "are been", "be"]),
        Q("How long have you ____ a bicycle?", "เธอ ____ จักรยานมานานเท่าไรแล้ว", ["had", "have", "has", "having"]),
        Q("We haven't seen Tom ____ last Monday.", "เราไม่ได้เจอทอม ____ วันจันทร์ที่แล้ว", ["since", "for", "from", "ago"]),
        Q("He has wanted to ski ____ he was a boy.", "เขาอยากเล่นสกี ____ ตอนเขายังเป็นเด็ก", ["since", "for", "when", "during"]),
        Q("What is the past participle of \"take\"?", "กริยาช่องที่ 3 ของ take คืออะไร", ["taken", "took", "taked", "taking"]),
        Q("What is the past participle of \"be\"?", "กริยาช่องที่ 3 ของ be คืออะไร", ["been", "was", "being", "be"]),
        Q("Since 2016 means the same as (in 2026): ____", "Since 2016 มีความหมายเท่ากับ (ในปี 2026): ____", ["for 10 years", "for 16 years", "for 2016 years", "since 10 years"]),
        Q("Which one is a point in time (use since)?", "ข้อไหนเป็นจุดเริ่มต้นของเวลา (ใช้ since)", ["last year", "two weeks", "an hour", "a long time"]),
        Q("Which one is a period of time (use for)?", "ข้อไหนเป็นช่วงเวลา (ใช้ for)", ["three months", "June", "2010", "Monday"]),
    ],
}

# ================================================================== 3. VOCABULARY 2
v2_words = [
    W("a helmet", "noun", "หมวกกันน็อก", "a hard hat that protects your head", "หมวกแข็งที่ปกป้องศีรษะ",
      "Always wear a helmet when you ride a bike.", "สวมหมวกกันน็อกทุกครั้งที่ขี่จักรยาน", "helmet", hl="helmet"),
    W("elbow pads", "noun", "สนับศอก", "soft pads that protect your elbows", "แผ่นนุ่มที่ปกป้องข้อศอก",
      "Protect your elbows by wearing elbow pads.", "ปกป้องข้อศอกด้วยการสวมสนับศอก", "elbow-pads"),
    W("knee pads", "noun", "สนับเข่า", "soft pads that protect your knees", "แผ่นนุ่มที่ปกป้องหัวเข่า",
      "Skateboarders wear knee pads.", "นักสเก็ตบอร์ดสวมสนับเข่า", "knee-pads"),
    W("brakes", "noun", "เบรก", "the parts of a bicycle that make it stop", "ส่วนของจักรยานที่ทำให้หยุด",
      "Check your brakes before you ride.", "ตรวจเบรกก่อนขี่ทุกครั้ง", "brakes"),
    W("a life jacket", "noun", "เสื้อชูชีพ", "a jacket that helps you float in water", "เสื้อที่ช่วยให้ลอยน้ำได้",
      "Wear a life jacket on a boat.", "สวมเสื้อชูชีพเมื่ออยู่บนเรือ", "life-jacket", hl="life jacket"),
    W("protect", "verb", "ปกป้อง", "to keep someone safe from danger", "ทำให้ปลอดภัยจากอันตราย",
      "A helmet will protect your head.", "หมวกกันน็อกจะปกป้องศีรษะของนักเรียน", emoji="🛡️"),
]
vocab2 = {
    "id": "vocab2", "title": T("Vocabulary 2: Safety Equipment", "คำศัพท์ 2: อุปกรณ์ความปลอดภัย"), "short": T("Vocabulary 2", "คำศัพท์ 2"),
    "pages": "Book p.55 · Workbook p.43",
    "learn": [
        L("Learn", "Stay safe! Safety equipment", "ปลอดภัยไว้ก่อน! อุปกรณ์ความปลอดภัย", [
            ("Safety equipment <b>protects</b> your body.", "อุปกรณ์ความปลอดภัยช่วยปกป้องร่างกาย"),
        ], table=[["Equipment", "It protects…"], ["a helmet 🪖", "your head"], ["elbow pads", "your elbows"], ["knee pads", "your knees"],
                  ["a life jacket 🦺", "you in the water"], ["brakes", "you: they stop your bike"]], page="📖 p.55"),
        L("Grammar tip", "a helmet, but elbow pads", "a helmet แต่ elbow pads", [
            ("One thing: <b>a</b> helmet, <b>a</b> life jacket.", "สิ่งของชิ้นเดียว: a helmet, a life jacket"),
            ("Things that come in twos: elbow pad<b>s</b>, knee pad<b>s</b>, brake<b>s</b>.", "สิ่งของที่มาเป็นคู่: elbow pads, knee pads, brakes (เติม s)"),
        ], examples=[("She's wearing <b>a</b> helmet and knee pad<b>s</b>.", "เธอสวมหมวกกันน็อกและสนับเข่า")], page="📖 p.55"),
    ],
    "words": v2_words,
    "book": [
        X(EX(1, "Listen and repeat. Then read and write.", "ฟังและพูดตาม แล้วอ่านและเขียน"), 55, ("Most skateboarding injuries happen when people do tricks and fall on the hard ground. Protect your elbows by wearing ____.", "การบาดเจ็บจากสเก็ตบอร์ดส่วนใหญ่เกิดเมื่อเล่นท่าแล้วล้มบนพื้นแข็ง ปกป้องข้อศอกด้วยการสวม ____"),
          ("elbow pads", "สนับศอก"), hint=("What protects your elbows?", "อะไรปกป้องข้อศอก")),
        X(EX(1, "Listen and repeat. Then read and write.", "ฟังและพูดตาม แล้วอ่านและเขียน"), 55, ("If you practice water sports, you might fall in the water. Wear a bright ____ on your body, even if you can swim.", "ถ้าเล่นกีฬาทางน้ำอาจตกน้ำได้ สวม ____ สีสดบนตัว แม้ว่าจะว่ายน้ำเป็น"),
          ("life jacket", "เสื้อชูชีพ"), hint=("It helps you float in the water.", "ช่วยให้ลอยน้ำได้")),
        X(EX(1, "Listen and repeat. Then read and write.", "ฟังและพูดตาม แล้วอ่านและเขียน"), 55, ("When you go cycling or skateboarding, always protect your knees by wearing ____.", "เมื่อปั่นจักรยานหรือเล่นสเก็ตบอร์ด ปกป้องหัวเข่าด้วยการสวม ____ เสมอ"),
          ("knee pads", "สนับเข่า"), hint=("What protects your knees?", "อะไรปกป้องหัวเข่า")),
        X(EX(1, "Listen and repeat. Then read and write.", "ฟังและพูดตาม แล้วอ่านและเขียน"), 55, ("Check your bicycle ____ often! If they work well, you can stop your bicycle quickly.", "ตรวจ ____ จักรยานบ่อย ๆ ถ้าทำงานดี จะหยุดจักรยานได้เร็ว"),
          ("brakes", "เบรก"), hint=("They help you stop.", "ช่วยให้หยุดได้")),
        X(EX(1, "Listen and repeat. Then read and write.", "ฟังและพูดตาม แล้วอ่านและเขียน"), 55, ("Skateboarders often have accidents. They should wear a ____ so that if they fall, they won't hurt their head.", "นักสเก็ตบอร์ดมักประสบอุบัติเหตุ ควรสวม ____ เพื่อไม่ให้ศีรษะบาดเจ็บถ้าล้ม"),
          ("helmet", "หมวกกันน็อก"), hint=("It protects your head.", "ปกป้องศีรษะ")),
        X(EX(2, "Listen and stick.", "ฟังและติดสติกเกอร์"), 55, ("Work with a partner. Listen and put the stickers in order.", "ทำกับเพื่อน ฟังแล้วติดสติกเกอร์ตามลำดับ"),
          kind="class", classNote=("Do this in class with the audio (TR: 5.5) and your book stickers.", "ทำในห้องเรียนพร้อมฟังเสียง (TR: 5.5) และสติกเกอร์ในหนังสือ")),
    ],
    "wb": [
        X(EX(1, "Look and find.", "ดูและหา"), 43, ("Which photos have brakes?", "ภาพไหนมีเบรก"), ("b, c", "b, c"),
          inst=("Look at the photos a, b, c and d. Which ones have the following equipment?", "ดูภาพ a, b, c และ d ภาพไหนมีอุปกรณ์เหล่านี้"), why=("This is the example in the workbook. Photos b and c have bicycles.", "ข้อนี้เป็นตัวอย่างในแบบฝึกหัด ภาพ b และ c มีจักรยาน")),
        X(EX(1, "Look and find.", "ดูและหา"), 43, ("Which photos have elbow pads?", "ภาพไหนมีสนับศอก"), ("a", "a"), hint=("Look for pads on the arms.", "มองหาสนับที่แขน")),
        X(EX(1, "Look and find.", "ดูและหา"), 43, ("Which photos have a helmet?", "ภาพไหนมีหมวกกันน็อก"), ("a, b, c, d", "a, b, c, d"), hint=("Look at every head!", "ดูศีรษะของทุกคน")),
        X(EX(1, "Look and find.", "ดูและหา"), 43, ("Which photos have knee pads?", "ภาพไหนมีสนับเข่า"), ("a", "a"), hint=("Look at the skateboarder's legs.", "ดูขาของนักสเก็ตบอร์ด")),
        X(EX(1, "Look and find.", "ดูและหา"), 43, ("Which photos have a life jacket?", "ภาพไหนมีเสื้อชูชีพ"), ("d", "d"), hint=("Who is in the water?", "ใครอยู่ในน้ำ")),
        X(EX(2, "Write.", "เขียน"), 43, ("What is the boy doing to his brakes? Why are brakes so important?", "เด็กชายกำลังทำอะไรกับเบรก ทำไมเบรกจึงสำคัญ"),
          ("He's squeezing his brakes. Brakes are important because they help you stop quickly and safely.", "เขากำลังบีบเบรก เบรกสำคัญเพราะช่วยให้หยุดได้เร็วและปลอดภัย"), kind="open",
          inst=("Describe the pictures in Activity 1.", "บรรยายภาพในกิจกรรมที่ 1"), hint=("Look at photo c. Where is his hand?", "ดูภาพ c มือของเขาอยู่ที่ไหน")),
        X(EX(2, "Write.", "เขียน"), 43, ("How many people are wearing helmets? How will the helmets protect them?", "มีกี่คนที่สวมหมวกกันน็อก หมวกจะปกป้องพวกเขาอย่างไร"),
          ("Four people are wearing helmets. The helmets will protect their heads if they fall or crash.", "มี 4 คนที่สวมหมวกกันน็อก หมวกจะปกป้องศีรษะถ้าพวกเขาล้มหรือชน"), kind="open",
          hint=("Count the helmets in photos a, b, c and d.", "นับหมวกในภาพ a, b, c และ d")),
        X(EX(3, "Listen.", "ฟัง"), 43, ("Circle the safety equipment that Carla can borrow: a helmet, a life jacket, brakes, elbow pads, knee pads.", "วงกลมอุปกรณ์ความปลอดภัยที่คาร์ลายืมได้"),
          kind="class", classNote=("Do this in class with the audio (TR: 5.2). The answer is in the recording.", "ทำในห้องเรียนพร้อมฟังเสียง (TR: 5.2) คำตอบอยู่ในเสียงที่ฟัง")),
        X(EX(4, "Listen again.", "ฟังอีกครั้ง"), 43, ("Complete the conversation between Carla and Alex.", "เติมบทสนทนาระหว่างคาร์ลากับอเล็กซ์"),
          kind="class", classNote=("Do this in class with the audio (TR: 5.3). Write the missing sentences you hear.", "ทำในห้องเรียนพร้อมฟังเสียง (TR: 5.3) เขียนประโยคที่หายไปตามที่ได้ยิน")),
    ],
    "speak": {
        "models": [
            T("What equipment do you need for skateboarding?", "เล่นสเก็ตบอร์ดต้องใช้อุปกรณ์อะไรบ้าง"),
            T("You need a helmet, knee pads and elbow pads.", "ต้องใช้หมวกกันน็อก สนับเข่า และสนับศอก"),
            T("Can I borrow your helmet, please?", "ขอยืมหมวกกันน็อกหน่อยได้ไหม"),
            T("Of course you can.", "ได้สิ"),
            T("Always check your brakes before you ride.", "ตรวจเบรกทุกครั้งก่อนขี่"),
        ],
        "turns": [
            {"q": T("What equipment do you need for kayaking?", "พายเรือคายัคต้องใช้อุปกรณ์อะไร"), "starter": T("You need…", "ต้องใช้…"),
             "example": T("You need a life jacket and a helmet.", "ต้องใช้เสื้อชูชีพและหมวกกันน็อก")},
            {"q": T("Ask your friend to borrow some equipment.", "ขอยืมอุปกรณ์จากเพื่อน"), "starter": T("Can I borrow your…, please?", "ขอยืม… หน่อยได้ไหม"),
             "example": T("Can I borrow your knee pads, please?", "ขอยืมสนับเข่าหน่อยได้ไหม")},
            {"q": T("Why are helmets important?", "ทำไมหมวกกันน็อกจึงสำคัญ"), "starter": T("Helmets are important because…", "หมวกกันน็อกสำคัญเพราะ…"),
             "example": T("Helmets are important because they protect your head.", "หมวกกันน็อกสำคัญเพราะปกป้องศีรษะ")},
        ],
    },
    "spell": [{"w": w, "th": th} for w, th in [("helmet", "หมวกกันน็อก"), ("elbow pads", "สนับศอก"), ("knee pads", "สนับเข่า"), ("brakes", "เบรก"), ("life jacket", "เสื้อชูชีพ"), ("protect", "ปกป้อง")]],
    "match": [],
    "sort": {"title": T("Which body part does it protect?", "อุปกรณ์นี้ปกป้องส่วนไหนของร่างกาย"),
             "bins": [T("Head 🙂", "ศีรษะ 🙂"), T("Arms and legs 💪🦵", "แขนและขา 💪🦵"), T("Whole body 🌊🛑", "ทั้งตัว 🌊🛑")],
             "items": [["a helmet", 0], ["a bike helmet", 0], ["elbow pads", 1], ["knee pads", 1], ["a life jacket", 2], ["brakes", 2, ("Brakes stop the bike, so they keep your whole body safe.", "เบรกหยุดจักรยาน จึงช่วยให้ทั้งตัวปลอดภัย")]]},
    "build": ["Always wear | a helmet | when you | ride a bike.", "Protect | your elbows | with | elbow pads.", "Wear | a life jacket | on | the boat.",
              "Check | your brakes | before | you ride.", "Can I | borrow | your helmet, | please?"],
    "quiz": [
        Q("What protects your head?", "อะไรปกป้องศีรษะ", ["a helmet", "knee pads", "brakes", "a life jacket"]),
        Q("What helps you float in water?", "อะไรช่วยให้ลอยน้ำได้", ["a life jacket", "a helmet", "elbow pads", "brakes"]),
        Q("What makes a bicycle stop?", "อะไรทำให้จักรยานหยุด", ["brakes", "knee pads", "a helmet", "pedals"]),
        Q("What protects your knees?", "อะไรปกป้องหัวเข่า", ["knee pads", "elbow pads", "a helmet", "a life jacket"]),
        Q("What protects your elbows?", "อะไรปกป้องข้อศอก", ["elbow pads", "knee pads", "brakes", "a life jacket"]),
        Q("You go kayaking. What do you wear?", "ไปพายเรือคายัค ต้องสวมอะไร", ["a life jacket", "knee pads", "elbow pads", "brakes"]),
        Q("Can I ____ your helmet, please?", "ขอ ____ หมวกกันน็อกหน่อยได้ไหม", ["borrow", "lend", "protect", "crash"]),
        Q("A helmet will ____ your head.", "หมวกกันน็อกจะ ____ ศีรษะ", ["protect", "crash", "flip", "travel"]),
    ],
}
# (tidy the match list: six clear pairs)
vocab2["match"] = [["a helmet", "🙂 head"], ["elbow pads", "💪 elbows"], ["knee pads", "🦵 knees"], ["a life jacket", "🌊 float in water"], ["brakes", "🛑 stop a bike"], ["goggles", "👀 eyes"]]

# ================================================================== 4. GRAMMAR 2
grammar2 = {
    "id": "grammar2", "title": T("Grammar 2: Adverbs of emphasis", "ไวยากรณ์ 2: คำวิเศษณ์เน้นความหมาย"), "short": T("Grammar 2", "ไวยากรณ์ 2"),
    "pages": "Book p.56 · Workbook p.44",
    "learn": [
        L("Rule 1", "Make adjectives stronger 💥", "ทำให้คำคุณศัพท์มีความหมายหนักขึ้น 💥", [
            ("Put <b>so, very, really, incredibly, extremely, super, totally</b> <b>before</b> an adjective.", "วาง so, very, really, incredibly, extremely, super, totally ไว้หน้าคำคุณศัพท์"),
            ("cool → <b>super</b> cool 😎", "cool (เจ๋ง) → super cool (เจ๋งสุด ๆ) 😎"),
        ], examples=[("Skateboarding is <b>so</b> cool.", "สเก็ตบอร์ดเจ๋งมาก"), ("That trick is <b>really</b> scary.", "ท่านั้นน่ากลัวมาก"),
                     ("Those knee pads look <b>super</b> silly.", "สนับเข่าพวกนั้นดูตลกสุด ๆ"), ("This boy's helmet looks <b>totally</b> cool.", "หมวกกันน็อกของเด็กคนนี้ดูเจ๋งสุด ๆ")], page="📖 p.56"),
        L("Rule 2", "Where does it go?", "วางไว้ตรงไหน", [
            ("Pattern: is / are / looks / seems + <b>adverb</b> + adjective", "รูปแบบ: is / are / looks / seems + คำวิเศษณ์ + คำคุณศัพท์"),
        ], table=[["Thing", "Verb", "Adverb", "Adjective"], ["I think skiing", "is", "extremely", "dangerous."], ["That sport", "is", "incredibly", "exciting."], ["Those tricks", "look", "very", "difficult."]],
          note=("✗ Skateboarding is cool really. ✓ Skateboarding is really cool.", "✗ Skateboarding is cool really. ✓ Skateboarding is really cool. (คำวิเศษณ์อยู่หน้าคำคุณศัพท์)"), page="📒 p.44"),
        L("Words", "Adjectives to use", "คำคุณศัพท์ที่ใช้ได้", [
        ], table=[["Adjective", "ไทย"], ["cool", "เจ๋ง"], ["exciting", "น่าตื่นเต้น"], ["scary", "น่ากลัว"], ["dangerous", "อันตราย"], ["difficult", "ยาก"], ["easy", "ง่าย"],
                  ["silly", "ตลก ไร้สาระ"], ["boring", "น่าเบื่อ"], ["fun", "สนุก"], ["funny", "ตลก"]], page="📖 p.56"),
        L("Talk", "Giving opinions", "การแสดงความคิดเห็น", [
            ("Start with <b>I think (that)…</b> Your friend can agree or disagree.", "เริ่มด้วย I think (that)… เพื่อนอาจเห็นด้วยหรือไม่เห็นด้วย"),
        ], examples=[("I think that skateboarding is incredibly easy.", "ฉันคิดว่าสเก็ตบอร์ดง่ายมาก"), ("That's interesting. I think it's really difficult!", "น่าสนใจนะ ฉันคิดว่ามันยากมาก"),
                     ("This sport looks extremely dangerous.", "กีฬานี้ดูอันตรายมาก"), ("That's true. But it's totally cool!", "จริง แต่มันเจ๋งสุด ๆ")], page="📖 p.56"),
    ],
    "book": [
        X(EX(1, "Talk about the pictures.", "พูดเกี่ยวกับภาพ"), 56, ("Talk about skateboarding.", "พูดเกี่ยวกับสเก็ตบอร์ด"), ("I think that skateboarding is incredibly easy.", "ฉันคิดว่าสเก็ตบอร์ดง่ายมาก"), kind="open",
          inst=("Work with a partner. Use the words in the box.", "ทำกับเพื่อน ใช้คำในกรอบ"), box=["skateboarding", "riding a bicycle", "trick", "the boy's bicycle", "equipment"],
          hint=("Use: is + so / very / really / incredibly + adjective.", "ใช้ is + so / very / really / incredibly + คำคุณศัพท์")),
        X(EX(1, "Talk about the pictures.", "พูดเกี่ยวกับภาพ"), 56, ("Talk about riding a bicycle.", "พูดเกี่ยวกับการขี่จักรยาน"), ("I think riding a bicycle is really fun.", "ฉันคิดว่าการขี่จักรยานสนุกมาก"), kind="open"),
        X(EX(1, "Talk about the pictures.", "พูดเกี่ยวกับภาพ"), 56, ("Talk about the trick.", "พูดเกี่ยวกับท่าผาดโผน"), ("That trick looks extremely difficult.", "ท่านั้นดูยากมาก"), kind="open"),
        X(EX(1, "Talk about the pictures.", "พูดเกี่ยวกับภาพ"), 56, ("Talk about the boy's bicycle.", "พูดเกี่ยวกับจักรยานของเด็กชาย"), ("The boy's bicycle looks super cool.", "จักรยานของเด็กชายดูเจ๋งสุด ๆ"), kind="open"),
        X(EX(1, "Talk about the pictures.", "พูดเกี่ยวกับภาพ"), 56, ("Talk about the equipment.", "พูดเกี่ยวกับอุปกรณ์"), ("The equipment is very important.", "อุปกรณ์สำคัญมาก"), kind="open"),
        X(EX(2, "Look and say.", "ดูและพูด"), 56, ("Work in a small group. Look at the photos in this book. Choose a page and talk about the photos.", "ทำเป็นกลุ่มเล็ก ดูภาพในหนังสือ เลือกหนึ่งหน้าแล้วพูดเกี่ยวกับภาพ"),
          ("This sport looks extremely dangerous. That's true. But it's totally cool!", "กีฬานี้ดูอันตรายมาก จริง แต่มันเจ๋งสุด ๆ"), kind="open",
          hint=("Try page 57: the kitesurfer. Say how the sport looks.", "ลองหน้า 57: นักไคท์เซิร์ฟ บอกว่ากีฬานี้ดูเป็นอย่างไร")),
    ],
    "wb": [
        X(EX(1, "What about you? Write your opinions.", "แล้วนักเรียนล่ะ เขียนความคิดเห็น"), 44, ("A sport that looks really dangerous:", "กีฬาที่ดูอันตรายมาก:"), ("Skateboarding looks really dangerous!", "สเก็ตบอร์ดดูอันตรายมาก"), kind="open",
          why=("This is the example in the workbook.", "ข้อนี้เป็นตัวอย่างในแบบฝึกหัด")),
        X(EX(1, "What about you? Write your opinions.", "แล้วนักเรียนล่ะ เขียนความคิดเห็น"), 44, ("A famous person who looks totally cool:", "คนดังที่ดูเจ๋งสุด ๆ:"), ("Emma Watson looks totally cool!", "เอ็มม่า วัตสัน ดูเจ๋งสุด ๆ"), kind="open",
          hint=("Write: (name) looks totally cool.", "เขียนว่า (ชื่อ) looks totally cool.")),
        X(EX(1, "What about you? Write your opinions.", "แล้วนักเรียนล่ะ เขียนความคิดเห็น"), 44, ("A school subject that is extremely difficult:", "วิชาที่ยากมาก:"), ("Science is extremely difficult!", "วิชาวิทยาศาสตร์ยากมาก"), kind="open",
          hint=("Write: (subject) is extremely difficult.", "เขียนว่า (วิชา) is extremely difficult.")),
        X(EX(1, "What about you? Write your opinions.", "แล้วนักเรียนล่ะ เขียนความคิดเห็น"), 44, ("A relative or friend who is super funny:", "ญาติหรือเพื่อนที่ตลกสุด ๆ:"), ("My cousin Tom is super funny!", "ทอม ลูกพี่ลูกน้องของฉันตลกสุด ๆ"), kind="open"),
        X(EX(1, "What about you? Write your opinions.", "แล้วนักเรียนล่ะ เขียนความคิดเห็น"), 44, ("A vacation that was very exciting:", "การไปเที่ยวที่น่าตื่นเต้นมาก:"), ("Our trip to the beach was very exciting!", "การไปเที่ยวทะเลของเราน่าตื่นเต้นมาก"), kind="open",
          hint=("It happened in the past, so use was.", "เกิดขึ้นในอดีต จึงใช้ was")),
        X(EX(2, "Write.", "เขียน"), 44, ("What is your favorite or least favorite thing? Why? Write five true sentences in your notebook.", "สิ่งที่ชอบที่สุดหรือไม่ชอบที่สุดคืออะไร ทำไม เขียนประโยคจริง 5 ประโยคลงในสมุด"),
          ("My favorite movie is Frozen. It is incredibly funny. My least favorite TV program is the news. It is so boring!", "ภาพยนตร์ที่ฉันชอบที่สุดคือ Frozen มันตลกมาก รายการทีวีที่ฉันชอบน้อยที่สุดคือข่าว มันน่าเบื่อมาก"), kind="open",
          box=["book", "extremely", "extreme sport", "incredibly", "movie", "musical group", "so", "super", "totally", "TV program"],
          hint=("Use some words from the box. Give a reason with because.", "ใช้คำในกรอบ บอกเหตุผลด้วย because")),
    ],
    "speak": {
        "models": [
            T("I think that skateboarding is incredibly easy.", "ฉันคิดว่าสเก็ตบอร์ดง่ายมาก"),
            T("That's interesting. I think it's really difficult!", "น่าสนใจนะ ฉันคิดว่ามันยากมาก"),
            T("This sport looks extremely dangerous.", "กีฬานี้ดูอันตรายมาก"),
            T("That's true. But it's totally cool!", "จริง แต่มันเจ๋งสุด ๆ"),
        ],
        "turns": [
            {"q": T("What do you think of hang-gliding?", "นักเรียนคิดอย่างไรกับการเล่นเครื่องร่อน"), "starter": T("I think hang-gliding is…", "ฉันคิดว่าการเล่นเครื่องร่อน…"),
             "example": T("I think hang-gliding is super scary!", "ฉันคิดว่าการเล่นเครื่องร่อนน่ากลัวสุด ๆ")},
            {"q": T("What do you think of English class?", "นักเรียนคิดอย่างไรกับวิชาภาษาอังกฤษ"), "starter": T("I think English class is…", "ฉันคิดว่าวิชาภาษาอังกฤษ…"),
             "example": T("I think English class is really fun!", "ฉันคิดว่าวิชาภาษาอังกฤษสนุกมาก")},
            {"q": T("Your friend says: This trick looks extremely easy. Answer.", "เพื่อนพูดว่า ท่านี้ดูง่ายมาก ให้ตอบ"), "starter": T("That's interesting. I think…", "น่าสนใจนะ ฉันคิดว่า…"),
             "example": T("That's interesting. I think it looks incredibly difficult!", "น่าสนใจนะ ฉันคิดว่ามันดูยากมาก")},
        ],
    },
    "build": ["Skateboarding | is | really | cool.", "That trick | looks | incredibly | dangerous.", "I think | skiing is | extremely | exciting.",
              "Those knee pads | look | super | silly.", "This sport | is | so | much fun!", "Hang-gliding | looks | totally | scary."],
    "sort": {"title": T("Is it an adverb (so, very…) or an adjective (cool, scary…)?", "เป็นคำวิเศษณ์ (so, very…) หรือคำคุณศัพท์ (cool, scary…)"),
             "bins": [T("Adverb 💥", "คำวิเศษณ์ 💥"), T("Adjective 🎨", "คำคุณศัพท์ 🎨")],
             "items": [["so", 0], ["very", 0], ["really", 0], ["incredibly", 0], ["extremely", 0], ["super", 0], ["totally", 0],
                       ["cool", 1], ["exciting", 1], ["scary", 1], ["dangerous", 1], ["difficult", 1], ["silly", 1], ["boring", 1]]},
    "match": [["cool", "เจ๋ง"], ["exciting", "น่าตื่นเต้น"], ["scary", "น่ากลัว"], ["dangerous", "อันตราย"], ["difficult", "ยาก"], ["silly", "ตลก ไร้สาระ"], ["boring", "น่าเบื่อ"], ["easy", "ง่าย"]],
    "quiz": [
        Q("Which sentence is correct?", "ประโยคไหนถูกต้อง", ["Skiing is really fun.", "Skiing is fun really.", "Really skiing is fun.", "Skiing really is fun really."]),
        Q("That trick looks ____ dangerous.", "ท่านั้นดู ____ อันตราย", ["extremely", "extreme", "extremes", "more extreme"]),
        Q("Which word is NOT an adverb of emphasis?", "คำไหนไม่ใช่คำวิเศษณ์เน้นความหมาย", ["silly", "super", "totally", "very"]),
        Q("Those knee pads ____ super silly.", "สนับเข่าพวกนั้น ____ ตลกสุด ๆ", ["look", "looks", "looking", "is look"]),
        Q("This boy's helmet ____ totally cool.", "หมวกกันน็อกของเด็กคนนี้ ____ เจ๋งสุด ๆ", ["looks", "look", "are", "looking"]),
        Q("I think math is ____ difficult.", "ฉันคิดว่าคณิตศาสตร์ ____ ยาก", ["incredibly", "incredible", "incredibles", "an incredibly"]),
        Q("Which word means \"น่ากลัว\"?", "คำไหนแปลว่า \"น่ากลัว\"", ["scary", "silly", "easy", "boring"]),
        Q("A: This sport looks dangerous. B: ____ But it's totally cool!", "A: กีฬานี้ดูอันตราย B: ____ แต่มันเจ๋งสุด ๆ", ["That's true.", "No, thanks.", "You're welcome.", "See you."]),
        Q("Where does the adverb go?", "คำวิเศษณ์วางไว้ตรงไหน", ["before the adjective", "after the adjective", "at the end", "before the subject"]),
    ],
}

# ================================================================== 5. SONG
song = {
    "id": "song", "title": T("Song: Extreme Sports", "เพลง: Extreme Sports"), "short": T("Song", "เพลง"), "pages": "Book p.57 · Workbook p.45",
    "learn": [
        L("Song", "🎵 Extreme Sports", "🎵 เพลง Extreme Sports", [
            ("Listen, read, and sing in class with T. Roy (TR: 5.7).", "ฟัง อ่าน และร้องเพลงในห้องเรียนกับครูรอย (TR: 5.7)"),
            ("The words of the song are in your book on page 57. 📖", "เนื้อเพลงอยู่ในหนังสือหน้า 57 📖"),
            ("The song is about how exciting extreme sports are: flying high and seeing sports everywhere.", "เพลงนี้พูดถึงความน่าตื่นเต้นของกีฬาผาดโผน การบินสูง และกีฬาที่อยู่ทุกหนทุกแห่ง"),
        ], page="📖 p.57"),
        L("Key words", "Key words in the song", "คำสำคัญในเพลง", [
        ], table=[["Word", "ไทย"], ["extreme sports", "กีฬาผาดโผน"], ["fly high", "บินสูง"], ["in the air", "ในอากาศ"], ["compare", "เปรียบเทียบ"],
                  ["look around", "มองไปรอบ ๆ"], ["everywhere", "ทุกที่"], ["super cool", "เจ๋งสุด ๆ"]],
          note=("Sing it in class! Clap on every \"Extreme sports!\"", "ร้องในห้องเรียน ปรบมือทุกครั้งที่ร้องว่า Extreme sports!"), page="📖 p.57"),
        L("Sounds of English", "The sounds ear and air", "เสียง ear และ air", [
            ("<b>ear</b> sounds like \"eer\": ear, here, we're, deer, cheer, fear, steer", "ear ออกเสียงคล้าย \"เอียร์\": ear, here, we're, deer, cheer, fear, steer"),
            ("<b>air</b> sounds like \"air\": air, hair, wear, dare, chair, fair, stair", "air ออกเสียงคล้าย \"แอร์\": air, hair, wear, dare, chair, fair, stair"),
        ], examples=[("ear / air", "ear / air"), ("here / hair", "here / hair"), ("we're / wear", "we're / wear"), ("deer / dare", "deer / dare")],
          note=("Press 🔊 and listen. Then say each pair. Can you hear the difference?", "กด 🔊 แล้วฟัง จากนั้นพูดทีละคู่ ได้ยินความแตกต่างไหม"), page="📖 p.57"),
    ],
    "book": [
        X(EX(1, "Listen, read, and sing.", "ฟัง อ่าน และร้อง"), 57, ("Sing the song \"Extreme Sports.\"", "ร้องเพลง Extreme Sports"),
          kind="class", classNote=("Sing it in class with the audio (TR: 5.7). The words are in your book.", "ร้องในห้องเรียนพร้อมเสียง (TR: 5.7) เนื้อเพลงอยู่ในหนังสือ")),
        X(EX(2, "Listen and repeat.", "ฟังและพูดตาม"), 57, ("ear, air · here, hair · we're, wear · deer, dare", "ear, air · here, hair · we're, wear · deer, dare"),
          kind="class", classNote=("In class: TR 5.8. At home: press 🔊 to hear each pair.", "ในห้องเรียน: TR 5.8 ที่บ้าน: กด 🔊 เพื่อฟังแต่ละคู่")),
    ],
    "wb": [
        X(EX(1, "Look and listen.", "ดูและฟัง"), 45, ("Check the sports that the singer has dreamed of doing: kitesurfing, motocross, skiing, hang-gliding, skateboarding, surfing.", "เลือกกีฬาที่นักร้องฝันว่าจะได้เล่น"),
          kind="class", classNote=("Do this in class with the audio (TR: 5.4). Kitesurfing is the example.", "ทำในห้องเรียนพร้อมฟังเสียง (TR: 5.4) ไคท์เซิร์ฟเป็นตัวอย่าง")),
        X(EX(2, "Write a new chorus for the song.", "แต่งท่อนร้องรับใหม่ให้เพลง"), 45, ("Make an acrostic poem! Each line starts with a letter of SPORTS.", "แต่งกลอนอักษรนำ แต่ละบรรทัดขึ้นต้นด้วยตัวอักษรของคำว่า SPORTS"),
          ("S: Skiing down the mountain · P: Paddling through the waves · O: Over the ramp we fly · R: Riding fast on my bike · T: Totally cool tricks · S: So exciting!", "S: เล่นสกีลงภูเขา · P: พายผ่านคลื่น · O: บินข้ามทางลาด · R: ขี่จักรยานเร็ว · T: ท่าเจ๋งสุด ๆ · S: น่าตื่นเต้นมาก"), kind="open",
          hint=("Start each line with the letter: S…, P…, O…, R…, T…, S…", "ขึ้นต้นแต่ละบรรทัดด้วยตัวอักษร S…, P…, O…, R…, T…, S…")),
        X(EX(3, "Listen and repeat.", "ฟังและพูดตาม"), 45, ("Which words rhyme with air? Which words rhyme with ear? air / ear, chair / cheer, fair / fear, hair / here, stair / steer, wear / we're", "คำไหนสัมผัสกับ air คำไหนสัมผัสกับ ear"),
          ("air: chair, fair, hair, stair, wear · ear: cheer, fear, here, steer, we're", "air: chair, fair, hair, stair, wear · ear: cheer, fear, here, steer, we're"),
          hint=("Say each word with 🔊. Does it sound like \"air\" or \"ear\"?", "ฟังแต่ละคำด้วย 🔊 ออกเสียงเหมือน air หรือ ear"), why=("Play Sort It to practise!", "เล่นเกมแยกกลุ่มเพื่อฝึก")),
    ],
    "speak": {
        "tip": T("Say each pair slowly. ear = \"eer\", air = \"air\".", "พูดทีละคู่ช้า ๆ ear = \"เอียร์\", air = \"แอร์\""),
        "models": [T("ear, air", "ear, air"), T("here, hair", "here, hair"), T("we're, wear", "we're, wear"), T("deer, dare", "deer, dare"),
                   T("cheer, chair", "cheer, chair"), T("fear, fair", "fear, fair"), T("I fear the chair is not fair here.", "ฉันกลัวว่าเก้าอี้ตรงนี้ไม่ยุติธรรม")],
        "turns": [{"q": T("Say a sentence with hair and here.", "พูดประโยคที่มีคำว่า hair และ here"), "starter": T("My hair…", "ผมของฉัน…"),
                   "example": T("My hair is wet because we're here at the beach.", "ผมของฉันเปียกเพราะเราอยู่ที่ชายหาด")}],
    },
    "sort": {"title": T("Does it rhyme with AIR or EAR? Press 🔊 to listen.", "สัมผัสกับ AIR หรือ EAR กด 🔊 เพื่อฟัง"),
             "bins": [T("air 🌬️", "air 🌬️"), T("ear 👂", "ear 👂")],
             "items": [["chair", 0], ["hair", 0], ["stair", 0], ["fair", 0], ["wear", 0], ["dare", 0],
                       ["cheer", 1], ["here", 1], ["steer", 1], ["fear", 1], ["we're", 1], ["deer", 1]]},
    "spell": [{"w": w, "th": th} for w, th in [("hair", "ผม"), ("here", "ที่นี่"), ("chair", "เก้าอี้"), ("cheer", "เชียร์"), ("wear", "สวมใส่"), ("fear", "ความกลัว"), ("deer", "กวาง"), ("air", "อากาศ")]],
    "quiz": [
        Q("Which word rhymes with \"air\"?", "คำไหนสัมผัสกับ air", ["chair", "cheer", "here", "deer"]),
        Q("Which word rhymes with \"ear\"?", "คำไหนสัมผัสกับ ear", ["here", "hair", "wear", "stair"]),
        Q("Which word rhymes with \"wear\"?", "คำไหนสัมผัสกับ wear", ["dare", "deer", "we're", "fear"]),
        Q("Which word rhymes with \"fear\"?", "คำไหนสัมผัสกับ fear", ["steer", "stair", "fair", "chair"]),
        Q("What is the name of the song in Unit 5?", "เพลงในบทที่ 5 ชื่ออะไร", ["Extreme Sports", "Cool Adventurers", "An Extra Challenge", "High Climber"]),
        Q("\"We're\" sounds the same as ____.", "\"We're\" ออกเสียงคล้าย ____", ["weer", "wear", "where", "were"]),
    ],
}

# ================================================================== 6. READING
reading = {
    "id": "reading", "title": T("Reading: Cool Adventurers", "การอ่าน: นักผจญภัยสุดเจ๋ง"), "short": T("Reading", "การอ่าน"), "pages": "Book p.58 · Workbook p.46",
    "learn": [
        L("Before you read", "Key words", "คำสำคัญ", [
        ], table=[["Word", "ไทย"], ["athlete", "นักกีฬา"], ["lucky", "โชคดี"], ["brave", "กล้าหาญ"], ["shark", "ฉลาม"], ["attack", "โจมตี"], ["bone", "กระดูก"],
                  ["competition", "การแข่งขัน"], ["courage", "ความกล้าหาญ"], ["blind", "ตาบอด"]], page="📖 p.58"),
        L("Summary", "Danny MacAskill 🚲", "แดนนี่ แม็คแอสกิล 🚲", [
            ("Read the full text \"Cool Adventurers\" in your book. This is a short summary.", "อ่านเรื่อง Cool Adventurers ฉบับเต็มในหนังสือ นี่คือสรุปสั้น ๆ"),
            ("Danny MacAskill is a famous extreme cyclist.", "แดนนี่ แม็คแอสกิลเป็นนักปั่นจักรยานผาดโผนที่มีชื่อเสียง"),
            ("He flips off buildings and rides on trains with his bike!", "เขาตีลังกาลงจากตึกและขี่จักรยานบนรถไฟ"),
            ("He has crashed many times, but he is very lucky. He has only broken a few bones and twelve helmets.", "เขาล้มหลายครั้ง แต่โชคดีมาก กระดูกหักเพียงไม่กี่ครั้ง และหมวกกันน็อกแตกไป 12 ใบ"),
        ], page="📖 p.58"),
        L("Summary", "Bethany Hamilton 🏄‍♀️", "เบธานี แฮมิลตัน 🏄‍♀️", [
            ("Bethany Hamilton is a surfer. She was born in Hawaii.", "เบธานี แฮมิลตันเป็นนักโต้คลื่น เกิดที่ฮาวาย"),
            ("She was an extremely good surfer at the age of eight.", "เธอโต้คลื่นเก่งมากตั้งแต่อายุ 8 ขวบ"),
            ("When she was 13, a shark attacked her and she lost her left arm.", "ตอนอายุ 13 ปี ฉลามโจมตีเธอ และเธอเสียแขนซ้ายไป"),
            ("One month later, she was back in the water! Since then, she has learned to surf with one arm and won competitions.", "เพียงหนึ่งเดือนต่อมา เธอก็กลับลงน้ำ ตั้งแต่นั้นเธอฝึกโต้คลื่นด้วยแขนข้างเดียวและชนะการแข่งขัน"),
        ], page="📖 p.58"),
        L("Compare", "Brave → braver, cool → cooler, lucky → luckier", "brave → braver, cool → cooler, lucky → luckier", [
            ("To compare two people, add <b>-er</b> to short adjectives.", "เมื่อเปรียบเทียบคนสองคน เติม -er ท้ายคำคุณศัพท์สั้น ๆ"),
            ("brave → brave<b>r</b> · cool → cool<b>er</b> · lucky → luck<b>ier</b> (y → ier)", "brave → braver · cool → cooler · lucky → luckier (เปลี่ยน y เป็น ier)"),
        ], examples=[("I think Danny is braver because he performs really dangerous tricks.", "ฉันคิดว่าแดนนี่กล้าหาญกว่าเพราะเขาเล่นท่าที่อันตรายมาก"),
                     ("But Bethany started surfing one month after her accident. That's incredibly brave!", "แต่เบธานีกลับมาโต้คลื่นหนึ่งเดือนหลังอุบัติเหตุ กล้าหาญมาก")], page="📖 p.58"),
        L("Risk", "Low risk or high risk?", "ความเสี่ยงต่ำหรือสูง", [
            ("Risk = the chance that something bad can happen.", "ความเสี่ยง = โอกาสที่จะเกิดเรื่องไม่ดี"),
            ("Low risk: skateboarding, cycling", "ความเสี่ยงต่ำ: สเก็ตบอร์ด ปั่นจักรยาน"),
            ("Middle: surfing, horseback riding", "ปานกลาง: โต้คลื่น ขี่ม้า"),
            ("High risk: kitesurfing, extreme cycling", "ความเสี่ยงสูง: ไคท์เซิร์ฟ ปั่นจักรยานผาดโผน"),
        ], page="📖 p.58"),
        L("Workbook reading", "An Extra Challenge (Workbook p.46)", "An Extra Challenge (แบบฝึกหัดหน้า 46)", [
            ("Read the full text in your workbook. This is a short summary.", "อ่านเรื่องฉบับเต็มในแบบฝึกหัด นี่คือสรุปสั้น ๆ"),
            ("Some athletes cannot see or hear, or have lost an arm or a leg. To do extreme sports, they need a lot of courage.", "นักกีฬาบางคนมองไม่เห็น ได้ยินไม่ชัด หรือเสียแขนหรือขาไป การเล่นกีฬาผาดโผนต้องใช้ความกล้าหาญมาก"),
            ("⛷️ Jade Etherington is a blind skier. She can see only 5 percent. A guide skis with her. She has had many crashes, but she has carried on skiing.", "⛷️ เจด เอเธอริงตันเป็นนักสกีตาบอด มองเห็นได้เพียง 5 เปอร์เซ็นต์ มีผู้นำทางเล่นสกีไปด้วย เธอล้มหลายครั้ง แต่ยังเล่นสกีต่อไป"),
            ("🛹 Felipe Nunes from Brazil lost his legs in an accident at age six. Now he is a skateboarder who wins competitions, and he goes everywhere on his skateboard.", "🛹 เฟลิเป นูเนส จากบราซิลเสียขาทั้งสองข้างจากอุบัติเหตุตอนอายุ 6 ขวบ ตอนนี้เขาเป็นนักสเก็ตบอร์ดที่ชนะการแข่งขัน และไปไหนมาไหนด้วยสเก็ตบอร์ด"),
        ], page="📒 p.46"),
    ],
    "book": [
        X(EX(1, "Listen and read.", "ฟังและอ่าน"), 58, ("What is Danny MacAskill's sport?", "แดนนี่ แม็คแอสกิลเล่นกีฬาอะไร"), ("Extreme cycling. He is a famous cyclist.", "ปั่นจักรยานผาดโผน เขาเป็นนักปั่นจักรยานที่มีชื่อเสียง"),
          inst=("Read \"Cool Adventurers\" in your book (TR: 5.9). Then answer.", "อ่านเรื่อง Cool Adventurers ในหนังสือ (TR: 5.9) แล้วตอบคำถาม"), hint=("Look at the first part about Danny.", "ดูส่วนแรกที่เกี่ยวกับแดนนี่")),
        X(EX(1, "Listen and read.", "ฟังและอ่าน"), 58, ("What amazing things does Danny do on his bike?", "แดนนี่ทำอะไรที่น่าทึ่งบนจักรยาน"), ("He flips off buildings and rides on trains.", "เขาตีลังกาลงจากตึกและขี่บนรถไฟ")),
        X(EX(1, "Listen and read.", "ฟังและอ่าน"), 58, ("How many helmets has Danny broken?", "แดนนี่ทำหมวกกันน็อกแตกไปกี่ใบ"), ("Twelve (12) helmets.", "12 ใบ")),
        X(EX(1, "Listen and read.", "ฟังและอ่าน"), 58, ("Why is Danny lucky?", "ทำไมแดนนี่จึงโชคดี"), ("Because he has crashed many times, but he has only broken a few bones.", "เพราะเขาล้มหลายครั้ง แต่กระดูกหักเพียงไม่กี่ครั้ง")),
        X(EX(1, "Listen and read.", "ฟังและอ่าน"), 58, ("Where was Bethany Hamilton born?", "เบธานี แฮมิลตันเกิดที่ไหน"), ("In Hawaii.", "ที่ฮาวาย")),
        X(EX(1, "Listen and read.", "ฟังและอ่าน"), 58, ("How old was Bethany when the shark attacked her? What did she lose?", "เบธานีอายุเท่าไรตอนฉลามโจมตี เธอเสียอะไรไป"), ("She was 13. She lost her left arm.", "เธออายุ 13 ปี เธอเสียแขนซ้ายไป")),
        X(EX(1, "Listen and read.", "ฟังและอ่าน"), 58, ("When was Bethany back in the water?", "เบธานีกลับลงน้ำเมื่อไร"), ("Just one month after her injury.", "เพียงหนึ่งเดือนหลังได้รับบาดเจ็บ")),
        X(EX(1, "Listen and read.", "ฟังและอ่าน"), 58, ("What has Bethany done since then?", "ตั้งแต่นั้นเบธานีทำอะไรบ้าง"), ("She has learned to surf with one arm, and she has won competitions.", "เธอฝึกโต้คลื่นด้วยแขนข้างเดียว และชนะการแข่งขัน"),
          hint=("Look for \"Since then\" in the text. It uses the present perfect!", "หาคำว่า Since then ในเนื้อเรื่อง ใช้ Present Perfect")),
        X(EX(2, "Compare the two athletes.", "เปรียบเทียบนักกีฬาสองคน"), 58, ("Talk with a partner. Decide which person is braver, which is cooler, and which is luckier. Explain why you think this.", "คุยกับเพื่อน ตัดสินว่าใครกล้าหาญกว่า ใครเจ๋งกว่า ใครโชคดีกว่า อธิบายเหตุผล"),
          ("I think Bethany is braver because she surfed again one month after the shark attack. I think Danny is luckier because he has crashed many times but he is OK.", "ฉันคิดว่าเบธานีกล้าหาญกว่าเพราะเธอกลับไปโต้คลื่นหนึ่งเดือนหลังถูกฉลามโจมตี ฉันคิดว่าแดนนี่โชคดีกว่าเพราะล้มหลายครั้งแต่ไม่เป็นไร"), kind="open",
          hint=("Use: I think … is braver / cooler / luckier because…", "ใช้ I think … is braver / cooler / luckier because…")),
    ],
    "wb": [
        X(EX(1, "Listen and read.", "ฟังและอ่าน"), 46, ("Read \"An Extra Challenge\" in your workbook.", "อ่านเรื่อง An Extra Challenge ในแบบฝึกหัด"),
          kind="class", classNote=("Read it in your workbook. Listen in class (TR: 5.6). Look at the summary in Learn.", "อ่านในแบบฝึกหัด ฟังในห้องเรียน (TR: 5.6) ดูสรุปในส่วน Learn")),
        X(EX(2, "Write.", "เขียน"), 46, ("Jade Etherington: Sport?", "เจด เอเธอริงตัน: กีฬา"), ("Blind skiing", "สกีสำหรับคนตาบอด"),
          inst=("Read about the two people again. Complete the chart.", "อ่านเรื่องของทั้งสองคนอีกครั้ง เติมตาราง")),
        X(EX(2, "Write.", "เขียน"), 46, ("Jade Etherington: Difficulties she has overcome?", "เจด เอเธอริงตัน: ความยากลำบากที่เอาชนะได้"), ("She has only 5 percent vision. She has had many crashes.", "เธอมองเห็นได้เพียง 5 เปอร์เซ็นต์ เธอล้มหลายครั้ง")),
        X(EX(2, "Write.", "เขียน"), 46, ("Jade Etherington: What has she done?", "เจด เอเธอริงตัน: เธอทำอะไรไปแล้วบ้าง"), ("She has carried on skiing.", "เธอยังเล่นสกีต่อไป")),
        X(EX(2, "Write.", "เขียน"), 46, ("Jade Etherington: What adjectives can you use to describe her?", "เจด เอเธอริงตัน: ใช้คำคุณศัพท์อะไรบรรยายเธอได้"), ("brave, strong, incredibly determined", "กล้าหาญ เข้มแข็ง มุ่งมั่นมาก"), kind="open"),
        X(EX(2, "Write.", "เขียน"), 46, ("Felipe Nunes: Sport?", "เฟลิเป นูเนส: กีฬา"), ("Skateboarding", "สเก็ตบอร์ด")),
        X(EX(2, "Write.", "เขียน"), 46, ("Felipe Nunes: Difficulties he has overcome?", "เฟลิเป นูเนส: ความยากลำบากที่เอาชนะได้"), ("He lost his legs in an accident at the age of six.", "เขาเสียขาทั้งสองข้างจากอุบัติเหตุตอนอายุ 6 ขวบ")),
        X(EX(2, "Write.", "เขียน"), 46, ("Felipe Nunes: What has he done?", "เฟลิเป นูเนส: เขาทำอะไรไปแล้วบ้าง"), ("He has become a skateboarder. He wins competitions, and his videos are an internet sensation.", "เขาเป็นนักสเก็ตบอร์ด ชนะการแข่งขัน และคลิปของเขาโด่งดังในอินเทอร์เน็ต")),
        X(EX(2, "Write.", "เขียน"), 46, ("Felipe Nunes: What adjectives can you use to describe him?", "เฟลิเป นูเนส: ใช้คำคุณศัพท์อะไรบรรยายเขาได้"), ("brave, super cool, hard-working", "กล้าหาญ เจ๋งสุด ๆ ขยัน"), kind="open"),
    ],
    "speak": {
        "models": [T("I think Danny is braver because he performs really dangerous tricks.", "ฉันคิดว่าแดนนี่กล้าหาญกว่าเพราะเขาเล่นท่าที่อันตรายมาก"),
                   T("But Bethany started surfing one month after her accident. That's incredibly brave!", "แต่เบธานีกลับมาโต้คลื่นหนึ่งเดือนหลังอุบัติเหตุ กล้าหาญมาก")],
        "turns": [
            {"q": T("Who is cooler, Danny or Bethany? Why?", "ใครเจ๋งกว่า แดนนี่หรือเบธานี ทำไม"), "starter": T("I think … is cooler because…", "ฉันคิดว่า … เจ๋งกว่าเพราะ…"),
             "example": T("I think Danny is cooler because he rides on trains!", "ฉันคิดว่าแดนนี่เจ๋งกว่าเพราะเขาขี่จักรยานบนรถไฟ")},
            {"q": T("Who is luckier? Why?", "ใครโชคดีกว่า ทำไม"), "starter": T("I think … is luckier because…", "ฉันคิดว่า … โชคดีกว่าเพราะ…"),
             "example": T("I think Danny is luckier because he has only broken a few bones.", "ฉันคิดว่าแดนนี่โชคดีกว่าเพราะกระดูกหักเพียงไม่กี่ครั้ง")},
        ],
    },
    "match": [["Danny MacAskill", "rides on trains"], ["Bethany Hamilton", "surfs with one arm"], ["Jade Etherington", "blind skier"], ["Felipe Nunes", "skateboarder from Brazil"],
              ["athlete", "นักกีฬา"], ["brave", "กล้าหาญ"], ["lucky", "โชคดี"], ["competition", "การแข่งขัน"]],
    "build": ["Danny | flips | off | buildings.", "A shark | attacked | Bethany | when she was 13.", "She has | learned | to surf | with one arm.",
              "I think | Bethany | is braver | than Danny.", "Felipe | goes everywhere | on | his skateboard."],
    "quiz": [
        Q("What is Danny MacAskill's sport?", "แดนนี่ แม็คแอสกิลเล่นกีฬาอะไร", ["extreme cycling", "surfing", "skiing", "kitesurfing"]),
        Q("How many helmets has Danny broken?", "แดนนี่ทำหมวกกันน็อกแตกไปกี่ใบ", ["twelve", "two", "twenty", "one"]),
        Q("Where was Bethany Hamilton born?", "เบธานี แฮมิลตันเกิดที่ไหน", ["Hawaii", "Brazil", "England", "Australia"]),
        Q("What attacked Bethany?", "อะไรโจมตีเบธานี", ["a shark", "a dog", "a snake", "a bear"]),
        Q("How old was Bethany when she lost her arm?", "เบธานีอายุเท่าไรตอนเสียแขน", ["13", "8", "6", "18"]),
        Q("When was Bethany back in the water?", "เบธานีกลับลงน้ำเมื่อไร", ["one month later", "one year later", "ten years later", "never"]),
        Q("The comparative of \"lucky\" is ____.", "รูปเปรียบเทียบของ lucky คือ ____", ["luckier", "luckyer", "more lucky", "luckest"]),
        Q("Jade Etherington is a ____.", "เจด เอเธอริงตันเป็น ____", ["blind skier", "surfer", "cyclist", "skateboarder"]),
        Q("Felipe Nunes is from ____.", "เฟลิเป นูเนส มาจาก ____", ["Brazil", "Hawaii", "Japan", "Thailand"]),
        Q("Which sport has a high risk?", "กีฬาไหนมีความเสี่ยงสูง", ["kitesurfing", "cycling", "skateboarding", "walking"]),
    ],
}

# ================================================================== 7. MISSION (value)
mission = {
    "id": "mission", "title": T("Mission: Connect with nature", "ภารกิจ: ใกล้ชิดธรรมชาติ"), "short": T("Mission 🌳", "ภารกิจ 🌳"), "pages": "Book p.59",
    "learn": [
        L("Value", "Our mission: Connect with nature 🌳", "ภารกิจของเรา: ใกล้ชิดธรรมชาติ 🌳", [
            ("<b>Connect with nature</b> means spending time outside and caring about the natural world.", "ใกล้ชิดธรรมชาติ หมายถึง ใช้เวลาอยู่กลางแจ้งและใส่ใจโลกธรรมชาติ"),
            ("Many extreme sports happen in nature: in the mountains, in the sea and in the sky.", "กีฬาผาดโผนหลายชนิดเล่นในธรรมชาติ: บนภูเขา ในทะเล และบนท้องฟ้า"),
            ("The photo on page 59 shows snowkiting in Idaho, USA.", "ภาพในหน้า 59 คือการเล่นสโนว์ไคท์ที่รัฐไอดาโฮ สหรัฐอเมริกา"),
        ], page="📖 p.59"),
        L("Explorer", "J. Michael Fay, National Geographic Explorer", "เจ. ไมเคิล เฟย์ นักสำรวจเนชั่นแนล จีโอกราฟิก", [
            ("J. Michael Fay is a conservationist. He protects nature.", "เจ. ไมเคิล เฟย์ เป็นนักอนุรักษ์ เขาปกป้องธรรมชาติ"),
            ("His message: If you like to walk, climb trees or explore, keep doing it! The world needs more people who are connected to Earth.", "ข้อคิดของเขา: ถ้าชอบเดิน ปีนต้นไม้ หรือสำรวจ ทำต่อไป โลกต้องการคนที่ใกล้ชิดกับโลกมากขึ้น"),
            ("Read his words in your book on page 59. 📖", "อ่านคำพูดของเขาในหนังสือหน้า 59 📖"),
        ], page="📖 p.59"),
        L("Think", "How can I connect with nature?", "ฉันจะใกล้ชิดธรรมชาติได้อย่างไร", [
            ("🚶 Go for a walk in the park.", "🚶 เดินเล่นในสวนสาธารณะ"),
            ("🌱 Plant a tree or water plants.", "🌱 ปลูกต้นไม้หรือรดน้ำต้นไม้"),
            ("🚲 Ride your bike outside (with a helmet!).", "🚲 ขี่จักรยานกลางแจ้ง (สวมหมวกกันน็อกด้วย)"),
            ("🏖️ Visit the beach and keep it clean.", "🏖️ ไปเที่ยวทะเลและช่วยกันรักษาความสะอาด"),
            ("📵 Put down your phone and look at birds, trees and the sky.", "📵 วางโทรศัพท์แล้วมองนก ต้นไม้ และท้องฟ้า"),
        ], page="📖 p.59"),
    ],
    "book": [
        X(("Think. Pair. Share. Question 1", "คิด จับคู่ แบ่งปัน: ข้อ 1"), 59, ("Are all extreme sports dangerous?", "กีฬาผาดโผนอันตรายทุกชนิดไหม"),
          ("No, not all. Some are very dangerous, but safety equipment and training make them safer.", "ไม่ทุกชนิด บางชนิดอันตรายมาก แต่อุปกรณ์ความปลอดภัยและการฝึกฝนช่วยให้ปลอดภัยขึ้น"), kind="open",
          hint=("Think about the risk chart on page 58.", "นึกถึงแผนภูมิความเสี่ยงในหน้า 58")),
        X(("Think. Pair. Share. Question 2", "คิด จับคู่ แบ่งปัน: ข้อ 2"), 59, ("What extreme sports are popular in your country?", "กีฬาผาดโผนอะไรเป็นที่นิยมในประเทศของนักเรียน"),
          ("In Thailand, rock climbing, surfing, skateboarding, scuba diving and kitesurfing are popular.", "ในประเทศไทย การปีนผา โต้คลื่น สเก็ตบอร์ด ดำน้ำลึก และไคท์เซิร์ฟเป็นที่นิยม"), kind="open"),
        X(("Think. Pair. Share. Question 3", "คิด จับคู่ แบ่งปัน: ข้อ 3"), 59, ("How do you connect with nature? What outdoor activities do you do?", "นักเรียนใกล้ชิดธรรมชาติอย่างไร ทำกิจกรรมกลางแจ้งอะไรบ้าง"),
          ("I ride my bike in the park and I swim in the sea with my family.", "ฉันขี่จักรยานในสวนสาธารณะ และว่ายน้ำในทะเลกับครอบครัว"), kind="open",
          hint=("Use: I go… / I ride… / I play… / I swim…", "ใช้ I go… / I ride… / I play… / I swim…")),
    ],
    "speak": {
        "models": [T("I connect with nature when I go hiking.", "ฉันใกล้ชิดธรรมชาติเมื่อไปเดินป่า"), T("Not all extreme sports are dangerous.", "กีฬาผาดโผนไม่ได้อันตรายทุกชนิด"),
                   T("The world needs people who love nature.", "โลกต้องการคนที่รักธรรมชาติ")],
        "turns": [
            {"q": T("What outdoor activities do you do?", "นักเรียนทำกิจกรรมกลางแจ้งอะไรบ้าง"), "starter": T("I like to… outside.", "ฉันชอบ… กลางแจ้ง"),
             "example": T("I like to play football and ride my bike outside.", "ฉันชอบเล่นฟุตบอลและขี่จักรยานกลางแจ้ง")},
            {"q": T("What can you do this week to connect with nature?", "สัปดาห์นี้นักเรียนจะทำอะไรเพื่อใกล้ชิดธรรมชาติ"), "starter": T("This week, I will…", "สัปดาห์นี้ ฉันจะ…"),
             "example": T("This week, I will plant a tree with my family.", "สัปดาห์นี้ ฉันจะปลูกต้นไม้กับครอบครัว")},
        ],
    },
    "sort": {"title": T("Does it help you connect with nature?", "กิจกรรมนี้ช่วยให้ใกล้ชิดธรรมชาติไหม"),
             "bins": [T("Yes 🌳", "ใช่ 🌳"), T("Not really 📱", "ไม่ค่อย 📱")],
             "items": [["going for a walk in the park", 0], ["planting a tree", 0], ["climbing a hill", 0], ["watching birds", 0], ["swimming in the sea", 0],
                       ["playing video games all day", 1], ["watching TV all weekend", 1], ["sitting on the sofa", 1]]},
    "quiz": [
        Q("\"Connect with nature\" means…", "\"ใกล้ชิดธรรมชาติ\" หมายถึง…", ["spend time outside and care about nature", "play games on a phone", "stay inside all day", "buy new sports equipment"]),
        Q("J. Michael Fay is a ____.", "เจ. ไมเคิล เฟย์ เป็น ____", ["conservationist", "surfer", "singer", "cyclist"]),
        Q("Which activity connects you with nature?", "กิจกรรมไหนช่วยให้ใกล้ชิดธรรมชาติ", ["climbing trees", "watching TV", "playing video games", "sleeping late"]),
        Q("Are all extreme sports dangerous?", "กีฬาผาดโผนอันตรายทุกชนิดไหม", ["No, safety equipment helps.", "Yes, all of them.", "Only on Mondays.", "I don't know."]),
    ],
}

# ================================================================== 8. WRITING
writing = {
    "id": "writing", "title": T("Writing: A Biography", "การเขียน: ชีวประวัติ"), "short": T("Writing", "การเขียน"), "pages": "Workbook p.47",
    "learn": [
        L("Learn", "What is a biography?", "ชีวประวัติคืออะไร", [
            ("A <b>biography</b> describes the life of another person.", "ชีวประวัติ คือ เรื่องที่เล่าชีวิตของบุคคลอื่น"),
            ("Connect the dates and events in the person's life to make it interesting.", "เชื่อมวันที่และเหตุการณ์ในชีวิตของบุคคลนั้นเพื่อให้น่าสนใจ"),
        ], page="📒 p.47"),
        L("Linking words", "Words to link dates and events", "คำเชื่อมวันที่และเหตุการณ์", [
        ], table=[["Linking word", "ไทย"], ["before", "ก่อน"], ["then", "จากนั้น"], ["suddenly", "ทันใดนั้น"], ["at the time", "ในเวลานั้น"], ["afterward", "หลังจากนั้น"],
                  ["since then", "ตั้งแต่นั้นมา"], ["the next year", "ปีต่อมา"], ["after (that)", "หลังจาก (นั้น)"]], page="📒 p.47"),
        L("Model", "High Climber: Matt Moniz (short summary)", "High Climber: แมตต์ โมนิซ (สรุปสั้น ๆ)", [
            ("Read the full biography in your workbook. 📒", "อ่านชีวประวัติฉบับเต็มในแบบฝึกหัด 📒"),
            ("In 2007, Matt's father invited him to climb Mount Everest. He loved it!", "ในปี 2007 พ่อของแมตต์ชวนเขาไปปีนภูเขาเอเวอเรสต์ เขาชอบมาก"),
            ("The next year, he climbed Kilimanjaro in Africa and Elbrus in Russia.", "ปีต่อมา เขาปีนภูเขาคิลิมันจาโรในแอฟริกาและเอลบรุสในรัสเซีย"),
            ("In 2015, an earthquake caused an avalanche on Everest. Matt helped rescue injured climbers and won an award.", "ในปี 2015 แผ่นดินไหวทำให้เกิดหิมะถล่มบนเอเวอเรสต์ แมตต์ช่วยเหลือนักปีนเขาที่บาดเจ็บและได้รับรางวัล"),
            ("After that, he stayed in Nepal for a month to help rebuild schools and homes.", "หลังจากนั้น เขาอยู่ที่เนปาลหนึ่งเดือนเพื่อช่วยสร้างโรงเรียนและบ้านขึ้นใหม่"),
        ], page="📒 p.47"),
        L("Plan", "Plan your biography", "วางแผนเขียนชีวประวัติ", [
            ("1. Who is the person? What is their exciting job, sport or trip?", "1. บุคคลนั้นคือใคร งาน กีฬา หรือการเดินทางที่น่าตื่นเต้นคืออะไร"),
            ("2. When and how did it start?", "2. เริ่มต้นเมื่อไรและอย่างไร"),
            ("3. What happened next? (then, the next year, suddenly)", "3. เกิดอะไรขึ้นต่อ (then, the next year, suddenly)"),
            ("4. What have they done since then? (since then + present perfect)", "4. ตั้งแต่นั้นมาเขาทำอะไรไปแล้วบ้าง (since then + Present Perfect)"),
        ], page="📒 p.47"),
    ],
    "wb": [
        X(EX(1, "Read.", "อ่าน"), 47, ("Read the biography \"High Climber.\" Underline the expressions that are used to link the events.", "อ่านชีวประวัติ High Climber ขีดเส้นใต้คำที่ใช้เชื่อมเหตุการณ์"),
          ("Before the age of nine · Then · suddenly · At the time · afterward · Since then · The next year · After that", "Before the age of nine · Then · suddenly · At the time · afterward · Since then · The next year · After that"),
          hint=("There are 8 linking expressions. Look at the list of linking words at the top of the page.", "มีคำเชื่อม 8 คำ ดูรายการคำเชื่อมด้านบนของหน้า"),
          steps=[("Paragraph 1 has seven of them.", "ย่อหน้าที่ 1 มี 7 คำ"), ("Paragraph 2 has one more, near the end.", "ย่อหน้าที่ 2 มีอีก 1 คำ ใกล้ตอนท้าย")]),
        X(EX(2, "Write in your notebook.", "เขียนลงในสมุด"), 47, ("Write a short biography about someone who has an exciting job, does an exciting sport, or has traveled to exciting places. Link the events and dates.", "เขียนชีวประวัติสั้น ๆ ของคนที่มีงาน กีฬา หรือการเดินทางที่น่าตื่นเต้น เชื่อมเหตุการณ์และวันที่"),
          ("Lily Evans is a rock climber. Before the age of ten, she only climbed trees. Then, in 2019, her uncle took her to a climbing wall. At the time, she was scared, but afterward she loved it. The next year, she climbed her first real mountain. Since then, she has won three competitions.", "ลิลลี่ อีแวนส์เป็นนักปีนผา ก่อนอายุ 10 ขวบ เธอปีนแค่ต้นไม้ จากนั้นในปี 2019 ลุงพาเธอไปที่กำแพงปีนผา ในเวลานั้นเธอกลัว แต่หลังจากนั้นเธอชอบมาก ปีต่อมาเธอปีนภูเขาจริงเป็นครั้งแรก ตั้งแต่นั้นมาเธอชนะการแข่งขัน 3 ครั้ง"), kind="open",
          hint=("Use the plan in Learn. Use at least four linking words.", "ใช้แผนในส่วน Learn ใช้คำเชื่อมอย่างน้อย 4 คำ")),
    ],
    "build": ["Before the age of nine, | Matt enjoyed | summer vacations | like most kids.", "Then | his life | suddenly | changed.", "The next year, | he climbed | two high | mountains.",
              "Since then, | there has been | no stopping | him.", "After that, | Matt stayed | in Nepal | for a month."],
    "sort": {"title": T("Is it a linking word or not?", "เป็นคำเชื่อมหรือไม่"),
             "bins": [T("Linking word 🔗", "คำเชื่อม 🔗"), T("Not a linking word", "ไม่ใช่คำเชื่อม")],
             "items": [["afterward", 0], ["since then", 0], ["the next year", 0], ["suddenly", 0], ["at the time", 0], ["before", 0], ["after that", 0],
                       ["mountain", 1], ["climbed", 1], ["helmet", 1], ["brave", 1]]},
    "quiz": [
        Q("A biography describes ____.", "ชีวประวัติเล่าเรื่อง ____", ["the life of another person", "how to play a sport", "a recipe", "the weather"]),
        Q("Which is a linking word?", "คำไหนเป็นคำเชื่อม", ["afterward", "avalanche", "climber", "rock"]),
        Q("____, he has climbed many mountains. (from then until now)", "____ เขาปีนภูเขามาหลายลูก (ตั้งแต่ตอนนั้นจนถึงตอนนี้)", ["Since then", "Before", "Suddenly", "At the time"]),
        Q("Matt climbed Mount Everest with his ____.", "แมตต์ปีนเอเวอเรสต์กับ ____", ["father", "teacher", "sister", "friend"]),
        Q("After the avalanche, Matt stayed in ____ to help.", "หลังหิมะถล่ม แมตต์อยู่ที่ ____ เพื่อช่วยเหลือ", ["Nepal", "Russia", "Africa", "Brazil"]),
        Q("Something that happens very quickly, with no warning, happens ____.", "สิ่งที่เกิดขึ้นเร็วมากโดยไม่ทันตั้งตัว เกิดขึ้น ____", ["suddenly", "afterward", "before", "since then"]),
    ],
}

SECTIONS = [opener, vocab1, grammar1, vocab2, grammar2, song, reading, mission, writing]

# ------------------------------------------------------------------ Practice and Unit Test bank
def B(q, qth, options, why, whyth, src):
    return {"q": T(q, qth), "options": options, "why": T(why, whyth), "src": src}


BANK = [
    B("Which word means \"to turn over in the air\"?", "คำไหนแปลว่า \"ตีลังกากลางอากาศ\"", ["flip", "land", "crash", "travel"], "Flip = turn over in the air.", "flip = ตีลังกา", "Vocabulary 1 · Book p.52"),
    B("Kitesurfers need lots of ____ in their arms.", "นักไคท์เซิร์ฟต้องมี ____ ที่แขนมาก", ["strength", "height", "length", "injury"], "Strength comes from strong.", "strength มาจาก strong", "Vocabulary 1 · Book p.52"),
    B("You can fly at a ____ of 6,000 m when hang-gliding.", "เล่นเครื่องร่อนบินได้ที่ ____ 6,000 เมตร", ["height", "length", "strength", "speed"], "Height = how high.", "height = ความสูง", "Vocabulary 1 · Book p.52"),
    B("The ____ of the top tube is 38 cm.", "____ ของท่อบนคือ 38 ซม.", ["length", "height", "strength", "weight"], "The top tube is long, so we measure its length.", "ท่อบนยาว จึงวัดความยาว", "Vocabulary 1 · Workbook p.40"),
    B("Serious ____ are not common in hang-gliding.", "____ ร้ายแรงไม่ค่อยเกิดในการเล่นเครื่องร่อน", ["accidents", "equipment", "heights", "lengths"], "An accident is something bad that you didn't plan.", "อุบัติเหตุคือเหตุร้ายที่ไม่ได้ตั้งใจ", "Vocabulary 1 · Book p.52"),
    B("He broke his arm. It was a bad ____.", "เขาแขนหัก เป็น ____ ที่ร้ายแรง", ["injury", "flip", "length", "equipment"], "An injury is a hurt part of your body.", "การบาดเจ็บคือส่วนของร่างกายที่เจ็บ", "Vocabulary 1 · Book p.52"),
    B("What are kitesurfers called?", "นักไคท์เซิร์ฟถูกเรียกว่าอะไร", ["Charlie Browners", "Sky Kings", "Wave Riders", "Board Masters"], "The book calls them Charlie Browners.", "ในหนังสือเรียกว่า Charlie Browners", "Vocabulary 1 · Book p.53"),
    B("Which is NOT a sport?", "ข้อไหนไม่ใช่กีฬา", ["strength", "skiing", "kitesurfing", "hang-gliding"], "Strength is a noun meaning power, not a sport.", "strength เป็นคำนามแปลว่าความแข็งแรง ไม่ใช่กีฬา", "Vocabulary 1 · Workbook p.40"),
    B("The secret message is: Extreme sports are ____!", "ข้อความลับคือ Extreme sports are ____!", ["cool", "boring", "silly", "easy"], "The words left are extreme sports, are, cool.", "คำที่เหลือคือ extreme sports, are, cool", "Vocabulary 1 · Workbook p.40"),
    B("A: What's the worst injury you've ever had? B: ____", "A: การบาดเจ็บที่แย่ที่สุดที่เธอเคยเป็นคืออะไร B: ____", ["I've broken a finger.", "Just a swimsuit.", "I agree.", "I like skateboarding."], "The answer must be an injury.", "คำตอบต้องเป็นการบาดเจ็บ", "Vocabulary 1 · Workbook p.41"),
    B("Surfing ____ my favorite sport for many years.", "การโต้คลื่น ____ กีฬาที่ฉันชอบที่สุดมาหลายปี", ["has been", "have been", "is been", "were"], "Surfing = it → has been.", "Surfing = it → has been", "Grammar 1 · Book p.54"),
    B("Many people have had accidents ____ last year.", "หลายคนประสบอุบัติเหตุ ____ ปีที่แล้ว", ["since", "for", "ago", "in"], "Last year is a point in time → since.", "last year เป็นจุดเริ่มต้น → since", "Grammar 1 · Book p.54"),
    B("Skiing has been my dad's favorite sport ____ the last twenty years.", "การเล่นสกีเป็นกีฬาที่พ่อชอบที่สุด ____ 20 ปีที่ผ่านมา", ["for", "since", "from", "at"], "Twenty years is a period of time → for.", "20 ปีเป็นช่วงเวลา → for", "Grammar 1 · Book p.54"),
    B("He ____ to go skiing since he was a boy.", "เขา ____ ไปเล่นสกีตั้งแต่ยังเด็ก", ["has wanted", "have wanted", "wants", "is wanting"], "He → has + wanted.", "He → has + wanted", "Grammar 1 · Book p.54"),
    B("People ____ kitesurfing since 2000.", "ผู้คน ____ ไคท์เซิร์ฟตั้งแต่ปี 2000", ["have enjoyed", "has enjoyed", "enjoying", "are enjoy"], "People = they → have enjoyed.", "People = they → have enjoyed", "Grammar 1 · Workbook p.42"),
    B("More than 10 million people have ____ skateboarding since the 1960s.", "คนมากกว่า 10 ล้านคน ____ สเก็ตบอร์ดตั้งแต่ทศวรรษ 1960", ["tried", "tryed", "try", "trying"], "try → tried (y changes to i).", "try → tried (y เปลี่ยนเป็น i)", "Grammar 1 · Workbook p.42"),
    B("How long have you ____ a bicycle?", "เธอ ____ จักรยานมานานเท่าไรแล้ว", ["had", "have", "has", "having"], "have → had (past participle).", "have → had (กริยาช่องที่ 3)", "Grammar 1 · Book p.54"),
    B("In 2026, \"since 2014\" is the same as ____.", "ในปี 2026 \"since 2014\" เท่ากับ ____", ["for 12 years", "for 14 years", "for 2014 years", "since 12 years"], "2026 minus 2014 = 12.", "2026 ลบ 2014 = 12", "Grammar 1 · Workbook p.42"),
    B("Which goes with FOR?", "ข้อไหนใช้กับ FOR", ["a month", "June", "2016", "last year"], "A month is a period of time.", "a month เป็นช่วงเวลา", "Grammar 1 · Book p.54"),
    B("Which goes with SINCE?", "ข้อไหนใช้กับ SINCE", ["I was born", "ten years", "an hour", "five days"], "\"I was born\" is a point in time.", "I was born เป็นจุดเริ่มต้นของเวลา", "Grammar 1 · Book p.54"),
    B("Protect your elbows by wearing ____.", "ปกป้องข้อศอกด้วยการสวม ____", ["elbow pads", "knee pads", "a helmet", "a life jacket"], "Elbow pads protect elbows.", "สนับศอกปกป้องข้อศอก", "Vocabulary 2 · Book p.55"),
    B("If you fall in the water, a ____ helps you float.", "ถ้าตกน้ำ ____ ช่วยให้ลอยได้", ["life jacket", "helmet", "brake", "knee pad"], "A life jacket helps you float.", "เสื้อชูชีพช่วยให้ลอยน้ำ", "Vocabulary 2 · Book p.55"),
    B("Check your bicycle ____ often so you can stop quickly.", "ตรวจ ____ จักรยานบ่อย ๆ เพื่อหยุดได้เร็ว", ["brakes", "helmets", "pads", "jackets"], "Brakes make a bicycle stop.", "เบรกทำให้จักรยานหยุด", "Vocabulary 2 · Book p.55"),
    B("Skateboarders should wear a ____ so they won't hurt their head.", "นักสเก็ตบอร์ดควรสวม ____ เพื่อไม่ให้ศีรษะบาดเจ็บ", ["helmet", "life jacket", "knee pads", "brakes"], "A helmet protects your head.", "หมวกกันน็อกปกป้องศีรษะ", "Vocabulary 2 · Book p.55"),
    B("In the workbook photos, who is wearing a life jacket?", "ในภาพของแบบฝึกหัด ใครสวมเสื้อชูชีพ", ["the kayaker (d)", "the skateboarder (a)", "the cyclist (b)", "nobody"], "The person in the kayak (d) wears a life jacket.", "คนในเรือคายัค (d) สวมเสื้อชูชีพ", "Vocabulary 2 · Workbook p.43"),
    B("Skateboarding is ____ cool.", "สเก็ตบอร์ด ____ เจ๋ง", ["really", "real", "reals", "more real"], "Use the adverb really before the adjective.", "ใช้คำวิเศษณ์ really หน้าคำคุณศัพท์", "Grammar 2 · Book p.56"),
    B("Which sentence is correct?", "ประโยคไหนถูกต้อง", ["That trick looks incredibly scary.", "That trick looks scary incredibly.", "That incredibly trick looks scary.", "Incredibly that trick scary looks."], "Adverb + adjective: incredibly scary.", "คำวิเศษณ์ + คำคุณศัพท์: incredibly scary", "Grammar 2 · Book p.56"),
    B("Those knee pads ____ super silly.", "สนับเข่าพวกนั้น ____ ตลกสุด ๆ", ["look", "looks", "is look", "looking"], "Those knee pads = they → look.", "Those knee pads = they → look", "Grammar 2 · Book p.56"),
    B("Which word is an adverb of emphasis?", "คำไหนเป็นคำวิเศษณ์เน้นความหมาย", ["extremely", "dangerous", "difficult", "exciting"], "Extremely makes an adjective stronger.", "extremely ทำให้คำคุณศัพท์หนักขึ้น", "Grammar 2 · Workbook p.44"),
    B("A: This sport looks extremely dangerous. B: That's true. But it's ____ cool!", "A: กีฬานี้ดูอันตรายมาก B: จริง แต่มัน ____ เจ๋ง", ["totally", "total", "totals", "more total"], "totally + cool.", "totally + cool", "Grammar 2 · Book p.56"),
    B("Which word rhymes with \"hair\"?", "คำไหนสัมผัสกับ hair", ["wear", "here", "we're", "deer"], "hair and wear both have the air sound.", "hair และ wear มีเสียง air", "Song · Book p.57"),
    B("Which word rhymes with \"here\"?", "คำไหนสัมผัสกับ here", ["cheer", "chair", "stair", "dare"], "here and cheer both have the ear sound.", "here และ cheer มีเสียง ear", "Song · Workbook p.45"),
    B("Which pair has DIFFERENT sounds?", "คู่ไหนออกเสียงต่างกัน", ["deer / dare", "chair / stair", "here / cheer", "fear / steer"], "deer has the ear sound, dare has the air sound.", "deer มีเสียง ear ส่วน dare มีเสียง air", "Song · Book p.57"),
    B("Danny MacAskill is a famous ____.", "แดนนี่ แม็คแอสกิลเป็น ____ ที่มีชื่อเสียง", ["cyclist", "surfer", "skier", "swimmer"], "He flips off buildings on his bicycle.", "เขาตีลังกาลงจากตึกด้วยจักรยาน", "Reading · Book p.58"),
    B("Bethany Hamilton lost her left arm when a ____ attacked her.", "เบธานี แฮมิลตันเสียแขนซ้ายเมื่อ ____ โจมตีเธอ", ["shark", "dog", "bear", "crocodile"], "A shark attacked her when she was 13.", "ฉลามโจมตีเธอตอนอายุ 13 ปี", "Reading · Book p.58"),
    B("Since then, Bethany ____ to surf with one arm.", "ตั้งแต่นั้นมา เบธานี ____ โต้คลื่นด้วยแขนข้างเดียว", ["has learned", "have learned", "learn", "is learn"], "Since then + present perfect: has learned.", "Since then + Present Perfect: has learned", "Reading · Book p.58"),
    B("I think Bethany is ____ than Danny.", "ฉันคิดว่าเบธานี ____ กว่าแดนนี่", ["braver", "more brave", "bravest", "bravier"], "brave → braver.", "brave → braver", "Reading · Book p.58"),
    B("Jade Etherington can see only ____ percent.", "เจด เอเธอริงตันมองเห็นได้เพียง ____ เปอร์เซ็นต์", ["5", "50", "15", "0"], "She has just 5 percent vision.", "เธอมองเห็นได้เพียง 5 เปอร์เซ็นต์", "Reading · Workbook p.46"),
    B("Felipe Nunes is a skateboarder from ____.", "เฟลิเป นูเนส เป็นนักสเก็ตบอร์ดจาก ____", ["Brazil", "Hawaii", "Nepal", "Russia"], "The workbook says he is Brazilian.", "ในแบบฝึกหัดบอกว่าเขาเป็นชาวบราซิล", "Reading · Workbook p.46"),
    B("What does \"connect with nature\" mean?", "\"ใกล้ชิดธรรมชาติ\" หมายความว่าอะไร", ["spend time outdoors and care about nature", "watch nature videos on a phone", "stay at home", "buy a new bike"], "It means being outside and caring about the natural world.", "หมายถึงอยู่กลางแจ้งและใส่ใจธรรมชาติ", "Mission · Book p.59"),
    B("Which is a linking word for a biography?", "คำไหนเป็นคำเชื่อมในชีวประวัติ", ["afterward", "avalanche", "summer", "rock"], "Afterward links events in time.", "afterward ใช้เชื่อมเหตุการณ์ตามเวลา", "Writing · Workbook p.47"),
    B("Matt Moniz climbed Mount Everest for the first time with his ____.", "แมตต์ โมนิซ ปีนเอเวอเรสต์ครั้งแรกกับ ____", ["father", "mother", "teacher", "friends"], "His father invited him to join a climb.", "พ่อชวนเขาไปปีนเขา", "Writing · Workbook p.47"),
]

# ------------------------------------------------------------------ build
UNIT = {"unit": U, "title": "Exciting Sports", "pages": "Book p.50 to 59 · Workbook p.40 to 47", "sections": SECTIONS}

if __name__ == "__main__":
    check_all(UNIT, BANK, ROOT)
    out = os.path.join(ROOT, "content")
    json.dump(UNIT, open(os.path.join(out, f"unit{U}.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    json.dump({"questions": BANK}, open(os.path.join(out, f"bank{U}.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    json.dump(TH, open(os.path.join(out, f"th{U}.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    write_check_me(UNIT, U, os.path.join(out, "CHECK-ME.md"))
    n_ex = sum(len(s.get("book", [])) + len(s.get("wb", [])) for s in SECTIONS)
    print(f"Unit {U}: {len(SECTIONS)} lessons, {n_ex} book and workbook questions, {len(BANK)} test questions, {len(TH)} Thai lines. All checks passed ✅")
