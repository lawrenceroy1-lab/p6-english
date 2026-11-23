"""Builds Unit 6 (History's a Mystery) for the P.6 English website.

Run:  python3 tools/build_unit06.py
Writes content/unit06.json, bank06.json, th06.json and the Unit 6 part of content/CHECK-ME.md.
T("English", "Thai") gives the English text and remembers its Thai. The checks are in tools/checks.py.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from checks import TH, T, check_all, write_check_me  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
U = "06"
IMG = "img/unit06/"
# Emoji shown until the Canva picture for a word is saved in img/unit06/
EMOJI = {"tomb": "🪦", "statue": "🗿", "die": "🥀", "bury": "🕳️", "excavate": "⛏️", "mummy": "🧟", "preserve": "🏺", "tattoo": "🐍",
         "treasure": "💰", "discover": "🔎", "object": "🗝️", "gold": "🪙", "thief": "🦹", "archaeologist": "🤠",
         "analyze": "🔬", "artifact": "🪓", "dna-test": "🧬", "site": "🗺️", "sample": "🧪"}


def W(w, pos, th, d, dth, ex, exth, img=None, emoji=None, hl=None):
    T(d, dth)
    T(ex, exth)
    out = {"w": w, "pos": pos, "th": th, "def": d, "ex": ex}
    if img and os.path.exists(os.path.join(ROOT, IMG + img + ".jpg")):
        out["img"] = IMG + img + ".jpg"
    else:                                    # no Canva picture yet: show an emoji instead
        out["emoji"] = emoji or EMOJI.get(img, "📝")
    if hl:
        out["hl"] = hl
    return out


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


EX = lambda n, en, th: (f"Exercise {n}: {en}", f"แบบฝึกหัดที่ {n}: {th}")

# ================================================================== 0. UNIT OPENER
opener = {
    "id": "opener", "title": T("Unit Opener: History's a Mystery", "เปิดบทเรียน: ประวัติศาสตร์คือปริศนา"),
    "short": T("Start", "เริ่มต้น"), "pages": "Book p.60 to 61",
    "learn": [
        L("Welcome", "Welcome to Unit 6: History's a Mystery!", "ยินดีต้อนรับสู่บทที่ 6: ประวัติศาสตร์คือปริศนา", [
            ("In this unit you will:", "ในบทนี้นักเรียนจะ:"),
            ("🏺 learn words about archaeology: tombs, mummies, treasure and artifacts", "🏺 เรียนคำศัพท์เกี่ยวกับโบราณคดี: สุสาน มัมมี่ สมบัติ และโบราณวัตถุ"),
            ("🔎 use the passive voice: <b>was found</b>, <b>were discovered</b>", "🔎 ใช้ประโยค Passive: was found, were discovered"),
            ("🕵️ say who did it with <b>by</b>: The mummy was found <b>by</b> hikers.", "🕵️ บอกว่าใครทำด้วย by: The mummy was found by hikers."),
            ("🎵 sing a song, 📖 read about the lost city of Atlantis, 🏛️ learn about local history, ✍️ write with examples", "🎵 ร้องเพลง 📖 อ่านเรื่องเมืองที่สาบสูญแอตแลนติส 🏛️ เรียนรู้ประวัติศาสตร์ท้องถิ่น ✍️ เขียนโดยยกตัวอย่าง"),
        ], page="📖 p.60"),
        L("Look", "Look at the big photo", "ดูภาพใหญ่ในหนังสือ", [
            ("Open your book to pages 60 and 61.", "เปิดหนังสือหน้า 60 และ 61"),
            ("This is Chichén Itzá in Yucatan, Mexico. It is a very old building made by the Maya people.", "นี่คือชิเชนอิตซาที่ยูกาตัง ประเทศเม็กซิโก เป็นสิ่งก่อสร้างเก่าแก่มากที่สร้างโดยชาวมายา"),
            ("It looks like a <b>pyramid</b>. It is big and it has steps on every side.", "มีลักษณะคล้ายพีระมิด ใหญ่มาก และมีบันไดทุกด้าน"),
        ], page="📖 p.60 to 61"),
        L("Word", "What is a mystery?", "ปริศนาคืออะไร", [
            ("A <b>mystery</b> is something that we cannot explain. We don't know the answer yet.", "ปริศนา คือ สิ่งที่เรายังอธิบายไม่ได้ ยังไม่รู้คำตอบ"),
            ("History is full of mysteries! Who built this? Why? How did they do it?", "ประวัติศาสตร์เต็มไปด้วยปริศนา ใครสร้าง ทำไม สร้างอย่างไร"),
        ], examples=[("It's a mystery!", "มันเป็นปริศนา"), ("Nobody knows how it was built.", "ไม่มีใครรู้ว่ามันถูกสร้างขึ้นอย่างไร")], page="📖 p.60"),
    ],
    "book": [
        X(("Look and answer: Question 1a", "ดูและตอบ: ข้อ 1a"), 61, ("True or false? Chichén Itzá is in Mexico.", "จริงหรือเท็จ ชิเชนอิตซาอยู่ในประเทศเม็กซิโก"),
          ("True. It is in Yucatan, Mexico.", "จริง อยู่ที่ยูกาตัง ประเทศเม็กซิโก"), choices=["True", "False"], right=0,
          hint=("Read the small words at the bottom of the photo.", "อ่านคำเล็ก ๆ ที่มุมล่างของภาพ")),
        X(("Look and answer: Question 1b", "ดูและตอบ: ข้อ 1b"), 61, ("True or false? The structure resembles a pyramid.", "จริงหรือเท็จ สิ่งก่อสร้างนี้มีลักษณะคล้ายพีระมิด"),
          ("True. It looks like a pyramid.", "จริง ดูเหมือนพีระมิด"), choices=["True", "False"], right=0,
          hint=("Resemble = look like.", "resemble = ดูเหมือน")),
        X(("Look and answer: Question 1c", "ดูและตอบ: ข้อ 1c"), 61, ("True or false? It's a small structure.", "จริงหรือเท็จ เป็นสิ่งก่อสร้างขนาดเล็ก"),
          ("False. It's a very big structure.", "เท็จ เป็นสิ่งก่อสร้างขนาดใหญ่มาก"), choices=["True", "False"], right=1),
        X(("Look and answer: Question 2", "ดูและตอบ: ข้อ 2"), 61, ("The main building has ____ sides. a. 3, b. 4, c. 5", "อาคารหลักมี ____ ด้าน a. 3, b. 4, c. 5"),
          ("b. 4 sides", "b. 4 ด้าน"), choices=["a. 3", "b. 4", "c. 5"], right=1,
          hint=("It has a square base, like a pyramid.", "ฐานเป็นสี่เหลี่ยมจัตุรัส เหมือนพีระมิด")),
    ],
    "speak": {
        "models": [T("History is full of mysteries.", "ประวัติศาสตร์เต็มไปด้วยปริศนา"), T("Chichén Itzá is in Mexico.", "ชิเชนอิตซาอยู่ในประเทศเม็กซิโก"),
                   T("It looks like a pyramid.", "มันดูเหมือนพีระมิด")],
        "turns": [
            {"q": T("What old places do you know in Thailand?", "นักเรียนรู้จักสถานที่เก่าแก่อะไรบ้างในประเทศไทย"), "starter": T("I know…", "ฉันรู้จัก…"),
             "example": T("I know Ayutthaya. It has very old temples.", "ฉันรู้จักอยุธยา ที่นั่นมีวัดเก่าแก่มาก")},
            {"q": T("Do you like history? Why?", "นักเรียนชอบประวัติศาสตร์ไหม ทำไม"), "starter": T("Yes, I do, because… / No, I don't, because…", "ชอบ เพราะ… / ไม่ชอบ เพราะ…"),
             "example": T("Yes, I do, because history is full of mysteries!", "ชอบ เพราะประวัติศาสตร์เต็มไปด้วยปริศนา")},
        ],
    },
}

# ================================================================== 1. VOCABULARY 1
v1_words = [
    W("tomb", "noun", "สุสาน", "a room or building where a dead person is put", "ห้องหรืออาคารที่เก็บร่างของผู้เสียชีวิต",
      "The king was put in a big stone tomb.", "กษัตริย์ถูกฝังไว้ในสุสานหินขนาดใหญ่", "tomb"),
    W("statue", "noun", "รูปปั้น", "a model of a person or animal made of stone, clay or metal", "รูปจำลองคนหรือสัตว์ที่ทำจากหิน ดินเหนียว หรือโลหะ",
      "There are more than 6,000 statues in the tomb.", "ในสุสานมีรูปปั้นมากกว่า 6,000 ตัว", "statue", hl="statues"),
    W("die", "verb", "ตาย เสียชีวิต", "to stop living", "หยุดมีชีวิต",
      "The flower died because it had no water.", "ดอกไม้ตายเพราะไม่ได้รับน้ำ", "die", hl="died"),
    W("bury", "verb", "ฝัง", "to put something in the ground and cover it", "นำสิ่งของลงไปในดินแล้วกลบ",
      "The dog buried its bone in the yard.", "สุนัขฝังกระดูกไว้ในสนาม", "bury", hl="buried"),
    W("excavate", "verb", "ขุดค้น", "to dig carefully to find old things", "ขุดอย่างระมัดระวังเพื่อหาสิ่งของเก่าแก่",
      "Archaeologists excavate old sites.", "นักโบราณคดีขุดค้นแหล่งโบราณ", "excavate"),
    W("mummy", "noun", "มัมมี่", "a dead body from long ago that was kept in good condition", "ร่างของผู้เสียชีวิตเมื่อนานมาแล้วที่ถูกเก็บรักษาไว้อย่างดี",
      "The mummy was found in a tomb in Peru.", "มัมมี่ถูกพบในสุสานที่ประเทศเปรู", "mummy"),
    W("preserve", "verb", "เก็บรักษา", "to keep something in good condition for a long time", "เก็บรักษาสิ่งของให้อยู่ในสภาพดีเป็นเวลานาน",
      "The old vase was beautifully preserved.", "แจกันเก่าถูกเก็บรักษาไว้อย่างสวยงาม", "preserve", hl="preserved"),
    W("tattoo", "noun", "รอยสัก", "a picture drawn on the skin that does not wash off", "ภาพที่วาดบนผิวหนังและล้างไม่ออก",
      "The mummy had tattoos of snakes and spiders.", "มัมมี่มีรอยสักรูปงูและแมงมุม", "tattoo", hl="tattoos"),
    W("treasure", "noun", "สมบัติ", "gold, jewels and other things that are worth a lot of money", "ทองคำ อัญมณี และสิ่งของที่มีค่ามาก",
      "The treasure was found in a field in England.", "สมบัติถูกพบในทุ่งนาที่ประเทศอังกฤษ", "treasure"),
    W("discover", "verb", "ค้นพบ", "to find something for the first time", "พบสิ่งใดสิ่งหนึ่งเป็นครั้งแรก",
      "Lily discovered an old coin on the beach.", "ลิลลี่ค้นพบเหรียญเก่าที่ชายหาด", "discover", hl="discovered"),
    W("object", "noun", "วัตถุ สิ่งของ", "a thing that you can see and touch", "สิ่งที่มองเห็นและจับต้องได้",
      "They found more than 3,500 objects.", "พวกเขาพบสิ่งของมากกว่า 3,500 ชิ้น", "object", hl="objects"),
    W("gold", "noun", "ทองคำ", "a shiny yellow metal that is worth a lot", "โลหะสีเหลืองเป็นเงางามที่มีค่ามาก",
      "The crown is made of gold.", "มงกุฎทำจากทองคำ", "gold"),
    W("thief (thieves)", "noun", "ขโมย", "a person who steals things", "คนที่ขโมยสิ่งของ",
      "The thieves stole the gold.", "พวกขโมยขโมยทองคำไป", "thief", hl="thieves"),
    W("archaeologist", "noun", "นักโบราณคดี", "a person who studies old things to learn about the past", "คนที่ศึกษาสิ่งของเก่าแก่เพื่อเรียนรู้อดีต",
      "The archaeologist found an old pot.", "นักโบราณคดีพบหม้อเก่า", "archaeologist"),
]
vocab1 = {
    "id": "vocab1", "title": T("Vocabulary 1: Amazing Discoveries", "คำศัพท์ 1: การค้นพบที่น่าทึ่ง"), "short": T("Vocabulary 1", "คำศัพท์ 1"),
    "pages": "Book p.62 to 63 · Workbook p.48 to 49",
    "learn": [
        L("Learn", "Discoveries tell us about the past", "การค้นพบบอกเราเกี่ยวกับอดีต", [
            ("<b>Archaeologists</b> dig in the ground to find old things.", "นักโบราณคดีขุดดินเพื่อหาสิ่งของเก่าแก่"),
            ("Each <b>discovery</b> helps us learn how people lived long ago.", "การค้นพบแต่ละครั้งช่วยให้เรารู้ว่าคนในอดีตใช้ชีวิตอย่างไร"),
        ], page="📖 p.62"),
        L("Reading", "Three discoveries (short summary)", "การค้นพบ 3 อย่าง (สรุปสั้น ๆ)", [
            ("Read the full texts on pages 62 and 63 in your book.", "อ่านเนื้อเรื่องเต็มในหนังสือหน้า 62 และ 63"),
            ("🇨🇳 210 BCE: A Chinese ruler, Qin Shihuang, was buried in a tomb with more than 6,000 statues: soldiers, dancers, acrobats and horses. The tomb is not completely excavated yet.", "🇨🇳 ปี 210 ก่อนคริสตกาล: จิ๋นซีฮ่องเต้ ผู้ปกครองจีน ถูกฝังในสุสานพร้อมรูปปั้นมากกว่า 6,000 ตัว ทั้งทหาร นักเต้น นักกายกรรม และม้า สุสานยังขุดค้นไม่เสร็จ"),
            ("🇵🇪 450 CE: A female mummy was found in a tomb in Peru. She was beautifully preserved, with tattoos of snakes and spiders.", "🇵🇪 ปี ค.ศ. 450: พบมัมมี่ผู้หญิงในสุสานที่ประเทศเปรู ร่างถูกเก็บรักษาไว้อย่างดี มีรอยสักรูปงูและแมงมุม"),
            ("🇬🇧 650 CE: Treasure was found in a field in England in 2009. Later, more than 3,500 objects and lots of gold were discovered. Who buried it? Nobody knows.", "🇬🇧 ปี ค.ศ. 650: พบสมบัติในทุ่งนาที่ประเทศอังกฤษในปี 2009 ต่อมาพบสิ่งของมากกว่า 3,500 ชิ้นและทองคำจำนวนมาก ใครเป็นคนฝัง ไม่มีใครรู้"),
        ], page="📖 p.62 to 63"),
        L("Dates", "BCE and CE", "BCE และ CE (ก่อนคริสตกาลและคริสต์ศักราช)", [
            ("<b>BCE</b> = before the common era (a long, long time ago). The numbers count down: 300 BCE, 200 BCE, 100 BCE.", "BCE = ก่อนคริสตกาล (นานมากแล้ว) ตัวเลขนับถอยหลัง: 300, 200, 100 ปีก่อนคริสตกาล"),
            ("<b>CE</b> = the common era. The numbers count up: 100 CE, 450 CE, 2026 CE.", "CE = คริสต์ศักราช ตัวเลขนับขึ้น: ค.ศ. 100, 450, 2026"),
        ], note=("210 BCE is older than 450 CE.", "210 ปีก่อนคริสตกาล เก่ากว่า ค.ศ. 450"), page="📒 p.49"),
        L("Spelling", "Irregular words: thief → thieves, die → died", "คำที่เปลี่ยนรูป: thief → thieves, die → died", [
        ], table=[["One", "More than one"], ["thief", "thieves"], ["mummy", "mummies"], ["statue", "statues"]],
          examples=[("die → <b>died</b>", "die → died (ตาย)"), ("bury → <b>buried</b>", "bury → buried (ฝัง)"), ("discover → <b>discovered</b>", "discover → discovered (ค้นพบ)")], page="📖 p.62"),
    ],
    "words": v1_words,
    "book": [
        X(EX(1, "Listen and read.", "ฟังและอ่าน"), 62, ("Listen to the texts on pages 62 and 63 and read them in your book.", "ฟังเนื้อเรื่องหน้า 62 และ 63 และอ่านตามในหนังสือ"),
          kind="class", classNote=("Do this in class with the audio (TR: 6.1). Then look at the Learn summary.", "ทำในห้องเรียนพร้อมฟังเสียง (TR: 6.1) แล้วดูสรุปในส่วน Learn")),
        X(EX(2, "Listen and repeat.", "ฟังและพูดตาม"), 62, ("Listen and repeat the new words.", "ฟังและพูดคำศัพท์ใหม่ตาม"),
          kind="class", classNote=("Do this in class (TR: 6.2), or use the 🔊 buttons in Word Cards.", "ทำในห้องเรียน (TR: 6.2) หรือกดปุ่ม 🔊 ในบัตรคำศัพท์")),
        X(EX(3, "Ask and answer.", "ถามและตอบ"), 63, ("How many statues did they find in China?", "พวกเขาพบรูปปั้นกี่ตัวที่ประเทศจีน"), ("More than 6,000.", "มากกว่า 6,000 ตัว"),
          inst=("Work with a partner. What did you learn?", "ทำกับเพื่อน นักเรียนได้เรียนรู้อะไร")),
        X(EX(3, "Ask and answer.", "ถามและตอบ"), 63, ("Who was buried with the statues?", "ใครถูกฝังพร้อมกับรูปปั้น"), ("The Chinese ruler Qin Shihuang.", "จิ๋นซีฮ่องเต้ ผู้ปกครองจีน")),
        X(EX(3, "Ask and answer.", "ถามและตอบ"), 63, ("Where was the female mummy found?", "มัมมี่ผู้หญิงถูกพบที่ไหน"), ("In a tomb in Peru.", "ในสุสานที่ประเทศเปรู")),
        X(EX(3, "Ask and answer.", "ถามและตอบ"), 63, ("What tattoos did the mummy have?", "มัมมี่มีรอยสักรูปอะไร"), ("Tattoos of snakes and spiders.", "รอยสักรูปงูและแมงมุม")),
        X(EX(3, "Ask and answer.", "ถามและตอบ"), 63, ("When was the treasure found in England?", "สมบัติถูกพบที่ประเทศอังกฤษเมื่อไร"), ("In 2009.", "ในปี 2009")),
        X(EX(3, "Ask and answer.", "ถามและตอบ"), 63, ("How many objects did archaeologists discover there?", "นักโบราณคดีค้นพบสิ่งของที่นั่นกี่ชิ้น"), ("More than 3,500 objects.", "มากกว่า 3,500 ชิ้น")),
        X(EX(3, "Ask and answer.", "ถามและตอบ"), 63, ("Do scientists know who buried the treasure?", "นักวิทยาศาสตร์รู้ไหมว่าใครฝังสมบัติ"), ("No, they don't. Maybe thieves hid it.", "ไม่รู้ อาจเป็นขโมยที่ซ่อนไว้")),
    ],
    "wb": [
        X(EX(1, "Do the puzzle.", "ทำปริศนา"), 48, ("Unscramble the letters: DUIBER, VEHSETI, TEUTAS, OLGD, MYMMU, NAERL, REPVRSEE, MOTB, TEACAVXE, CEOBTJ", "เรียงตัวอักษรให้เป็นคำ"),
          ("buried, thieves, statue, gold, mummy, learn, preserve, tomb, excavate, object", "buried, thieves, statue, gold, mummy, learn, preserve, tomb, excavate, object"),
          box=["buried", "died", "excavate", "gold", "learn", "mummy", "object", "preserve", "statue", "thieves", "tomb"],
          hint=("The words are in the box. DEID = died is the example.", "คำอยู่ในกรอบ DEID = died เป็นตัวอย่าง"), say=False),
        X(EX(1, "Do the puzzle.", "ทำปริศนา"), 48, ("Use the numbered letters to find the secret message.", "ใช้ตัวอักษรที่มีหมายเลขหาข้อความลับ"),
          ("Learning about the past is fun!", "การเรียนรู้เกี่ยวกับอดีตสนุกมาก"),
          steps=[("Letter 1 is the l in gold. Letter 2 is the last e in preserve.", "ตัวที่ 1 คือ l ใน gold ตัวที่ 2 คือ e ตัวสุดท้ายใน preserve"),
                 ("Word 1: l-e-a-r-N-i-n-g. Word 2: a-b-o-u-t.", "คำที่ 1: l-e-a-r-N-i-n-g คำที่ 2: a-b-o-u-t"),
                 ("Then: t-h-e, p-a-s-t, i-s, F-u-N!", "จากนั้น: t-h-e, p-a-s-t, i-s, F-u-N!")],
          hint=("Write each word in the boxes first. Then find each number.", "เขียนแต่ละคำลงในช่องก่อน แล้วหาตัวเลขแต่ละตัว"), say=False),
        X(EX(2, "Label the pictures.", "เขียนชื่อภาพ"), 49, ("Picture 1: old pots and bowls in a museum", "ภาพที่ 1: หม้อและชามเก่าในพิพิธภัณฑ์"), ("objects", "สิ่งของ"),
          why=("This is the example in the workbook.", "ข้อนี้เป็นตัวอย่างในแบบฝึกหัด")),
        X(EX(2, "Label the pictures.", "เขียนชื่อภาพ"), 49, ("Picture 2: a stone figure of a person", "ภาพที่ 2: รูปคนที่ทำจากหิน"), ("statue", "รูปปั้น")),
        X(EX(2, "Label the pictures.", "เขียนชื่อภาพ"), 49, ("Picture 3: two men carefully digging and cleaning a stone wall", "ภาพที่ 3: ชายสองคนกำลังขุดและทำความสะอาดผนังหินอย่างระมัดระวัง"), ("excavate", "ขุดค้น"),
          hint=("What do archaeologists do at a site?", "นักโบราณคดีทำอะไรที่แหล่งขุดค้น")),
        X(EX(2, "Label the pictures.", "เขียนชื่อภาพ"), 49, ("Picture 4: a close-up of an old coin", "ภาพที่ 4: เหรียญเก่าในระยะใกล้"), ("gold", "ทองคำ"),
          hint=("Old coins like this are often made of… (a word from Exercise 1)", "เหรียญเก่าแบบนี้มักทำจาก… (คำจากแบบฝึกหัดที่ 1)")),
        X(EX(2, "Label the pictures.", "เขียนชื่อภาพ"), 49, ("Picture 5: a wrapped body in an old wooden box", "ภาพที่ 5: ร่างที่ถูกห่อไว้ในกล่องไม้เก่า"), ("mummy", "มัมมี่")),
        X(EX(2, "Label the pictures.", "เขียนชื่อภาพ"), 49, ("Picture 6: a big pile of old coins", "ภาพที่ 6: เหรียญเก่ากองใหญ่"), ("treasure (gold coins)", "สมบัติ (เหรียญทอง)"),
          hint=("Lots of gold coins together are…", "เหรียญทองจำนวนมากรวมกันคือ…")),
        X(EX(3, "Listen.", "ฟัง"), 49, ("Check the words in Activity 2 that you hear.", "เลือกคำในกิจกรรมที่ 2 ที่ได้ยิน"),
          kind="class", classNote=("Do this in class with the audio (TR: 6.1).", "ทำในห้องเรียนพร้อมฟังเสียง (TR: 6.1)")),
        X(EX(4, "Look at the timeline.", "ดูเส้นเวลา"), 49, ("Which event took place before the common era (BCE)?", "เหตุการณ์ใดเกิดขึ้นก่อนคริสตกาล"),
          ("The statues of soldiers were put in the Chinese tomb (210 BCE).", "รูปปั้นทหารถูกนำไปไว้ในสุสานจีน (210 ปีก่อนคริสตกาล)"),
          hint=("Find the only event on the left side of 0.", "หาเหตุการณ์เดียวที่อยู่ทางซ้ายของเลข 0")),
        X(EX(4, "Look at the timeline.", "ดูเส้นเวลา"), 49, ("Which event occurred first in the common era (CE)?", "เหตุการณ์ใดเกิดขึ้นก่อนในคริสต์ศักราช"),
          ("The female mummy in Peru (450 CE).", "มัมมี่ผู้หญิงในเปรู (ค.ศ. 450)"), hint=("450 CE or 650 CE: which is first?", "ค.ศ. 450 หรือ ค.ศ. 650 อันไหนมาก่อน")),
    ],
    "speak": {
        "models": [T("How many statues did they find in China?", "พวกเขาพบรูปปั้นกี่ตัวที่ประเทศจีน"), T("More than 6,000.", "มากกว่า 6,000 ตัว"),
                   T("The mummy was beautifully preserved.", "มัมมี่ถูกเก็บรักษาไว้อย่างดี"), T("Did thieves hide the treasure?", "ขโมยเป็นคนซ่อนสมบัติหรือเปล่า")],
        "turns": [
            {"q": T("Which discovery do you like best? Why?", "นักเรียนชอบการค้นพบไหนมากที่สุด ทำไม"), "starter": T("I like the… best because…", "ฉันชอบ… มากที่สุดเพราะ…"),
             "example": T("I like the statues best because each one is different.", "ฉันชอบรูปปั้นมากที่สุดเพราะแต่ละตัวไม่เหมือนกัน")},
            {"q": T("Would you like to be an archaeologist?", "นักเรียนอยากเป็นนักโบราณคดีไหม"), "starter": T("Yes, I would, because… / No, I wouldn't, because…", "อยาก เพราะ… / ไม่อยาก เพราะ…"),
             "example": T("Yes, I would, because I want to discover treasure!", "อยาก เพราะฉันอยากค้นพบสมบัติ")},
        ],
    },
    "spell": [{"w": w, "th": th} for w, th in [("tomb", "สุสาน"), ("statue", "รูปปั้น"), ("bury", "ฝัง"), ("excavate", "ขุดค้น"), ("mummy", "มัมมี่"), ("preserve", "เก็บรักษา"),
                                               ("tattoo", "รอยสัก"), ("treasure", "สมบัติ"), ("discover", "ค้นพบ"), ("object", "สิ่งของ"), ("gold", "ทองคำ"), ("thieves", "พวกขโมย")]],
    "match": [[w["w"], f'<img src="{w["img"]}" alt="" loading="lazy">' if w.get("img") else f'<span style="font-size:2em">{w["emoji"]}</span>'] for w in v1_words],
    "sort": {"title": T("Is it a thing (noun) or an action (verb)?", "เป็นสิ่งของ (คำนาม) หรือการกระทำ (คำกริยา)"),
             "bins": [T("Thing (noun) 🏺", "สิ่งของ (คำนาม) 🏺"), T("Action (verb) ⛏️", "การกระทำ (คำกริยา) ⛏️")],
             "items": [["tomb", 0], ["statue", 0], ["mummy", 0], ["tattoo", 0], ["treasure", 0], ["object", 0], ["gold", 0], ["thief", 0],
                       ["die", 1], ["bury", 1], ["excavate", 1], ["preserve", 1], ["discover", 1]]},
    "build": ["The statues | were buried | with | the ruler.", "The mummy | had tattoos | of snakes | and spiders.", "Archaeologists | discovered | more than | 3,500 objects.",
              "Did thieves | hide | the | treasure?", "Learning about | the past | is | fun!"],
    "quiz": [
        Q("A person who studies old things to learn about the past is an ____.", "คนที่ศึกษาสิ่งของเก่าเพื่อเรียนรู้อดีตคือ ____", ["archaeologist", "astronaut", "athlete", "artist"]),
        Q("A room where a dead king was put is a ____.", "ห้องที่เก็บร่างของกษัตริย์คือ ____", ["tomb", "statue", "site", "sample"]),
        Q("A person who steals things is a ____.", "คนที่ขโมยสิ่งของคือ ____", ["thief", "mummy", "ruler", "hiker"]),
        Q("The plural of \"thief\" is ____.", "พหูพจน์ของ thief คือ ____", ["thieves", "thiefs", "thiefes", "thieve"]),
        Q("To dig carefully to find old things is to ____.", "ขุดอย่างระมัดระวังเพื่อหาสิ่งของเก่าคือ ____", ["excavate", "preserve", "bury", "die"]),
        Q("Gold, jewels and things worth a lot of money are ____.", "ทองคำ อัญมณี และสิ่งของมีค่ามากคือ ____", ["treasure", "tattoos", "tombs", "statues"]),
        Q("The mummy was beautifully ____. It looked almost new.", "มัมมี่ถูก ____ ไว้อย่างดี ดูเกือบเหมือนใหม่", ["preserved", "buried", "stolen", "died"]),
        Q("How many statues are in Qin Shihuang's tomb?", "ในสุสานจิ๋นซีฮ่องเต้มีรูปปั้นกี่ตัว", ["more than 6,000", "about 60", "exactly 600", "3,500"]),
        Q("Where was the female mummy found?", "มัมมี่ผู้หญิงถูกพบที่ไหน", ["Peru", "England", "China", "Mexico"]),
        Q("Which is older?", "อันไหนเก่ากว่า", ["210 BCE", "450 CE", "650 CE", "2009 CE"]),
        Q("The secret message is: Learning about the past is ____!", "ข้อความลับคือ Learning about the past is ____!", ["fun", "hard", "old", "gold"]),
    ],
}

# ================================================================== 2. GRAMMAR 1
grammar1 = {
    "id": "grammar1", "title": T("Grammar 1: Passive voice, simple past", "ไวยากรณ์ 1: Passive Voice ในอดีต"),
    "short": T("Grammar 1", "ไวยากรณ์ 1"), "pages": "Book p.64 · Workbook p.50",
    "learn": [
        L("Rule 1", "Active or passive?", "Active หรือ Passive", [
            ("<b>Active:</b> the person who does the action comes first. <span class='k2'>Thieves</span> stole the gold.", "Active: ผู้กระทำอยู่หน้าประโยค ขโมยขโมยทองคำไป"),
            ("<b>Passive:</b> the thing that the action happens to comes first. <span class='k2'>The gold</span> was stolen.", "Passive: สิ่งที่ถูกกระทำอยู่หน้าประโยค ทองคำถูกขโมยไป"),
        ], note=("Use the passive when you don't know (or don't care) who did the action.", "ใช้ Passive เมื่อไม่รู้ (หรือไม่สำคัญ) ว่าใครเป็นผู้กระทำ"), page="📖 p.64"),
        L("Rule 2", "was / were + past participle", "was / were + กริยาช่องที่ 3", [
            ("I, he, she, it, one thing → <b>was</b>", "I, he, she, it, สิ่งของหนึ่งชิ้น → was"),
            ("we, you, they, many things → <b>were</b>", "we, you, they, สิ่งของหลายชิ้น → were"),
        ], table=[["Who / what", "was / were", "past participle", ""], ["The Sphinx", "was", "built", "around 2500 BCE."], ["The treasure", "was", "discovered", "in a field."],
                  ["The statues", "were", "found", "in 1974."], ["It", "wasn't", "excavated", "until 1925."], ["The treasures", "weren't", "stolen.", ""]], page="📖 p.64"),
        L("Rule 3", "Questions in the passive", "คำถามใน Passive", [
            ("Move was / were to the front.", "ย้าย was / were ไปไว้หน้าประโยค"),
        ], examples=[("<b>When were</b> the statues <b>discovered</b>?", "รูปปั้นถูกค้นพบเมื่อไร"), ("<b>Was</b> it <b>discovered</b> near here? Yes, it was. / No, it wasn't.", "มันถูกค้นพบแถวนี้ไหม ใช่ / ไม่ใช่"),
                     ("<b>When were</b> you <b>born</b>? In 2014.", "เธอเกิดเมื่อไร ปี 2014")], page="📒 p.50"),
        L("Verbs", "Past participles for this unit", "กริยาช่องที่ 3 ในบทนี้", [
        ], table=[["Verb", "Past participle"], ["find", "found"], ["build", "built"], ["steal", "stolen"], ["hide", "hidden"], ["bury", "buried"], ["put", "put"],
                  ["give", "given"], ["send", "sent"], ["break", "broken"], ["catch", "caught"], ["buy", "bought"], ["discover", "discovered"]], page="📖 p.64"),
        L("Tip", "\"I was born…\" is passive!", "\"I was born…\" เป็น Passive", [
            ("We always say <b>I was born</b> in 2014. Never \"I born\".", "เราพูดว่า I was born in 2014 เสมอ ไม่พูดว่า I born"),
        ], examples=[("I was born in Bangkok.", "ฉันเกิดที่กรุงเทพฯ"), ("My brother was born in 2016.", "น้องชายของฉันเกิดปี 2016")], page="📒 p.50"),
    ],
    "book": [
        X(EX(1, "Read. Complete the sentences.", "อ่าน เติมประโยคให้สมบูรณ์"), 64, ("The English treasure that ____ (find) in a field is a big mystery!", "สมบัติอังกฤษที่ ____ (find) ในทุ่งนาเป็นปริศนาใหญ่"),
          ("was found", "ถูกพบ"), inst=("Use the words in parentheses. Then talk with a partner. What do you think happened?", "ใช้คำในวงเล็บ แล้วคุยกับเพื่อน นักเรียนคิดว่าเกิดอะไรขึ้น"),
          hint=("The treasure = one thing → was + past participle.", "สมบัติ = หนึ่งสิ่ง → was + กริยาช่องที่ 3")),
        X(EX(1, "Read. Complete the sentences.", "อ่าน เติมประโยคให้สมบูรณ์"), 64, ("It ____ (discover) by accident.", "มัน ____ (discover) โดยบังเอิญ"), ("was discovered", "ถูกค้นพบ")),
        X(EX(1, "Read. Complete the sentences.", "อ่าน เติมประโยคให้สมบูรณ์"), 64, ("We know when the objects ____ (bury) there.", "เรารู้ว่าสิ่งของ ____ (bury) ไว้ที่นั่นเมื่อไร"), ("were buried", "ถูกฝัง"),
          hint=("The objects = many things → were.", "สิ่งของหลายชิ้น → were")),
        X(EX(1, "Read. Complete the sentences.", "อ่าน เติมประโยคให้สมบูรณ์"), 64, ("But why ____ the gold ____ (hide)?", "แต่ทำไมทองคำ ____ (hide)"), ("why was the gold hidden?", "ทำไมทองคำถูกซ่อนไว้"),
          hint=("It's a question: was comes before the gold. hide → hidden.", "เป็นคำถาม was อยู่หน้า the gold ส่วน hide → hidden")),
        X(EX(1, "Read. Complete the sentences.", "อ่าน เติมประโยคให้สมบูรณ์"), 64, ("____ it ____ (steal)?", "____ มัน ____ (steal)"), ("Was it stolen?", "มันถูกขโมยหรือเปล่า"), hint=("steal → stolen.", "steal → stolen")),
        X(EX(1, "Read. Complete the sentences.", "อ่าน เติมประโยคให้สมบูรณ์"), 64, ("Or ____ the objects ____ (put) in the field because thieves were coming?", "หรือสิ่งของ ____ (put) ไว้ในทุ่งนาเพราะขโมยกำลังมา"),
          ("Or were the objects put in the field…?", "หรือสิ่งของถูกนำไปไว้ในทุ่งนา…"), hint=("put → put (it does not change).", "put → put (ไม่เปลี่ยนรูป)")),
        X(EX(1, "Read. Complete the sentences.", "อ่าน เติมประโยคให้สมบูรณ์"), 64, ("What do you think happened to the treasure?", "นักเรียนคิดว่าเกิดอะไรขึ้นกับสมบัติ"),
          ("I think the treasure was hidden by people because thieves were coming.", "ฉันคิดว่าสมบัติถูกซ่อนไว้เพราะขโมยกำลังมา"), kind="open"),
        X(EX(2, "Play a game.", "เล่นเกม"), 64, ("where / the thieves / catch?", "ที่ไหน / พวกขโมย / จับ"), ("Where were the thieves caught?", "พวกขโมยถูกจับที่ไหน"),
          inst=("Take turns with a partner. Make correct sentences, then mark X or O.", "ผลัดกันกับเพื่อน แต่งประโยคให้ถูกต้อง แล้วกา X หรือ O")),
        X(EX(2, "Play a game.", "เล่นเกม"), 64, ("the jewelry / steal / last night", "เครื่องประดับ / ขโมย / เมื่อคืน"), ("The jewelry was stolen last night.", "เครื่องประดับถูกขโมยเมื่อคืน")),
        X(EX(2, "Play a game.", "เล่นเกม"), 64, ("gold objects / discover / my yard", "สิ่งของทองคำ / ค้นพบ / สนามบ้านฉัน"), ("Gold objects were discovered in my yard.", "สิ่งของทองคำถูกค้นพบในสนามบ้านฉัน")),
        X(EX(2, "Play a game.", "เล่นเกม"), 64, ("the treasure / not hide / the ocean", "สมบัติ / ไม่ได้ซ่อน / มหาสมุทร"), ("The treasure wasn't hidden in the ocean.", "สมบัติไม่ได้ถูกซ่อนไว้ในมหาสมุทร")),
        X(EX(2, "Play a game.", "เล่นเกม"), 64, ("when / these statues / build?", "เมื่อไร / รูปปั้นเหล่านี้ / สร้าง"), ("When were these statues built?", "รูปปั้นเหล่านี้ถูกสร้างเมื่อไร")),
        X(EX(2, "Play a game.", "เล่นเกม"), 64, ("the skiers / not find / the snow", "นักสกี / ไม่ได้พบ / หิมะ"), ("The skiers weren't found in the snow.", "นักสกีไม่ได้ถูกพบในหิมะ")),
        X(EX(2, "Play a game.", "เล่นเกม"), 64, ("two mummies / bury / this tomb", "มัมมี่สองร่าง / ฝัง / สุสานนี้"), ("Two mummies were buried in this tomb.", "มัมมี่สองร่างถูกฝังในสุสานนี้")),
        X(EX(2, "Play a game.", "เล่นเกม"), 64, ("the artifact / not buy / a store", "โบราณวัตถุ / ไม่ได้ซื้อ / ร้านค้า"), ("The artifact wasn't bought in a store.", "โบราณวัตถุไม่ได้ถูกซื้อจากร้านค้า")),
        X(EX(2, "Play a game.", "เล่นเกม"), 64, ("how / this pottery / break?", "อย่างไร / เครื่องปั้นดินเผานี้ / แตก"), ("How was this pottery broken?", "เครื่องปั้นดินเผานี้แตกได้อย่างไร")),
    ],
    "wb": [
        X(EX(1, "Look and write.", "ดูและเขียน"), 50, ("The coins ____ in a hole in the ground.", "เหรียญ ____ ในหลุมในดิน"), ("were buried", "ถูกฝัง"),
          inst=("Complete the sentences. Use the words in the box.", "เติมประโยคให้สมบูรณ์ ใช้คำในกรอบ"), box=["be born", "bury", "call", "find", "give", "hide"],
          why=("This is the example in the workbook.", "ข้อนี้เป็นตัวอย่างในแบบฝึกหัด")),
        X(EX(1, "Look and write.", "ดูและเขียน"), 50, ("The police think they ____ many years ago by thieves.", "ตำรวจคิดว่าเหรียญ ____ เมื่อหลายปีก่อนโดยขโมย"), ("were hidden", "ถูกซ่อน"),
          hint=("They = the coins. What did the thieves do with them?", "They = เหรียญ ขโมยทำอะไรกับเหรียญ")),
        X(EX(1, "Look and write.", "ดูและเขียน"), 50, ("A cat ____ up a tree this morning.", "แมว ____ บนต้นไม้เมื่อเช้านี้"), ("was found", "ถูกพบ"), hint=("One cat → was.", "แมวหนึ่งตัว → was")),
        X(EX(1, "Look and write.", "ดูและเขียน"), 50, ("The firefighters ____. They came and saved it.", "นักดับเพลิง ____ พวกเขามาช่วยแมว"), ("were called", "ถูกเรียก"), hint=("Someone phoned the firefighters.", "มีคนโทรเรียกนักดับเพลิง")),
        X(EX(1, "Look and write.", "ดูและเขียน"), 50, ("My daughter ____ on my birthday.", "ลูกสาวของฉัน ____ ในวันเกิดของฉัน"), ("was born", "เกิด"), hint=("Use be born.", "ใช้ be born")),
        X(EX(1, "Look and write.", "ดูและเขียน"), 50, ("I ____ the best birthday present in the world: a daughter!", "ฉัน ____ ของขวัญวันเกิดที่ดีที่สุดในโลก คือ ลูกสาว"), ("was given", "ได้รับ"), hint=("Use give → given.", "ใช้ give → given")),
        X(EX(2, "Write. What about you?", "เขียน แล้วนักเรียนล่ะ"), 50, ("When ____ you ____? (be born)", "เธอ ____ เมื่อไร (be born)"), ("When were you born? I was born in 2014.", "เธอเกิดเมื่อไร ฉันเกิดปี 2014"), kind="open",
          inst=("Make five questions. Then answer with true sentences in your notebook.", "แต่งคำถาม 5 ข้อ แล้วตอบด้วยประโยคที่เป็นจริงลงในสมุด")),
        X(EX(2, "Write. What about you?", "เขียน แล้วนักเรียนล่ะ"), 50, ("____ you ____ something cute when you were a kid? (call)", "เธอ ____ ด้วยชื่อน่ารัก ๆ ตอนเป็นเด็กไหม (call)"),
          ("Were you called something cute when you were a kid? Yes, I was. I was called \"Bunny.\"", "ตอนเด็กเธอถูกเรียกด้วยชื่อน่ารัก ๆ ไหม ใช่ ฉันถูกเรียกว่า \"บันนี่\""), kind="open"),
        X(EX(2, "Write. What about you?", "เขียน แล้วนักเรียนล่ะ"), 50, ("As a child, ____ you ____ a special gift that you still have? (give)", "ตอนเด็ก เธอ ____ ของขวัญพิเศษที่ยังเก็บไว้ไหม (give)"),
          ("As a child, were you given a special gift that you still have? Yes, I was. I was given a teddy bear.", "ตอนเด็กเธอได้รับของขวัญพิเศษที่ยังเก็บไว้ไหม ใช่ ฉันได้รับตุ๊กตาหมี"), kind="open"),
        X(EX(2, "Write. What about you?", "เขียน แล้วนักเรียนล่ะ"), 50, ("____ you ever ____ to bed early because you were naughty? (send)", "เธอเคย ____ เข้านอนเร็วเพราะซนไหม (send)"),
          ("Were you ever sent to bed early because you were naughty? No, I wasn't!", "เธอเคยถูกส่งเข้านอนเร็วเพราะซนไหม ไม่เคย"), kind="open"),
        X(EX(2, "Write. What about you?", "เขียน แล้วนักเรียนล่ะ"), 50, ("Write your own question with was or were.", "แต่งคำถามของตัวเองด้วย was หรือ were"),
          ("Were you taken to the zoo when you were small? Yes, I was.", "ตอนเล็ก ๆ เธอเคยถูกพาไปสวนสัตว์ไหม ใช่"), kind="open"),
    ],
    "speak": {
        "models": [T("The Sphinx was built around 2500 BCE.", "สฟิงซ์ถูกสร้างขึ้นประมาณ 2500 ปีก่อนคริสตกาล"), T("When were the statues discovered?", "รูปปั้นถูกค้นพบเมื่อไร"),
                   T("The statues were found in 1974.", "รูปปั้นถูกพบในปี 1974"), T("The treasures weren't stolen.", "สมบัติไม่ได้ถูกขโมย"), T("When were you born?", "เธอเกิดเมื่อไร")],
        "turns": [
            {"q": T("When were you born?", "เธอเกิดเมื่อไร"), "starter": T("I was born in…", "ฉันเกิดใน…"), "example": T("I was born in 2014.", "ฉันเกิดปี 2014")},
            {"q": T("Where were you born?", "เธอเกิดที่ไหน"), "starter": T("I was born in (place)…", "ฉันเกิดที่…"), "example": T("I was born in Bangkok.", "ฉันเกิดที่กรุงเทพฯ")},
            {"q": T("Were you given a present on your last birthday?", "วันเกิดครั้งที่แล้วเธอได้รับของขวัญไหม"), "starter": T("Yes, I was. I was given… / No, I wasn't.", "ได้ ฉันได้รับ… / ไม่ได้"),
             "example": T("Yes, I was. I was given a new bike.", "ได้ ฉันได้รับจักรยานคันใหม่")},
        ],
    },
    "sort": {"title": T("WAS or WERE?", "WAS หรือ WERE"),
             "bins": [T("was (one)", "was (หนึ่ง)"), T("were (more than one)", "were (มากกว่าหนึ่ง)")],
             "items": [["the treasure", 0], ["the mummy", 0], ["a cat", 0], ["the Sphinx", 0], ["I", 0], ["my daughter", 0],
                       ["the statues", 1], ["the coins", 1], ["two mummies", 1], ["the thieves", 1], ["we", 1], ["you", 1, ("We say: you were.", "เราพูดว่า you were")]]},
    "build": ["The treasure | was | discovered | in a field.", "The statues | were | found | in 1974.", "When | were | you | born?",
              "The jewelry | was stolen | last | night.", "The gold | wasn't | hidden | in the ocean.", "Two mummies | were buried | in | this tomb."],
    "match": [["find", "found"], ["build", "built"], ["steal", "stolen"], ["hide", "hidden"], ["give", "given"], ["send", "sent"], ["break", "broken"], ["catch", "caught"], ["buy", "bought"]],
    "quiz": [
        Q("The treasure ____ discovered in a field.", "สมบัติ ____ ค้นพบในทุ่งนา", ["was", "were", "is", "did"]),
        Q("The statues ____ found in 1974.", "รูปปั้น ____ พบในปี 1974", ["were", "was", "are", "did"]),
        Q("When ____ you born?", "เธอ ____ เกิดเมื่อไร", ["were", "was", "did", "are"]),
        Q("The jewelry was ____ last night.", "เครื่องประดับถูก ____ เมื่อคืน", ["stolen", "stole", "steal", "stealed"]),
        Q("Was the gold ____?", "ทองคำถูก ____ หรือเปล่า", ["hidden", "hid", "hide", "hided"]),
        Q("Which sentence is passive?", "ประโยคไหนเป็น Passive", ["The coins were buried.", "Thieves buried the coins.", "They bury coins.", "I am burying coins."]),
        Q("The past participle of \"build\" is ____.", "กริยาช่องที่ 3 ของ build คือ ____", ["built", "builded", "build", "building"]),
        Q("The past participle of \"catch\" is ____.", "กริยาช่องที่ 3 ของ catch คือ ____", ["caught", "catched", "catch", "cought"]),
        Q("The artifact ____ bought in a store.", "โบราณวัตถุ ____ ซื้อจากร้านค้า", ["wasn't", "weren't", "didn't", "isn't"]),
        Q("We use the passive when we don't know ____.", "เราใช้ Passive เมื่อไม่รู้ว่า ____", ["who did the action", "the time", "the place", "the color"]),
    ],
}

# ================================================================== 3. VOCABULARY 2
v2_words = [
    W("analyze", "verb", "วิเคราะห์", "to study something very carefully to learn about it", "ศึกษาบางสิ่งอย่างละเอียดเพื่อเรียนรู้เกี่ยวกับมัน",
      "Scientists analyze the objects they find.", "นักวิทยาศาสตร์วิเคราะห์สิ่งของที่พบ", "analyze"),
    W("an artifact", "noun", "โบราณวัตถุ", "an old object that was made by people long ago", "สิ่งของเก่าที่คนในอดีตทำขึ้น",
      "This stone axe is an artifact.", "ขวานหินเล่มนี้เป็นโบราณวัตถุ", "artifact", hl="artifact"),
    W("a DNA test", "noun", "การตรวจดีเอ็นเอ", "a test that shows what is in the body's cells, and who your family is", "การตรวจที่บอกว่ามีอะไรในเซลล์ของร่างกาย และใครเป็นครอบครัวของเรา",
      "A DNA test showed they were from the same family.", "การตรวจดีเอ็นเอแสดงว่าพวกเขามาจากครอบครัวเดียวกัน", "dna-test", hl="DNA test"),
    W("a site", "noun", "แหล่งขุดค้น สถานที่", "a place where archaeologists dig or explore", "สถานที่ที่นักโบราณคดีขุดหรือสำรวจ",
      "Archaeologists study the site carefully.", "นักโบราณคดีศึกษาแหล่งขุดค้นอย่างละเอียด", "site", hl="site"),
    W("a sample", "noun", "ตัวอย่าง", "a small amount of something that is studied", "สิ่งของจำนวนเล็กน้อยที่นำไปศึกษา",
      "They took a sample of food from his stomach.", "พวกเขาเก็บตัวอย่างอาหารจากกระเพาะของเขา", "sample", hl="sample"),
]
vocab2 = {
    "id": "vocab2", "title": T("Vocabulary 2: How Archaeologists Work", "คำศัพท์ 2: นักโบราณคดีทำงานอย่างไร"), "short": T("Vocabulary 2", "คำศัพท์ 2"),
    "pages": "Book p.65 · Workbook p.51",
    "learn": [
        L("Learn", "Solving mysteries like a scientist 🔬", "ไขปริศนาแบบนักวิทยาศาสตร์ 🔬", [
            ("1. Find a <b>site</b>.", "1. หาแหล่งขุดค้น"), ("2. Dig and find <b>artifacts</b>.", "2. ขุดและพบโบราณวัตถุ"),
            ("3. Take a <b>sample</b> (a small piece).", "3. เก็บตัวอย่าง (ชิ้นเล็ก ๆ)"), ("4. <b>Analyze</b> it in a lab.", "4. วิเคราะห์ในห้องปฏิบัติการ"),
            ("5. Do a <b>DNA test</b> to learn about the person's family.", "5. ตรวจดีเอ็นเอเพื่อรู้เรื่องครอบครัวของบุคคลนั้น"),
        ], page="📖 p.65"),
        L("Story", "The Iceman 🧊", "มนุษย์น้ำแข็ง 🧊", [
            ("The Iceman is a mummy that was found in the ice in 1991.", "มนุษย์น้ำแข็งเป็นมัมมี่ที่ถูกพบในน้ำแข็งเมื่อปี 1991"),
            ("Scientists analyzed samples and artifacts from the site. Now we know a lot about how he lived and what he ate.", "นักวิทยาศาสตร์วิเคราะห์ตัวอย่างและโบราณวัตถุจากแหล่งขุดค้น ตอนนี้เรารู้มากขึ้นว่าเขาใช้ชีวิตอย่างไรและกินอะไร"),
        ], page="📒 p.51"),
    ],
    "words": v2_words,
    "book": [
        X(EX(1, "Listen and repeat. Then read and write.", "ฟังและพูดตาม แล้วอ่านและเขียน"), 65, ("When archaeologists make a new discovery, they have to ____ it.", "เมื่อนักโบราณคดีค้นพบสิ่งใหม่ พวกเขาต้อง ____ มัน"),
          ("analyze", "วิเคราะห์"), box=["analyze", "an artifact", "a DNA test", "a site", "a sample"], hint=("It's a verb: to study carefully.", "เป็นคำกริยา: ศึกษาอย่างละเอียด")),
        X(EX(1, "Listen and repeat. Then read and write.", "ฟังและพูดตาม แล้วอ่านและเขียน"), 65, ("To learn about a person's family, archaeologists do a ____. This test tells them who the person's father was, for example.", "เพื่อเรียนรู้เรื่องครอบครัว นักโบราณคดีทำ ____ การตรวจนี้บอกได้ เช่น ใครเป็นพ่อของบุคคลนั้น"),
          ("DNA test", "การตรวจดีเอ็นเอ")),
        X(EX(1, "Listen and repeat. Then read and write.", "ฟังและพูดตาม แล้วอ่านและเขียน"), 65, ("We can find out what people ate before they died. We can take a ____ of food from inside the person's stomach.", "เรารู้ได้ว่าคนกินอะไรก่อนตาย เราเก็บ ____ อาหารจากในกระเพาะ"),
          ("sample", "ตัวอย่าง")),
        X(EX(1, "Listen and repeat. Then read and write.", "ฟังและพูดตาม แล้วอ่านและเขียน"), 65, ("Archaeologists always study the ____ where something was discovered. This helps them to learn why people lived there.", "นักโบราณคดีศึกษา ____ ที่ค้นพบสิ่งของเสมอ ช่วยให้รู้ว่าทำไมคนจึงอาศัยอยู่ที่นั่น"),
          ("site", "แหล่งขุดค้น")),
        X(EX(1, "Listen and repeat. Then read and write.", "ฟังและพูดตาม แล้วอ่านและเขียน"), 65, ("Archaeologists often look for pottery and other ____ near the site. These objects help them learn how people lived.", "นักโบราณคดีมักหาเครื่องปั้นดินเผาและ ____ อื่น ๆ ใกล้แหล่งขุดค้น สิ่งของเหล่านี้ช่วยให้รู้ว่าคนใช้ชีวิตอย่างไร"),
          ("artifacts", "โบราณวัตถุ"), hint=("\"Other\" + plural noun.", "other + คำนามพหูพจน์")),
        X(EX(2, "Listen and stick.", "ฟังและติดสติกเกอร์"), 65, ("Order the stickers to tell how the archaeologist solved the mysteries. Work with a partner.", "เรียงสติกเกอร์เพื่อเล่าว่านักโบราณคดีไขปริศนาอย่างไร ทำกับเพื่อน"),
          kind="class", classNote=("Do this in class with the audio (TR: 6.5) and your book stickers.", "ทำในห้องเรียนพร้อมฟังเสียง (TR: 6.5) และสติกเกอร์ในหนังสือ")),
    ],
    "wb": [
        X(EX(1, "Write.", "เขียน"), 51, ("____ is a place that archaeologists want to excavate or explore.", "____ คือสถานที่ที่นักโบราณคดีอยากขุดค้นหรือสำรวจ"), ("A site", "แหล่งขุดค้น"),
          inst=("Complete the definitions with words from the box.", "เติมความหมายด้วยคำในกรอบ"), box=["analyze", "an artifact", "a DNA test", "a sample", "a site"]),
        X(EX(1, "Write.", "เขียน"), 51, ("____ is an object found at the site. It is not a living thing. It was made by someone.", "____ คือสิ่งของที่พบที่แหล่งขุดค้น ไม่มีชีวิต และมีคนทำขึ้น"), ("An artifact", "โบราณวัตถุ")),
        X(EX(1, "Write.", "เขียน"), 51, ("____ is a way to discover what is in the body's cells. It can help you find your relatives.", "____ คือวิธีค้นหาสิ่งที่อยู่ในเซลล์ ช่วยหาญาติได้"), ("A DNA test", "การตรวจดีเอ็นเอ")),
        X(EX(1, "Write.", "เขียน"), 51, ("Scientists ____ the objects they find to learn how old the objects are.", "นักวิทยาศาสตร์ ____ สิ่งของที่พบเพื่อรู้ว่าเก่าแค่ไหน"), ("analyze", "วิเคราะห์")),
        X(EX(1, "Write.", "เขียน"), 51, ("____ is a small amount of something, such as food, that someone studies.", "____ คือสิ่งของจำนวนเล็กน้อย เช่น อาหาร ที่นำไปศึกษา"), ("A sample", "ตัวอย่าง")),
        X(EX(2, "Listen and write.", "ฟังและเขียน"), 51, ("How do we know so much about the Iceman? Listen and write a word from Activity 1 after each sentence.", "เรารู้เรื่องมนุษย์น้ำแข็งได้อย่างไร ฟังแล้วเขียนคำจากกิจกรรมที่ 1"),
          kind="class", classNote=("Do this in class with the audio (TR: 6.2).", "ทำในห้องเรียนพร้อมฟังเสียง (TR: 6.2)")),
    ],
    "speak": {
        "models": [T("How did she discover they were from the same family?", "เธอค้นพบได้อย่างไรว่าพวกเขามาจากครอบครัวเดียวกัน"), T("I think she did a DNA test!", "ฉันคิดว่าเธอตรวจดีเอ็นเอ"),
                   T("They took a sample of food from his stomach.", "พวกเขาเก็บตัวอย่างอาหารจากกระเพาะของเขา")],
        "turns": [
            {"q": T("How can scientists learn what people ate long ago?", "นักวิทยาศาสตร์รู้ได้อย่างไรว่าคนในอดีตกินอะไร"), "starter": T("They can take…", "พวกเขาสามารถเก็บ…"),
             "example": T("They can take a sample of food and analyze it.", "พวกเขาสามารถเก็บตัวอย่างอาหารแล้วนำไปวิเคราะห์")},
            {"q": T("What artifacts are in your house that are very old?", "ในบ้านของนักเรียนมีสิ่งของเก่าแก่อะไรบ้าง"), "starter": T("We have an old…", "เรามี… เก่า"),
             "example": T("We have an old clay pot from my grandmother.", "เรามีหม้อดินเก่าจากคุณยาย")},
        ],
    },
    "spell": [{"w": w, "th": th} for w, th in [("analyze", "วิเคราะห์"), ("artifact", "โบราณวัตถุ"), ("site", "แหล่งขุดค้น"), ("sample", "ตัวอย่าง"), ("archaeologist", "นักโบราณคดี"), ("discovery", "การค้นพบ")]],
    "match": [["analyze", "study carefully"], ["an artifact", "an old object made by people"], ["a DNA test", "find your family"], ["a site", "a place to dig"], ["a sample", "a small amount to study"], ["excavate", "dig carefully"]],
    "build": ["Scientists | analyze | the objects | they find.", "They took | a sample | of food | from his stomach.", "A DNA test | can help you | find | your relatives.", "Archaeologists | study | the site | carefully."],
    "quiz": [
        Q("A place where archaeologists dig is ____.", "สถานที่ที่นักโบราณคดีขุดคือ ____", ["a site", "a sample", "a tattoo", "a DNA test"]),
        Q("An old object made by people is ____.", "สิ่งของเก่าที่คนทำขึ้นคือ ____", ["an artifact", "a site", "a sample", "a mummy"]),
        Q("A small amount of something to study is ____.", "สิ่งของจำนวนเล็กน้อยที่นำไปศึกษาคือ ____", ["a sample", "a site", "an artifact", "a tomb"]),
        Q("To learn who your family is, you can do ____.", "เพื่อรู้ว่าใครเป็นครอบครัว ทำ ____ ได้", ["a DNA test", "a sample", "a site", "a statue"]),
        Q("Scientists ____ the objects to learn how old they are.", "นักวิทยาศาสตร์ ____ สิ่งของเพื่อรู้ว่าเก่าแค่ไหน", ["analyze", "bury", "steal", "hide"]),
        Q("The Iceman was found in ____.", "มนุษย์น้ำแข็งถูกพบใน ____", ["the ice", "the sea", "a tomb in Peru", "a field in England"]),
    ],
}

# ================================================================== 4. GRAMMAR 2
grammar2 = {
    "id": "grammar2", "title": T("Grammar 2: Passive voice with by + agent", "ไวยากรณ์ 2: Passive Voice กับ by + ผู้กระทำ"), "short": T("Grammar 2", "ไวยากรณ์ 2"),
    "pages": "Book p.66 · Workbook p.52",
    "learn": [
        L("Rule 1", "Who did it? Add by + the person", "ใครทำ เติม by + ผู้กระทำ", [
            ("When we know who did the action, we add <b>by</b> + the person (the agent).", "เมื่อรู้ว่าใครทำ ให้เติม by + ผู้กระทำ"),
        ], examples=[("Active: <span class='k2'>The hiker</span> found the mummy.", "Active: นักเดินป่าพบมัมมี่"), ("Passive: The mummy was found <b>by</b> <span class='k2'>the hiker</span>.", "Passive: มัมมี่ถูกพบโดยนักเดินป่า")], page="📖 p.66"),
        L("Rule 2", "From active to passive in 3 steps", "เปลี่ยน Active เป็น Passive ใน 3 ขั้น", [
            ("1. Move the object to the front: <b>the bottles</b>", "1. ย้ายกรรมไปไว้หน้าประโยค: the bottles"),
            ("2. Add was / were + past participle: <b>weren't found</b>", "2. เติม was / were + กริยาช่องที่ 3: weren't found"),
            ("3. Add by + the agent: <b>by the divers</b>", "3. เติม by + ผู้กระทำ: by the divers"),
        ], examples=[("The divers didn't find the bottles. → The bottles weren't found by the divers.", "นักดำน้ำไม่ได้พบขวด → ขวดไม่ได้ถูกพบโดยนักดำน้ำ")], page="📖 p.66"),
        L("Rule 3", "Questions with by", "คำถามที่มี by", [
        ], examples=[("<b>Was</b> the pottery <b>broken by</b> thieves?", "เครื่องปั้นดินเผาถูกขโมยทำแตกหรือเปล่า"), ("<b>Were</b> those statues <b>discovered by</b> archaeologists?", "รูปปั้นเหล่านั้นถูกค้นพบโดยนักโบราณคดีหรือเปล่า"),
                     ("<b>Who was</b> the Iceman <b>found by</b>?", "มนุษย์น้ำแข็งถูกพบโดยใคร")], page="📒 p.52"),
        L("Story", "The Iceman story", "เรื่องมนุษย์น้ำแข็ง", [
            ("In 1991, a mummy was discovered by hikers in the ice. He was called the \"Iceman.\"", "ในปี 1991 นักเดินป่าค้นพบมัมมี่ในน้ำแข็ง เขาถูกเรียกว่า \"มนุษย์น้ำแข็ง\""),
            ("He was studied by scientists for ten years. In 2001, he was analyzed by Paul Gostner, who found an injury in his arm.", "นักวิทยาศาสตร์ศึกษาเขาเป็นเวลา 10 ปี ในปี 2001 พอล กอสต์เนอร์วิเคราะห์และพบบาดแผลที่แขน"),
            ("Now we know he was killed by someone. But who? He was born over 5,000 years ago, so we don't know!", "ตอนนี้เรารู้ว่าเขาถูกใครบางคนฆ่า แต่ใครล่ะ เขาเกิดเมื่อกว่า 5,000 ปีก่อน เราจึงไม่รู้"),
        ], page="📖 p.66"),
    ],
    "book": [
        X(EX(1, "Read. Complete the sentences.", "อ่าน เติมประโยคให้สมบูรณ์"), 66, ("One day in 1991 / a mummy / discover / hikers.", "วันหนึ่งในปี 1991 / มัมมี่ / ค้นพบ / นักเดินป่า"),
          ("One day in 1991, a mummy was discovered by hikers.", "วันหนึ่งในปี 1991 มัมมี่ถูกค้นพบโดยนักเดินป่า"), inst=("Work with a partner. Complete the sentences. Then tell the story.", "ทำกับเพื่อน เติมประโยคให้สมบูรณ์ แล้วเล่าเรื่อง")),
        X(EX(1, "Read. Complete the sentences.", "อ่าน เติมประโยคให้สมบูรณ์"), 66, ("He / bury / in the ice.", "เขา / ฝัง / ในน้ำแข็ง"), ("He was buried in the ice.", "เขาถูกฝังอยู่ในน้ำแข็ง"), hint=("No agent here: we don't know who.", "ข้อนี้ไม่มีผู้กระทำ เราไม่รู้ว่าใคร")),
        X(EX(1, "Read. Complete the sentences.", "อ่าน เติมประโยคให้สมบูรณ์"), 66, ("The mummy / describe / people around the world as the \"Iceman.\"", "มัมมี่ / เรียกขาน / ผู้คนทั่วโลก ว่า \"มนุษย์น้ำแข็ง\""),
          ("The mummy was described by people around the world as the \"Iceman.\"", "มัมมี่ถูกผู้คนทั่วโลกเรียกว่า \"มนุษย์น้ำแข็ง\"")),
        X(EX(1, "Read. Complete the sentences.", "อ่าน เติมประโยคให้สมบูรณ์"), 66, ("For the next ten years, the Iceman / study / scientists.", "ตลอด 10 ปีต่อมา มนุษย์น้ำแข็ง / ศึกษา / นักวิทยาศาสตร์"),
          ("For the next ten years, the Iceman was studied by scientists.", "ตลอด 10 ปีต่อมา มนุษย์น้ำแข็งถูกศึกษาโดยนักวิทยาศาสตร์")),
        X(EX(1, "Read. Complete the sentences.", "อ่าน เติมประโยคให้สมบูรณ์"), 66, ("At the site, artifacts / find / archaeologists.", "ที่แหล่งขุดค้น โบราณวัตถุ / พบ / นักโบราณคดี"),
          ("At the site, artifacts were found by archaeologists.", "ที่แหล่งขุดค้น โบราณวัตถุถูกพบโดยนักโบราณคดี"), hint=("Artifacts = many things → were.", "โบราณวัตถุหลายชิ้น → were")),
        X(EX(1, "Read. Complete the sentences.", "อ่าน เติมประโยคให้สมบูรณ์"), 66, ("Samples of food / take / from his stomach by scientists.", "ตัวอย่างอาหาร / เก็บ / จากกระเพาะโดยนักวิทยาศาสตร์"),
          ("Samples of food were taken from his stomach by scientists.", "ตัวอย่างอาหารถูกเก็บจากกระเพาะของเขาโดยนักวิทยาศาสตร์"), hint=("take → taken.", "take → taken")),
        X(EX(1, "Read. Complete the sentences.", "อ่าน เติมประโยคให้สมบูรณ์"), 66, ("In 2001 / the Iceman / analyze / Paul Gostner, who found an injury in the arm.", "ในปี 2001 / มนุษย์น้ำแข็ง / วิเคราะห์ / พอล กอสต์เนอร์ ผู้พบบาดแผลที่แขน"),
          ("In 2001, the Iceman was analyzed by Paul Gostner, who found an injury in the arm.", "ในปี 2001 มนุษย์น้ำแข็งถูกวิเคราะห์โดยพอล กอสต์เนอร์ ผู้พบบาดแผลที่แขน")),
        X(EX(1, "Read. Complete the sentences.", "อ่าน เติมประโยคให้สมบูรณ์"), 66, ("Now we know that the Iceman / kill / someone.", "ตอนนี้เรารู้ว่ามนุษย์น้ำแข็ง / ฆ่า / ใครบางคน"),
          ("Now we know that the Iceman was killed by someone.", "ตอนนี้เรารู้ว่ามนุษย์น้ำแข็งถูกใครบางคนฆ่า")),
        X(EX(1, "Read. Complete the sentences.", "อ่าน เติมประโยคให้สมบูรณ์"), 66, ("But who / he / kill / by?", "แต่ใคร / เขา / ฆ่า / โดย"), ("But who was he killed by?", "แต่เขาถูกใครฆ่า"),
          hint=("Question: who + was + he + past participle + by?", "คำถาม: who + was + he + กริยาช่องที่ 3 + by")),
        X(EX(1, "Read. Complete the sentences.", "อ่าน เติมประโยคให้สมบูรณ์"), 66, ("The mummy / born / over 5,000 years ago, so we don't know!", "มัมมี่ / เกิด / กว่า 5,000 ปีก่อน เราจึงไม่รู้"),
          ("The mummy was born over 5,000 years ago, so we don't know!", "มัมมี่เกิดเมื่อกว่า 5,000 ปีก่อน เราจึงไม่รู้")),
        X(EX(2, "Play a game.", "เล่นเกม"), 66, ("Cut out the cubes in the back of the book. Play with a partner. Take turns. Make sentences.", "ตัดลูกเต๋าท้ายเล่ม เล่นกับเพื่อน ผลัดกันแต่งประโยค"),
          ("A surfer, catch, stink lily. → A surfer was caught by a stink lily!", "นักโต้คลื่น จับ ดอกไม้เหม็น → นักโต้คลื่นถูกดอกไม้เหม็นจับ"), kind="open",
          hint=("Use was / were + past participle + by. Funny sentences are OK!", "ใช้ was / were + กริยาช่องที่ 3 + by ประโยคตลก ๆ ก็ได้")),
    ],
    "wb": [
        X(EX(1, "Read and write.", "อ่านและเขียน"), 52, ("Around 246 BCE, about 700,000 men ____ (hire) the Chinese emperor Qin Shihuang to make an army of men.", "ประมาณ 246 ปีก่อนคริสตกาล ชายราว 700,000 คน ____ (hire) จักรพรรดิจิ๋นซีฮ่องเต้ให้สร้างกองทัพ"),
          ("were hired by", "ถูกจ้างโดย"), inst=("Use the words in parentheses and by if needed.", "ใช้คำในวงเล็บ และเติม by ถ้าจำเป็น"), why=("This is the example in the workbook.", "ข้อนี้เป็นตัวอย่างในแบบฝึกหัด")),
        X(EX(1, "Read and write.", "อ่านและเขียน"), 52, ("For nearly forty years, thousands of statues ____ (make) the men.", "เกือบสี่สิบปี รูปปั้นหลายพันตัว ____ (make) ชายเหล่านั้น"), ("were made by", "ถูกสร้างโดย"),
          hint=("The men made them → add by.", "ชายเหล่านั้นเป็นผู้สร้าง → เติม by")),
        X(EX(1, "Read and write.", "อ่านและเขียน"), 52, ("When the ruler died in 210 BCE, the statues ____ (bury) with him in a tomb.", "เมื่อผู้ปกครองสิ้นพระชนม์ใน 210 ปีก่อนคริสตกาล รูปปั้น ____ (bury) พร้อมกับเขาในสุสาน"), ("were buried", "ถูกฝัง"),
          hint=("\"With him\" comes next, not an agent. No by.", "ตามด้วย with him ไม่ใช่ผู้กระทำ จึงไม่ต้องมี by")),
        X(EX(1, "Read and write.", "อ่านและเขียน"), 52, ("This incredible treasure ____ (forget) for centuries…", "สมบัติอันน่าทึ่งนี้ ____ (forget) เป็นเวลาหลายศตวรรษ…"), ("was forgotten", "ถูกลืม"), hint=("forget → forgotten.", "forget → forgotten")),
        X(EX(1, "Read and write.", "อ่านและเขียน"), 52, ("…but in 1974 it ____ (find) Chinese farmers!", "…แต่ในปี 1974 มัน ____ (find) ชาวนาจีน"), ("was found by", "ถูกพบโดย")),
        X(EX(1, "Read and write.", "อ่านและเขียน"), 52, ("When the site ____ (excavate) archaeologists a few years later,…", "เมื่อแหล่งขุดค้น ____ (excavate) นักโบราณคดีในไม่กี่ปีต่อมา…"), ("was excavated by", "ถูกขุดค้นโดย")),
        X(EX(1, "Read and write.", "อ่านและเขียน"), 52, ("…more than 6,000 statues ____ (discover).", "…รูปปั้นมากกว่า 6,000 ตัว ____ (discover)"), ("were discovered", "ถูกค้นพบ")),
        X(EX(1, "Read and write.", "อ่านและเขียน"), 52, ("Originally, the statues ____ (paint) in different colors.", "แต่เดิม รูปปั้น ____ (paint) ด้วยสีต่าง ๆ"), ("were painted", "ถูกทาสี")),
    ],
    "speak": {
        "models": [T("The mummy was found by the hiker.", "มัมมี่ถูกพบโดยนักเดินป่า"), T("The bottles weren't found by the divers.", "ขวดไม่ได้ถูกพบโดยนักดำน้ำ"),
                   T("Was the pottery broken by thieves?", "เครื่องปั้นดินเผาถูกขโมยทำแตกหรือเปล่า"), T("A surfer was caught by a stink lily!", "นักโต้คลื่นถูกดอกไม้เหม็นจับ")],
        "turns": [
            {"q": T("Make it passive: Archaeologists found the statues.", "เปลี่ยนเป็น Passive: Archaeologists found the statues."), "starter": T("The statues were…", "The statues were…"),
             "example": T("The statues were found by archaeologists.", "รูปปั้นถูกพบโดยนักโบราณคดี")},
            {"q": T("Make it passive: Hikers discovered the Iceman.", "เปลี่ยนเป็น Passive: Hikers discovered the Iceman."), "starter": T("The Iceman was…", "The Iceman was…"),
             "example": T("The Iceman was discovered by hikers.", "มนุษย์น้ำแข็งถูกค้นพบโดยนักเดินป่า")},
            {"q": T("Make a funny sentence with by.", "แต่งประโยคตลก ๆ ที่มี by"), "starter": T("A … was … by a …", "A … was … by a …"),
             "example": T("A teacher was chased by a chicken!", "ครูถูกไก่ไล่")},
        ],
    },
    "build": ["The mummy | was found | by | the hiker.", "Artifacts | were found | by | archaeologists.", "Was the pottery | broken | by | thieves?",
              "Who | was the Iceman | found | by?", "The statues | were made | by | the men.", "The treasure | was found | by | Chinese farmers."],
    "sort": {"title": T("Active or passive?", "Active หรือ Passive"),
             "bins": [T("Active 🏃", "Active 🏃"), T("Passive 📦", "Passive 📦")],
             "items": [["Hikers found the mummy.", 0], ["Thieves stole the gold.", 0], ["Scientists analyzed the samples.", 0], ["Farmers found the statues.", 0],
                       ["The mummy was found by hikers.", 1], ["The gold was stolen.", 1], ["The samples were analyzed.", 1], ["The statues were found by farmers.", 1]]},
    "match": [["Hikers found the mummy.", "The mummy was found by hikers."], ["Farmers found the statues.", "The statues were found by farmers."],
              ["Thieves broke the pottery.", "The pottery was broken by thieves."], ["Scientists studied the Iceman.", "The Iceman was studied by scientists."],
              ["Divers found the bottles.", "The bottles were found by divers."], ["A dog ate my homework.", "My homework was eaten by a dog."]],
    "quiz": [
        Q("The mummy was found ____ the hiker.", "มัมมี่ถูกพบ ____ นักเดินป่า", ["by", "with", "from", "of"]),
        Q("Passive of \"Thieves stole the gold\":", "Passive ของ Thieves stole the gold:", ["The gold was stolen by thieves.", "The gold stole thieves.", "Thieves were stolen by the gold.", "The gold is steal by thieves."]),
        Q("The statues ____ made by the men.", "รูปปั้น ____ สร้างโดยชายเหล่านั้น", ["were", "was", "did", "are"]),
        Q("____ was the Iceman found by?", "มนุษย์น้ำแข็งถูกพบโดย ____", ["Who", "What", "Where", "When"]),
        Q("In 1974, the statues were found by ____.", "ในปี 1974 รูปปั้นถูกพบโดย ____", ["Chinese farmers", "hikers", "divers", "thieves"]),
        Q("The Iceman was found by hikers in ____.", "มนุษย์น้ำแข็งถูกพบโดยนักเดินป่าในปี ____", ["1991", "1974", "2009", "2001"]),
        Q("The treasure was ____ for centuries.", "สมบัติถูก ____ เป็นเวลาหลายศตวรรษ", ["forgotten", "forgot", "forget", "forgetted"]),
        Q("Was the pottery broken by thieves? No, it ____.", "เครื่องปั้นดินเผาถูกขโมยทำแตกหรือเปล่า ไม่ ____", ["wasn't", "weren't", "didn't", "isn't"]),
    ],
}

# ================================================================== 5. SONG
song = {
    "id": "song", "title": T("Song: So Much to Learn", "เพลง: So Much to Learn"), "short": T("Song", "เพลง"), "pages": "Book p.67 · Workbook p.53",
    "learn": [
        L("Song", "🎵 So Much to Learn", "🎵 เพลง So Much to Learn", [
            ("Listen, read, and sing in class with T. Roy (TR: 6.7).", "ฟัง อ่าน และร้องเพลงในห้องเรียนกับครูรอย (TR: 6.7)"),
            ("The words of the song are in your book on page 67. 📖", "เนื้อเพลงอยู่ในหนังสือหน้า 67 📖"),
            ("The song is about why history is exciting: there is so much to discover and learn.", "เพลงนี้พูดถึงความน่าตื่นเต้นของประวัติศาสตร์ ยังมีอีกมากให้ค้นพบและเรียนรู้"),
        ], page="📖 p.67"),
        L("Key words", "Key words in the song", "คำสำคัญในเพลง", [
        ], table=[["Word", "ไทย"], ["mystery", "ปริศนา"], ["buried", "ถูกฝัง"], ["mummies", "มัมมี่"], ["excavated", "ถูกขุดค้น"], ["kings", "กษัตริย์"],
                  ["treasure", "สมบัติ"], ["underground", "ใต้ดิน"], ["look around", "มองไปรอบ ๆ"]],
          note=("The photo on page 67 is a Roman villa in Bath, England.", "ภาพในหน้า 67 คือบ้านโรมันโบราณที่เมืองบาธ ประเทศอังกฤษ"), page="📖 p.67"),
        L("Sounds of English", "The sound in bought, caught, astronaut", "เสียงใน bought, caught, astronaut", [
            ("These letters can make the same sound \"aw\": <b>ough</b>, <b>augh</b>, <b>au</b>, <b>aw</b>.", "ตัวอักษรเหล่านี้ออกเสียง \"ออ\" เหมือนกัน: ough, augh, au, aw"),
            ("b<b>ough</b>t · c<b>augh</b>t · astron<b>au</b>t · s<b>aw</b>", "bought · caught · astronaut · saw"),
        ], examples=[("The gold was stolen. It wasn't bought.", "ทองคำถูกขโมย ไม่ได้ถูกซื้อมา"), ("Two weeks later, the thieves were caught.", "สองสัปดาห์ต่อมา ขโมยถูกจับ"),
                     ("A scientist was brought to the site.", "นักวิทยาศาสตร์ถูกพามาที่แหล่งขุดค้น"), ("An astronaut prepared his flight.", "นักบินอวกาศเตรียมการบิน")], page="📖 p.67"),
    ],
    "book": [
        X(EX(1, "Listen, read, and sing.", "ฟัง อ่าน และร้อง"), 67, ("Sing the song \"So Much to Learn.\"", "ร้องเพลง So Much to Learn"),
          kind="class", classNote=("Sing it in class with the audio (TR: 6.7). The words are in your book.", "ร้องในห้องเรียนพร้อมเสียง (TR: 6.7) เนื้อเพลงอยู่ในหนังสือ")),
        X(EX(2, "Listen and repeat.", "ฟังและพูดตาม"), 67, ("The gold was stolen. It wasn't bought.", "ทองคำถูกขโมย ไม่ได้ถูกซื้อมา"),
          kind="class", classNote=("In class: TR 6.8. At home: press 🔊 and repeat the four sentences in Speak.", "ในห้องเรียน: TR 6.8 ที่บ้าน: กด 🔊 แล้วพูดตาม 4 ประโยคในส่วนฝึกพูด")),
    ],
    "wb": [
        X(EX(1, "Listen to the song.", "ฟังเพลง"), 53, ("Number the words in the order that you first hear them (1 to 5): scientists, mummies, money, pottery, statues.", "ใส่หมายเลขตามลำดับที่ได้ยินครั้งแรก (1 ถึง 5)"),
          kind="class", classNote=("Do this in class with the audio (TR: 6.3). Statues is number 1 (the example).", "ทำในห้องเรียนพร้อมฟังเสียง (TR: 6.3) statues เป็นหมายเลข 1 (ตัวอย่าง)")),
        X(EX(2, "Listen.", "ฟัง"), 53, ("Circle the words that have the same sound as augh in taught: drought, saw, frown, knew, bought, course, astronaut, fought, caught, sew, draw", "วงกลมคำที่มีเสียงเหมือน augh ใน taught"),
          ("bought, fought, caught, saw, draw, astronaut (and course)", "bought, fought, caught, saw, draw, astronaut (และ course)"),
          hint=("Say each word with 🔊. Does it sound like \"taught\"?", "ฟังแต่ละคำด้วย 🔊 ออกเสียงเหมือน taught ไหม"),
          why=("drought and frown have the \"ow\" sound; knew has \"oo\"; sew has \"oh\". Course has the same vowel, but with an r.", "drought และ frown ออกเสียง \"เอา\" knew ออกเสียง \"อู\" sew ออกเสียง \"โอ\" ส่วน course มีเสียงสระเดียวกันแต่มี r")),
        X(EX(2, "Listen.", "ฟัง"), 53, ("Underline the letters that make the sound.", "ขีดเส้นใต้ตัวอักษรที่ทำให้เกิดเสียงนั้น"),
          ("t(augh)t, b(ough)t, f(ough)t, c(augh)t, s(aw), dr(aw), astron(au)t, c(our)se", "t(augh)t, b(ough)t, f(ough)t, c(augh)t, s(aw), dr(aw), astron(au)t, c(our)se")),
    ],
    "speak": {
        "models": [T("The gold was stolen. It wasn't bought.", "ทองคำถูกขโมย ไม่ได้ถูกซื้อมา"), T("Two weeks later, the thieves were caught.", "สองสัปดาห์ต่อมา ขโมยถูกจับ"),
                   T("A scientist was brought to the site.", "นักวิทยาศาสตร์ถูกพามาที่แหล่งขุดค้น"), T("An astronaut prepared his flight.", "นักบินอวกาศเตรียมการบิน"),
                   T("taught, bought, caught, saw, draw", "taught, bought, caught, saw, draw")],
        "turns": [{"q": T("Say a sentence with caught and bought.", "พูดประโยคที่มีคำว่า caught และ bought"), "starter": T("I…", "ฉัน…"),
                   "example": T("I caught a fish and my dad bought ice cream.", "ฉันจับปลาได้ และพ่อซื้อไอศกรีม")}],
    },
    "sort": {"title": T("Does it have the \"aw\" sound like taught?", "มีเสียง \"ออ\" เหมือน taught ไหม"),
             "bins": [T("Yes: aw 🗣️", "ใช่: ออ 🗣️"), T("No ✋", "ไม่ใช่ ✋")],
             "items": [["bought", 0], ["caught", 0], ["fought", 0], ["saw", 0], ["draw", 0], ["astronaut", 0], ["taught", 0],
                       ["drought", 1, ("drought sounds like \"out\".", "drought ออกเสียงเหมือน out")], ["frown", 1], ["knew", 1], ["sew", 1, ("sew sounds like \"so\".", "sew ออกเสียงเหมือน so")]]},
    "spell": [{"w": w, "th": th} for w, th in [("bought", "ซื้อ (ช่อง 2, 3)"), ("caught", "จับ (ช่อง 2, 3)"), ("taught", "สอน (ช่อง 2, 3)"), ("astronaut", "นักบินอวกาศ"), ("draw", "วาด"), ("mystery", "ปริศนา")]],
    "quiz": [
        Q("Which word has the same sound as \"taught\"?", "คำไหนมีเสียงเหมือน taught", ["caught", "drought", "frown", "knew"]),
        Q("Which word has a DIFFERENT sound?", "คำไหนออกเสียงต่างจากคำอื่น", ["sew", "saw", "draw", "bought"]),
        Q("What is the name of the song in Unit 6?", "เพลงในบทที่ 6 ชื่ออะไร", ["So Much to Learn", "Extreme Sports", "The Lost City", "History Rocks"]),
        Q("Two weeks later, the thieves were ____.", "สองสัปดาห์ต่อมา ขโมยถูก ____", ["caught", "catched", "catch", "cought"]),
        Q("Which letters make the \"aw\" sound in astronaut?", "ตัวอักษรใดทำให้เกิดเสียง \"ออ\" ใน astronaut", ["au", "as", "ro", "na"]),
        Q("The gold was stolen. It wasn't ____.", "ทองคำถูกขโมย ไม่ได้ถูก ____", ["bought", "buyed", "brought", "boat"]),
    ],
}

# ================================================================== 6. READING
reading = {
    "id": "reading", "title": T("Reading: The Lost City of Atlantis", "การอ่าน: เมืองที่สาบสูญแอตแลนติส"), "short": T("Reading", "การอ่าน"), "pages": "Book p.68 · Workbook p.54",
    "learn": [
        L("Before you read", "Key words", "คำสำคัญ", [
        ], table=[["Word", "ไทย"], ["lost", "สาบสูญ หายไป"], ["destroy", "ทำลาย"], ["earthquake", "แผ่นดินไหว"], ["sink (sank)", "จม"], ["wildlife", "สัตว์ป่า"],
                  ["imagination", "จินตนาการ"], ["exist", "มีอยู่"], ["diver", "นักดำน้ำ"]], page="📖 p.68"),
        L("Summary", "The Lost City of Atlantis 🌊", "เมืองที่สาบสูญแอตแลนติส 🌊", [
            ("Read the full text in your book. This is a short summary.", "อ่านเนื้อเรื่องเต็มในหนังสือ นี่คือสรุปสั้น ๆ"),
            ("Atlantis was a \"lost city.\" In the story, it was destroyed in one terrible night of fire and earthquakes, and it sank into the sea.", "แอตแลนติสเป็น \"เมืองที่สาบสูญ\" ในเรื่องเล่า เมืองถูกทำลายในคืนที่เลวร้ายด้วยไฟและแผ่นดินไหว แล้วจมลงสู่ทะเล"),
            ("A famous man named Plato first told the story more than 2,000 years ago. He said Atlantis was full of gold, silver and amazing wildlife.", "ชายผู้มีชื่อเสียงชื่อเพลโตเล่าเรื่องนี้เป็นคนแรกเมื่อกว่า 2,000 ปีก่อน เขาบอกว่าแอตแลนติสเต็มไปด้วยทองคำ เงิน และสัตว์ป่าที่น่าทึ่ง"),
            ("Many people have looked for it, but no artifacts have ever been found.", "หลายคนเคยออกตามหา แต่ไม่เคยพบโบราณวัตถุใด ๆ เลย"),
            ("Most people think Atlantis was never a real place. It's probably just a story, but some people still hope it will be found one day.", "คนส่วนใหญ่คิดว่าแอตแลนติสไม่เคยมีอยู่จริง น่าจะเป็นแค่เรื่องเล่า แต่บางคนยังหวังว่าจะพบในสักวัน"),
        ], page="📖 p.68"),
        L("Workbook reading", "Trash Is Treasure (Workbook p.54)", "Trash Is Treasure ขยะคือสมบัติ (แบบฝึกหัดหน้า 54)", [
            ("Read the full text in your workbook. This is a short summary.", "อ่านเนื้อเรื่องเต็มในแบบฝึกหัด นี่คือสรุปสั้น ๆ"),
            ("There are many kinds of archaeologists:", "นักโบราณคดีมีหลายประเภท:"),
            ("🔬 Forensic archaeologists analyze DNA and help the police.", "🔬 นักโบราณคดีนิติวิทยาศาสตร์วิเคราะห์ดีเอ็นเอและช่วยตำรวจ"),
            ("🗺️ Landscape archaeologists study sites.", "🗺️ นักโบราณคดีภูมิทัศน์ศึกษาแหล่งโบราณ"),
            ("🦴 Osteologists study bones.", "🦴 นักกระดูกวิทยาศึกษากระดูก"),
            ("🗑️ \"Garbologists\" study trash. Old trash shows what people threw away, what they ate and what diseases they had.", "🗑️ \"นักขยะวิทยา\" ศึกษาขยะ ขยะเก่าบอกว่าคนทิ้งอะไร กินอะไร และเป็นโรคอะไร"),
        ], page="📒 p.54"),
    ],
    "book": [
        X(EX(1, "Listen and read.", "ฟังและอ่าน"), 68, ("How was Atlantis destroyed?", "แอตแลนติสถูกทำลายอย่างไร"), ("In one terrible night of fire and earthquakes. It sank into the sea.", "ในคืนที่เลวร้ายด้วยไฟและแผ่นดินไหว และจมลงสู่ทะเล"),
          inst=("Read \"The Lost City of Atlantis\" in your book (TR: 6.9). Then answer.", "อ่านเรื่อง The Lost City of Atlantis ในหนังสือ (TR: 6.9) แล้วตอบคำถาม")),
        X(EX(1, "Listen and read.", "ฟังและอ่าน"), 68, ("Who first told the story of Atlantis?", "ใครเป็นคนแรกที่เล่าเรื่องแอตแลนติส"), ("A famous man named Plato.", "ชายผู้มีชื่อเสียงชื่อเพลโต")),
        X(EX(1, "Listen and read.", "ฟังและอ่าน"), 68, ("When did he tell the story?", "เขาเล่าเรื่องนี้เมื่อไร"), ("More than 2,000 years ago.", "เมื่อกว่า 2,000 ปีก่อน")),
        X(EX(1, "Listen and read.", "ฟังและอ่าน"), 68, ("What was the city full of?", "เมืองนี้เต็มไปด้วยอะไร"), ("Gold, silver and incredible wildlife.", "ทองคำ เงิน และสัตว์ป่าที่น่าทึ่ง")),
        X(EX(1, "Listen and read.", "ฟังและอ่าน"), 68, ("Have any artifacts from Atlantis been found?", "เคยพบโบราณวัตถุจากแอตแลนติสไหม"), ("No. No artifacts have ever been discovered.", "ไม่เคย ไม่เคยมีการค้นพบโบราณวัตถุเลย")),
        X(EX(1, "Listen and read.", "ฟังและอ่าน"), 68, ("What do most people think about Atlantis?", "คนส่วนใหญ่คิดอย่างไรเกี่ยวกับแอตแลนติส"), ("They think it was never a real place. It's probably just a story.", "คิดว่ามันไม่เคยมีอยู่จริง น่าจะเป็นแค่เรื่องเล่า")),
        X(EX(2, "Discuss and draw.", "อภิปรายและวาดภาพ"), 68, ("Imagine you and your partner are archaeologists. You have just discovered Atlantis. Draw and label three artifacts you find there.", "สมมติว่านักเรียนและเพื่อนเป็นนักโบราณคดีที่เพิ่งค้นพบแอตแลนติส วาดและเขียนชื่อโบราณวัตถุ 3 ชิ้นที่พบ"),
          ("a gold crown, a silver plate, a statue of a dolphin", "มงกุฎทองคำ จานเงิน รูปปั้นโลมา"), kind="open",
          hint=("Think: the city was full of gold, silver and wildlife.", "คิดถึงเมืองที่เต็มไปด้วยทองคำ เงิน และสัตว์ป่า")),
    ],
    "wb": [
        X(EX(1, "Listen and read.", "ฟังและอ่าน"), 54, ("Read \"Trash Is Treasure\" in your workbook.", "อ่านเรื่อง Trash Is Treasure ในแบบฝึกหัด"),
          kind="class", classNote=("Read it in your workbook. Listen in class (TR: 6.5). Look at the summary in Learn.", "อ่านในแบบฝึกหัด ฟังในห้องเรียน (TR: 6.5) ดูสรุปในส่วน Learn")),
        X(EX(2, "Check T for True and F for False.", "เลือก T ถ้าจริง F ถ้าเท็จ"), 54, ("Not all archaeologists work at ancient sites.", "นักโบราณคดีไม่ได้ทำงานที่แหล่งโบราณทุกคน"), ("T (True)", "T (จริง)"),
          choices=["T", "F"], right=0, why=("Forensic archaeologists help the police, and garbologists study trash.", "นักโบราณคดีนิติวิทยาศาสตร์ช่วยตำรวจ และนักขยะวิทยาศึกษาขยะ")),
        X(EX(2, "Check T for True and F for False.", "เลือก T ถ้าจริง F ถ้าเท็จ"), 54, ("The trash buried underground can't help us learn about the past.", "ขยะที่ฝังอยู่ใต้ดินช่วยให้เราเรียนรู้อดีตไม่ได้"), ("F (False)", "F (เท็จ)"),
          choices=["T", "F"], right=1, why=("We can learn about human history from what people threw away.", "เราเรียนรู้ประวัติศาสตร์จากสิ่งที่คนทิ้งได้")),
        X(EX(2, "Check T for True and F for False.", "เลือก T ถ้าจริง F ถ้าเท็จ"), 54, ("Biodegradable trash decomposes quickly when it is buried.", "ขยะที่ย่อยสลายได้ย่อยสลายเร็วเมื่อถูกฝัง"), ("F (False)", "F (เท็จ)"),
          choices=["T", "F"], right=1, why=("It does not decompose as quickly as we thought.", "มันไม่ได้ย่อยสลายเร็วอย่างที่เราคิด")),
        X(EX(3, "Read again. Label the tree.", "อ่านอีกครั้ง เติมแผนภาพต้นไม้"), 54, ("What does each kind of archaeologist study? garbology, landscape, forensic, osteology", "นักโบราณคดีแต่ละประเภทศึกษาอะไร"),
          ("garbology: trash · landscape: sites · forensic: DNA (and crimes) · osteology: bones", "ขยะวิทยา: ขยะ · ภูมิทัศน์: แหล่งโบราณ · นิติวิทยาศาสตร์: ดีเอ็นเอ (และคดีอาชญากรรม) · กระดูกวิทยา: กระดูก")),
    ],
    "speak": {
        "models": [T("Atlantis sank into the sea.", "แอตแลนติสจมลงสู่ทะเล"), T("No artifacts have ever been found.", "ไม่เคยพบโบราณวัตถุเลย"), T("I think it's just a story.", "ฉันคิดว่ามันเป็นแค่เรื่องเล่า")],
        "turns": [
            {"q": T("Do you think Atlantis was a real place?", "นักเรียนคิดว่าแอตแลนติสมีอยู่จริงไหม"), "starter": T("I think… because…", "ฉันคิดว่า… เพราะ…"),
             "example": T("I think it's just a story because nothing was ever found.", "ฉันคิดว่าเป็นแค่เรื่องเล่า เพราะไม่เคยพบอะไรเลย")},
            {"q": T("What three artifacts would you find in Atlantis?", "นักเรียนจะพบโบราณวัตถุ 3 ชิ้นอะไรในแอตแลนติส"), "starter": T("I would find…", "ฉันจะพบ…"),
             "example": T("I would find a gold crown, a silver plate and a statue.", "ฉันจะพบมงกุฎทองคำ จานเงิน และรูปปั้น")},
        ],
    },
    "match": [["Plato", "first told the story"], ["earthquake", "แผ่นดินไหว"], ["sink", "จม"], ["garbologist", "studies trash"], ["osteologist", "studies bones"], ["forensic archaeologist", "analyzes DNA"]],
    "build": ["Atlantis | sank | into | the sea.", "Plato | first told | the story | of Atlantis.", "No artifacts | have ever been | found.", "Garbologists | study | trash."],
    "quiz": [
        Q("Who first told the story of Atlantis?", "ใครเล่าเรื่องแอตแลนติสเป็นคนแรก", ["Plato", "Qin Shihuang", "Paul Gostner", "Johan Reinhard"]),
        Q("Atlantis sank into ____.", "แอตแลนติสจมลงสู่ ____", ["the sea", "a desert", "the ice", "a river"]),
        Q("Atlantis was destroyed by fire and ____.", "แอตแลนติสถูกทำลายด้วยไฟและ ____", ["earthquakes", "snow", "thieves", "wind"]),
        Q("How many artifacts from Atlantis have been found?", "พบโบราณวัตถุจากแอตแลนติสกี่ชิ้น", ["none", "6,000", "3,500", "five"]),
        Q("Most people think Atlantis was ____.", "คนส่วนใหญ่คิดว่าแอตแลนติส ____", ["just a story", "in Thailand", "found in 1974", "a mummy"]),
        Q("A \"garbologist\" studies ____.", "นักขยะวิทยาศึกษา ____", ["trash", "bones", "stars", "plants"]),
        Q("An osteologist is interested in ____.", "นักกระดูกวิทยาสนใจ ____", ["bones", "trash", "DNA", "gold"]),
    ],
}

# ================================================================== 7. MISSION
mission = {
    "id": "mission", "title": T("Mission: Learn about local history", "ภารกิจ: เรียนรู้ประวัติศาสตร์ท้องถิ่น"), "short": T("Mission 🏛️", "ภารกิจ 🏛️"), "pages": "Book p.69",
    "learn": [
        L("Value", "Our mission: Learn about local history 🏛️", "ภารกิจของเรา: เรียนรู้ประวัติศาสตร์ท้องถิ่น 🏛️", [
            ("<b>Local history</b> is the history of the place where you live: your town, your temple, your market, your family.", "ประวัติศาสตร์ท้องถิ่น คือ ประวัติของสถานที่ที่เราอาศัยอยู่ เช่น เมือง วัด ตลาด และครอบครัวของเรา"),
            ("When we learn about the past, we understand our home better, and we take care of old places.", "เมื่อเรียนรู้อดีต เราจะเข้าใจบ้านเกิดมากขึ้น และช่วยกันดูแลสถานที่เก่าแก่"),
        ], page="📖 p.69"),
        L("Explorer", "Johan Reinhard, National Geographic Explorer", "โยฮัน ไรน์ฮาร์ด นักสำรวจเนชั่นแนล จีโอกราฟิก", [
            ("Johan Reinhard is an anthropologist. He studies people and how they lived in the past.", "โยฮัน ไรน์ฮาร์ดเป็นนักมานุษยวิทยา เขาศึกษามนุษย์และวิถีชีวิตในอดีต"),
            ("The photo shows him with a mummy on Mount Llullaillaco, Argentina.", "ภาพแสดงเขากับมัมมี่บนภูเขายูยาอิยาโก ประเทศอาร์เจนตินา"),
            ("His message: He wanted to learn about people from the past who lived very different lives. He was so happy to find a job that does this! Read his words on page 69. 📖", "ข้อคิดของเขา: เขาอยากเรียนรู้เกี่ยวกับคนในอดีตที่ใช้ชีวิตต่างจากเขามาก และดีใจมากที่พบอาชีพแบบนี้ อ่านคำพูดของเขาในหน้า 69 📖"),
        ], page="📖 p.69"),
        L("Think", "How can I learn about local history?", "ฉันจะเรียนรู้ประวัติศาสตร์ท้องถิ่นได้อย่างไร", [
            ("👵 Ask your grandparents about the old days.", "👵 ถามปู่ย่าตายายเกี่ยวกับเรื่องราวในอดีต"),
            ("🛕 Visit an old temple or a museum near your home.", "🛕 ไปเที่ยววัดเก่าหรือพิพิธภัณฑ์ใกล้บ้าน"),
            ("📷 Look at old photos of your town.", "📷 ดูภาพถ่ายเก่าของเมือง"),
            ("🚯 Don't write on or damage old buildings.", "🚯 อย่าขีดเขียนหรือทำลายสิ่งก่อสร้างเก่าแก่"),
        ], page="📖 p.69"),
    ],
    "book": [
        X(("Think. Pair. Share. Question 1", "คิด จับคู่ แบ่งปัน: ข้อ 1"), 69, ("Is it important to protect historical places in your country? Why or why not?", "การปกป้องสถานที่ทางประวัติศาสตร์ในประเทศสำคัญไหม ทำไม"),
          ("Yes, it is, because they tell us about our past, and when they are destroyed, they are lost forever.", "สำคัญ เพราะสถานที่เหล่านั้นบอกเล่าอดีตของเรา และถ้าถูกทำลายก็จะหายไปตลอดกาล"), kind="open"),
        X(("Think. Pair. Share. Question 2", "คิด จับคู่ แบ่งปัน: ข้อ 2"), 69, ("What do you think we can learn from people who lived in ancient times?", "นักเรียนคิดว่าเราเรียนรู้อะไรจากคนในสมัยโบราณได้บ้าง"),
          ("We can learn how they built houses, what they ate, and how they lived without phones and cars.", "เราเรียนรู้ได้ว่าพวกเขาสร้างบ้านอย่างไร กินอะไร และใช้ชีวิตอย่างไรโดยไม่มีโทรศัพท์และรถยนต์"), kind="open"),
        X(("Think. Pair. Share. Question 3", "คิด จับคู่ แบ่งปัน: ข้อ 3"), 69, ("Which places are of historical interest in your area?", "ในพื้นที่ของนักเรียนมีสถานที่ทางประวัติศาสตร์ที่น่าสนใจที่ไหนบ้าง"),
          ("There is a very old temple and an old market near my school.", "มีวัดเก่าแก่มากและตลาดเก่าใกล้โรงเรียนของฉัน"), kind="open",
          hint=("Think of old temples, museums, old markets or old houses near you.", "นึกถึงวัดเก่า พิพิธภัณฑ์ ตลาดเก่า หรือบ้านเก่าใกล้บ้าน")),
    ],
    "speak": {
        "models": [T("It's important to protect historical places.", "การปกป้องสถานที่ทางประวัติศาสตร์เป็นสิ่งสำคัญ"), T("There is an old temple near my house.", "มีวัดเก่าอยู่ใกล้บ้านของฉัน"),
                   T("We can learn a lot from the past.", "เราเรียนรู้จากอดีตได้มาก")],
        "turns": [
            {"q": T("What old place near you would you like to visit?", "นักเรียนอยากไปเที่ยวสถานที่เก่าแก่ที่ไหนใกล้บ้าน"), "starter": T("I'd like to visit…", "ฉันอยากไปเที่ยว…"),
             "example": T("I'd like to visit the old temple near my school.", "ฉันอยากไปเที่ยววัดเก่าใกล้โรงเรียน")},
            {"q": T("What question would you ask your grandparents about the past?", "นักเรียนจะถามปู่ย่าตายายเรื่องอดีตว่าอะไร"), "starter": T("I would ask: …", "ฉันจะถามว่า: …"),
             "example": T("I would ask: What was our town like when you were a child?", "ฉันจะถามว่า: ตอนคุณยายเป็นเด็ก เมืองของเราเป็นอย่างไร")},
        ],
    },
    "sort": {"title": T("Does it protect history or damage it?", "สิ่งนี้ปกป้องหรือทำลายประวัติศาสตร์"),
             "bins": [T("Protect ✅", "ปกป้อง ✅"), T("Damage ❌", "ทำลาย ❌")],
             "items": [["visiting a museum quietly", 0], ["asking grandparents about the past", 0], ["keeping old photos safe", 0], ["cleaning an old temple", 0],
                       ["writing your name on an old wall", 1], ["taking stones from a site", 1], ["throwing trash at a historical place", 1]]},
    "quiz": [
        Q("Local history is the history of ____.", "ประวัติศาสตร์ท้องถิ่นคือประวัติของ ____", ["the place where you live", "the moon", "another planet", "a video game"]),
        Q("Johan Reinhard is an ____.", "โยฮัน ไรน์ฮาร์ดเป็น ____", ["anthropologist", "astronaut", "athlete", "actor"]),
        Q("Which action protects history?", "การกระทำใดปกป้องประวัติศาสตร์", ["visiting a museum quietly", "writing on old walls", "taking stones from a site", "breaking pottery"]),
        Q("Where was the mummy in the photo on page 69 found?", "มัมมี่ในภาพหน้า 69 ถูกพบที่ไหน", ["Argentina", "Peru", "England", "China"]),
    ],
}

# ================================================================== 8. WRITING
writing = {
    "id": "writing", "title": T("Writing: Exemplification", "การเขียน: การยกตัวอย่าง"), "short": T("Writing", "การเขียน"), "pages": "Workbook p.55",
    "learn": [
        L("Learn", "Writing with examples", "การเขียนโดยยกตัวอย่าง", [
            ("In <b>exemplification writing</b>, you give examples to support your important ideas.", "การเขียนแบบยกตัวอย่าง คือ การยกตัวอย่างมาสนับสนุนความคิดสำคัญ"),
            ("Examples show the reader that you know what you are writing about.", "ตัวอย่างแสดงให้ผู้อ่านเห็นว่าเรารู้เรื่องที่เขียนจริง"),
        ], page="📒 p.55"),
        L("Words", "Words that introduce examples", "คำที่ใช้นำตัวอย่าง", [
        ], table=[["Expression", "ไทย"], ["for instance", "ตัวอย่างเช่น"], ["such as", "เช่น"], ["namely", "กล่าวคือ"], ["specifically", "โดยเฉพาะ"], ["a good example is", "ตัวอย่างที่ดีคือ"]],
          examples=[("Archaeologists find many things, <b>such as</b> pottery, coins and statues.", "นักโบราณคดีพบสิ่งของหลายอย่าง เช่น เครื่องปั้นดินเผา เหรียญ และรูปปั้น"),
                    ("<b>A good example is</b> the Iceman.", "ตัวอย่างที่ดีคือมนุษย์น้ำแข็ง")], page="📒 p.55"),
        L("Model", "Memories from the Past (short summary)", "Memories from the Past (สรุปสั้น ๆ)", [
            ("Read the full text in your workbook. 📒", "อ่านเนื้อเรื่องเต็มในแบบฝึกหัด 📒"),
            ("New discoveries tell us about the past. A good example is the Iceman, found in 1991 by hikers in the Alps.", "การค้นพบใหม่บอกเราเกี่ยวกับอดีต ตัวอย่างที่ดีคือมนุษย์น้ำแข็ง ที่นักเดินป่าพบในเทือกเขาแอลป์เมื่อปี 1991"),
            ("The Peruvian mummy also tells us a lot. For instance, she was probably 12 to 14 years old, and she had strong bones and great teeth.", "มัมมี่เปรูก็บอกเราได้มาก ตัวอย่างเช่น เธอน่าจะอายุ 12 ถึง 14 ปี และมีกระดูกแข็งแรงและฟันดี"),
        ], page="📒 p.55"),
        L("Plan", "Plan: The terra-cotta statues", "วางแผน: รูปปั้นดินเผา", [
            ("1. Main idea: The terra-cotta statues tell us a lot about the past.", "1. ใจความสำคัญ: รูปปั้นดินเผาบอกเราเกี่ยวกับอดีตได้มาก"),
            ("2. Example: For instance, there are more than 6,000 statues, such as soldiers, horses and acrobats.", "2. ตัวอย่าง: เช่น มีรูปปั้นมากกว่า 6,000 ตัว เช่น ทหาร ม้า และนักกายกรรม"),
            ("3. Example: Specifically, each statue has a different face.", "3. ตัวอย่าง: โดยเฉพาะ รูปปั้นแต่ละตัวมีใบหน้าไม่เหมือนกัน"),
            ("4. End: Say why the discovery is amazing.", "4. สรุป: บอกว่าทำไมการค้นพบนี้จึงน่าทึ่ง"),
        ], page="📒 p.55"),
    ],
    "wb": [
        X(EX(1, "Read.", "อ่าน"), 55, ("Read \"Memories from the Past.\" Underline all the expressions that refer to examples.", "อ่านเรื่อง Memories from the Past ขีดเส้นใต้คำที่ใช้นำตัวอย่างทั้งหมด"),
          ("A good example is · namely · For instance · Specifically", "A good example is · namely · For instance · Specifically"),
          hint=("There are 4 expressions. Look for the words in the list at the top of the page.", "มีทั้งหมด 4 คำ หาคำที่อยู่ในรายการด้านบนของหน้า")),
        X(EX(2, "Write in your notebook.", "เขียนลงในสมุด"), 55, ("Write about the terra-cotta statues. What does this discovery tell us about the past? Use examples.", "เขียนเกี่ยวกับรูปปั้นดินเผา การค้นพบนี้บอกอะไรเกี่ยวกับอดีต ใช้ตัวอย่าง"),
          ("The terra-cotta statues tell us a lot about the past. A good example is the army of soldiers. There are more than 6,000 statues, such as soldiers, horses and acrobats. Specifically, each statue has a different face. This tells us that the workers were very skilled.", "รูปปั้นดินเผาบอกเราเกี่ยวกับอดีตได้มาก ตัวอย่างที่ดีคือกองทัพทหาร มีรูปปั้นมากกว่า 6,000 ตัว เช่น ทหาร ม้า และนักกายกรรม โดยเฉพาะ รูปปั้นแต่ละตัวมีใบหน้าไม่เหมือนกัน แสดงว่าคนงานมีฝีมือมาก"), kind="open",
          hint=("Use the plan in Learn. Use at least two example words.", "ใช้แผนในส่วน Learn ใช้คำนำตัวอย่างอย่างน้อย 2 คำ")),
    ],
    "sort": {"title": T("Does it introduce an example?", "เป็นคำที่ใช้นำตัวอย่างไหม"),
             "bins": [T("Example word 💡", "คำนำตัวอย่าง 💡"), T("Not an example word", "ไม่ใช่คำนำตัวอย่าง")],
             "items": [["for instance", 0], ["such as", 0], ["namely", 0], ["specifically", 0], ["a good example is", 0],
                       ["suddenly", 1], ["afterward", 1], ["since then", 1], ["mummy", 1]]},
    "build": ["A good example | is | the | Iceman.", "Archaeologists find | many things, | such as | pottery and coins.", "For instance, | she was | probably 12 | years old.",
              "Specifically, | each statue | has a | different face."],
    "quiz": [
        Q("Which expression introduces an example?", "คำไหนใช้นำตัวอย่าง", ["for instance", "suddenly", "since then", "afterward"]),
        Q("Archaeologists find many things, ____ pottery and coins.", "นักโบราณคดีพบสิ่งของหลายอย่าง ____ เครื่องปั้นดินเผาและเหรียญ", ["such as", "because", "but", "so"]),
        Q("The Peruvian mummy was probably ____ years old.", "มัมมี่เปรูน่าจะอายุ ____ ปี", ["12 to 14", "20 to 25", "5 to 6", "40"]),
        Q("Exemplification writing uses ____.", "การเขียนแบบยกตัวอย่างใช้ ____", ["examples", "jokes", "songs", "questions only"]),
    ],
}

SECTIONS = [opener, vocab1, grammar1, vocab2, grammar2, song, reading, mission, writing]


def B(q, qth, options, why, whyth, src):
    return {"q": T(q, qth), "options": options, "why": T(why, whyth), "src": src}


BANK = [
    B("A person who studies old things to learn about the past is an ____.", "คนที่ศึกษาสิ่งของเก่าเพื่อเรียนรู้อดีตคือ ____", ["archaeologist", "astronaut", "athlete", "engineer"], "Archaeologists study the past.", "นักโบราณคดีศึกษาอดีต", "Vocabulary 1 · Book p.62"),
    B("Inside the tomb in China, there are more than 6,000 ____.", "ในสุสานที่จีนมี ____ มากกว่า 6,000 ตัว", ["statues", "mummies", "thieves", "samples"], "The tomb has soldier, dancer and horse statues.", "ในสุสานมีรูปปั้นทหาร นักเต้น และม้า", "Vocabulary 1 · Book p.62"),
    B("The female mummy was found in a tomb in ____.", "มัมมี่ผู้หญิงถูกพบในสุสานที่ ____", ["Peru", "China", "England", "Egypt"], "She was found in Peru.", "เธอถูกพบที่เปรู", "Vocabulary 1 · Book p.63"),
    B("The mummy had ____ of snakes and spiders.", "มัมมี่มี ____ รูปงูและแมงมุม", ["tattoos", "statues", "coins", "samples"], "Tattoos are pictures on the skin.", "รอยสักคือภาพบนผิวหนัง", "Vocabulary 1 · Book p.63"),
    B("In 2009, ____ was found in a field in England.", "ในปี 2009 พบ ____ ในทุ่งนาที่อังกฤษ", ["treasure", "a mummy", "a tomb", "a statue"], "Treasure with lots of gold was found.", "พบสมบัติที่มีทองคำจำนวนมาก", "Vocabulary 1 · Book p.63"),
    B("People who steal things are ____.", "คนที่ขโมยสิ่งของคือ ____", ["thieves", "thiefs", "archaeologists", "rulers"], "One thief, two thieves.", "thief หนึ่งคน thieves หลายคน", "Vocabulary 1 · Workbook p.48"),
    B("To dig carefully to find old things is to ____.", "ขุดอย่างระมัดระวังเพื่อหาสิ่งของเก่าคือ ____", ["excavate", "preserve", "analyze", "die"], "Archaeologists excavate sites.", "นักโบราณคดีขุดค้นแหล่งโบราณ", "Vocabulary 1 · Book p.62"),
    B("Which event happened before the common era?", "เหตุการณ์ใดเกิดขึ้นก่อนคริสตกาล", ["the statues in the Chinese tomb", "the female mummy in Peru", "the treasure in England", "the Iceman discovery"], "210 BCE is before the common era.", "210 ปีก่อนคริสตกาล อยู่ก่อนคริสต์ศักราช", "Vocabulary 1 · Workbook p.49"),
    B("The secret message on Workbook p.48 is: Learning about the past is ____!", "ข้อความลับในแบบฝึกหัดหน้า 48 คือ Learning about the past is ____!", ["fun", "old", "hard", "gold"], "F-U-N!", "F-U-N!", "Vocabulary 1 · Workbook p.48"),
    B("The Sphinx ____ built around 2500 BCE.", "สฟิงซ์ ____ สร้างขึ้นประมาณ 2500 ปีก่อนคริสตกาล", ["was", "were", "is", "did"], "One thing → was.", "หนึ่งสิ่ง → was", "Grammar 1 · Book p.64"),
    B("The statues ____ found in 1974.", "รูปปั้น ____ พบในปี 1974", ["were", "was", "are", "did"], "Many statues → were.", "รูปปั้นหลายตัว → were", "Grammar 1 · Book p.64"),
    B("We know when the objects were ____ there.", "เรารู้ว่าสิ่งของถูก ____ ไว้ที่นั่นเมื่อไร", ["buried", "buryed", "bury", "burying"], "bury → buried.", "bury → buried", "Grammar 1 · Book p.64"),
    B("Why ____ the gold hidden?", "ทำไมทองคำ ____ ถูกซ่อน", ["was", "were", "did", "is"], "Question: was + the gold + hidden.", "คำถาม: was + the gold + hidden", "Grammar 1 · Book p.64"),
    B("The jewelry was ____ last night.", "เครื่องประดับถูก ____ เมื่อคืน", ["stolen", "stole", "stealed", "steal"], "steal → stolen.", "steal → stolen", "Grammar 1 · Book p.64"),
    B("When were you ____?", "เธอ ____ เมื่อไร", ["born", "bear", "borned", "birth"], "We say: When were you born?", "เราพูดว่า When were you born?", "Grammar 1 · Workbook p.50"),
    B("A cat was found up a tree. The firefighters ____ called.", "พบแมวบนต้นไม้ นักดับเพลิง ____ ถูกเรียก", ["were", "was", "did", "are"], "Firefighters = many people → were.", "นักดับเพลิงหลายคน → were", "Grammar 1 · Workbook p.50"),
    B("The artifact ____ bought in a store.", "โบราณวัตถุ ____ ซื้อจากร้านค้า", ["wasn't", "weren't", "didn't", "don't"], "One artifact → wasn't.", "โบราณวัตถุหนึ่งชิ้น → wasn't", "Grammar 1 · Book p.64"),
    B("A place where archaeologists dig is a ____.", "สถานที่ที่นักโบราณคดีขุดคือ ____", ["site", "sample", "tattoo", "statue"], "A site is a place to excavate or explore.", "แหล่งขุดค้นคือที่ที่ขุดหรือสำรวจ", "Vocabulary 2 · Workbook p.51"),
    B("An object made by people long ago is an ____.", "สิ่งของที่คนในอดีตทำขึ้นคือ ____", ["artifact", "analyze", "earthquake", "astronaut"], "Artifacts are made by people.", "โบราณวัตถุทำโดยมนุษย์", "Vocabulary 2 · Workbook p.51"),
    B("They took a ____ of food from his stomach.", "พวกเขาเก็บ ____ อาหารจากกระเพาะของเขา", ["sample", "site", "statue", "tomb"], "A sample is a small amount to study.", "ตัวอย่างคือสิ่งของจำนวนเล็กน้อยที่นำไปศึกษา", "Vocabulary 2 · Book p.65"),
    B("To find a person's family, scientists do a ____.", "เพื่อหาครอบครัวของบุคคล นักวิทยาศาสตร์ทำ ____", ["DNA test", "site", "sample cake", "statue"], "A DNA test shows family.", "การตรวจดีเอ็นเอบอกเรื่องครอบครัว", "Vocabulary 2 · Book p.65"),
    B("Scientists ____ objects to learn how old they are.", "นักวิทยาศาสตร์ ____ สิ่งของเพื่อรู้ว่าเก่าแค่ไหน", ["analyze", "bury", "hide", "steal"], "Analyze = study carefully.", "analyze = ศึกษาอย่างละเอียด", "Vocabulary 2 · Workbook p.51"),
    B("The mummy was found ____ the hiker.", "มัมมี่ถูกพบ ____ นักเดินป่า", ["by", "of", "from", "at"], "by + the person who did it.", "by + ผู้กระทำ", "Grammar 2 · Book p.66"),
    B("In 1991, a mummy was discovered by ____.", "ในปี 1991 มัมมี่ถูกค้นพบโดย ____", ["hikers", "divers", "farmers", "thieves"], "Hikers found the Iceman.", "นักเดินป่าพบมนุษย์น้ำแข็ง", "Grammar 2 · Book p.66"),
    B("Samples of food were ____ from his stomach by scientists.", "ตัวอย่างอาหารถูก ____ จากกระเพาะโดยนักวิทยาศาสตร์", ["taken", "took", "take", "taked"], "take → taken.", "take → taken", "Grammar 2 · Book p.66"),
    B("Passive of \"The divers didn't find the bottles\":", "Passive ของ The divers didn't find the bottles:", ["The bottles weren't found by the divers.", "The bottles didn't found the divers.", "The divers weren't found the bottles.", "The bottles wasn't find by divers."], "were + not + found + by.", "were + not + found + by", "Grammar 2 · Book p.66"),
    B("Who was the Iceman ____ by?", "มนุษย์น้ำแข็งถูก ____ โดยใคร", ["found", "find", "finded", "finding"], "Who + was + subject + past participle + by?", "Who + was + ประธาน + กริยาช่องที่ 3 + by", "Grammar 2 · Workbook p.52"),
    B("In 1974, the terra-cotta army was found by Chinese ____.", "ในปี 1974 กองทัพดินเผาถูกพบโดย ____ ชาวจีน", ["farmers", "hikers", "divers", "astronauts"], "Farmers found it.", "ชาวนาเป็นผู้พบ", "Grammar 2 · Workbook p.52"),
    B("Originally, the statues were ____ in different colors.", "แต่เดิมรูปปั้นถูก ____ ด้วยสีต่าง ๆ", ["painted", "paint", "painting", "paints"], "paint → painted.", "paint → painted", "Grammar 2 · Workbook p.52"),
    B("Which word has the same sound as \"caught\"?", "คำไหนมีเสียงเหมือน caught", ["bought", "frown", "knew", "sew"], "bought and caught both have the aw sound.", "bought และ caught มีเสียง ออ", "Song · Book p.67"),
    B("Which word does NOT have the aw sound?", "คำไหนไม่มีเสียง ออ", ["drought", "draw", "saw", "astronaut"], "drought sounds like \"out\".", "drought ออกเสียงเหมือน out", "Song · Workbook p.53"),
    B("The Unit 6 song is called ____.", "เพลงในบทที่ 6 ชื่อ ____", ["So Much to Learn", "Extreme Sports", "Trash Is Treasure", "Lost City"], "The song is So Much to Learn.", "เพลงชื่อ So Much to Learn", "Song · Book p.67"),
    B("Who first told the story of Atlantis?", "ใครเล่าเรื่องแอตแลนติสเป็นคนแรก", ["Plato", "Johan Reinhard", "Qin Shihuang", "Paul Gostner"], "Plato told the story more than 2,000 years ago.", "เพลโตเล่าเรื่องนี้เมื่อกว่า 2,000 ปีก่อน", "Reading · Book p.68"),
    B("Atlantis was destroyed by fire and ____.", "แอตแลนติสถูกทำลายด้วยไฟและ ____", ["earthquakes", "floods of gold", "thieves", "snow"], "It was one terrible night of fire and earthquakes.", "เป็นคืนที่เลวร้ายด้วยไฟและแผ่นดินไหว", "Reading · Book p.68"),
    B("Most people think Atlantis ____.", "คนส่วนใหญ่คิดว่าแอตแลนติส ____", ["was never a real place", "is in England", "was found in 2009", "is under the ice"], "It's probably just a story.", "น่าจะเป็นแค่เรื่องเล่า", "Reading · Book p.68"),
    B("Garbologists study ____.", "นักขยะวิทยาศึกษา ____", ["trash", "bones", "DNA", "stars"], "Garbage = trash.", "garbage = ขยะ", "Reading · Workbook p.54"),
    B("\"Biodegradable trash decomposes quickly when it is buried.\" True or false?", "\"ขยะย่อยสลายได้ย่อยสลายเร็วเมื่อถูกฝัง\" จริงหรือเท็จ", ["False", "True", "Not in the text", "Both"], "It does not decompose as quickly as we thought.", "มันไม่ได้ย่อยสลายเร็วอย่างที่คิด", "Reading · Workbook p.54"),
    B("Johan Reinhard is an ____.", "โยฮัน ไรน์ฮาร์ดเป็น ____", ["anthropologist", "astronaut", "artist", "athlete"], "He studies people of the past.", "เขาศึกษามนุษย์ในอดีต", "Mission · Book p.69"),
    B("Which action helps protect local history?", "การกระทำใดช่วยปกป้องประวัติศาสตร์ท้องถิ่น", ["visiting a museum quietly", "writing on old walls", "taking stones from a site", "throwing trash"], "Respect old places.", "เคารพสถานที่เก่าแก่", "Mission · Book p.69"),
    B("Which expression introduces an example?", "คำไหนใช้นำตัวอย่าง", ["a good example is", "suddenly", "the next year", "afterward"], "It tells the reader an example is coming.", "บอกผู้อ่านว่ากำลังจะมีตัวอย่าง", "Writing · Workbook p.55"),
]

UNIT = {"unit": U, "title": "History's a Mystery", "pages": "Book p.60 to 69 · Workbook p.48 to 55", "sections": SECTIONS}

if __name__ == "__main__":
    check_all(UNIT, BANK, ROOT)
    out = os.path.join(ROOT, "content")
    json.dump(UNIT, open(os.path.join(out, f"unit{U}.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    json.dump({"questions": BANK}, open(os.path.join(out, f"bank{U}.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    json.dump(TH, open(os.path.join(out, f"th{U}.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    write_check_me(UNIT, U, os.path.join(out, "CHECK-ME.md"))
    n_ex = sum(len(s.get("book", [])) + len(s.get("wb", [])) for s in SECTIONS)
    print(f"Unit {U}: {len(SECTIONS)} lessons, {n_ex} book and workbook questions, {len(BANK)} test questions, {len(TH)} Thai lines. All checks passed ✅")
