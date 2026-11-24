
# P.6 English Communication Website (Explore Our World 6, Units 5 to 8): Project Rules

These rules apply in every session. Read them before doing anything.

## WHO I AM
Lawrence Jose (students call me T. Roy). I teach English Communication to class 6/1 only (about 26 students) in Thailand. Complete beginner with code. When I need to do something myself, give me simple steps, one at a time. Keep chat messages short.

## THE GOAL
A free website for my 6/1 students. Book: Explore Our World 6, 2nd edition (National Geographic Learning), Units 5 to 8, plus the Workbook. Students open one link on Mac, Windows, iPad or phone. No app, no password.

Units:
- Unit 5: Exciting Sports
- Unit 6: History's a Mystery
- Unit 7: Chocolate!
- Unit 8: Cool Vacations!
Also: Review pages, "Let's Talk" pages and the Irregular Verbs list.

## SOURCE FILES (never publish, never edit, never move)
The two PDFs in this folder must be kept out of the website by .gitignore.
- "explore our world 6 2e student book unit 5 to 8 .pdf" (the Student Book): 23 photos of book spreads (2 pages per photo). No text layer, so read it by looking at the pages.
- "explorer-our-world-2ed-6-workbook_compress.pdf" (the Workbook): the whole workbook (84 PDF pages). Units 5 to 8 are on PDF pages 42 to 77 (Unit 5 starts p.42, Unit 6 p.50, Unit 7 p.58, Unit 8 p.66). Grammar reference pages are near the end.
There is NO answer key. Every answer I (Codex) write for a workbook or book exercise must be listed in content/CHECK-ME.md with the unit, page and exercise, so T. Roy can check it. Never guess when the book is unclear: ask.

## COPYRIGHT AND PICTURES
- Never put photos, scans or crops of the book or workbook on the site.
- Never copy song lyrics. For songs, show only the song title, the key words and a "sing it in class" note.
- Reading passages: do not copy the whole text. Write a short summary in simple words, and the comprehension questions, with a 📖 page badge so students read the full text in their book.
- Exercise instructions and short sentences from exercises may be used, as on the maths site.
- Pictures: use Canva (connected) to make clean pictures for vocabulary words. Make them in the background: never show image previews in the chat (it makes the chat heavy). Export from Canva at 800 px, trim the white space, save small JPGs (about 30 to 80 KB) in img/unitX/.

## TECH RULES (same as the maths site)
- Plain HTML, CSS and JavaScript only. No frameworks, no build step. Free on GitHub Pages.
- All content in data files, one per unit (content/unit05.json and so on), built by Python scripts in tools/ that check the data.
- Fast on slow school wifi and phones. Pictures load only when needed.
- `<meta name="robots" content="noindex">` on every page.
- Bump the ?v= number in the HTML files after changing CSS or JS.

## REUSE FROM THE MATHS SITE
The maths site is in /Users/lawrencejose/Documents/P6-Math-Website (live: https://lawrenceroy1-lab.github.io/p6-maths/). Read its code and copy what works, adapting it:
- js/common.js: name picker with forgiving "Did you mean…?" for Thai students' nickname spellings, "Is this you?", teacher login (type "teacher" or "Lawrence", PIN checked by Google).
- js/thai.js + tools/build_thai.py: Thai under every English text, with a 🇹🇭 ไทย on/off switch, numbers checked.
- js/draw.js: smart-board pen ("✏️ Draw", "👆 Click page").
- js/unit.js patterns: tabs, numbered list on the right to jump to any card or question, Back and Next everywhere (except the Unit Test), progress ticks, answers hidden behind a "👀 Show answer" button.
- Class Battle and class games pages for the teacher's projector (see lesson7.html / js/lesson7.js).
- Leaderboard, Practice and Unit Test (see js/tests.js, leaderboard.html).

## STUDENTS, TEACHER AND SCORES (same Google Sheet as maths)
- Google Sheet ID 1Dexvm47MWauw4FAWitfSSsrZe-lKpU9YHeaSGvX9G_c. The "Students" tab has the class lists (A class, B no., C nickname, D shown name, E other spellings). This site uses class 6/1 only, so students only pick their name (no class step).
- Nicknames only. Never real names. Never type or store the teacher PIN (it lives in the sheet's Settings tab, cell B2).
- Scores: the Apps Script code is in the maths project at apps-script/Code.gs (v5). To add English, write a v6 that keeps maths working exactly as now and adds: a "subject" field; English rows go to a new "English Scores" tab; ?action=leaderboard&subject=English. Keep the SAME web app link (Deploy > Manage deployments > edit > New version). Save the v6 code in both projects and give T. Roy click-by-click steps.

## SITE STRUCTURE
Home page: one big card per unit (5, 6, 7, 8) plus Review / Let's Talk and Irregular Verbs.
Each unit has tabs for its book lessons, following the book in order:
Vocabulary 1, Grammar 1, Song, Vocabulary 2, Grammar 2, Reading, Value, Mission/Writing (check the actual book pages).
Activities (pick what fits each lesson):
1. VOCABULARY CARDS: picture (Canva) + word + Thai meaning + example sentence + 🔊 listen button (browser speech, English voice, slow and normal speed).
2. LISTEN AND SPELL: hear the word, type it, instant feedback.
3. GRAMMAR: one rule per card in simple English with Thai, examples with the key part coloured, then Guided Practice in book order: question first, 💡 Hint, steps, answer only after "👀 Show answer".
4. READING: short summary, key words, comprehension questions with Show answer, 📖 page badge.
5. WORKBOOK PRACTICE: every workbook exercise for the unit in page order, with hints and Show answer.
6. SPEAKING: model sentences with 🔊, "Your turn" prompts, optional speaking check with the browser microphone (only where the browser supports it; never record or store voices).
7. MATCH GAME, SPEED QUIZ (Kahoot style), FLASHCARDS (in order, Back/Next, list on the right).
8. CLASS BATTLE (teacher only, projector).
Plus per unit: Practice, Unit Test (to the sheet as "Unit Test"), Leaderboard.

## DESIGN RULES
- Big, bold, easy to read on projectors and phones (body text 20px+ on phones, 24px+ on computers).
- Fun for 11 to 12 year olds, clean, no clutter. Same colour system as maths: orange = question, yellow = hint, green = answer, blue = teaching, dark blue = titles.
- English names only in new examples (Lily, James, Emma, Tom, Sophie). Never Thai or Chinese names.
- Teacher name on the site: "T. Roy". No em dashes anywhere.

## ACCURACY RULES
- Follow the book's page order. Include every exercise from the Student Book and Workbook pages for Units 5 to 8.
- Correct, natural English. American spelling, as in the book.
- Every answer I write goes in content/CHECK-ME.md until T. Roy confirms it.
- Thai: simple, natural Thai for 11-year-olds. Tell T. Roy it should be checked by a Thai colleague.

## HOW WE WORK
- Build Unit 5 completely first and show it in the preview. Wait for feedback before Unit 6.
- Before changing or deleting any file T. Roy made, say which file and what change, and wait for OK.
- Keep messages short and light. No image previews in the chat. After each task, say exactly what changed.

## PUBLISHING
GitHub account lawrenceroy1-lab (gh CLI at /usr/local/bin/gh is logged in). Create a new repo "p6-english" and publish with GitHub Pages: https://lawrenceroy1-lab.github.io/p6-english/
When T. Roy says "publish my changes": bump ?v=, then git add, commit and push. Never commit the two book PDFs, AGENTS.md or this prompt file.
