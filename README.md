# Yes, you KANJI! - CS50x 2022 Final Project
### Video Demo:  https://www.youtube.com/watch?v=LDyY9wfDZpc

## **1. About "Yes, you KANJI!"**

### **1.1. What is "Yes, you KANJI!"?**

"Yes, you Kanji!" (hereafter shortened to YYK) is a web application that enables the user to study and review how to read (and write) Japanese language. It focuses on teaching the contents of the Japanese Language Proficiency Test (JLPT) up to the highest level (N1). YYK consists of several parts. The initial explanation of the Japanese writing system (in case the user is a new learner of Japanese), the learning and reviewing of the Japanese syllabaries (hiragana and katakana), the learning and reviewing of kanji (Chinese characters that make up most of the words in Japanese), the learning and reviewing of radicals (smaller parts of kanji that are used to divide them in different groups), the learning and reviewing of vocabulary and a sort of dictionary to browse all of it at any time.

YYK has a study and a review function, that will gradually show the user new content and review old content, until the user has finished studying all that they need to read (and write) Japanese more proficiently, and pass the test, if so desired. Users need to create an account in order to keep track of their study progress. YYK uses the [SuperMemo 2](https://www.supermemo.com/en/archives1990-2015/english/ol/sm2) method to help users study and review content.

### **1.2. How did the idea for YYK come about?**

The idea for YYK was born out of the desire to create a single app that contains all information needed to learn how to read Japanese up to the level that is most important for most learners of Japanese, and present that information in an easy to understand order and format. I have studied Japanese for about 14 years, but most actively in the past 5 years. In order to get up to speed on the aforementioned proficiency test, I had to use a lot of resources to get the required study information, then gather everything and format it myself to use in various flash card applications and so on. While the studying itself certainly takes up the most time, just getting everything ready took a not insignificant amount of that time. YYK is basically the application I wish I had when I started studying Japanese from scratch 5 years ago.

### **1.3. What does YYK do exactly?**

One of the basic functionalities of YYK lies in the relations between radicals, kanji and words. YYK draws it's Japanese data from a single database (more on that in a dedicated section below), that is queried in different ways to always see relevant information. For example, if the user selects a radical, YYK will display all kanji that are in that radicals group. If the user then selects a kanji, YYK will display all words that contain that kanji. The same will work the other way around, once a word is selected, YYK will display all kanji within that word. If a kanji is selected, YYK will also show the radical it belongs to. One of the goals of this application was to have all the relevant data for studying always just a few clicks away.

However, the dictionary functionality is just a minor part of the application.

In order to reach JLPT N1 proficiency, the user has to learn 2387 kanji and about 14000+ words. YYK has a study function to show the user new kanji and their related words, and a review function to repeat content the user has already studied. For this to work, the user needs to create an account. The user can then set their own study goals. The amount of new kanji and new words per each session can be set by the user. For every session, YYK will then present the set amount of new kanji and new words. Only words that contain kanji the user has already studied will be presented. If the amount of new words that can be studied with the currently known kanji exceeds the limit set by the user, new kanji study is paused until the user has caught up with the word study. A study session is fairly straightforward, the user is presented with new content twice. On the second viewing, the user can decide to view this content again or to mark it as learned for the day. The user can view the content as often as they like, until it is marked learned. The [SuperMemo 2](https://www.supermemo.com/en/archives1990-2015/english/ol/sm2) method specifies, that new content first viewed is to be reviewed the following day, so everything that is studied in this way will enter the review queue for the next day.

Review sessions are structured a bit differently.

For each content to be reviewed in a review session, the user will first be presented with a mostly blank card. Only the radical or kanji or word itself is presented. The user can take their time to see if they can remember the other information, such as reading, meaning, etc. Once the user pushes the "Reveal" button, all information will be displayed. The user can then decide how hard it was for them to recall the information. The [SuperMemo 2](https://www.supermemo.com/en/archives1990-2015/english/ol/sm2) method suggests to rank the quality of the answer from 0 to 5, where 0 is forgotten and 5 is a perfect answer. Depending on the users answer, the content will be reviewed again at a different time. In general, the higher the quality, the less reviews. YYK uses the SM-2 algorithm to calculate the time of the next review for each reviewed item.

Because of the way this algorithm works, it is more important to review as often as possible, than it is to study as often as possible.

## **2. About the creation of the app**

### **2.1. What did I initially expect before starting to work on YYK?**

Before I started to create the actual application, I imagined how things would most likely go. I considered that, in order to connect all the different study content together, I would most likely have to create my own database to draw from. At the time I did not know what to expect from it. I didn't know if I would have to enter all data in some sort of csv by myself, or if there was another way to do it. Relatively early I started thinking about SQL queries and what would be helpful to know. I quickly realized that the SQL I had learned thus far in CS50 may be insufficient and that I would have to learn more about SQL in order to code this app.

### **2.2. What did I initially want to do? What did I end up doing?**

Initially I considered creating an android app, as that was one of the suggestions for a final project. I had already found a tutorial on how to start developing android apps, and I also installed the IDE for it, but then I realized, that many things, that needed to be done in order to make everything work, were not entirely clear to me yet. So I figured, I could just work on it as a python flask app at first, and then switch to android once I was comfortable with the SQL queries and the way the data was handled. During creation however, I realized that it was already a way bigger project than I had anticipated, so I settled on the flask app instead. The database was not yet created, so that was the first step.

Some progress can be seen in two other videos I uploaded to show my friends.

https://www.youtube.com/watch?v=Kr8Qw_erNC4

https://www.youtube.com/watch?v=H66DwuY1Bjo

## **3. About dictionary.db - The database creation**

### **3.1. Structure of the database**

The database structure of dictionary.db changed multiple times over the course of developing YYK, but the general idea has remained the same. The database was supposed to have tables for radicals, kanji and vocabulary and link them together so related data can be accessed easiy. (i.e. kanji related to a specific radical can be easily shown)

Once I started working on it, I quickly realized that I needed to make an entirely seperate python app to create the database. That way, whenever I wanted something to change, I could just alter the app and create a new database with the desired changes. I started making KanjiDB, with its app createDB.py. Now, when createDB.py is run, it uses different input files to create the dictionary.db.

### **3.2. Creation of KanjiDB/createDB.py**

#### **3.2.1. Schema**

The database is currently created using the following schema.

<details>
  <summary>Schema</summary>

```SQL
CREATE TABLE kana (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, type TEXT NOT NULL, kana TEXT NOT NULL, romaji TEXT NOT NULL, subtype TEXT NOT NULL, number INTEGER NOT NULL)
CREATE TABLE radicals (id INTEGER PRIMARY KEY NOT NULL, radical TEXT NOT NULL, title TEXT NOT NULL, name TEXT NOT NULL, english TEXT NOT NULL, radical_group TEXT NOT NULL, strokecount INTEGER NOT NULL, unicode TEXT NOT NULL)
CREATE TABLE kanji (id INTEGER PRIMARY KEY NOT NULL, kanji TEXT NOT NULL, unicode TEXT NOT NULL, onyomi TEXT, kunyomi TEXT, meaning TEXT, radical_id INTEGER NOT NULL, strokecount INTEGER NOT NULL, grade INTEGER NOT NULL, jlpt INTEGER, FOREIGN KEY (radical_id) REFERENCES radicals(id))
CREATE TABLE strokeorder (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, svg_black TEXT NOT NULL, svg_color TEXT NOT NULL, svg_strokes TEXT NOT NULL, kanji_unicode TEXT NOT NULL, FOREIGN KEY (kanji_unicode) REFERENCES kanji(unicode))
CREATE TABLE vocabulary (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, word TEXT NOT NULL, reading TEXT, meaning TEXT, type TEXT, jlpt INTEGER, category TEXT)
```

</details>

At first, only the tables radicals, kanji and vocabulary existed. I added strokeorder and kana when I realized I wanted/needed them for a better app.

#### **3.2.2. Kanji data**

Considering how I could implement kanji, I looked online if there was some data to be found. Luckily, [The KANJIDIC Project](http://www.edrdg.org/wiki/index.php/KANJIDIC_Project) had a dictionary of thousands of kanji with all kinds of relevant data readily available, under a license I could use for YYK. Unfortunately, this came in a massive XML file, with all kinds of kanji and information I didn't need. So I started looking how to process XML, and I found out about [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). With a lot of trial and error I managed to process the XML file, extract only the kanji I wanted and get the right information to then store in the database. One big advantage was that the xml file also containted the unicode information for every kanji, which helped immensely with adding more data later on.

<details>
  <summary>Kanji code</summary>

```PY
with open("input/kanjidic2.xml", "r") as dic:
    raw = dic.read()

data = BeautifulSoup(raw, "xml")
characters = data.find_all("character")

kanji_dic = []
no = 0
grade_check = 0
jlpt_check = 0
progress = 0
max = len(characters) - 1

# Process all characters
for character in characters:
    kanji = {}
    literal = character.find("literal")
    radical = character.find("rad_value", {"rad_type": "classical"})
    grade = character.find("grade")
    strokes = character.find("stroke_count")
    jlpt = character.find("jlpt")
    unicodetmp = character.find("cp_value", {"cp_type": "ucs"})
    on = character.find_all("reading", {"r_type": "ja_on"})
    kun = character.find_all("reading", {"r_type": "ja_kun"})
    meaning = character.find_all(lambda tag: tag.name == "meaning" and not tag.attrs)
    if not grade == None:
        grade_check = grade.get_text()
    else:
        grade_check = 0
    if not jlpt == None:
        jlpt_check = jlpt.get_text()
    else:
        jlpt_check = 0

    # Only process characters that either have a Grade from 1 to 9 or a JLPT level from 1 to 5
    if int(grade_check) in range(1, 9) or int(jlpt_check) in range(1, 6):

        no = no + 1

        # Check for valid unicode (for some reason some entries in the XML had different styling, throwing off the process)
        if not len(unicodetmp.get_text()) == 5:
            input_unicode = "0" + unicodetmp.get_text()
        else:
            input_unicode = unicodetmp.get_text()
        input_unicode = input_unicode.lower()

        # Check for valid Grade and JLPT
        if not grade == None:
            input_grade = grade.get_text()
        else:
            input_grade = ""
        if not jlpt == None:
            input_jlpt = jlpt.get_text()
        else:
            input_jlpt = 0

        # Add everything to a temporary dictionary
        kanji = {"No": no, "Kanji": literal.get_text(), "Unicode": input_unicode, "ON": onkun_check(on), "KUN": onkun_check(
            kun), "Meaning": print_meaning(meaning), "Radical": radical.get_text(), "Strokes": strokes.get_text(), "Grade": input_grade, "JLPT": input_jlpt}
        kanji_dic.append(kanji)

# Sort the dictionary by Grade, Radical and Strokes
sorted_dic = sorted(kanji_dic, key=lambda y: (int(y["Grade"]), int(y["Radical"]), int(y["Strokes"])))

# Add the ID number for each Kanji based on the prior sorting
for i in range(len(sorted_dic)):
    sorted_dic[i].update({"No": (i + 1)})

# Write Kanji to the database
for i in range(len(sorted_dic)):

    cursor.execute("INSERT INTO kanji (id, kanji, unicode, onyomi, kunyomi, meaning, radical_id, strokecount, grade, jlpt) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (int(sorted_dic[i]["No"]), sorted_dic[i]["Kanji"], sorted_dic[i]["Unicode"], sorted_dic[i]["ON"], sorted_dic[i]["KUN"], sorted_dic[i]["Meaning"], int(sorted_dic[i]["Radical"]), int(sorted_dic[i]["Strokes"]), int(sorted_dic[i]["Grade"]), int(sorted_dic[i]["JLPT"])))

cursor.execute("UPDATE kanji SET grade = 7 WHERE grade = 8")
cursor.execute("UPDATE kanji SET grade = 8 WHERE grade = 9")
```

</details>

#### **3.2.3. Vocabulary data**

When looking for a way to find vocabulary data to use for the database, I quickly found this [app](https://github.com/coolmule0/JLPT-N5-N1-Japanese-Vocabulary-Anki) on github. It takes data from [jisho.org](https://jisho.org/), a well known Japanese-English dictionary site. As all the data involved can be used with the right licenses, I downloaded the app and used it to pull the data. In the process I had to install things like pip and panda to make it work. In the end, I had trouble using the data just as csv, so I created the actual [Anki](https://ankiweb.net) decks and exported the data manually. (Anki was a huge inspiration for YYK) Thus I created my own vocabulary csv file to use as input for the database app. I ran into some trouble with trailing \n so I added another column that is not being used in the creation of the database. As I already formatted the csv for my use, adding the vocabulary data to the database was trivial.

<details>
  <summary>Vocabulary code</summary>

```PY
# Write vocabulary to database
vocabulary = []
vocab = open("input/vocabulary.txt", "r")
rows = (line.split("\t") for line in vocab)
for row in rows:
    word = {"Expression": row[0], "Reading": row[2], "Meaning": row[1], "Type": row[3], "JLPT": row[4], "Category": row[5]}
    vocabulary.append(word)
vocab.close()

counter = 0
for i in range(len(vocabulary)):

    counter = counter + 1
    cursor.execute("INSERT INTO vocabulary (id, word, reading, meaning, type, jlpt, category) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (counter, vocabulary[i]["Expression"], vocabulary[i]["Reading"], vocabulary[i]["Meaning"], vocabulary[i]["Type"], vocabulary[i]["JLPT"], vocabulary[i]["Category"]))

# Give words that use advanced kanji not in the learning list a special designation
cursor.execute("UPDATE vocabulary SET category = 'advanced_kanji' WHERE category = 'kanji' AND NOT EXISTS (SELECT kanji FROM kanji WHERE vocabulary.word LIKE '%' || kanji.kanji || '%')")
```

</details>

### **3.2.4. Radical data**

When trying to get radical data from the previously used xml, I quickly ran into problems with availabilty. For some reason not all the data I wanted was available, so I ended up using my own records of radicals, accumulated over years of studying Japanese, and created the input file manually. Most of it was previously written down into my own notes from various Japanese sources.

<details>
  <summary>Radical code</summary>

  ```PY
# Write radicals to database
radicals = []
counter = 1
rads = open("input/radicals.txt", "r")
rows = (line.split("\t") for line in rads)

# Store radicals in temporary dictionary and append it to the radicals list
for row in rows:
    radical = {"Radical": row[0], "Title": row[1], "Number": counter, "Name": row[2], "English": row[3],
    "Group": row[4], "Strokes": row[5], "Unicode": row[6]}
    radicals.append(radical)
    counter = counter + 1

# Write the list to the database
for i in range(len(radicals)):
    cursor.execute("INSERT INTO radicals (id, radical, title, name, english, radical_group, strokecount, unicode) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                             (int(radicals[i]["Number"]), radicals[i]["Radical"], radicals[i]["Title"], radicals[i]["Name"], radicals[i]["English"], radicals[i]["Group"], radicals[i]["Strokes"], radicals[i]["Unicode"]))
```

</details>

#### **3.2.5. Strokeorder data**

I quickly realized that just showing a Chinese character would not help much to learn how to write them. Kanji have a specific order in which the strokes are written, and there are some fonts and other ways to display that information. While looking for a way to best implement this into my database, I found out about [KanjiVG](https://kanjivg.tagaini.net/). They had created SVG files for how to write kanji, stroke by stroke, and stored them in a database under each kanji's unicode. Since I already had unicode data, it was easy to go through their database and pull only the data I needed. However, stroke counts (the order of the strokes) were missing from that database, so I ended up using the actual svg files as input for my database. I would have liked to use a single file as input, but could not reproduce how they created their own database. I experimented with adding svg data to an html page with jinja and figured that I could store the raw data in a separate SQL table. I also figured out how to alter the svg data, so I could use different colors for each stroke (as the original color was just black), something that is often done when showing stroke orders. One thing that was important to me, was that the color coding be easily visible for people with different kinds of color blindness. [This article](https://davidmathlogic.com/colorblind/) mentioning [this paper](https://www.nature.com/articles/nmeth.1618) helped in my decision for the most appropriate color coding.

<details>
  <summary>Strokeorder code</summary>

```PY
progress = 0
max = len(sorted_dic)
# Color coding for color blindness, as suggested by Wong
COLOR = ["#000000","#E69F00","#56B4E9","#009E73","#F0E442","#0072B2","#D55E00","#CC79A7"]
for i in range(len(sorted_dic)):
    svg = "input/svg/" + sorted_dic[i]["Unicode"] + ".svg"
    with open(svg, "r") as data:
        raw = data.read()
    data = BeautifulSoup(raw, "xml")

    paths = data.find("g", {"id": "kvg:StrokePaths_" + sorted_dic[i]["Unicode"]})
    path = paths.find_all("path")

    # Create black and color paths
    count = 0
    output_black = ""
    output_color = ""
    for j in path:
        string = str(j)
        string = string[:-2]
        style_color = "style=\"fill:none;stroke:" + COLOR[count] + ";stroke-width:3;stroke-linecap:round;stroke-linejoin:round;\"/>"
        style_black = "style=\"fill:none;stroke:#000000;stroke-width:3;stroke-linecap:round;stroke-linejoin:round;\"/>"
        color = string + style_color
        black = string + style_black
        output_color = output_color + color
        output_black = output_black + black
        count = count + 1
        if count == 8:
            count = 0

        strokes = data.find("g", {"id": "kvg:StrokeNumbers_" + sorted_dic[i]["Unicode"]})

    cursor.execute("INSERT INTO strokeorder (svg_black, svg_color, svg_strokes, kanji_unicode) VALUES (?, ?, ?, ?)", (str(output_black), str(output_color), str(strokes), sorted_dic[i]["Unicode"]))
```

</details>

#### **3.2.6. Kana data**

After some consideration, I figured I wanted to add kana information for people new to Japanese, as reading kana is basically the first step to reading Japanese and basically a requirement for learning kanji efficiently. Since there are not that many symbols, I decided to manually input them into the createDB.py app.

<details>
  <summary>Kana code</summary>

```PY
# Write hiragana to database
mono = [
    [["0", "あ", "a"], ["1", "い", "i"], ["2", "う", "u"], ["3", "え", "e"], ["4", "お", "o"]],
    [["5", "か", "ka"], ["6", "き", "ki"], ["7", "く", "ku"], ["8", "け", "ke"], ["9", "こ", "ko"]],
    [["10", "さ", "sa"], ["11", "し", "shi"], ["12", "す", "su"], ["13", "せ", "se"], ["14", "そ", "so"]],
    [["15", "た", "ta"], ["16", "ち", "chi"], ["17", "つ", "tsu"], ["18", "て", "te"], ["19", "と", "to"]],
    [["20", "な", "na"], ["21", "に", "ni"], ["22", "ぬ", "nu"], ["23", "ね", "ne"], ["24", "の", "no"]],
    [["25", "は", "ha"], ["26", "ひ", "hi"], ["27", "ふ", "fu"], ["28", "へ", "he"], ["29", "ほ", "ho"]],
    [["30", "ま", "ma"], ["31", "み", "mi"], ["32", "む", "mu"], ["33", "め", "me"], ["34", "も", "mo"]],
    [["35", "や", "ya"], ["0", "0", "0"], ["36", "ゆ", "yu"], ["0", "0", "0"], ["37", "よ", "yo"]],
    [["38", "ら", "ra"], ["39", "り", "ri"], ["40", "る", "ru"], ["41", "れ", "re"], ["42", "ろ", "ro"]],
    [["43", "わ", "wa"], ["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"], ["44", "を", "wo"]],
    [["0", "0", "0"], ["0", "0", "0"], ["45", "ん", "n"], ["0", "0", "0"], ["0", "0", "0"]]
    ]

di = [
    [["46", "きゃ", "kya"], ["47", "きゅ", "kyu"], ["48", "きょ", "kyo"]],
    [["49", "しゃ", "sha"], ["50", "しゅ", "shu"], ["51", "しょ", "sho"]],
    [["52", "ちゃ", "cha"], ["53", "ちゅ", "chu"], ["54", "ちょ", "cho"]],
    [["55", "にゃ", "nya"], ["56", "にゅ", "nyu"], ["57", "にょ", "nyo"]],
    [["58", "ひゃ", "hya"], ["59", "ひゅ", "hyu"], ["60", "ひょ", "hyo"]],
    [["61", "みゃ", "mya"], ["62", "みゅ", "myu"], ["63", "みょ", "myo"]],
    [["64", "りゃ", "rya"], ["65", "りゅ", "ryu"], ["66", "りょ", "ryo"]]
    ]

monodia = [
    [["67", "が", "ga"], ["68", "ぎ", "gi"], ["69", "ぐ", "gu"], ["70", "げ", "ge"], ["71", "ご", "go"]],
    [["72", "ざ", "za"], ["73", "じ", "ji"], ["74", "ず", "zu"], ["75", "ぜ", "ze"], ["76", "ぞ", "zo"]],
    [["77", "だ", "da"], ["78", "ぢ", "ji"], ["79", "づ", "zu"], ["80", "で", "de"], ["81", "ど", "do"]],
    [["82", "ば", "ba"], ["83", "び", "bi"], ["84", "ぶ", "bu"], ["85", "べ", "be"], ["86", "ぼ", "bo"]],
    [["87", "ぱ", "pa"], ["88", "ぴ", "pi"], ["89", "ぷ", "pu"], ["90", "ぺ", "pe"], ["91", "ぽ", "po"]]
    ]

didia = [
    [["92", "ぎゃ", "gya"], ["93", "ぎゅ", "gyu"], ["94", "ぎょ", "gyo"]],
    [["95", "じゃ", "ja"], ["96", "じゅ", "ju"], ["97", "じょ", "jo"]],
    [["98", "ぢゃ", "ja"], ["99", "ぢゅ", "ju"], ["100", "ぢょ", "jo"]],
    [["101", "びゃ", "bya"], ["102", "びゅ", "byu"], ["103", "びょ", "byo"]],
    [["104", "ぴゃ", "pya"], ["105", "ぴゅ", "pyu"], ["106", "ぴょ", "pyo"]]
    ]

for rows in mono:
    for data in rows:
        cursor.execute("INSERT INTO kana (type, kana, romaji, subtype, number) VALUES ('hiragana', ?, ?, 'monograph', ?)", (data[1], data[2], data[0]))
for rows in di:
    for data in rows:
        cursor.execute("INSERT INTO kana (type, kana, romaji, subtype, number) VALUES ('hiragana', ?, ?, 'digraph', ?)", (data[1], data[2], data[0]))
for rows in monodia:
    for data in rows:
        cursor.execute("INSERT INTO kana (type, kana, romaji, subtype, number) VALUES ('hiragana', ?, ?, 'monograph diacritic', ?)", (data[1], data[2], data[0]))
for rows in didia:
    for data in rows:
        cursor.execute("INSERT INTO kana (type, kana, romaji, subtype, number) VALUES ('hiragana', ?, ?, 'digraph diacritic', ?)", (data[1], data[2], data[0]))

# Write katakana to database
mono = [
    [["0", "ア", "a"], ["1", "イ", "i"], ["2", "ウ", "u"], ["3", "エ", "e"], ["4", "オ", "o"]],
    [["5", "カ", "ka"], ["6", "キ", "ki"], ["7", "ク", "ku"], ["8", "ケ", "ke"], ["9", "コ", "ko"]],
    [["10", "サ", "sa"], ["11", "シ", "shi"], ["12", "ス", "su"], ["13", "セ", "se"], ["14", "ソ", "so"]],
    [["15", "タ", "ta"], ["16", "チ", "chi"], ["17", "ツ", "tsu"], ["18", "テ", "te"], ["19", "ト", "to"]],
    [["20", "ナ", "na"], ["21", "ニ", "ni"], ["22", "ヌ", "nu"], ["23", "ネ", "ne"], ["24", "ノ", "no"]],
    [["25", "ハ", "ha"], ["26", "ヒ", "hi"], ["27", "フ", "fu"], ["28", "ヘ", "he"], ["29", "ホ", "ho"]],
    [["30", "マ", "ma"], ["31", "ミ", "mi"], ["32", "ム", "mu"], ["33", "メ", "me"], ["34", "モ", "mo"]],
    [["35", "ヤ", "ya"], ["0", "0", "0"], ["36", "ユ", "yu"], ["0", "0", "0"], ["37", "ヨ", "yo"]],
    [["38", "ラ", "ra"], ["39", "リ", "ri"], ["40", "ル", "ru"], ["41", "レ", "re"], ["42", "ロ", "ro"]],
    [["43", "ワ", "wa"], ["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"], ["44", "ヲ", "wo"]],
    [["0", "0", "0"], ["0", "0", "0"], ["45", "ン", "n"], ["0", "0", "0"], ["0", "0", "0"]]
    ]

di = [
    [["46", "キャ", "kya"], ["47", "キュ", "kyu"], ["48", "キョ", "kyo"]],
    [["49", "シャ", "sha"], ["50", "シュ", "shu"], ["51", "ショ", "sho"]],
    [["52", "チャ", "cha"], ["53", "チュ", "chu"], ["54", "チョ", "cho"]],
    [["55", "ニャ", "nya"], ["56", "ニュ", "nyu"], ["57", "ニョ", "nyo"]],
    [["58", "ヒャ", "hya"], ["59", "ヒュ", "hyu"], ["60", "ヒョ", "hyo"]],
    [["61", "ミャ", "mya"], ["62", "ミュ", "myu"], ["63", "ミョ", "myo"]],
    [["64", "リャ", "rya"], ["65", "リュ", "ryu"], ["66", "リョ", "ryo"]]
    ]

monodia = [
    [["67", "ガ", "ga"], ["68", "ギ", "gi"], ["69", "グ", "gu"], ["70", "ゲ", "ge"], ["71", "ゴ", "go"]],
    [["72", "ザ", "za"], ["73", "ジ", "ji"], ["74", "ズ", "zu"], ["75", "ゼ", "ze"], ["76", "ゾ", "zo"]],
    [["77", "ダ", "da"], ["78", "ヂ", "ji"], ["79", "ヅ", "zu"], ["80", "デ", "de"], ["81", "ド", "do"]],
    [["82", "バ", "ba"], ["83", "ビ", "bi"], ["84", "ブ", "bu"], ["85", "ベ", "be"], ["86", "ボ", "bo"]],
    [["87", "パ", "pa"], ["88", "ピ", "pi"], ["89", "プ", "pu"], ["90", "ペ", "pe"], ["91", "ポ", "po"]]
    ]

didia = [
    [["92", "ギャ", "gya"], ["93", "ギュ", "gyu"], ["94", "ギョ", "gyo"]],
    [["95", "ジャ", "ja"], ["96", "ジュ", "ju"], ["97", "ジョ", "jo"]],
    [["98", "ヂャ", "ja"], ["99", "ヂュ", "ju"], ["100", "ヂョ", "jo"]],
    [["101", "ビャ", "bya"], ["102", "ビュ", "byu"], ["103", "ビョ", "byo"]],
    [["104", "ピャ", "pya"], ["105", "ピュ", "pyu"], ["106", "ピョ", "pyo"]]
    ]

for rows in mono:
    for data in rows:
        cursor.execute("INSERT INTO kana (type, kana, romaji, subtype, number) VALUES ('katakana', ?, ?, 'monograph', ?)", (data[1], data[2], data[0]))
for rows in di:
    for data in rows:
        cursor.execute("INSERT INTO kana (type, kana, romaji, subtype, number) VALUES ('katakana', ?, ?, 'digraph', ?)", (data[1], data[2], data[0]))
for rows in monodia:
    for data in rows:
        cursor.execute("INSERT INTO kana (type, kana, romaji, subtype, number) VALUES ('katakana', ?, ?, 'monograph diacritic', ?)", (data[1], data[2], data[0]))
for rows in didia:
    for data in rows:
        cursor.execute("INSERT INTO kana (type, kana, romaji, subtype, number) VALUES ('katakana', ?, ?, 'digraph diacritic', ?)", (data[1], data[2], data[0]))
```

</details>

## **4. About users.db**

### **4.1. Structure of the database**

Users.db is the database used to store user data. Of course it stores the username, id and hash used for login, but it also stores the users last study and review session dates, as well as the users session settings. It also has a study table in which each piece of content that is studied by each user gets its own entry. With this, YYK keeps track of what a user has already studied and when reviews are due. I created a UserDB/createDB.py, but it is very simple as it is literally just an empty database, to be filled by YYK.

For each new item studied, YYK will enter the following info into the study table:

Type of content (kanji, radical, word), the id of that content from its own table, the user id of the user who studied it, when it was first seen (as a date), how often it has been seen (the review count is used by the SuperMemo 2 method), what the current ease is (the value that is calculated by the SuperMemo 2 method) and the date it is due next (the result of the SuperMemo 2 calculation)

### **4.2. Creation of KanjiDB/createDB.py**

#### **4.2.1. Schema**

The database is currently created using the following schema.

<details>
  <summary>Schema</summary>

```SQL
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL, kan_int INTEGER DEFAULT 5, wrd_int INTEGER DEFAULT 25, rev_int INTEGER DEFAULT 100, last_radical INTEGER DEFAULT 0, last_kanji INTEGER DEFAULT 0, last_word INTEGER DEFAULT 0, last_kanji_study TEXT, last_kanji_review TEXT, last_word_study TEXT, last_word_review TEXT, last_radical_review TEXT)
CREATE TABLE study (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, type TEXT NOT NULL, type_id INTEGER NOT NULL, user_id INTEGER NOT NULL, first_seen TEXT, review_count INTEGER DEFAULT 1, ef REAL DEFAULT 2.5, date_due TEXT)
```

</details>

## **5. YYK - How does it work?**

### **5.1. File Breakdown**

YYK consists of 3 .py files. app.py, database.py and functions.py. After finishing the app, I ended up with about 1400 lines of code, so I wanted to break it up a little bit and reduce some clutter. At first I did all SQL queries in the app.py, but with the desire to separate app routes and regular functions, I decided to put all database operations into a seperate database.py, that is then used by both the app.py and functions.py

#### **5.1.1. database.py**

database.py only consists of two functions, all database queries run through this file.

<details>
  <summary>Imports</summary>

```PY
import sqlite3
```

</details>

**db_insert** is used to insert or change data from the users.db database. It is mostly used when settings are changed or review data is updated. Since the dictionary.db is never changed, there is no need to update or insert into it.

<details>
  <summary>db_insert</summary>

```PY
# Insert or change data from the users database.
def db_insert(query):
    # Connect to the database
    user_con = sqlite3.connect('db/users.db', check_same_thread=False)
    userdb = user_con.cursor()
    # Execute the query
    userdb.execute(query)
    # Commit the changes
    user_con.commit()
    # Close the database
    user_con.close()
```

</details>

**db_query** is used for all other database queries, user.db or dictionary.db. For each query, the user is required to decide "dict" or "users" before the query.

<details>
  <summary>db_query</summary>

```PY
# Query data from either the users or the dictionary database
def db_query(db, query):
    # Connect to the user database
    if db == "users":
        # Connect to the database
        user_con = sqlite3.connect('db/users.db', check_same_thread=False)
        userdb = user_con.cursor()
        # Execute the query
        result = userdb.execute(query)
        # Fetch all results
        result = userdb.fetchall()
        # Close the database
        user_con.close()
    # Connect to the dictionary database
    if db == "dict":
        # Connect to the database
        dic_con = sqlite3.connect('db/dictionary.db', check_same_thread=False)
        dictdb = dic_con.cursor()
        # Execute the query
        result = dictdb.execute(query)
        # Fetch all results
        result = dictdb.fetchall()
        # Close the database
        dic_con.close()

    # Hand the results back
    return result
```

</details>

#### **5.1.2. functions.py**

Functions.py consists of 11 functions that are not flask app routes. Datetime is used to get the current date and to do some
date calculations in connection with the SuperMemo 2 method.

<details>
  <summary>Imports</summary>

```PY
from functools import wraps
from flask import session, redirect
from datetime import date, datetime, timedelta
import math
from database import db_query
```

</details>

**login_required** is a standart function to be used in flask. Not only did we use it in finance, but it can also be found on the flask documentation page. It is used to force the user to login to view specific pages that require data from the users.db database.

<details>
  <summary>login_required</summary>

```PY
# Enable functionality to require login on certain pages
def login_required(f):
    # As per https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
```

</details>

**perform_search** is a function that carries out a search of the database with a user input. Since there are many different things to search for, readings, meanings, kanji, a dedicated function was created to handle the multiple types of searches used.
Because a string of kanji entered should return all possible combinations of vocabulary and kanji and radicals, the string is taken apart and searched for in all possible combinations. For example, if the user searches for "食料品", the search function needs to search for　"食", "料" and "品" separately for both kanji and radicals. For vocabulary however, the function needs to search for "食", "料", "品",　"食料", "料品" and "食料品". In order to achieve this, the function first takes the string apart and then puts it back together in all possible combinations, then forms a search query with all the combinations. For all other data fields to search, a simple LIKE query with wildcards is sufficient. This function only looks for one type of data at a time, so it needs to be called three times to search for radicals, kanji or vocabulary.

<details>
  <summary>perform_search</summary>

```PY
# The search function performing the actual search
def perform_search(search, type):
    # Create the string and results variables
    string = ""
    results = []
    # Depending on what type of data we are searching, the search strings need to be different
    if type == "word":
        column = "word"
        start = "SELECT word, reading, meaning FROM vocabulary WHERE word = "
    elif type == "radical":
        column = "title"
        start = "SELECT title, name, english FROM radicals WHERE title = "
    else:
        column = "kanji"
        start = "SELECT kanji, onyomi, meaning FROM kanji WHERE kanji = "

    # Since different words can be formed with different combinations of kanji, make sure we are looking for all of them
    combo = [search[i: j] for i in range(len(search))
             for j in range(i + 1, len(search) + 1)]

    for i in range(len(combo)):
        if i == (len(combo) - 1):
            string += "'" + combo[i] + "'"
        else:
            string += "'" + combo[i] + "'" + " OR " + column + " = "

    # Put the start and the generated string together to form the search query that will look for all word and kanji combinations
    query = start + string

    # Execute the search for all combinations of words and kanji and radicals
    wtk = db_query("dict", query)
    # Append search results to the results list
    for row in wtk:
        results.append(row)

    # Depending on what type of data we are looking for, the next strings need to change also. All results will be added to the list.

    # If we are looking for a word
    if type == "word":
        # Search the reading
        read = db_query("dict", "SELECT word, reading, meaning FROM vocabulary WHERE reading LIKE '%' || '{}' || '%'".format(search))
        for row in read:
            results.append(row)
        # Search the meaning
        mean = db_query("dict", "SELECT word, reading, meaning FROM vocabulary WHERE meaning LIKE '%' || '{}' || '%'".format(search))
        for row in mean:
            results.append(row)

    # If we are looking for a radical
    elif type == "radical":
        # Search the name
        name = db_query("dict", "SELECT title, name, english FROM radicals WHERE name LIKE '%' || '{}' || '%'".format(search))
        for row in name:
            results.append(row)
        # Search the english name
        english = db_query("dict", "SELECT title, name, english FROM radicals WHERE english LIKE '%' || '{}' || '%'".format(search))
        for row in english:
            results.append(row)

    # If we are looking for kanji
    else:
        # Search the onyomi
        on = db_query("dict", "SELECT kanji, onyomi, meaning FROM kanji WHERE onyomi LIKE '%' || '{}' || '%'".format(search))
        for row in on:
            results.append(row)
        # Search the kunyomi
        kun = db_query("dict", "SELECT kanji, onyomi, meaning FROM kanji WHERE kunyomi LIKE '%' || '{}' || '%'".format(search))
        for row in kun:
            results.append(row)
        # Search the meaning
        mean = db_query("dict", "SELECT kanji, onyomi, meaning FROM kanji WHERE meaning LIKE '%' || '{}' || '%'".format(search))
        for row in mean:
            results.append(row)

    # Return the results list
    return results
```

</details>

**check_session** is used to check if the user has already studied the relevant study that is calling the check. For example, if the user attempts to check the kanji study page, the check_session function will check the users latest kanji study and return results based on if it was on that day or not. In general, the user should not study the same content more than once a day. So this check will make sure this does not happen. It uses datetime to compare the users last study (as logged in the users table) with the date today. This function will only return "yes" or "no", to see if the limit was reached or not.

<details>
  <summary>check_session</summary>

```PY
# The function used to check the last study session and if it was today or not
def check_session(type):
    today = date.today()
    # In case the user is new, we may see an error, so use try
    try:
        lastdate = datetime.strptime(type, '%Y-%m-%d').date()
        if lastdate == today:
            limit = "yes"
        else:
            limit = "no"
    except:
        limit = "no"

    return limit
```

</details>

**word_check** is used to check if the user still has words to study before attempting to enable new kanji study. Sometimes there are a lot of words to study after a new kanji session is finished. If the number of words exceeds the users set amount, the new kanji study needs to be delayed until the user is finished. Likewise, new words should not be looked up until all previously new words have been studied. This function checks for this. The first query will check for all words WITHOUT kanji the user has not yet studied. Then, a second query will check the study database for all known words by that user. Then, the known words will be subtracted from the previous results. If there still remain words after this check, then these words need to be studied first. This function either returns a list of words or an empty list.

<details>
  <summary>word_check</summary>

```PY
# The function to check the users records to figure out whether words remain to be studied
def word_check(user_data):
    # To check if the user still has some words to study, first query the words from the list
    words = db_query("dict", "SELECT v.id, v.word FROM vocabulary AS v WHERE v.category = 'kanji' AND NOT EXISTS (SELECT kanji FROM kanji AS k WHERE v.word LIKE '%' || k.kanji || '%' AND k.id > '{}')".format(user_data))
    # Check which words the user already knows
    known = db_query("users", "SELECT type_id FROM study WHERE user_id = '{}' AND type = 'word'".format(session["user_id"]))

    # Compare the list of words to study with the list of words already known
    list = []
    for entry in words:
        check = 0
        for data in known:
            if entry[0] == data[0]:
                check = 1
        if not check == 1:
            list.append(entry[0])

    # Return the list of new words to study, if any
    return list
```

</details>

**check_study** is used to check what has to be studied. It takes input from check_session and word_check. It gets the "yes" or "no" from check_session, and the list from word_check. If the list is empty, then no words need to be studied. Combining the "yes" or "no" anser from the word or kanji study limit with the need to study words or not, the function can figure out what the user needs to study next, if anything. It returns "yes" or "no" for all three of these checks.

<details>
  <summary>check_study</summary>

```PY
# Check whether words or kanji have to be studied
def check_study(last_kanji_study, last_word_study, last_kanji):
    # Use the check_session function to see if anything was studied today
    kanjilimit = check_session(last_kanji_study)
    wordlimit = check_session(last_word_study)
    # Check if there are remaining words to study, regardless of todays study
    list = word_check(last_kanji)
    # If no words remain, set no, otherwise yes.
    if not list:
        words = "no"
    else:
        words = "yes"

    # If we already studied kanji today, no kanji need to be studied anymore
    if kanjilimit == "yes":
        kanjistudy = "no"
    # Otherwise, if we still have words left, no kanji need to be studied at this time
    else:
        if words == "yes":
            kanjistudy = "no"
        # Otherwise, if we have no words left but words were studied today, no kanji need to be studied
        else:
            if wordlimit == "yes":
                kanjistudy = "no"
            # If kanji were not studied today, and no words remain, and words were not studied already today, enable new kanji study
            else:
                kanjistudy = "yes"

    # If words have already been studied today, no words need to be studied
    if wordlimit == "yes":
        wordstudy = "no"
    # If words have not been studied today and there are still words left to study, study them
    else:
        if words == "yes":
            wordstudy = "yes"
        # If there are no more words, no study is needed
        else:
            wordstudy = "no"

    # Return the results
    return kanjistudy, wordstudy, words
```

</details>

**check_review** is used to check if the user has to review a certain type of content. As far as reviews are concerned, depending on how the user rates their own answers, there may be some days where no reviews are due. First, the function will check if a review has already happened on that day. In that case, even if there are still reviews schedule, no new reviews will be shown that day. (because the users set limit has been reached) However, if no review happened on that day, the function checks if there are any items to review at all. It does so by getting todays date and comparing it to the due date for all entries in the study table for that user. If the date is earlier or on the date for today, that means there are reviews to be scheduled for todays session. The function returns a simple "yes" or "no".

<details>
  <summary>check_review</summary>

```PY
# Check whether the type has to be reviewed
def check_review(typelimit, type):
    # Get the date for today
    today = date.today()
    # If this type has been reviewed today, then no other review needs to happen
    if typelimit == "yes":
        typereview = "no"
    # If the type has not been reviewed today, check if there are any reviews that are scheduled for today
    else:
        start = "SELECT type_id FROM study WHERE type = '"
        user_id = "' AND user_id = '"
        date_due = "' AND date_due <= '"
        end = "'"
        query = start + type + user_id + str(session["user_id"]) + date_due + str(today) + end
        list = db_query("users", query)
        # If there are no reviews today, set no, otherwise yes
        if not list:
            typereview = "no"
        else:
            typereview = "yes"

    return typereview
```

</details>

**check_reviews** is used to check what has to be reviewed. It takes input from check_session and check_review and shows what has to be reviewed, if anything. This function is just a simple combination of other functions, to make it easier to use in the app route. check_session is used three times on the three different types of content, then the data received from that is used to call the check_review function to see if those contents have reviews scheduled for today. It will return "yes" or "no" for all three of the review content types.

<details>
  <summary>check_reviews</summary>

```PY
# Check whether words or kanji have to be reviewed
def check_reviews(last_radical_review, last_kanji_review, last_word_review):
    # First, use check_session to determine if we already reviewed today
    radicallimit = check_session(last_radical_review)
    kanjilimit = check_session(last_kanji_review)
    wordlimit = check_session(last_word_review)

    # Hand the review information over to the check_review function.
    radicalreview = check_review(radicallimit, "radical")
    kanjireview = check_review(kanjilimit, "kanji")
    wordreview = check_review(wordlimit, "word")

    return radicalreview, kanjireview, wordreview
```

</details>

**new_number** is used during reviews and study. During study, the user is free to decide what to show again and what to consider learned for now. During reviews, if the user forgets something or has a particularly bad response, the content may show up again during the same review session. While looping through what has to be studied, new_number keeps track of what the current maximum id in the list of things currently in study/review rotation is. The ID is used so flask knows what it has to hand to JavaScript via JSON, and what is already done. Also, since the items that are finished are entirely up to the user, it is not certain which numbers will be gone first, so it is not safe to just increase the number by one for each content handed to JSON. new_number checks if the number is available and keeps increasing until it finds the next available number to hand back.

<details>
  <summary>new_number</summary>

```PY
# Function to determine the next number in a list
def new_number(numberlist, number):
    # Check what the current biggest item in the numberlist is
    newmax = numberlist[0]
    for entry in numberlist:
        if entry > newmax:
            newmax = entry
    # If the number is the same OR bigger than the current max, set it to the mininum
    if number == newmax or number > newmax:
        number = numberlist[0]
    # If not, go to the next possible number
    else:
        number = number + 1
        if not number in numberlist:
            while not number in numberlist:
                number = number + 1

    return number
```

</details>

**create_svg** is used so that SVG data can be handed to JavaScript via json, so data can be displayed during study and review of kanji. When the user first visits the study or review page for kanji, the first displayed kanji will have the SVG data handed to the site via jinja, so displaying it is easy. However, when the user starts fetching data from flask via JavaScript, showing the new SVG data proved to be a challenge, so I opted to create the entire SVG code as one long string and hand it to JavaScript via JSON, to enter as innerHTML for a specific DIV. Since every kanji has different SVG data, this needs to happen every time the user requests the next kanji in their study or review session.

<details>
  <summary>create_svg</summary>

```PY
# The function to create svgdata to hand into JavaScript
def create_svg(black, color, strokes):
    # Create black strokes
    svgbl = "<svg id=\"svgblack\" viewBox=\"0 0 100 100\" class=\"strokes\">" + black + "</svg>"
    # Create black strokes with count
    svgblst = "<svg id=\"svgblackstrokes\" viewBox=\"0 0 100 100\" class=\"strokes\">" + black + strokes + "</svg>"
    # Create color strokes
    svgcl = "<svg id=\"svgcolor\" viewBox=\"0 0 100 100\" class=\"strokes\">" + color + "</svg>"
    # Create color strokes with count
    svgclst = "<svg id=\"svgcolorstrokes\" viewBox=\"0 0 100 100\" class=\"strokes\">" + color + strokes + "</svg>"
    # Combine the data
    svgdata = svgbl + svgblst + svgcl + svgclst

    return svgdata
```

</details>

**super_memo** is used to calculate the new values and the next due date for every item studied and reviewed. It is basically the one thing that applies the SuperMemo 2 algorithm. The SuperMemo 2 algorithm calculates the next due date of any item to study by calculating the E-Factor of the item by using the number of times the item has been reviewed and the quality of the users answer. If the quality is low, the E-Factor will remain unchanged and the interval is set back to 1, meaning the item will return again very soon. If the quality is good enough, the new E-Factor will be calculated based on the users answer and the current interval, as well as the current E-Factor. Then, the new due date will be calculated based on that. For more details, please check https://www.supermemo.com/en/archives1990-2015/english/ol/sm2.

<details>
  <summary>super_memo</summary>

```PY
# The SuperMemo2 calculation
def super_memo(e_factor, review_count, quality):
    # If the response quality was less than 3
    if quality < 3:
        # The E-Factor remains unchanged
        new_e = e_factor
        # The interval gets set back to 1
        new_n = 1
    # If the response quality was 3 or more
    else:
        # Calculate the new E-Factor based on the SuperMemo formula and round to the nearest decimal
        new_e = round((e_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))), 1)
        # If the new factor is less than 1.3, set it to 1.3
        if new_e < 1.3:
            new_e = 1.3

        # Add 1 to the review count (it goes up with every review)
        new_n = review_count + 1
    # If new_n is 1, the next review comes in 1 day
    if new_n == 1:
        due_date = date.today() + timedelta(days=1)
    # If new_n is 2, the next review comes in 6 days
    elif new_n == 2:
        due_date = date.today() + timedelta(days=6)
    # If new_n is more than 2, the next review will be calculated
    else:
        # Calculate the new interval based on the SuperMemo formula and round it to the next biggest int
        interval = math.ceil((review_count - 1) * new_e)
        # The new due date is calculated using the time delta between today and the amount of days calculated before
        due_date = date.today() + timedelta(days=interval)
    # Return new E-Factor, new review_count and new interval
    return new_e, new_n, due_date
```

</details>

**get_kana** is the function used to hand hiragana or katakana to the kana pages. Instead of just having one unorganized list of kana, I decided to divide them into their subtypes. The "target" input is decided by the button the user clicks. There are buttons for hiragana and katakana. Depending on that, the function will either query hiragana or katakana data. Since each kana has a hiragana and a katakana version, the html pages for both of these can be identical, and only the data handed needs to change.

<details>
  <summary>get_kana</summary>

```PY
# Mini function to query for hiragana or katakana
def get_kana(target):
    # The start string is the same
    start = "SELECT kana, romaji, number FROM kana WHERE type = '"
    # The query for monographs
    monoend = "' AND subtype = 'monograph'"
    # The query for digraphs
    diend = "' AND subtype = 'digraph'"
    # The query for monograph diacritics
    monodiaend = "' AND subtype = 'monograph diacritic'"
    # The query for digraph diacritics
    didiaend = "' AND subtype = 'digraph diacritic'"
    # Get all the needed kana data
    mono_string = start + target + monoend
    mono = db_query("dict", mono_string)
    di_string = start + target + diend
    di = db_query("dict", di_string)
    monodia_string = start + target + monodiaend
    monodia = db_query("dict", monodia_string)
    didia_string = start + target + didiaend
    didia = db_query("dict", didia_string)
    # Check if we are doing hiragana or katakana
    if target == "hiragana":
        syllabary = "Hiragana"
    else:
        syllabary = "Katakana"

    return mono, di, monodia, didia, syllabary
```

</details>

#### **5.1.3. app.py**

app.py consists only of the initial configuration and the app routes, therefore I will discuss the workings of the different app routes together with the relevant html files. As far as imports go, all functions from database.py and functions.py are imported.

Besides Flask and Flask_session, werkzeug.security is used to generate and check password hashes, much like in finance. Datetime is used to get todays date to check for review and study times. The app also has to calculate new dates based on some factors like the SuperMemo 2 method. flask_gtts is used to generate Japanese text to speech from word meanings (read the hiragana and create a temporary mp3 that is automatically linked through jinja, so every word of the more than 17.000 can be listened to, but doesn't need to have the mp3s generated and saved in advance). gtts is used to temporarily generate mp3s used for review and study sessions. They are deleted after. os.path.exists is used to check if an mp3 already exists or not. In order to prevent loading issues, some app routes will wait until the file exists after calling gtts to create it, before they hand the data to JSON. os.remove is used to remove the mp3s after the study session is finished or after a word has been deemed finished by the user. math is used for... math... And random is used to randomize lists for review purposes, so the user does not always see everything they studied on the same day in the same order again.

<details>
<summary>Imports</summary>

```PY
from database import db_insert, db_query
from functions import *
from flask import Flask, render_template, session, request, redirect, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date, timedelta
from flask_gtts import gtts
from gtts import gTTS
from os.path import exists
from os import remove
import math
import random
```

</details>

##### **5.1.3.1. layout.html**

The layout file which all other html files extend. Much like finance, it contains all the important links to other parts of the site. I used bootstrap to create most of the styling for YYK. In fact, some of the bootstrap design previews were a heavy inspiration for the design of this layout. I was also inspired by finance to keep some important links at the bottom.

If the user is not logged in, Register and Login options will be at the top right. Those will be replaced by Profile and Logout when the user is logged in. This is done by using "{% if session["user_id"] %}" in jinja.

##### **5.1.3.2. about.html**

The about page that explains what YYK is and does, much like this markdown, however much simpler and shorter.

##### **5.1.3.3. acknowledgements.html**

All data or ideas that I used that were created by other people are listed here, with the appropriate licenses, as well as some other acknowledgements.

##### **5.1.3.4. error.html**

This page is used for whenever user input does not result in the desired outcome. For example, a wrong password, an invalid input. The user will be redirected to this page and shown the error code. An example of this happening would be:

```PY
if not request.form.get("password") == request.form.get("confirmation"):
    return render_template("error.html", message="Password does not match confirmation.")
```

The html for this is very simple.

```HTML
{% block main %}
  <div class="text-center">
    <h5>{{ message }}</h5>
  </div>
{% endblock %}
```

I opted to not use any funny cats at this time :)

##### **5.1.3.5. how_to.html**

This page explains to the user how to use YYK. Where to start their study and how to proceed for each study session.

##### **5.1.3.6. index.html**

The first page the user sees upon opening YYK. If the user is not logged in, only the YYK logo will be displayed. If the user is logged in, the Study and Review options will appear instead. The Study and Review options use bootstrap cards as their design.

<details>
  <summary>HTML excerpt</summary>

```HTML
{% if session["user_id"] %}
  <div class="container-fluid">
    <div class="row justify-content-md-around">
      <div class="col-md-auto text-center">
        <div class="card" style="width: 25vw;">
          <img class="card-img-top center" src="static/img/study.jpg" style="width: 24vw; height: 15vw" alt="Japanese for study">
          <div class="card-body">
            <p class="card-text"><a href="/study" class="btn btn-lg btn-outline-primary">Study</a></p>
          </div>
        </div>
      </div>
      <div class="col-md-auto text-center">
        <div class="card" style="width: 25vw;">
          <img class="card-img-top center" src="static/img/practice.jpg" style="width: 24vw; height: 15vw" alt="Japanese for practice">
          <div class="card-body">
            <p class="card-text"><a href="/review" class="btn btn-lg btn-outline-primary">Review</a></p>
          </div>
        </div>
      </div>
    </div>
  </div>
{% else %}
  <div class="container text-center">
    <img class="img-fluid w-75" alt="yes, you kanji logo" style="width: auto; height: 15vw" src="static/img/logo.jpg">
  </div>
{% endif %}
```

</details>

##### **5.1.3.7. kana_review.html**

On this page users can check their knowledge of the kana they have studied prior to YYK or in the kana_study section.
One kana is displayed, hiragana or katakana, depending on how the user got to the page, and when the user clicks on reveal, the reading is displayed. The user can so check themselves and see if they mastered all kana or not. Once the user clicks through all kana, their score will be displayed, depending on how many they got right.

This was the first time I managed to use fetch to request data from flask and get it back to JavaScript with JSON. I failed many times prior and had to do a lot of research to get it to work. For some reason I had no success with ajax as taught by the CS50 shorts. I also had some issues with pushing buttons before everything has loaded, so I opted to disabled all buttons by default and only enable them once all loading has finished. In the same way, once a button is pushed, in order to not being pushed again immediately before loading is finished, I opted to disable all buttons once pushed.

<details>
  <summary>Code Explanation</summary>

Once the user accesses the page, depending on whether they are choosing hiragana or katakana, the app route will load the appropriate syllabary.

```PY
# First, check what we are reviewing, hiragana or katakana, and query the correct data
target = request.args["review"]
if target == "hiragana":
    syllabary = "Hiragana"
    temp = db_query("dict", "SELECT kana, romaji, number FROM kana WHERE type = 'hiragana' ORDER BY RANDOM()")
else:
    syllabary = "Katakana"
    temp = db_query("dict", "SELECT kana, romaji, number FROM kana WHERE type = 'katakana' ORDER BY RANDOM()")
```

Then, in order to give the user a new order for every review, we create a list from all items and then shuffle it.
Because of the way kana are displayed in their respective tables on the kana_study page, there are some entries with only 0 as data. Those will be filtered out during list creation.

```PY
# Create a new list and put in the queried kana
kana = []
for item in temp:
    if not item[0] == "0":
        newitem = list(item)
        kana.append(newitem)

# Randomize the list so the user can have a different order for each review
random.shuffle(kana)
for i in range(len(kana)):
    kana[i].append(i)
```

Finally, we pick the first card in the list to hand to Jinja.

```PY
# Pick the first card to be shown
card = [kana[0][0], kana[0][1], kana[0][2], kana[0][3]]

return render_template("kana_review.html", kana=kana, syllabary=syllabary, card=card)
```

The user will see a card with everything but the kana hidden. Once the user thinks they know what the kana is, they can press the reveal button. The reveal() function is called when the reveal button is pressed. It will show the reading and audio, and also display the "Incorrect" and "Correct" buttons. The user can decide whether their guess was correct and push the appropriate button.

```JS
function reveal() {
  document.getElementById("hiddenreading").style.display = "inline";
  document.getElementById("hiddenaudio").style.display = "inline";
  document.getElementById("hiddenbuttons").style.display = "inline";
  document.getElementById("revealbutton").style.display = "none";
}
```

The function getData(cardNo, answer) will fetch the next kana data, after the user has pressed either the "Correct" or "Incorrect" button. Flask will then assemble the new data and send it to JavaScript. Since the kana are randomized every time the user accesses the kana_review.html page, they are handed to JavaScript by JSON as a list. After randomization the entries are numbered, so getData will get the current No as input, which flask will use to hand the next piece of data back to JavaScript. The function also takes the answer as input, which is either "correct" or incorrect. For each time the user is correct, a counter is updated, so the user knows how many they got right at the end. Once the function gets the number 107 back from flask, the session will finish. There are only 106 kana (and combinations) in each session.

```JS
function getData(cardNo, answer) {
  if (answer == 'correct') {
    counter++;
  }

  let url = "/kana_review";
  let data = { "number": cardNo, "style": "{{ syllabary }}", "kana": {{ kana|tojson }}};

  fetch(url, {
    "method": "POST",
    "headers": {"Content-Type": "application/json"},
    "body": JSON.stringify(data),
  }).then(response => response.json())
  .then(data => {
    console.log(data);
    if (data["number"] == "107") {
      document.getElementById('nextc').setAttribute('disabled', '');
      document.getElementById('nexti').setAttribute('disabled', '');
      document.getElementById("hiddenaudio").style.display = "none";
      document.getElementById('labelrom').innerHTML = "";
      document.getElementById('labellis').innerHTML = "";
      document.getElementById('cardtitle').innerHTML = "Finish!";
      document.getElementById('cardroman').innerHTML = "Correct: " + counter + " out of 106.";
    }
    else {
      document.getElementById('nextc').setAttribute('onclick', data["correct"]);
      document.getElementById('nexti').setAttribute('onclick', data["incorrect"]);
      document.getElementById('cardtitle').innerHTML = data["kana"];
      document.getElementById("revealbutton").style.display = "inline";
      document.getElementById("hiddenreading").style.display = "none";
      document.getElementById("hiddenaudio").style.display = "none";
      document.getElementById("hiddenbuttons").style.display = "none";
      document.getElementById('cardroman').innerHTML = data["romaji"];
      document.getElementById('cardaudio').setAttribute('src', data["audio"]);
    }

  })

  .catch((err) => console.log("Access failed: " + url + " Reason: " + err));
}
```

This is what happens on the flask side during this session.

```PY
jsonData = request.get_json()
number = int(jsonData["number"])

# If we reach 107, meaning the user has seen all kana, only send the number (the results will be displayed by JS)
if number == 107:
    data = {"number": number}
    return jsonify(data)
kana = jsonData["kana"]

# Format the string used to load the audio file
audio = "static/mp3/" + str(kana[number][2]) + ".mp3"
# Increase numbers until we hit 107
if not number == 107:
    next = int(number) + 1
else:
    next = number

# Format the string used to call next kana for both buttons
correct = "getData(" + str(next) + ", 'correct')"
incorrect = "getData(" + str(next) + ", 'incorrect')"

# Return the data to the page
data = {"kana": kana[number][0], "romaji": kana[number][1], "number": kana[number]
        [3], "audio": audio, "correct": correct, "incorrect": incorrect}
return jsonify(data)
```

</details>

##### **5.1.3.8. kana_study.html**

The kana_study page displays all the different kana to the user. There are about 50, but they can also combine and form new sounds. The user can click on any kana to load the data. They can also click next or previous to see them in order. They can also listen to the pronunciation. The pronunciation was provided by gTTs and saved prior to making the app. For other words I found it better to load gTTs on the fly, but there are only about 106 different pronunciations for kana, and the files are quite small, so I decided to save them and load them from flask instead. Here again, data is fetched from flask via JSON.

There is also an explanation on some of the quirks of Japanese and specific combinations of symbols and sounds.

<details>
  <summary>Code explanation</summary>

Depending on which button the user used to get to the page, the syllabary will either be hiragana or katakana. This is handed to python using the GET argument. All kana for that syllabary are loaded and all of them and the first one to be displayed handed to jinja.

```PY
target = request.args.get("study")

mono, di, monodia, didia, syllabary = get_kana(target)

# Pick the first card to be shown
card = [mono[0][0], mono[0][1], mono[0][2]]
return render_template("kana_study.html", mono=mono, di=di, monodia=monodia, didia=didia, syllabary=syllabary, card=card)
```

The user can then click either on any symbol they see to load a bigger view of it, including sounds, or click next or previous to get to the next or previous symbol. The JavaScript for this is similar to the one in the kana_review route. However, it catches some cases, like disabling the appropriate buttons when on the first or last kana. The selected kana is fetched from flask via JavaScript, using the id no of the kana in question.

```JS
function getData(cardNo) {
  let url = "/kana_study";
  let data = { "number": cardNo, "style": "{{ syllabary }}" };
  fetch(url, {
    "method": "POST",
    "headers": {"Content-Type": "application/json"},
    "body": JSON.stringify(data),
  }).then(response => response.json())
  .then(data => {
    console.log(data);
    document.getElementById('cardtitle').innerHTML = data["kana"];
    document.getElementById('cardroman').innerHTML = data["romaji"];
    document.getElementById('cardaudio').setAttribute('src', data["audio"]);
    if (data["number"] == "0") {
      document.getElementById('previous').setAttribute('disabled', '');
    }
    else {
      document.getElementById('previous').removeAttribute('disabled');
      document.getElementById('previous').setAttribute('onclick', data["previous"]);
    }

    if (data["number"] == "106") {
      document.getElementById('next').setAttribute('disabled', '');
    }
    else {
      document.getElementById('next').removeAttribute('disabled');
      document.getElementById('next').setAttribute('onclick', data["next"]);
    }

  })

  .catch((err) => console.log("Access failed: " + url + " Reason: " + err));
}
```

This is the python side of that exchange.

```PY
# Get the data from JSON
jsonData = request.get_json()
number = str(jsonData["number"])
syllabary = jsonData["style"]
# If the user is currently on the hiragana page, return hiragana results
if syllabary == "Hiragana":
    kana = db_query("dict", "SELECT kana, romaji, number FROM kana WHERE type = 'hiragana' AND number = '{}'".format(number))
# If the user is currently on the katakana page, return katakana results
elif syllabary == "Katakana":
    kana = db_query("dict", "SELECT kana, romaji, number FROM kana WHERE type = 'katakana' AND number = '{}'".format(number))

# Format the string used to load the audio file
audio = "static/mp3/" + str(kana[0][2]) + ".mp3"
# Check what number we are and what number to send for previous and next kana
if not number == 106:
    next = int(number) + 1
else:
    next = number

# Format the string used to call next kana
next = "getData(" + str(next) + ")"

if not number == 0:
    previous = int(number) - 1
else:
    previous = number

# Format the string used to call previous kana
previous = "getData(" + str(previous) + ")"

# Return the data to the page
data = {"kana": kana[0][0], "romaji": kana[0][1], "number": kana[0][2], "audio": audio, "next": next, "previous": previous}
return jsonify(data)
```

</details>

##### **5.1.3.9. kana.html**

The kana page offers the user the choice of either studying or reviewing hiragana or katakana. Depending on which the user selects, kana_study or kana_review are called either with hiragana or katakana data.

##### **5.1.3.10. kanji_overview.html**

The kanji_overview page is called by the GET method of the /kanji route. This is just a table of all kanji in the YYK database, in the order they will appear during study, which is sorted by grade. The user can choose to sort by JLPT instead. I was not sure at the time how to sort a table, so what actually happens is the app loads both tables and hides one of them via html (style:" display: none;"). When the user clicks the button, the appropriate table is hidden and the other displayed. If the user clicks on a kanji, it will open the POST route.

<details>
  <summary>SQL queries for the tables</summary>

```PY
# Get a list sorted by grade
grade = db_query("dict", "SELECT id, kanji, onyomi, kunyomi, meaning, grade, jlpt FROM kanji ORDER BY grade")
# Get a list sorted by jlpt
jlpt = db_query("dict", "SELECT id, kanji, onyomi, kunyomi, meaning, grade, jlpt FROM kanji ORDER BY jlpt DESC")
```
</details>

##### **5.1.3.11. kanji.html**

The kanji page is called by the POST method of the /kanji route. Here the user can see detailed information about the selected kanji. There is a stroke order display, that can be toggled to display colors or black only, as well as show the stroke counts or not. The user can see all words that use this kanji sorted by their appearance in the different JLPT levels from 5 to 1. Some words are not in that category, so they are under NA. The user can come here through various ways, either from the kanji_overview route, from the vocabulary page, or the radical page.

If the user clicks on the radical of that kanji, the radical page is displayed. If the user clicks on any word, the vocabulary page for that word is displayed.

<details>
  <summary>Code explanation</summary>

The strokes are basically four different svgs, depending on if the user wants black, color, with or without stroke counts.
This is the html:

```HTML
<svg id="svgblack" viewBox="0 0 100 100" class="strokes">
  {{ svg_black|safe }}
</svg>
<svg id="svgblackstrokes" viewBox="0 0 100 100" class="strokes">
  {{ svg_black|safe }}{{ svg_strokes|safe }}
</svg>
<svg id="svgcolor" viewBox="0 0 100 100" class="strokes">
  {{ svg_color|safe }}
</svg>
<svg id="svgcolorstrokes" viewBox="0 0 100 100" class="strokes">
  {{ svg_color|safe }}{{ svg_strokes|safe }}
</svg>
```

The JavaScript code on the buttons will toggle between the different svgs. There are two functions involved, toggleStrokes() and toggleColor(). Since there are a couple different places where these functions are used, they are found in the script.js file.

```JS
var strokeToggle = "off";
var color = "black";

function toggleStrokes() {
  if (strokeToggle == "off" && color == "black") {
    document.getElementById("svgblack").style.display = "none";
    document.getElementById("svgblackstrokes").style.display = "block";
  strokeToggle = "on";
  }
  else if (strokeToggle == "on" && color == "black") {
    document.getElementById("svgblack").style.display = "block";
    document.getElementById("svgblackstrokes").style.display = "none";
    strokeToggle = "off";
  }
  else if (strokeToggle == "off" && color == "color") {
    document.getElementById("svgcolor").style.display = "none";
    document.getElementById("svgcolorstrokes").style.display = "block";
    strokeToggle = "on";
  }
  else if (strokeToggle == "on" && color == "color") {
    document.getElementById("svgcolor").style.display = "block";
    document.getElementById("svgcolorstrokes").style.display = "none";
    strokeToggle = "off";
  }
}

function toggleColor() {
  if (strokeToggle == "off" && color == "black") {
    document.getElementById("svgblack").style.display = "none";
    document.getElementById("svgcolor").style.display = "block";
    color = "color";
  }
  else if (strokeToggle == "on" && color == "black") {
    document.getElementById("svgblackstrokes").style.display = "none";
    document.getElementById("svgcolorstrokes").style.display = "block";
    color = "color";
  }
  else if (strokeToggle == "off" && color == "color") {
    document.getElementById("svgcolor").style.display = "none";
    document.getElementById("svgblack").style.display = "block";
    color = "black";
  }
  else if (strokeToggle == "on" && color == "color") {
    document.getElementById("svgcolorstrokes").style.display = "none";
    document.getElementById("svgblackstrokes").style.display = "block";
    color = "black";
  }
}
```

The data to display on the page is accumulated by several SQL queries.

```PY
kanji = request.form.get("kanji")
# Get the info for that kanji
info = db_query(
    "dict", "SELECT id, kanji, onyomi, kunyomi, meaning, radical_id, strokecount, grade, jlpt, unicode FROM kanji WHERE kanji = '{}'".format(kanji))
# Get the radical for that kanji
radical = db_query("dict", "SELECT radical, title FROM radicals WHERE id = '{}'".format(info[0][5]))
# Get the SVG data for that kanji
svg = db_query(
    "dict", "SELECT svg_black, svg_color, svg_strokes FROM strokeorder WHERE kanji_unicode = '{}'".format(info[0][9]))

# Get all words including that kanji
words = db_query(
    "dict", "SELECT word, reading, meaning, jlpt FROM vocabulary WHERE word LIKE '%{}%' ORDER BY jlpt DESC".format(kanji))
# Get JLPT levels for all words including that kanji
jlpt = db_query("dict", "SELECT DISTINCT jlpt FROM vocabulary WHERE word LIKE '%{}%' ORDER BY jlpt DESC".format(kanji))

return render_template("kanji.html", kanji=kanji, info=info, radical=radical, svg_black=svg[0][0], svg_color=svg[0][1], svg_strokes=svg[0][2], words=words, jlpt=jlpt)
```
</details>

##### **5.1.3.12. login.html**

A simple page allowing the user to login. Several safety checks check for wrong usernames or passwords. If the username exists and the password is correct, the session will rememember the current user.

<details>
  <summary>Code</summary>

```PY
# Safety checks
if not request.form.get("username"):
    return render_template("error.html", message="Must provide username.")

if not request.form.get("password"):
    return render_template("error.html", message="Must provide password.")

# Check database for username
check = db_query("users", "SELECT * FROM users WHERE username = '{}'".format(request.form.get("username")))

# Check usernamen and password
if len(check) == 0 or not check_password_hash(check[0][2], request.form.get("password")):
    return render_template("error.html", message="Invalid username and/or password.")

# Remember the user that is logged in
session["user_id"] = check[0][0]

return redirect("/")
```

</details>

##### **5.1.3.13. profile.html**

If the user is logged in, they can access their profile page. Here they can change their session settings. The recommended settings are 5 kanji and 25 words per study session and 100 reviews per review session. The settings can go up to 30 kanji, 100 words and 400 reviews, though these settings would be rather extreme and not recommended.

The user can also see some statistics about their study progress, using bootstrap progress bars.

If the user is new, there will be no statistics, as the last session dates do not exist yet. Previously the page would throw an error, but I fixed it to just display a message instead.

<details>
  <summary>Code explanation</summary>

First we need to check if the user is new, and if not, do a lot of checks and calculations for the statistics to be displayed.

```PY
# If the method is get, display the user profile according to the current data
if request.method == "GET":
    # Get the user data
    user_data = db_query(
        "users", "SELECT username, kan_int, wrd_int, rev_int, last_kanji, last_radical, last_word FROM users WHERE id = '{}'".format(session["user_id"]))
    # If the user data does not have the needed entries, that means the user is new, no statistics are available
    if user_data[0][4] == 0 or user_data[0][5] == 0 or user_data[0][6] == 0:
        newuser = "yes"
        return render_template("profile.html", user_data=user_data, newuser=newuser)
    # If the user data has all needed entries, perform some queries to fetch the needed data to show statistics
    else:
        newuser = "no"
        # Current Grade
        grade = db_query("dict", "SELECT grade FROM kanji WHERE id = '{}'".format(user_data[0][4]))
        # The ID of the first kanji in that grade
        min = db_query("dict", "SELECT min(id) FROM kanji WHERE grade = '{}'".format(grade[0][0]))
        # The amount of all kanji in that grade
        amount = db_query("dict", "SELECT COUNT(id) FROM kanji WHERE grade = '{}'".format(grade[0][0]))
        # To find out user progress for this grade, subtract the first ID from the last studied kanji ID
        gradeprog = (user_data[0][4] - (min[0][0] - 1))
        # Calculate percentage of all kanji studied in this grade
        gradeper = round(((gradeprog / amount[0][0]) * 100), 1)
        # Calculate percentage of all kanji studied in total
        totalper = round(((user_data[0][4] / 2387) * 100), 1)
        # The amount of all radicals studied by that user
        radamount = db_query(
            "users", "SELECT COUNT(id) FROM study WHERE type = 'radical' AND user_id = '{}'".format(session["user_id"]))
        # Calculate percentage of all radicals studied
        radper = round(((radamount[0][0] / 214) * 100), 1)
        # The amount of all words studied by that user
        wordamount = db_query(
            "users", "SELECT COUNT(id) FROM study WHERE type = 'word' AND user_id = '{}'".format(session["user_id"]))
        # Calculate percentage of all words studied
        wordper = round(((wordamount[0][0] / 14071) * 100), 1)
        # Get the last radical, kanji and word studied by that user
        last_rad = db_query("dict", "SELECT title FROM radicals WHERE id = '{}'".format(user_data[0][5]))
        last_kan = db_query("dict", "SELECT kanji FROM kanji WHERE id = '{}'".format(user_data[0][4]))
        last_wrd = db_query("dict", "SELECT word FROM vocabulary WHERE id = '{}'".format(user_data[0][6]))
        # How many days does it take to study everything based on current user settings
        kanjidays = math.ceil((2387 - user_data[0][4]) / user_data[0][1])
        worddays = math.ceil((14071 - wordamount[0][0]) / user_data[0][2])

        return render_template("profile.html", user_data=user_data, newuser=newuser, grade=grade[0][0], gradeprog=gradeprog, amount=amount[0][0], gradeper=gradeper, totalper=totalper, radamount=radamount[0][0], radper=radper, wordamount=wordamount[0][0], wordper=wordper, last_rad=last_rad, last_kan=last_kan, last_wrd=last_wrd, kanjidays=kanjidays, worddays=worddays)
```

If the user wishes to change their password or other settings, the app will check for what the user intends to change first. There is a hidden form input item in the form that will send either "session-options" or "change-password" along with the values the user intended to change. Several safety checks, such as for correct password or valid session data will prevent the user from setting incorrect values.

```PY

# If the method is post, check for what the user wants to do and act accordingly
if request.method == "POST":

    # If the user wants to change the session options
    if request.form["checkform"] == "session-options":

        if int(request.form.get("kanji-interval")) > 30:
            return render_template("error.html", message="Kanji interval must be no more than 30.")
        if int(request.form.get("word-interval")) > 100:
            return render_template("error.html", message="Word interval must be no more than 100.")
        if int(request.form.get("review-interval")) > 400:
            return render_template("error.html", message="Review interval must be no more than 400.")

        # Update the database with the new options
        db_insert("UPDATE users SET kan_int = '{0}', wrd_int = '{1}', rev_int = '{2}' WHERE id = '{3}'".format(request.form.get(
            "kanji-interval"), request.form.get("word-interval"), request.form.get("review-interval"), session["user_id"]))

        return redirect("/profile")

    # If the user wants to change the password
    if request.form["checkform"] == "change-password":
        # Get the username
        user = db_query("users", "SELECT username FROM users WHERE id = '{}'".format(session["user_id"]))

        # Do some safety checks for the user input
        if not request.form.get("password"):
            return render_template("error.html", message="Must provide current password.")

        if not request.form.get("newpassword") or not request.form.get("confirmation"):
            return render_template("error.html", message="Must provide new password and confirmation.")

        if not request.form.get("newpassword") == request.form.get("confirmation"):
            return render_template("error.html", message="Password does not match confirmation.")

        # Check old hash
        check = db_query("users", "SELECT hash FROM users WHERE username = '{}'".format(user[0][0]))

        # Ensure current password is correct
        if not check_password_hash(check[0][0], request.form.get("password")):
            return render_template("error.html", message="Invalid password.")

        # Change the password
        db_insert("UPDATE users SET hash = '{0}' WHERE id = '{1}'".format(generate_password_hash(
            request.form.get("newpassword"), method="pbkdf2:sha256", salt_length=8), session["user_id"]))

        return redirect("/profile")
```

</details>

##### **5.1.3.14. radical_overview.html**

The radical_overview page is called by the GET method of the /radicals route. This is just a table of all radicals in the YYK database, ordered by the number of strokes, as is common. The user can toggle to display only the radicals of a certain stroke count, as opposed to all of them. If the user clicks on a radical, it will open the POST route.

<details>
  <summary>Code</summary>

```PY
radicals = db_query("dict", "SELECT strokecount, title, id, english FROM radicals ORDER BY id, strokecount")
# The number of possible radical strokes is a well known part of radical study so I hardcoded this here
strokes = [*range(1, 18)]

return render_template("radical_overview.html", radicals=radicals, strokes=strokes)
```

</details>

##### **5.1.3.15. radical.html**

If the user clicks on a radical in any place radicals appear, they will be sent to the radical page. Here they can view information about the radical. There is a table of all kanji that can be written with that radical. The table can be sorted by strokes, grade or JLPT level of the kanji, and further only display all kanji that are of a certain strokecount, grade or JLPT level. This uses the same trick as in kanji_overview. Instead of the table getting sorted, all tables are handed over at first and all but one hidden from view. Then, when the button is pressed, the desired table is shown and the others hidden. If the user clicks on a kanji, it will open the POST route of the /kanji route.

<details>
  <summary>Code explanation</summary>

In order to display all the relevant information, a couple of SQL queries need to be made. First, get all the information from the radicals table about the requested radical. Then, get all kanji that have the same radical_id. In order to sort by strokecount another query will look for only the distinct stroke count. Same goes for grade and jlpt.

```PY
radical = request.form.get("radical")
# Get the data for this radical
info = db_query(
    "dict", "SELECT id, radical, name, english, radical_group, strokecount FROM radicals WHERE title = '{}'".format(radical))
# Get all kanji that belong to this radical
kanji = db_query("dict", "SELECT id, kanji, strokecount, grade, jlpt FROM kanji WHERE radical_id = '{}'".format(info[0][0]))
# Check for strokecount numbers for all the kanji for this radical
kanjistrokes = db_query(
    "dict", "SELECT DISTINCT strokecount FROM kanji WHERE radical_id = '{}' ORDER BY strokecount".format(info[0][0]))
# Check for grades for all the kanji for this radical
kanjigrade = db_query("dict", "SELECT DISTINCT grade FROM kanji WHERE radical_id = '{}' ORDER BY id".format(info[0][0]))
# Check for jlpt for all the kanji for this radical
kanjijlpt = db_query("dict", "SELECT DISTINCT jlpt FROM kanji WHERE radical_id = '{}' ORDER BY id".format(info[0][0]))

return render_template("radical.html", radical=radical, info=info, kanji=kanji, kanjistrokes=kanjistrokes, kanjigrade=kanjigrade, kanjijlpt=kanjijlpt)
```

</details>

##### **5.1.3.16. register.html**

A simple user registration page. The user password is hashed and stored in the database, as well as the username and id. For the purpose of this final project, I decided to not include any e-mail functionality. Though that would certainly be the next step if this ever gets a release elsewhere.

<details>
  <summary>Code</summary>

```PY
# Safety checks
if not request.form.get("username"):
    return render_template("error.html", message="Must provide username.")

if not request.form.get("password") or not request.form.get("confirmation"):
    return render_template("error.html", message="Must provide password and confirmation.")

if not request.form.get("password") == request.form.get("confirmation"):
    return render_template("error.html", message="Password does not match confirmation.")

check = db_query("users", "SELECT * FROM users WHERE username = '{}'".format(request.form.get("username")))
if not len(check) == 0:
    return render_template("error.html", message="Username already exists.")

# If everything passed, register the user.
db_insert("INSERT INTO users (username, hash) VALUES ('{0}', '{1}')".format(request.form.get(
    "username"), generate_password_hash(request.form.get("password"), method="pbkdf2:sha256", salt_length=8)))

return redirect("/")
```

</details>

##### **5.1.3.17. review_kanji.html** &
##### **5.1.3.18. review_radicals.html** &
##### **5.1.3.19. review_words.html**

The review sessions for kanji, radicals and words. Before the page is displayed, the app route will check if there are any items to review. If not, there will only be a message. If yes, the items to be reviewed will be randomized and put into a list, that will be handed to JavaScript. The data is then handed back and forth between JavaScript and flask via JSON. If the users answers quality is too low, the review will come again in this session. Once a review is done, it will be kicked off the current list. Once all reviews are done, the app route will calculate when every reviewed item is due next, using the users answers for every single review. Then the data is updated in the database, and the session is finished. If the user does not finish the session, the data is not stored and the session starts over the next time the user visits the page again.

In order to handle all the data back and forth, most of it is handled to JavaScript via jinja "tojson". This does not look very nice when the html is inspected, but works on the users end beautifully. In the future, if I learn of better ways to do this, this would definitely be a point to improve on.

Because these are all very similar, I will only talk about review_kanji in detail.

<details>
  <summary>Code explanation</summary>

The reveal functions ultimate purpose is to reveal the data the user is trying to recall, but it also serves as a safeguard.
There were some issues with pressing buttons twice quickly or pressing before JS had finished loading, so now the reveal
function also works to remove the disabled attribute that the other function puts in place.

```JS
function reveal() {
  for (var j = 0; j < 6; j++) {
    document.getElementById('ef-' + j).removeAttribute('disabled');
    document.getElementById('ef-' + j).style.display = "inline";
  }

  for (var j = 1; j < 6; j++) {
    document.getElementById('review-field' + j).style.display = "inline";
  }

  document.getElementById('ef-exp').style.display = "inline";
  document.getElementById('review-title1').style.display = "inline";
  document.getElementById('review-reveal').style.display = "none";
}
```

The getData function is used in every iteration of study or review content pages, but depending on content it varies in several places so I opted to put it on the actual html page in order to better keep track of what each function needs for which content. This is one example. This is the function used in kanji reviews.

The immediate setting of the attribute disabled is meant as a safeguard to prevent the user from pressing any buttons before all content has loaded. A counter will keep track of where the user is at so that different things can happen once the user has gone through the content once. In reviews, a review that the user has evaluated at 4 or 5 is considered finished. okcheck is an array meant to keep track of which review is finished and which has to come around again. If a review is marked "ok" it will not come back. Reviews will continue until all are marked ok. The efValue is used in the supermemo calculation. It only counts the first answer for every review per session and hands it to flask later to calculate the new E-Factor for that specific item.
Then, the data is handed to flask and new data is called by fetch and all required fields are updated. Once all data is loaded, buttons that are needed are enabled again.

```JS
var efValue = [];
var okCheck = [];
var counter = 0;
var second = 0;

function getData(listNo, action) {
  document.getElementById('strokesbutton').setAttribute("disabled", "");
  document.getElementById('colorbutton').setAttribute("disabled", "");
  for (var j = 0; j < 6; j++) {
    document.getElementById('ef-' + j).setAttribute("disabled", "");
  }

  counter = counter + 1;
  var id = parseInt(document.getElementById("studyid").innerHTML);

  if (second == 0) {
    efValue.push(action);
    if (action == "5" || action == "4") {
      okCheck.push("ok");
    }
    else {
      okCheck.push("");
    }

  }
  else {
    if (action == "5" || action == "4") {
      okCheck[id] = "ok";
    }
  }

  if (counter == {{ max }}) {
    second = 1;
    counter = 0;
  }

  let url = "/review_kanji";
  let data = { "number": listNo, "okcheck": okCheck, "efvalue": efValue, "max": {{ max }}, "reviewlist": {{ reviewlist|tojson }}};
  fetch(url, {
    "method": "POST",
    "headers": {"Content-Type": "application/json"},
    "body": JSON.stringify(data),
  }).then(response => response.json())
  .then(data => {
    console.log(data);
    if (data == "done") {
      document.getElementById('everything').style.display = "none";
      document.getElementById('finished').style.display = "block";
    }

    for (var j = 0; j < 6; j++) {
      document.getElementById('ef-' + j).style.display = "none";
      var value = "getData('" + data[0] + "', '" + j + "')";
      document.getElementById('ef-' + j).setAttribute("onclick", value);
    }

    for (var j = 1; j < 6; j++) {
      document.getElementById('review-field' + j).style.display = "none";
    }

    document.getElementById('ef-exp').style.display = "none";
    document.getElementById('review-title1').style.display = "none";
    document.getElementById('review-reveal').style.display = "inline";
    document.getElementById('svgbtntitle').innerHTML = data[9];
    document.getElementById('review-title1').innerHTML = data[5];
    document.getElementById('review-field1').innerHTML = data[3];
    document.getElementById('review-field2').innerHTML = data[4];
    document.getElementById('review-field3').innerHTML = data[7];
    document.getElementById('review-field4').innerHTML = data[8];
    document.getElementById('review-field5').innerHTML = data[6];
    document.getElementById('titlelabel').innerHTML = "No: " + data[1]
    document.getElementById('studyid').innerHTML = data[0];
    document.getElementById('strokesbutton').removeAttribute('disabled');
    document.getElementById('colorbutton').removeAttribute('disabled');
  })

  .catch((err) => console.log("Access failed: " + url + " Reason: " + err));
}
```

On the python side of things, first the app will calculate what reviews are due today and then format them to hand them over to jinja and JavaScript. The study list is made by getting the list of all content to review, make sure its not more than what the user settings allow for, and then gathering additional data, such as radical data and svg data for kanji. The list is randomized so the user does not see the same content in the same order every time.

```PY
first = []
reviewlist = []
review = ""
max = 0
# Check user data regarding kanji reviews
user_data = db_query("users", "SELECT last_kanji_review, rev_int FROM users WHERE id = '{}'".format(session["user_id"]))
today = date.today()

# Check if kanji have already been reviewed today
reviewlimit = check_session(str(user_data[0][0]))

# If kanji have not been reviewed, check if there are kanji to review
if reviewlimit == "no":
    kanji = db_query("users", "SELECT type_id, date_due FROM study WHERE type = 'kanji' AND user_id = '{0}' AND date_due <= '{1}'".format(
        session["user_id"], today))

    # If there were no results:
    if not kanji:
        review = "done"

    else:
        # Append all entries to a list
        list = []
        review = "notdone"
        for entry in kanji:
            list.append(entry[0])

        # Break the list up into the maximum review settings set by the user
        parts = [list[x:x+int(user_data[0][1])] for x in range(0, len(list), int(user_data[0][1]))]
        query = f"SELECT id, kanji, onyomi, kunyomi, meaning, radical_id, grade, jlpt, unicode FROM kanji WHERE id IN ({','.join(['{}']*len(parts[0]))})".format(
            *parts[0])
        temp = db_query("dict", query)

        # Create the review list from the queried reviews
        for row in temp:
            # Look up the radical for the current kanji
            radical = db_query("dict", "SELECT title FROM radicals WHERE id = '{}'".format(row[5]))
            # Look up the svg for the current kanji
            svg = db_query(
                "dict", "SELECT svg_black, svg_color, svg_strokes FROM strokeorder WHERE kanji_unicode = '{}'".format(row[8]))
            # Build the list
            list = [row[0], row[1], row[2], row[3], row[4], radical[0][0], row[6], row[7], svg[0][0], svg[0][1], svg[0][2]]
            reviewlist.append(list)

        # Shuffle the list so the kanji do not come in the order in which they were first presented
        random.shuffle(reviewlist)
        for i in range(len(reviewlist)):
            reviewlist[i].insert(0, i)

        # Append a number to the beginning of each list entry
        first.append(reviewlist[0])
        max = len(reviewlist)
else:
    review = "done"

return render_template("review_kanji.html", review=review, first=first, reviewlist=reviewlist, max=max)
```

If the user is currently reviewing, python gets data from JavaScript and hands some data back. A numberlist will be created that keeps track of what numbers of the original review list are still in the circulation. All items that have an "ok" in okcheck are removed from that list.
The new_number function will make sure the next data handed is not already finished, it also keeps track of what is the last item in the current list. Necessary data is assembled and handed back to JavaScript.
Once the numberlist is empty, the study session is completed. The new E-Factor of each item is calculated based on the efvalue handed over by JavaScript. The super_memo function calculates the new values to be stored. The user database is updated and the session finishes.

```PY
# Get the data from the study progress
jsonData = request.get_json()
number = int(jsonData["number"])
reviewlist = jsonData["reviewlist"]
max = jsonData["max"]
okcheck = jsonData["okcheck"]
efvalue = jsonData["efvalue"]

# Create a list of numbers equal to the number of items the user is studying
numberlist = [*range(max)]

# Check if any items are already finished and remove the entry from the list
for i in range(len(okcheck)):
    if okcheck[i] == "ok":
        if i in numberlist:
            numberlist.remove(i)

# Once the list is empty, the user is done studying
if not numberlist:
    for i in range(max):
        # Update the user DB according to the supermemo method
        data = db_query("users", "SELECT ef, review_count FROM study WHERE type = 'kanji' AND user_id = '{0}' AND type_id = '{1}'".format(
            session["user_id"], reviewlist[i][1]))
        # Calculate new ef, new interval and the new due date by calling the super_memo function
        new_e, new_n, due_date = super_memo(data[0][0], data[0][1], int(efvalue[i]))
        db_insert("UPDATE study SET ef = '{0}', review_count = '{1}', date_due = '{2}' WHERE type = 'kanji' AND user_id = '{3}' AND type_id = '{4}'".format(
            new_e, new_n, due_date, session["user_id"], reviewlist[i][1]))
    today = date.today()
    db_insert("UPDATE users SET last_kanji_review = '{0}' WHERE id = '{1}'".format(today, session["user_id"]))

    # The review session is finished
    data = "done"
    return jsonify(data)

# Determine the next number using the function
number = new_number(numberlist, number)

# Get SVG data
svgdata = create_svg(reviewlist[number][9], reviewlist[number][10], reviewlist[number][11])

# Return review data
data = [reviewlist[number][0], reviewlist[number][1], reviewlist[number][2], reviewlist[number][3], reviewlist[number][4], reviewlist[number][5], reviewlist[number][6],
        reviewlist[number][7], reviewlist[number][8], svgdata]

return jsonify(data)
```

</details>

##### **5.1.3.21. search.html**

The search page, making use of the perform_search function. The user can type anything in the search bar on top, and the database will look for the search term in radicals, kanji and word tables. The user can search for Japanese terms in either kanji, hiragana or katakana, as well as search for English. One minor flaw is that if the user looks for something like "eat", things like "heat" will also be displayed. Unfortunately I did not manage to figure out how to make the search more accurate. All verbs are stored with "to" however, so the user could search for "to eat" to get more specific results. This however only applies to search terms in English. Japanese search terms do not have that issue. Please see the section for functions.py to find more info about how the search is performed.

<details>
  <summary>Code</summary>

```PY
# Take the users search input
search = request.form.get("search")

# If no search term was entered, hand empty results to prevent error
if not search:
    vocabulary = []
    radical = []
    kanji = []
    return render_template("search.html", search=search, vocabulary=vocabulary, radical=radical, kanji=kanji)

# If a search term was entered, perform valid search
else:
    # combine the searchterm in different arrangements in order to find all relevant kanji and radical and word combinations
    vocabulary = perform_search(search, "word")
    radical = perform_search(search, "radical")
    kanji = perform_search(search, "kanji")

    return render_template("search.html", search=search, vocabulary=vocabulary, radical=radical, kanji=kanji)
```

</details>

##### **5.1.3.22. study_kana.html**

The study page for kana. It will display a table for all hiragana and a table for all katakana words in YYK. Due to the data being insufficient on that part, it was unfortunately not possible to integrate these words with the other words that contain kanji, in order to study everything together. The problem was to figure out when to study what word, but most of the hiragana and katakana words were pulled with incorrect JLPT assignments. (I assume the assignments did not exist on the website, as there are NO official vocabulary lists for the JLPT available) This could very well be adjusted for any future release, but would have absolutely exceeded the scope of this app as a final project for CS50, as it would have taken way too much time for not that much return.

For now, if any user is interested in these words, they can take a look at the table and study the ones they feel are useful.

<details>
  <summary>SQL</summary>

```PY
hiragana = db_query("dict", "SELECT word, reading, meaning, jlpt FROM vocabulary WHERE category = 'hiragana' ORDER BY reading")
katakana = db_query("dict", "SELECT word, reading, meaning, jlpt FROM vocabulary WHERE category = 'katakana' ORDER BY reading")

return render_template("study_kana.html", hiragana=hiragana, katakana=katakana)
```

</details>

##### **5.1.3.23. study_kanji.html** &
##### **5.1.3.24. study_words.html**

The user can study new kanji or words here. When the user goes to the page, YYK will check their session settings and load the amount of content the user wants to study. Then, in the case of kanji, YYK will check if the radical is already known. If not, the radical will be displayed before the kanji. This means that, while the number of kanji to study is set by the user, the number of radicals that will appear depends on what kanji are coming up. For both kanji and words, the user will be presented with each new entry once, and upon clicking "Next" on each entry once, they will see each entry a second time. This time they can decide whether to see it again during this session or if they are satisfied and think they have learned it for now. If the user clicks "Got it" then the entry will not be shown again for this time and the app route adjusts the study list appropriately. Data is handed back and forth between flask and JavaScript via JSON and fetch. Once the user has clicked "Got it" on all entries, the app route will record the users newly studied content in the database, to be reviewed in the next review session.

In order to handle all the data back and forth, most of it is handled to JavaScript via jinja "tojson". This does not look very nice when the html is inspected, but works on the users end beautifully. In the future, if I learn of better ways to do this, this would definitely be a point to improve on. Since kanji and words are handled very similarly, I will only look at kanji in detail here.

<details>
  <summary>Code explanation</summary>

Just as in the review section, the reveal function will be called on the second round of a study session. It's main function is to reveal the data the user is supposed to memorize, but it also functions as a safeguard. It will remove the disabled state set by the other function in order to keep the user from pushing buttons too early.

```JS
function reveal() {
document.getElementById('again').removeAttribute('disabled');
document.getElementById('gotit').removeAttribute('disabled');
document.getElementById('again').style.display = "inline";
document.getElementById('gotit').style.display = "inline";
for (var j = 1; j < 4; j++) {
    document.getElementById('field' + j).style.display = "inline";
}

document.getElementById('title1').style.display = "inline";
document.getElementById('reveal').style.display = "none";
}
```

getData also works very similar to reviews, but it does not have to keep track of any efvalues. While handing the data back and forth between JavaScript and python, this function will make sure that every new study item is viewed once, and then for every item that is shown after, the user needs to decide if they want to see this item again in this session or not. For every item, the data is fetched and the correct fields are updated. For Kanji and Radicals, these fields vary so a bit more updating is needed than for words. Once all items are marked "ok" via toStudy, the session is finished.

```JS
var toStudy = [];
var counter = 0;
var second = 0;

function getData(listNo, action) {
document.getElementById('strokesbutton').setAttribute("disabled", "");
document.getElementById('colorbutton').setAttribute("disabled", "");
counter = counter + 1
var id = parseInt(document.getElementById("studyid").innerHTML);
if (counter == {{ max }}) {
    counter = 0;
    second = 1;
}

if (action == "next") {
    document.getElementById('next').setAttribute("disabled", "");
    toStudy.push("");
}
else if (action == "gotit") {
    document.getElementById('gotit').setAttribute("disabled", "");
    document.getElementById('again').setAttribute("disabled", "");
    toStudy[id] = "ok";
}
else {
    document.getElementById('gotit').setAttribute("disabled", "");
    document.getElementById('again').setAttribute("disabled", "");
}

let url = "/study_kanji";
let data = { "number": listNo, "okcheck": toStudy, "max": {{ max }}, "studylist": {{ studylist|tojson }}};
fetch(url, {
    "method": "POST",
    "headers": {"Content-Type": "application/json"},
    "body": JSON.stringify(data),
}).then(response => response.json())
.then(data => {
    console.log(data);
    if (data == "done") {
    document.getElementById('everything').style.display = "none";
    document.getElementById('finished').style.display = "block";
    }

    if (second == 1) {
    document.getElementById('next').style.display = "none";
    document.getElementById('again').style.display = "none";
    document.getElementById('gotit').style.display = "none";
    for (var j = 1; j < 4; j++) {
        document.getElementById('field' + j).style.display = "none";
    }

    document.getElementById('title1').style.display = "none";
    document.getElementById('reveal').style.display = "inline";
    }

    if (data[1] == "radical") {
    document.getElementById('label1').innerHTML = "Name";
    document.getElementById('label2').innerHTML = "Group";
    document.getElementById('label3').innerHTML = "Strokes";
    document.getElementById('label4').innerHTML = "All variations";
    document.getElementById('label5').innerHTML = "";
    document.getElementById('typehead').innerHTML = "New radical";
    document.getElementById('svgbtntitle').innerHTML = data[3];
    document.getElementById('svgtogglebuttons').style.display = "none";
    document.getElementById('title1').innerHTML = data[6];
    document.getElementById('field1').innerHTML = data[5];
    document.getElementById('field2').innerHTML = data[7];
    document.getElementById('field3').innerHTML = data[8];
    document.getElementById('field4').innerHTML = data[4];
    document.getElementById('field5').innerHTML = "";
    }
    else {
    document.getElementById('label1').innerHTML = "On-yomi";
    document.getElementById('label2').innerHTML = "Kun-yomi";
    document.getElementById('label3').innerHTML = "Grade";
    document.getElementById('label4').innerHTML = "JLPT";
    document.getElementById('label5').innerHTML = "Radical";
    document.getElementById('typehead').innerHTML = "New kanji";
    document.getElementById('svgbtntitle').innerHTML = data[14];
    document.getElementById('svgtogglebuttons').style.display = "inline";
    document.getElementById('title1').innerHTML = data[6];
    document.getElementById('field1').innerHTML = data[4];
    document.getElementById('field2').innerHTML = data[5];
    document.getElementById('field3').innerHTML = data[11];
    document.getElementById('field4').innerHTML = data[12];
    document.getElementById('field5').innerHTML = data[8];
    }

    document.getElementById('titlelabel').innerHTML = "No: " + data[2]
    document.getElementById('studyid').innerHTML = data[0];
    if (second == 0) {
    let nextData = "getData('" + data[0] + "', 'next')";
    document.getElementById('next').setAttribute("onclick", nextData);
    }
    else {
    let againData = "getData('" + data[0] + "', 'again')";
    document.getElementById('again').setAttribute("onclick", againData);
    let gotItData = "getData('" + data[0] + "', 'gotit')";
    document.getElementById('gotit').setAttribute("onclick", gotItData);
    }

    document.getElementById('next').removeAttribute('disabled');
    document.getElementById('strokesbutton').removeAttribute('disabled');
document.getElementById('colorbutton').removeAttribute('disabled');
})

.catch((err) => console.log("Access failed: " + url + " Reason: " + err));
}
```

On the python side, after checking if we need to study at all, first of all we need to assemble all new items for study. If we study kanji, the app will check for all unknown radicals and place them before their kanji for each session.
Basically, the app will check for new kanji based on the users settings, then check for radicals every time, and add the radical only if it is unknown. Every item is added to a list to be handed to JavaScript for studying. At the end, a counter is added so all items to study in one session are numbered.

```PY
# Set some variables to base settings, change them as needed througout this check
studylist = []
max = 0
first = []
# Check userdata for last study sessions
user_data = db_query(
    "users", "SELECT last_kanji_study, last_word_study, last_kanji, kan_int FROM users WHERE id = '{}'".format(session["user_id"]))
kanjistudy, wordstudy, words = check_study(user_data[0][0], user_data[0][1], user_data[0][2])

if kanjistudy == "yes":
    # Get the kanji the user has to study
    kanji = db_query("dict", "SELECT id, kanji, onyomi, kunyomi, meaning, radical_id, strokecount, grade, jlpt, unicode FROM kanji WHERE id > '{0}' ORDER BY id ASC LIMIT '{1}'".format(
        user_data[0][2], user_data[0][3]))

    # Combine a list to study from Kanji and possible radicals
    for row in kanji:
        # Get the svg data for that kanji
        svg = db_query(
            "dict", "SELECT svg_black, svg_color, svg_strokes FROM strokeorder WHERE kanji_unicode = '{}'".format(row[9]))
        # Get the radical for that kanji
        radical = db_query(
            "dict", "SELECT id, title, radical, name, english, radical_group, strokecount FROM radicals WHERE id = '{}'".format(row[5]))
        # Check if that radical is already known
        known = db_query("users", "SELECT type_id FROM study WHERE user_id = '{0}' AND type_id = '{1}' AND type = 'radical'".format(
            session["user_id"], row[0]))
        # If the radical is not yet in the users study records
        if not known:
            # Prepare the radical
            newradical = ["radical", radical[0][0], radical[0][1], radical[0]
                            [2], radical[0][3], radical[0][4], radical[0][5], radical[0][6]]
            # If the radical has not been added yet in the current check
            if newradical not in studylist:
                studylist.append(newradical)
        # Prepare the kanji
        newkanji = ["kanji", row[0], row[1], row[2], row[3], row[4], radical[0][0], radical[0]
                    [1], radical[0][3], row[6], row[7], row[8], row[9], svg[0][0], svg[0][1], svg[0][2]]
        studylist.append(newkanji)
    # Iterate over the list and numerate all items
    counter = 0
    for list in studylist:
        list.insert(0, counter)
        counter = counter + 1
    first.append(studylist[0])
    max = len(studylist)

return render_template("study_kanji.html", studylist=studylist, first=first, max=max, kanjistudy=kanjistudy, wordstudy=wordstudy, words=words)
```

If the session is already underway, python and JavaScript hand data back and forth.
Similar to the review part, there is a numberlist that checks which items from the studylist are done (marked "ok" by the user) and which are not. All items that are finished are removed from the numberlist, so if the list is empty, that means the study session is finished. The SuperMemo 2 method states that all newly reviewed items get the same values, so nothing needs to be calculated at this point. The study entry in the users.db database for every item will first be created at this point. In subsequent reviews, this item will just be updated. The downside of this is that with more users, the more they study, the bigger the database grows. It may be more prudent to have these items set already for each user and only changed so the database size itself stays the same. For the purposes of this final project, I decided against bloating the database for now.

```PY
# Get the data from the study progress
jsonData = request.get_json()
number = int(jsonData["number"])
studylist = jsonData["studylist"]
max = jsonData["max"]
okcheck = jsonData["okcheck"]

# Create a list of numbers equal to the number of items the user is studying
numberlist = [*range(max)]

# Check if any items are already finished and remove the entry from the list
for i in range(len(okcheck)):
    if okcheck[i] == "ok":
        if i in numberlist:
            numberlist.remove(i)

# Once the list is empty, the user is done studying
if not numberlist:
    # Check todays date and get tomorrows date as well
    today = date.today()
    tomorrow = date.today() + timedelta(days=1)
    for entry in studylist:
        # Insert radical data into the user database
        if entry[1] == "radical":
            db_insert("UPDATE users SET last_radical = '{0}' WHERE id = '{1}'".format(entry[2], session["user_id"]))
            db_insert("INSERT INTO study (type, type_id, user_id, first_seen, review_count, date_due) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(
                entry[1], entry[2], session["user_id"], today, 1, tomorrow))
        # Insert kanji data into the user database
        else:
            db_insert("UPDATE users SET last_kanji = '{0}' WHERE id = '{1}'".format(entry[2], session["user_id"]))
            db_insert("INSERT INTO study (type, type_id, user_id, first_seen, review_count, date_due) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(
                entry[1], entry[2], session["user_id"], today, 1, tomorrow))
    db_insert("UPDATE users SET last_kanji_study = '{0}' WHERE id = '{1}'".format(today, session["user_id"]))

    # The study session is finished
    data = "done"
    return jsonify(data)

# Determine the next number using the function
number = new_number(numberlist, number)

# If the current item is a radical
if studylist[number][1] == "radical":
    title = "<h5 class=\"card-title main-symbol\">" + studylist[number][3] + "</h5>"
    data = [studylist[number][0], studylist[number][1], studylist[number][2], title, studylist[number]
            [4], studylist[number][5], studylist[number][6], studylist[number][7], studylist[number][8], numberlist]

# If the current item is a kanji
else:
    # Get SVG data
    svgdata = create_svg(studylist[number][14], studylist[number][15], studylist[number][16])

    data = [studylist[number][0], studylist[number][1], studylist[number][2], studylist[number][3], studylist[number][4], studylist[number][5], studylist[number][6],
            studylist[number][7], studylist[number][8], studylist[number][9], studylist[number][10], studylist[number][11], studylist[number][12], studylist[number][13], svgdata]

return jsonify(data)
```

</details>

##### **5.1.3.25. study.html**

The front page for new study. On page request, YYK will check what the user currently has to study. If there is still kanji study to do and all word study is complete, then kanji study will be available. If there is still word study to do, then no kanji study will be available. If there are no more words to study, but the last word study happened on that day, then there will be no new kanji study for that day. If the user manually enters the url for any of the study pages, the page will display a message appropriate to the users current study status.

There is also the option to study kana words. This option is independent from the other study options, as there are no records to keep and the users can study kana words, if they want, on their own pace.

As YYK focuses on kanji and words containing kanji, kana words are just a minor addon.

<details>
  <summary>Code</summary>

```PY
# Check the user data
user_data = db_query(
    "users", "SELECT last_kanji_study, last_word_study, last_kanji FROM users WHERE id = '{}'".format(session["user_id"]))
# Use the check study function to determine what needs to be studied
kanjistudy, wordstudy, words = check_study(user_data[0][0], user_data[0][1], user_data[0][2])

return render_template("study.html", kanjistudy=kanjistudy, wordstudy=wordstudy, words=words)
```

</details>

##### **5.1.3.26. vocabulary_list.html**

The vocabulary_list is the GET route of the /vocabulary app route. It is a (very big) table of all vocabulary entries in the YYK database, of which there are 17685. This table takes a while to load and is not very practical, but I just liked the idea of having it all in one place at least once. I decided to break it down in several smaller pieces so the user can load only what is needed, but that took even longer to load and didn't work well. So the compromise for now, in order to have any vocabulary list at all, is this list.

The user can sort either by kana (what would be alphabetical in English) or by JLPT level.

<details>
  <summary>SQL</summary>

```PY
vocabulary_kana = db_query("dict", "SELECT word, reading, meaning, jlpt FROM vocabulary ORDER BY reading")
vocabulary_jlpt = db_query("dict", "SELECT word, reading, meaning, jlpt FROM vocabulary ORDER BY jlpt DESC, reading ASC")

return render_template("vocabulary_list.html", kana=vocabulary_kana, jlpt=vocabulary_jlpt)
```

</details>

##### **5.1.3.27. vocabulary.html**

The POST method of the /vocabulary route. The user can reach this by clicking on a vocabulary entry in different locations, such as the kanji page or the vocabulary list. The user can see the meaning, reading, as well as the different kanji of which a word is composed. The user can also listen to the pronunciation as generated by flask-gTTs on the fly.

<details>
  <summary>Code</summary>

```PY
word = request.form.get("vocabulary")
# Get the information for this word
lookup = "SELECT word, reading, meaning, jlpt FROM vocabulary WHERE word = \"" + word + "\";"
lookup = db_query("dict", lookup)
# Get the list of kanji
kanji = db_query("dict", "SELECT kanji FROM kanji ORDER BY id")

# Separate each kanji in the word to be able to look them up individually
kanjistring = ""
for i in kanji:
    if i[0] in word:
        kanjistring += i[0]

return render_template("vocabulary.html", lookup=lookup, kanjistring=kanjistring)
```
</details>

#### **5.1.4. static**

##### **5.1.4.1. script.js**

Some scripts that toggle certain things from being visible or invisible. There are many other scripts in the various html files, but some of them would not work in the separate .js file because some of their content was handed to them with jinja.
It contains toggleStrokes(), toggleColor(), toggleGrade(), toggleKanjiJlpt(), toggleHiragana(), toggleKatakana(), toggleStats(), toggleSet(), toggleVocabJlpt(), toggleKana(), sortStrokes(), sortGrade() and sortJlpt(). Basically, there is a lot of toggling going on.

##### **5.1.4.2. styles.css**

Some edited style sheets, mostly to keep some things invisible that the user is not supposed to initially see. There are only a few minor adjustments to some other things.

##### **5.1.4.3. img - Calligraphy**

My wife was kind enough to write the Japanese words for some of the menu entries, like Study, Review, Kanji, Vocabulary, Kana, Radical. I digitized and edited it using gimp, for use in this app.

##### **5.1.4.4. mp3 - gTTs**

While some text-to-speech data is created by flask-gTTs on the fly, specifically the pronunciation of words, the pronunciation of kana was generated by me prior to creating the app. As there are only 106 different sounds to pronounce, and the mp3 files are quite short and small, I decided on saving those and loading them from the folder instead of generating them with flask-gTTs every time. In general, temporarily created mp3s for study or review sessions are deleted by the app route, and otherwise created mp3s are deleted on session end.

CS50x 2022 Final Project - Yes, you Kanji! - 2022 - Michanoku - Michael Werker
