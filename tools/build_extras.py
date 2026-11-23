"""Builds the Review and Let's Talk page (Book p.90 to 93) and the Irregular Verbs page (Book p.94).
Run: python3 tools/build_extras.py"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
import checks  # noqa: E402
from checks import T  # noqa: E402
from unitkit import Kit, L, X, Q, B, EX, S, sort  # noqa: E402

# ================================================================== REVIEW (p.90 to 91)
review = {
    "id": "review", "title": T("Review Units 5 to 8", "ทบทวนบทที่ 5 ถึง 8"), "short": T("Review", "ทบทวน"), "pages": "Book p.90 to 91",
    "learn": [
        L("Review", "What did we learn in Units 5 to 8?", "เราเรียนอะไรไปบ้างในบทที่ 5 ถึง 8", [], table=[
            ["Unit", "Grammar", "Example"],
            ["5", "present perfect + for / since", "I've had my bike for three years."],
            ["5", "so, very, really, extremely…", "That trick looks really dangerous."],
            ["6", "passive: was / were + past participle", "The statues were found in 1974."],
            ["6", "passive + by", "The mummy was found by hikers."],
            ["7", "past progressive + when", "I was drinking hot chocolate when I burned my hand."],
            ["7", "so that + could / would", "I printed the recipe so that I could read it."],
            ["8", "second conditional", "If I went on a safari, I would take photos."],
            ["8", "would rather … than …", "I'd rather go camping than stay at a hotel."]], page="📖 p.90"),
    ],
    "book": [
        X(EX(1, "Listen to the phone call.", "ฟังโทรศัพท์"), 90, ("Check the things that Carlos has done: learned to surf, fallen in the water a lot, surfed well, worn a life jacket, had an accident, been hang-gliding.", "เลือกสิ่งที่คาร์ลอสได้ทำไปแล้ว"), kind="class",
          classNote=("Do this in class with the audio (TR: 8.10).", "ทำในห้องเรียนพร้อมฟังเสียง (TR: 8.10)")),
        X(EX(2, "Listen again. Answer the questions.", "ฟังอีกครั้ง ตอบคำถาม"), 90, ("How long has Carlos been at the camp? (and 4 more questions)", "คาร์ลอสอยู่ที่แคมป์มานานเท่าไรแล้ว (และอีก 4 ข้อ)"), kind="class",
          classNote=("Do this in class with the audio (TR: 8.11). The example answer is \"for four days.\"", "ทำในห้องเรียนพร้อมฟังเสียง (TR: 8.11) ตัวอย่างคำตอบคือ \"for four days\"")),
        X(EX(3, "Discuss a vacation or camp that you enjoyed.", "คุยเรื่องการเที่ยวหรือค่ายที่ประทับใจ"), 90, ("Work with a partner. Ask and answer questions. Use the words in the box.", "ทำกับเพื่อน ถามและตอบ ใช้คำในกรอบ"),
          ("I went to the beach last year. It was totally awesome. · Really? What was the weather like?", "ฉันไปทะเลเมื่อปีที่แล้ว สนุกสุด ๆ · จริงเหรอ อากาศเป็นอย่างไร"), kind="open",
          box=["weather", "family", "city or country", "friends", "activities", "place where you stayed", "extremely", "so", "incredibly", "super", "really", "totally"]),
        X(EX(4, "Discuss.", "อภิปราย"), 90, ("Talk about your dream vacation. Use: if / would, would rather.", "พูดถึงการเที่ยวในฝัน ใช้ if / would และ would rather"),
          ("If I went on vacation, I would go on a photo safari! · No way! I would rather go to a theme park!", "ถ้าฉันไปเที่ยว ฉันจะไปซาฟารีถ่ายภาพ · ไม่เอา ฉันอยากไปสวนสนุกมากกว่า"), kind="open"),
        X(EX(5, "Look at the pictures. What were they doing?", "ดูภาพ พวกเขากำลังทำอะไร"), 91, ("1. At 3 p.m.,…", "1. ตอน 3 p.m.…"), ("d. Daniel was printing the recipe.", "d. แดเนียลกำลังพิมพ์สูตรอาหาร"),
          choices=["a", "b", "c", "d", "e", "f"], right=3, why=("This is the example in the book.", "ข้อนี้เป็นตัวอย่างในหนังสือ"), inst=("Draw lines.", "ลากเส้นจับคู่")),
        X(EX(5, "Look at the pictures. What were they doing?", "ดูภาพ พวกเขากำลังทำอะไร"), 91, ("2. At 3:10 p.m.,…", "2. ตอน 3:10 p.m.…"), ("a. Alex was putting the ingredients on the table.", "a. อเล็กซ์กำลังวางส่วนผสมบนโต๊ะ"),
          choices=["a", "b", "c", "d", "e", "f"], right=0, hint=("Picture 2: things on the table.", "ภาพที่ 2: ของบนโต๊ะ")),
        X(EX(5, "Look at the pictures. What were they doing?", "ดูภาพ พวกเขากำลังทำอะไร"), 91, ("3. At 3:15 p.m.,…", "3. ตอน 3:15 p.m.…"), ("e. the boys were putting cocoa powder into the blender.", "e. เด็กผู้ชายกำลังใส่ผงโกโก้ลงในเครื่องปั่น"),
          choices=["a", "b", "c", "d", "e", "f"], right=4),
        X(EX(5, "Look at the pictures. What were they doing?", "ดูภาพ พวกเขากำลังทำอะไร"), 91, ("4. At 3:20 p.m.,…", "4. ตอน 3:20 p.m.…"), ("f. they were putting cinnamon on the milkshakes.", "f. พวกเขากำลังโรยอบเชยบนมิลค์เชค"),
          choices=["a", "b", "c", "d", "e", "f"], right=5),
        X(EX(5, "Look at the pictures. What were they doing?", "ดูภาพ พวกเขากำลังทำอะไร"), 91, ("5. At 3:25 p.m.,…", "5. ตอน 3:25 p.m.…"), ("b. they were putting the milkshakes in the fridge.", "b. พวกเขากำลังนำมิลค์เชคเข้าตู้เย็น"),
          choices=["a", "b", "c", "d", "e", "f"], right=1),
        X(EX(5, "Look at the pictures. What were they doing?", "ดูภาพ พวกเขากำลังทำอะไร"), 91, ("6. At 3:40 p.m.,…", "6. ตอน 3:40 p.m.…"), ("c. the boys' sister was taking their milkshakes!", "c. พี่สาวของเด็ก ๆ กำลังเอามิลค์เชคไป"),
          choices=["a", "b", "c", "d", "e", "f"], right=2),
        X(EX(6, "Ask and answer questions.", "ถามและตอบ"), 91, ("Where / the Sphinx / build?", "ที่ไหน / สฟิงซ์ / สร้าง"), ("Where was the Sphinx built? It was built in Egypt.", "สฟิงซ์ถูกสร้างที่ไหน ถูกสร้างที่อียิปต์"),
          inst=("Work with a partner. Take notes.", "ทำกับเพื่อน จดบันทึก"), why=("The question is the example in the book. The Sphinx is in Egypt.", "คำถามเป็นตัวอย่างในหนังสือ สฟิงซ์อยู่ที่อียิปต์")),
        X(EX(6, "Ask and answer questions.", "ถามและตอบ"), 91, ("How many / terra-cotta statues / make?", "กี่ตัว / รูปปั้นดินเผา / สร้าง"), ("How many terra-cotta statues were made? Thousands. More than 6,000 were discovered.", "รูปปั้นดินเผาถูกสร้างกี่ตัว หลายพันตัว ค้นพบแล้วมากกว่า 6,000 ตัว"),
          hint=("Remember Unit 6, page 62.", "นึกถึงบทที่ 6 หน้า 62")),
        X(EX(6, "Ask and answer questions.", "ถามและตอบ"), 91, ("Who / the objects with the English gold / discover / by?", "ใคร / สิ่งของกับทองคำในอังกฤษ / ค้นพบ / โดย"),
          ("Who were the objects with the English gold discovered by? They were discovered by archaeologists.", "สิ่งของกับทองคำในอังกฤษถูกค้นพบโดยใคร ถูกค้นพบโดยนักโบราณคดี"), hint=("Remember Unit 6, page 63.", "นึกถึงบทที่ 6 หน้า 63")),
        X(EX(7, "Listen to the answers.", "ฟังคำตอบ"), 91, ("Win a point for each correct answer!", "ได้หนึ่งคะแนนต่อหนึ่งคำตอบที่ถูก"), kind="class",
          classNote=("Do this in class with the audio (TR: 8.12).", "ทำในห้องเรียนพร้อมฟังเสียง (TR: 8.12)")),
        X(EX(8, "Write.", "เขียน"), 91, ("Work in small groups. Create a brochure for a weekend trip. Use words in the box.", "ทำเป็นกลุ่มเล็ก สร้างแผ่นพับสำหรับการเที่ยวสุดสัปดาห์ ใช้คำในกรอบ"),
          ("Weekend Camping Trip! Sleep in a tent by the river. Go on a tour with a guide and see the ruins. Bring sunglasses and relax in nature. Buy your ticket today!",
           "ทริปตั้งแคมป์สุดสัปดาห์ นอนเต็นท์ริมแม่น้ำ ไปทัวร์กับไกด์ชมซากโบราณ นำแว่นกันแดดไปและผ่อนคลายในธรรมชาติ ซื้อตั๋ววันนี้"), kind="open",
          box=["camping", "guide", "site", "relax", "suitcase", "tent", "ticket", "environment", "passport", "natural", "ruins", "sunglasses", "theme park", "tour"]),
    ],
    "speak": S([("I went to the beach last year. It was totally awesome.", "ฉันไปทะเลเมื่อปีที่แล้ว สนุกสุด ๆ"), ("Really? What was the weather like?", "จริงเหรอ อากาศเป็นอย่างไร"),
                ("If I went on vacation, I would go on a photo safari!", "ถ้าฉันไปเที่ยว ฉันจะไปซาฟารีถ่ายภาพ"), ("No way! I would rather go to a theme park!", "ไม่เอา ฉันอยากไปสวนสนุกมากกว่า")],
               [("Tell about a vacation you enjoyed.", "เล่าเรื่องการเที่ยวที่ประทับใจ", "Last year, I went to… It was…", "ปีที่แล้ว ฉันไป… มัน…", "Last year, I went to Chiang Mai. It was really cool!", "ปีที่แล้ว ฉันไปเชียงใหม่ อากาศเย็นสบายมาก"),
                ("What is your dream vacation?", "การเที่ยวในฝันของนักเรียนคืออะไร", "If I could go anywhere, I would…", "ถ้าไปได้ทุกที่ ฉันจะ…", "If I could go anywhere, I would go to Japan and see the snow.", "ถ้าไปได้ทุกที่ ฉันจะไปญี่ปุ่นและดูหิมะ")]),
    "sort": sort(("Which unit's grammar is it?", "เป็นไวยากรณ์ของบทไหน"), [("Unit 5", "บทที่ 5"), ("Unit 6", "บทที่ 6"), ("Unit 7", "บทที่ 7"), ("Unit 8", "บทที่ 8")],
                 [["I've lived here for ten years.", 0], ["It's totally cool!", 0], ["The statues were found in 1974.", 1], ["The mummy was found by hikers.", 1],
                  ["I was sleeping when the phone rang.", 2], ["I took an umbrella so that I wouldn't get wet.", 2], ["If I had money, I would travel.", 3], ["I'd rather swim than hike.", 3]]),
    "build": ["I've had | my bike | for | three years.", "The treasure | was found | by | farmers.", "I was cooking | when | the cat | jumped in.",
              "If I went | to the beach, | I would | swim.", "I'd rather | go camping | than | stay home."],
    "quiz": [
        Q("I've lived here ____ 2018.", "ฉันอยู่ที่นี่ ____ ปี 2018", ["since", "for", "at", "by"]),
        Q("The statues ____ found by farmers.", "รูปปั้น ____ พบโดยชาวนา", ["were", "was", "are", "did"]),
        Q("I ____ cooking when the phone rang.", "ฉัน ____ ทำอาหารตอนที่โทรศัพท์ดัง", ["was", "were", "am", "did"]),
        Q("I printed the recipe so that I ____ read it.", "ฉันพิมพ์สูตรอาหารเพื่อที่จะ ____ อ่านได้", ["could", "can", "will", "am"]),
        Q("If I ____ rich, I would travel.", "ถ้าฉัน ____ รวย ฉันจะเดินทาง", ["were", "am", "be", "will be"]),
        Q("I'd rather swim ____ hike.", "ฉันอยากว่ายน้ำ ____ เดินป่า", ["than", "or", "then", "and"]),
        Q("That trick looks ____ dangerous.", "ท่านั้นดู ____ อันตราย", ["extremely", "extreme", "extremes", "more extreme"]),
        Q("At 3 p.m., Daniel was ____ the recipe.", "ตอนบ่ายสาม แดเนียลกำลัง ____ สูตรอาหาร", ["printing", "print", "printed", "prints"]),
        Q("Where was the Sphinx built?", "สฟิงซ์ถูกสร้างที่ไหน", ["in Egypt", "in China", "in Peru", "in England"]),
        Q("Who was the Iceman found by?", "มนุษย์น้ำแข็งถูกพบโดยใคร", ["hikers", "farmers", "divers", "thieves"]),
    ],
}

# ================================================================== LET'S TALK 1: I love it! (p.92)
talk1 = {
    "id": "talk1", "title": T("Let's Talk: I love it!", "มาคุยกัน: ฉันชอบมาก"), "short": T("Let's Talk 1", "มาคุยกัน 1"), "pages": "Book p.92",
    "learn": [
        L("Goals", "I will…", "ฉันจะ…", [("💬 start a conversation", "💬 เริ่มต้นบทสนทนา"), ("🔀 change the topic", "🔀 เปลี่ยนเรื่อง"),
                                       ("↩️ bring the topic back on track", "↩️ พากลับมาเรื่องเดิม"), ("👍👎 discuss likes and dislikes", "👍👎 พูดถึงสิ่งที่ชอบและไม่ชอบ")], page="📖 p.92"),
        L("Phrases", "Useful phrases", "สำนวนที่มีประโยชน์", [], table=[
            ["Start", "Change the topic", "Likes and dislikes", "Back on track"],
            ["Is everyone ready?", "By the way,…", "What's it like?", "Anyway,…"],
            ["Ready?", "Hey!", "What's it about?", "Back to…"],
            ["Let's start.", "Before I forget,…", "I love it! / I hate it.", "Look,…"]], page="📖 p.92"),
        L("Model", "The conversation (short summary)", "บทสนทนา (สรุปสั้น ๆ)", [
            ("Read the full conversation in your book. 📖", "อ่านบทสนทนาฉบับเต็มในหนังสือ 📖"),
            ("Three boys are ready to play a history game. One boy changes the topic: <b>By the way</b>, have you seen the new shark movie?", "เด็กผู้ชายสามคนพร้อมเล่นเกมประวัติศาสตร์ คนหนึ่งเปลี่ยนเรื่อง: By the way, เคยดูหนังฉลามเรื่องใหม่ไหม"),
            ("They talk about the movie: <b>What's it like?</b> It's awesome. <b>I love it.</b>", "พวกเขาคุยเรื่องหนัง: What's it like? It's awesome. I love it."),
            ("Then one boy brings them back: <b>Anyway</b>, let's talk about it later. <b>Back to</b> the game.", "แล้วอีกคนพากลับมา: Anyway, let's talk about it later. Back to the game."),
        ], page="📖 p.92"),
    ],
    "book": [
        X(EX(1, "Listen and read.", "ฟังและอ่าน"), 92, ("Listen to the conversation and read it in your book.", "ฟังบทสนทนาและอ่านตามในหนังสือ"), kind="class",
          classNote=("Do this in class with the audio (TR: 8.13).", "ทำในห้องเรียนพร้อมฟังเสียง (TR: 8.13)")),
        X(EX(2, "Read and say.", "อ่านและพูด"), 92, ("Work in groups of three. Have a conversation. Use the chart. Take turns. Change the subject to something else.", "ทำเป็นกลุ่มสามคน สนทนาโดยใช้ตาราง ผลัดกันพูด เปลี่ยนไปพูดเรื่องอื่น"),
          ("Is everyone ready to do our science project? · Yes! · Hey, before I forget, have you tried the new ice cream shop? · No. What's it like? · I love it! · Anyway, back to the project.",
           "ทุกคนพร้อมทำโครงงานวิทยาศาสตร์ไหม · พร้อม · เดี๋ยวก่อนลืม เคยลองร้านไอศกรีมใหม่ไหม · ยัง เป็นอย่างไร · ชอบมาก · เอาละ กลับมาที่โครงงาน"), kind="open"),
    ],
    "speak": S([("Is everyone ready to play the game?", "ทุกคนพร้อมเล่นเกมไหม"), ("By the way, have you seen the new shark movie?", "ว่าแต่ เคยดูหนังฉลามเรื่องใหม่ไหม"),
                ("No, I haven't. What's it like?", "ยังเลย เป็นอย่างไรบ้าง"), ("It's awesome. I love it.", "สุดยอด ฉันชอบมาก"), ("Anyway, let's talk about it later. Back to the game.", "เอาละ ไว้คุยทีหลัง กลับมาเล่นเกมกัน")],
               [("Start a conversation with your group.", "เริ่มต้นบทสนทนากับกลุ่ม", "Is everyone ready to…?", "ทุกคนพร้อม… ไหม", "Is everyone ready to start our English project?", "ทุกคนพร้อมเริ่มโครงงานภาษาอังกฤษไหม"),
                ("Change the topic.", "เปลี่ยนเรื่อง", "By the way,…", "ว่าแต่…", "By the way, have you played the new soccer game?", "ว่าแต่ เคยเล่นเกมฟุตบอลใหม่ไหม"),
                ("Bring the topic back.", "พากลับมาเรื่องเดิม", "Anyway, back to…", "เอาละ กลับมาที่…", "Anyway, back to our project.", "เอาละ กลับมาที่โครงงานของเรา")]),
    "sort": sort(("What does the phrase do?", "สำนวนนี้ใช้ทำอะไร"), [("Start 💬", "เริ่ม 💬"), ("Change the topic 🔀", "เปลี่ยนเรื่อง 🔀"), ("Back on track ↩️", "กลับเรื่องเดิม ↩️")],
                 [["Is everyone ready?", 0], ["Let's start.", 0], ["Ready?", 0], ["By the way,…", 1], ["Before I forget,…", 1], ["Hey!", 1], ["Anyway,…", 2], ["Back to the game.", 2], ["Look,…", 2]]),
    "match": [["What's it like?", "It's awesome."], ["What's it about?", "It's about a shark."], ["Is everyone ready?", "Yes, let's start!"], ["Do you like it?", "I love it!"],
              ["By the way,…", "change the topic"], ["Anyway, back to…", "back on track"]],
    "build": ["Is | everyone ready | to play | the game?", "By the way, | have you seen | the new | shark movie?", "Anyway, | let's talk | about it | later."],
    "quiz": [
        Q("Which phrase changes the topic?", "สำนวนไหนใช้เปลี่ยนเรื่อง", ["By the way,…", "Back to the game.", "Let's start.", "Anyway,…"]),
        Q("Which phrase brings the topic back?", "สำนวนไหนใช้พากลับมาเรื่องเดิม", ["Anyway, back to…", "By the way,…", "Before I forget,…", "Hey!"]),
        Q("A: What's it like? B: ____", "A: What's it like? B: ____", ["It's awesome. I love it.", "Yes, I'm ready.", "By the way.", "Back to the game."]),
        Q("Which phrase starts a conversation?", "สำนวนไหนใช้เริ่มบทสนทนา", ["Is everyone ready?", "Anyway,…", "I hate it.", "Look,…"]),
    ],
}

# ================================================================== LET'S TALK 2: Excuse me. (p.93)
talk2 = {
    "id": "talk2", "title": T("Let's Talk: Excuse me.", "มาคุยกัน: ขอโทษนะคะ/ครับ"), "short": T("Let's Talk 2", "มาคุยกัน 2"), "pages": "Book p.93",
    "learn": [
        L("Goals", "I will…", "ฉันจะ…", [("❓ ask for clarification", "❓ ขอคำอธิบายเพิ่ม"), ("🤔 express doubt", "🤔 แสดงความไม่แน่ใจ"), ("🙋 interrupt politely", "🙋 ขัดจังหวะอย่างสุภาพ")], page="📖 p.93"),
        L("Phrases", "Useful phrases", "สำนวนที่มีประโยชน์", [], table=[
            ["I missed it", "I'm not sure", "Interrupt politely", "Ask again", "Answer"],
            ["Hey, what did ___ say?", "I think she said ___, but I'm not sure.", "Excuse me, ___.", "Could you repeat that?", "Sure. I'll go over it again."],
            ["I didn't catch that.", "Let's check.", "Could I ask a question, please?", "Could you say / explain that again?", "No problem! I'll explain it again."],
            ["I missed that.", "", "", "", "Of course!"]], page="📖 p.93"),
        L("Model", "The conversation (short summary)", "บทสนทนา (สรุปสั้น ๆ)", [
            ("Read the full conversation in your book. 📖", "อ่านบทสนทนาฉบับเต็มในหนังสือ 📖"),
            ("Two students missed what the teacher said. One thinks they have to match pictures and sentences, <b>but I'm not sure</b>.", "นักเรียนสองคนไม่ได้ยินที่ครูพูด คนหนึ่งคิดว่าต้องจับคู่ภาพกับประโยค แต่ไม่แน่ใจ"),
            ("So they ask politely: <b>Excuse me</b>, Ms. Trujillo. <b>Could you repeat that?</b> The teacher says: <b>Sure. I'll go over it again.</b>", "จึงถามอย่างสุภาพ: Excuse me, Ms. Trujillo. Could you repeat that? ครูตอบว่า: Sure. I'll go over it again."),
        ], page="📖 p.93"),
    ],
    "book": [
        X(EX(3, "Listen and read.", "ฟังและอ่าน"), 93, ("Listen to the conversation and read it in your book.", "ฟังบทสนทนาและอ่านตามในหนังสือ"), kind="class",
          classNote=("Do this in class with the audio (TR: 8.14).", "ทำในห้องเรียนพร้อมฟังเสียง (TR: 8.14)")),
        X(EX(4, "Listen.", "ฟัง"), 93, ("You will hear two discussions. Circle the answers.", "ฟังการสนทนาสองเรื่อง วงกลมคำตอบ"), kind="class",
          classNote=("Do this in class with the audio (TR: 8.15).", "ทำในห้องเรียนพร้อมฟังเสียง (TR: 8.15)")),
        X(EX(5, "Read and discuss.", "อ่านและอภิปราย"), 93, ("Situation 1: Your teacher is going over the answers. You missed the last answer.", "สถานการณ์ที่ 1: ครูกำลังเฉลยคำตอบ นักเรียนไม่ได้ยินข้อสุดท้าย"),
          ("Hey, what did she say? I missed that. · I think she said \"b,\" but I'm not sure. · Excuse me, T. Roy. Could you repeat the last answer? · Sure. I'll go over it again.",
           "เมื่อกี้ครูพูดว่าอะไร ฉันไม่ได้ยิน · คิดว่า b แต่ไม่แน่ใจ · ขอโทษค่ะ/ครับครูรอย ช่วยพูดคำตอบข้อสุดท้ายอีกครั้งได้ไหม · ได้ เดี๋ยวครูทวนให้"), kind="open",
          inst=("Work in groups of three. Choose a situation and discuss.", "ทำเป็นกลุ่มสามคน เลือกสถานการณ์แล้วสนทนา")),
        X(EX(5, "Read and discuss.", "อ่านและอภิปราย"), 93, ("Situation 2: Your teacher is explaining tonight's homework. You didn't quite understand.", "สถานการณ์ที่ 2: ครูกำลังอธิบายการบ้านคืนนี้ นักเรียนไม่ค่อยเข้าใจ"),
          ("Excuse me, could I ask a question, please? Could you explain the homework again? · No problem! I'll explain it again.", "ขอโทษค่ะ/ครับ ขอถามหน่อยได้ไหม ช่วยอธิบายการบ้านอีกครั้งได้ไหม · ได้เลย เดี๋ยวครูอธิบายอีกครั้ง"), kind="open"),
    ],
    "speak": S([("Hey, what did she say?", "เมื่อกี้เธอพูดว่าอะไร"), ("I think she said we have to match the pictures and sentences, but I'm not sure.", "คิดว่าเธอบอกให้จับคู่ภาพกับประโยค แต่ไม่แน่ใจ"),
                ("I missed it, too. Let's ask her.", "ฉันก็ไม่ได้ยิน ไปถามกันเถอะ"), ("Excuse me. Could you repeat that?", "ขอโทษนะคะ/ครับ ช่วยพูดอีกครั้งได้ไหม"), ("Sure. I'll go over it again.", "ได้เลย เดี๋ยวทวนให้อีกครั้ง")],
               [("You didn't hear the teacher. Ask politely.", "นักเรียนไม่ได้ยินครู ถามอย่างสุภาพ", "Excuse me, could you…?", "ขอโทษค่ะ/ครับ ช่วย… ได้ไหม", "Excuse me, T. Roy. Could you say that again, please?", "ขอโทษค่ะ/ครับครูรอย ช่วยพูดอีกครั้งได้ไหม"),
                ("Your friend asks: What did he say? You aren't sure.", "เพื่อนถามว่าเขาพูดว่าอะไร นักเรียนไม่แน่ใจ", "I think he said…, but I'm not sure.", "คิดว่าเขาพูดว่า… แต่ไม่แน่ใจ", "I think he said page 50, but I'm not sure.", "คิดว่าเขาบอกหน้า 50 แต่ไม่แน่ใจ")]),
    "sort": sort(("What does the phrase do?", "สำนวนนี้ใช้ทำอะไร"), [("I missed it 🙉", "ไม่ได้ยิน 🙉"), ("I'm not sure 🤔", "ไม่แน่ใจ 🤔"), ("Ask politely 🙋", "ถามอย่างสุภาพ 🙋")],
                 [["I didn't catch that.", 0], ["I missed that.", 0], ["What did she say?", 0], ["…but I'm not sure.", 1], ["Let's check.", 1],
                  ["Excuse me,…", 2], ["Could you repeat that?", 2], ["Could I ask a question, please?", 2]]),
    "match": [["Could you repeat that?", "Sure. I'll go over it again."], ["Could you explain that again?", "No problem!"], ["What did she say?", "I didn't catch that."],
              ["Could I ask a question, please?", "Of course!"], ["Excuse me,…", "interrupt politely"], ["…but I'm not sure.", "express doubt"]],
    "build": ["Excuse me. | Could you | repeat | that?", "I think | she said page 50, | but | I'm not sure.", "Sure. | I'll go over | it | again."],
    "quiz": [
        Q("You didn't hear the teacher. What do you say?", "นักเรียนไม่ได้ยินครู ควรพูดว่าอะไร", ["Excuse me. Could you repeat that?", "Back to the game.", "I love it!", "By the way."]),
        Q("Which phrase shows doubt?", "สำนวนไหนแสดงความไม่แน่ใจ", ["…but I'm not sure.", "Of course!", "I love it.", "Let's start."]),
        Q("A: Could you explain that again? B: ____", "A: Could you explain that again? B: ____", ["No problem! I'll explain it again.", "I missed that.", "Anyway.", "I hate it."]),
        Q("\"I didn't catch that\" means ____.", "\"I didn't catch that\" หมายความว่า ____", ["I didn't hear it.", "I dropped the ball.", "I'm hungry.", "I agree."]),
    ],
}

RK = Kit("review", {})
REVIEW_BANK = [
    B("I've had my bike ____ three years.", "ฉันมีจักรยานมา ____ สามปี", ["for", "since", "at", "ago"], "Three years is a period of time.", "สามปีเป็นช่วงเวลา", "Review · Unit 5"),
    B("Skateboarding is ____ cool.", "สเก็ตบอร์ด ____ เจ๋ง", ["really", "real", "reals", "more real"], "Adverb before the adjective.", "คำวิเศษณ์อยู่หน้าคำคุณศัพท์", "Review · Unit 5"),
    B("The treasure ____ discovered in a field.", "สมบัติ ____ ค้นพบในทุ่งนา", ["was", "were", "is", "did"], "One thing → was.", "หนึ่งสิ่ง → was", "Review · Unit 6"),
    B("The Iceman was found ____ hikers.", "มนุษย์น้ำแข็งถูกพบ ____ นักเดินป่า", ["by", "from", "of", "with"], "by + who did it.", "by + ผู้กระทำ", "Review · Unit 6"),
    B("At 3 p.m., Daniel ____ printing the recipe.", "ตอนบ่ายสาม แดเนียล ____ พิมพ์สูตรอาหาร", ["was", "were", "is", "did"], "Daniel → was.", "Daniel → was", "Review · Book p.91"),
    B("They were putting the milkshakes in the ____.", "พวกเขากำลังนำมิลค์เชคเข้า ____", ["fridge", "blender", "oven", "bag"], "That's at 3:25 p.m.", "นั่นคือตอน 3:25 p.m.", "Review · Book p.91"),
    B("We used a blender so that we ____ mix quickly.", "เราใช้เครื่องปั่นเพื่อจะ ____ ผสมได้เร็ว", ["could", "can", "will", "are"], "so that + could.", "so that + could", "Review · Unit 7"),
    B("If I went on vacation, I ____ go on a photo safari.", "ถ้าฉันไปเที่ยว ฉัน ____ ไปซาฟารีถ่ายภาพ", ["would", "will", "am", "did"], "Second conditional: would + verb.", "Second Conditional: would + กริยา", "Review · Book p.90"),
    B("I would rather go to a theme park ____ go camping.", "ฉันอยากไปสวนสนุก ____ ไปตั้งแคมป์", ["than", "or", "then", "and"], "would rather … than …", "would rather … than …", "Review · Unit 8"),
    B("Where was the Sphinx built?", "สฟิงซ์ถูกสร้างที่ไหน", ["in Egypt", "in China", "in Mexico", "in Peru"], "The Sphinx is in Egypt.", "สฟิงซ์อยู่ที่อียิปต์", "Review · Book p.91"),
    B("Which phrase changes the topic?", "สำนวนไหนใช้เปลี่ยนเรื่อง", ["By the way,…", "Back to the game.", "Is everyone ready?", "Let's start."], "By the way introduces a new topic.", "By the way ใช้เริ่มเรื่องใหม่", "Let's Talk · Book p.92"),
    B("Which phrase brings the topic back?", "สำนวนไหนพากลับมาเรื่องเดิม", ["Anyway, back to…", "Hey!", "Before I forget,…", "What's it like?"], "Anyway brings the talk back.", "Anyway พาบทสนทนากลับมา", "Let's Talk · Book p.92"),
    B("A: What's it like? B: ____", "A: What's it like? B: ____", ["It's awesome.", "Yes, please.", "I'm ten.", "By the way."], "Say what you think of it.", "บอกว่าคิดอย่างไร", "Let's Talk · Book p.92"),
    B("You didn't hear the teacher. Say: \"Excuse me. ____\"", "ไม่ได้ยินครู พูดว่า \"Excuse me. ____\"", ["Could you repeat that?", "I love it.", "Anyway.", "Let's start."], "Ask politely to hear it again.", "ขออย่างสุภาพให้พูดอีกครั้ง", "Let's Talk · Book p.93"),
    B("\"I think she said page 50, but I'm not ____.\"", "\"คิดว่าเธอบอกหน้า 50 แต่ไม่ ____\"", ["sure", "ready", "late", "hungry"], "I'm not sure = doubt.", "I'm not sure = ไม่แน่ใจ", "Let's Talk · Book p.93"),
    B("A: Could you explain that again? B: ____", "A: Could you explain that again? B: ____", ["No problem! I'll explain it again.", "I hate it.", "I missed it.", "Back to the game."], "Answer politely: Sure / No problem.", "ตอบอย่างสุภาพ: Sure / No problem", "Let's Talk · Book p.93"),
]

# ================================================================== IRREGULAR VERBS (p.94)
VERBS = """be was/were been|beat beat beaten|become became become|begin began begun|bend bent bent|bite bit bitten|bleed bled bled|blow blew blown|break broke broken|bring brought brought|build built built|buy bought bought|catch caught caught|choose chose chosen|come came come|cost cost cost|cut cut cut|dig dug dug|do did done|draw drew drawn|drink drank drunk|drive drove driven|eat ate eaten|fall fell fallen|feed fed fed|feel felt felt|fight fought fought|find found found|fly flew flown|forget forgot forgotten|forgive forgave forgiven|freeze froze frozen|get got gotten|give gave given|go went gone|grow grew grown|hang hung hung|have had had|hear heard heard|hide hid hidden|hit hit hit|hold held held|hurt hurt hurt|keep kept kept|know knew known|leave left left|lend lent lent|let let let|lie lay lain|light lit lit|lose lost lost|make made made|meet met met|pay paid paid|put put put|read read read|ride rode ridden|ring rang rung|rise rose risen|run ran run|say said said|see saw seen|sell sold sold|send sent sent|set set set|sew sewed sewn|shake shook shaken|shine shone shone|show showed shown|shut shut shut|sing sang sung|sink sank sunk|sit sat sat|sleep slept slept|slide slid slid|speak spoke spoken|spend spent spent|spin spun spun|stand stood stood|steal stole stolen|stick stuck stuck|sting stung stung|stink stank stunk|sweep swept swept|swim swam swum|swing swung swung|take took taken|teach taught taught|tear tore torn|tell told told|think thought thought|throw threw thrown|understand understood understood|wake up woke up woken up|wear wore worn|win won won|write wrote written"""
TH_V = {"be": "เป็น อยู่ คือ", "beat": "ตี ชนะ", "become": "กลายเป็น", "begin": "เริ่ม", "bend": "งอ", "bite": "กัด", "bleed": "เลือดออก", "blow": "เป่า พัด", "break": "ทำแตก หัก",
        "bring": "นำมา", "build": "สร้าง", "buy": "ซื้อ", "catch": "จับ", "choose": "เลือก", "come": "มา", "cost": "มีราคา", "cut": "ตัด", "dig": "ขุด", "do": "ทำ", "draw": "วาด",
        "drink": "ดื่ม", "drive": "ขับ", "eat": "กิน", "fall": "ตก ล้ม", "feed": "ให้อาหาร", "feel": "รู้สึก", "fight": "ต่อสู้", "find": "พบ หา", "fly": "บิน", "forget": "ลืม",
        "forgive": "ให้อภัย", "freeze": "แข็งตัว", "get": "ได้รับ", "give": "ให้", "go": "ไป", "grow": "เติบโต ปลูก", "hang": "แขวน", "have": "มี", "hear": "ได้ยิน", "hide": "ซ่อน",
        "hit": "ตี ชน", "hold": "ถือ", "hurt": "ทำให้เจ็บ", "keep": "เก็บ", "know": "รู้", "leave": "ออกจาก ทิ้งไว้", "lend": "ให้ยืม", "let": "ปล่อยให้", "lie": "นอนลง", "light": "จุดไฟ",
        "lose": "ทำหาย แพ้", "make": "ทำ สร้าง", "meet": "พบ", "pay": "จ่าย", "put": "วาง", "read": "อ่าน", "ride": "ขี่", "ring": "(กริ่ง) ดัง", "rise": "ขึ้น", "run": "วิ่ง",
        "say": "พูด", "see": "เห็น", "sell": "ขาย", "send": "ส่ง", "set": "ตั้ง วาง", "sew": "เย็บ", "shake": "เขย่า", "shine": "ส่องแสง", "show": "แสดง", "shut": "ปิด",
        "sing": "ร้องเพลง", "sink": "จม", "sit": "นั่ง", "sleep": "นอนหลับ", "slide": "ลื่น ไถล", "speak": "พูด", "spend": "ใช้ (เงิน เวลา)", "spin": "หมุน", "stand": "ยืน",
        "steal": "ขโมย", "stick": "ติด แปะ", "sting": "ต่อย (แมลง)", "stink": "เหม็น", "sweep": "กวาด", "swim": "ว่ายน้ำ", "swing": "แกว่ง", "take": "เอาไป ถ่าย (รูป)",
        "teach": "สอน", "tear": "ฉีก", "tell": "บอก เล่า", "think": "คิด", "throw": "ขว้าง โยน", "understand": "เข้าใจ", "wake up": "ตื่น", "wear": "สวมใส่", "win": "ชนะ", "write": "เขียน"}
rows = []
for item in VERBS.split("|"):
    parts = item.split()
    if parts[0] == "wake":
        rows.append(("wake up", "woke up", "woken up"))
    else:
        rows.append(tuple(parts))
assert all(r[0] in TH_V for r in rows), [r for r in rows if r[0] not in TH_V]

GROUPS = [("a", "b"), ("c", "e"), ("f", "g"), ("h", "m"), ("p", "s"), ("t", "w")]
GROUP_TH = {"a": "ก", "c": "ข", "f": "ค", "h": "ง", "p": "จ", "t": "ฉ"}
verb_sections = []
rnd = random.Random(7)
for a, z in GROUPS:
    vs = [r for r in rows if a <= r[0][0] <= z]
    name = f"Verbs {a.upper()} to {z.upper()}"
    sec = {"id": f"verbs-{a}", "title": T(f"Irregular verbs: {a.upper()} to {z.upper()}", f"กริยาอปกติ: {a.upper()} ถึง {z.upper()}"), "short": T(name, f"กริยา {a.upper()} ถึง {z.upper()}"), "pages": "Book p.94"}
    table = [["Verb", "Simple past", "Past participle", "ไทย"]] + [[f"<b>{v}</b>", p, pp, TH_V[v]] for v, p, pp in vs]
    sec["learn"] = [L("Verbs", f"{name}: all forms", f"{name}: ทุกรูป", [
        ("Simple past: for finished actions (Yesterday I <b>went</b>…).", "Simple past: ใช้กับการกระทำที่จบแล้ว (Yesterday I went…)"),
        ("Past participle: for the present perfect and the passive (I have <b>gone</b>…, It was <b>found</b>…).", "Past participle: ใช้กับ Present Perfect และ Passive (I have gone…, It was found…)")],
        table=table, page="📖 p.94")]
    sec["flash"] = [{"front": T(f"{v} → ?", f"{v} ({TH_V[v]}) → ?"), "back": T(f"{v} · {p} · {pp}", f"{v} · {p} · {pp}")} for v, p, pp in vs]
    sec["match"] = [[v, p] for v, p, pp in vs]
    sec["spell"] = [{"w": p.split("/")[0], "th": f"{v} (past)"} for v, p, pp in vs if p != v]
    quiz = []
    for v, p, pp in vs:
        others = [r[1] for r in rows if r[1] != p]
        quiz.append(Q(f"The simple past of \"{v}\" is ____.", f"กริยาช่องที่ 2 ของ {v} คือ ____", [p] + rnd.sample(others, 3)))
        if pp != p:
            others = [r[2] for r in rows if r[2] != pp]
            quiz.append(Q(f"The past participle of \"{v}\" is ____.", f"กริยาช่องที่ 3 ของ {v} คือ ____", [pp] + rnd.sample(others, 3)))
    sec["quiz"] = quiz
    sec["sort"] = sort(("Is it the simple past or the past participle?", "เป็น simple past หรือ past participle"), [("Simple past (2)", "ช่องที่ 2"), ("Past participle (3)", "ช่องที่ 3")],
                       [[p, 0] for v, p, pp in vs if p != pp][:6] + [[pp, 1] for v, p, pp in vs if p != pp][:6]) if sum(1 for r in vs if r[1] != r[2]) >= 3 else None
    if not sec["sort"]:
        del sec["sort"]
    verb_sections.append(sec)

VK = Kit("verbs", {})
VERB_BANK = []
for v, p, pp in rows:
    others = [r[1] for r in rows if r[1] != p]
    VERB_BANK.append(B(f"The simple past of \"{v}\" is ____.", f"กริยาช่องที่ 2 ของ {v} คือ ____", [p] + rnd.sample(others, 3), f"{v} → {p} → {pp}", f"{v} → {p} → {pp}", "Irregular Verbs · Book p.94"))
    if pp != p:
        others = [r[2] for r in rows if r[2] != pp]
        VERB_BANK.append(B(f"The past participle of \"{v}\" is ____.", f"กริยาช่องที่ 3 ของ {v} คือ ____", [pp] + rnd.sample(others, 3), f"{v} → {p} → {pp}", f"{v} → {p} → {pp}", "Irregular Verbs · Book p.94"))

if __name__ == "__main__":
    RK.build("Review and Let's Talk", "Book p.90 to 93", [review, talk1, talk2], REVIEW_BANK)
    VK.build("Irregular Verbs", "Book p.94", verb_sections, VERB_BANK)
