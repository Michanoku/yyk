from functools import wraps
from flask import session, redirect
from datetime import date, datetime, timedelta
import math
from database import db_query


# Enable functionality to require login on certain pages
def login_required(f):
    # As per https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


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