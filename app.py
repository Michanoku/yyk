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

# Configuration
app = Flask(__name__)
gtts(app)

# Template auto reload
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Use filesystem for session instead of cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# The index page
@app.route("/")
def index():
    return render_template("index.html")


# The user registration page
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

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

    # If not POST but GET
    else:
        return render_template("register.html")


# The user login page
@app.route("/login", methods=["GET", "POST"])
def login():

    # Clear the session
    session.clear()

    # If the method is post, attempt to login the user
    if request.method == "POST":

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

    # If the method is get, display login page
    else:
        return render_template("login.html")


# The logout function
@app.route("/logout")
def logout():

    # Clear the session
    session.clear()

    return redirect("/")


# The profile page
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

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


# The search page
@app.route("/search", methods=["POST"])
def search():
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


# The study page
@app.route("/study", methods=["GET"])
@login_required
def study_screen():
    # Check the user data
    user_data = db_query(
        "users", "SELECT last_kanji_study, last_word_study, last_kanji FROM users WHERE id = '{}'".format(session["user_id"]))
    # Use the check study function to determine what needs to be studied
    kanjistudy, wordstudy, words = check_study(user_data[0][0], user_data[0][1], user_data[0][2])

    return render_template("study.html", kanjistudy=kanjistudy, wordstudy=wordstudy, words=words)


# The study kanji page
@app.route("/study_kanji", methods=["GET", "POST"])
@login_required
def study_kanji():

    if request.method == "GET":

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

    # If the method is post
    else:

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


# The word study page
@app.route("/study_words", methods=["GET", "POST"])
@login_required
def study_words():
    # If the method is get
    if request.method == "GET":

        # Set some variables to base settings, change them as needed througout this check
        studylist = []
        max = 0
        first = []
        # Check userdata for last study sessions
        user_data = db_query(
            "users", "SELECT last_kanji_study, last_word_study, last_kanji, wrd_int FROM users WHERE id = '{}'".format(session["user_id"]))
        kanjistudy, wordstudy, words = check_study(user_data[0][0], user_data[0][1], user_data[0][2])

        if wordstudy == "yes":
            list = word_check(user_data[0][2])
            # Calculate how many words to study for this session based on user preference
            parts = [list[x:x+int(user_data[0][3])] for x in range(0, len(list), int(user_data[0][3]))]
            query = f"SELECT id, word, reading, meaning, type, jlpt FROM vocabulary WHERE id IN ({','.join(['{}']*len(parts[0]))})".format(
                *parts[0])
            temp = db_query("dict", query)

            # Assemble the study list for this
            counter = 0
            studylist = []
            for row in temp:
                list = [counter, row[0], row[1], row[2], row[3], row[4], row[5]]
                studylist.append(list)
                counter = counter + 1
            first = []
            first.append(studylist[0])
            max = len(studylist)

        return render_template("study_words.html", studylist=studylist, first=first, max=max, kanjistudy=kanjistudy, wordstudy=wordstudy, words=words)

    # If the method is post
    else:

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
                    file = "static/mp3/temp/" + str(i) + ".mp3"
                    if exists(file):
                        remove(file)

        # Once the list is empty, the user is done studying
        if not numberlist:
            today = date.today()
            tomorrow = date.today() + timedelta(days=1)
            db_insert("UPDATE users SET last_word = '{0}', last_word_study = '{1}' WHERE id = '{2}'".format(
                studylist[max - 1][1], today, session["user_id"]))
            for entry in studylist:
                db_insert("INSERT INTO study (type, type_id, user_id, first_seen, review_count, date_due) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(
                    "word", entry[1], session["user_id"], today, 1, tomorrow))
                file = "static/mp3/temp/" + str(entry[0]) + ".mp3"
                if exists(file):
                    remove(file)

            data = "done"
            return jsonify(data)

        # Determine the next number using the function
        number = new_number(numberlist, number)

        # Create mp3 file
        file = "static/mp3/temp/" + str(studylist[number][0]) + ".mp3"
        if exists(file):
            remove(file)
        tts = gTTS(studylist[number][3], lang='ja', slow='true')
        tts.save(file)

        # Wait for the file to be created
        while not exists(file):
            time.sleep(1)

        # Return study data
        data = [studylist[number][0], studylist[number][1], studylist[number][2], studylist[number]
                [3], studylist[number][4], studylist[number][5], studylist[number][6], file]

        return jsonify(data)


# The study kana words page
@app.route("/study_kana", methods=["GET"])
@login_required
def study_kana():
    hiragana = db_query("dict", "SELECT word, reading, meaning, jlpt FROM vocabulary WHERE category = 'hiragana' ORDER BY reading")
    katakana = db_query("dict", "SELECT word, reading, meaning, jlpt FROM vocabulary WHERE category = 'katakana' ORDER BY reading")

    return render_template("study_kana.html", hiragana=hiragana, katakana=katakana)


# The review page
@app.route("/review", methods=["GET"])
@login_required
def review_screen():
    # Check the user data
    user_data = db_query(
        "users", "SELECT last_radical_review, last_kanji_review, last_word_review FROM users WHERE id = '{}'".format(session["user_id"]))

    # Check what kind of reviews are to be done today using the check_reviews function
    radicalreview, kanjireview, wordreview = check_reviews(user_data[0][0], user_data[0][1], user_data[0][2])

    return render_template("review.html", radicalreview=radicalreview, kanjireview=kanjireview, wordreview=wordreview)


# The radical review page
@app.route("/review_radicals", methods=["GET", "POST"])
@login_required
def review_radicals():

    # If the method is get
    if request.method == "GET":
        first = []
        reviewlist = []
        review = ""
        max = 0
        # Check user data regarding radical reviews
        user_data = db_query("users", "SELECT last_radical_review, rev_int FROM users WHERE id = '{}'".format(session["user_id"]))
        today = date.today()

        # Check if radicals have already been reviewed today
        reviewlimit = check_session(str(user_data[0][0]))

        # If radicals have not been reviewed, check if there are radicals to review
        if reviewlimit == "no":
            radicals = db_query("users", "SELECT type_id, date_due FROM study WHERE type = 'radical' AND user_id = '{0}' AND date_due <= '{1}'".format(
                session["user_id"], today))

            # If there were no results:
            if not radicals:
                review = "done"

            else:
                # Append all entries to a list
                list = []
                review = "notdone"
                for entry in radicals:
                    list.append(entry[0])

                # Break the list up into the maximum review settings set by the user
                parts = [list[x:x+int(user_data[0][1])] for x in range(0, len(list), int(user_data[0][1]))]
                query = f"SELECT id, title, radical, name, english, radical_group, strokecount, unicode FROM radicals WHERE id IN ({','.join(['{}']*len(parts[0]))})".format(
                    *parts[0])
                temp = db_query("dict", query)

                # Create the review list from the queried reviews
                for row in temp:
                    # Build the list
                    list = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]]
                    reviewlist.append(list)

                # Shuffle the list so the radicals do not come in the order in which they were first presented
                random.shuffle(reviewlist)
                for i in range(len(reviewlist)):
                    reviewlist[i].insert(0, i)

                # Append a number to the beginning of each list entry
                first.append(reviewlist[0])
                max = len(reviewlist)
        else:
            review = "done"

        return render_template("review_radicals.html", review=review, first=first, reviewlist=reviewlist, max=max)

    # If the method is post
    else:
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
                data = db_query("users", "SELECT ef, review_count FROM study WHERE type = 'radical' AND user_id = '{0}' AND type_id = '{1}'".format(
                    session["user_id"], reviewlist[i][1]))
                # Calculate new ef, new interval and the new due date by calling the super_memo function
                new_e, new_n, due_date = super_memo(data[0][0], data[0][1], int(efvalue[i]))
                db_insert("UPDATE study SET ef = '{0}', review_count = '{1}', date_due = '{2}' WHERE type = 'radical' AND user_id = '{0}' AND type_id = '{1}'".format(
                    new_e, new_n, due_date, session["user_id"], reviewlist[i][1]))
            today = date.today()
            db_insert("UPDATE users SET last_radical_review = '{0}' WHERE id = '{1}'".format(today, session["user_id"]))

            # The review session is finished
            data = "done"
            return jsonify(data)

        # Determine the next number using the function
        number = new_number(numberlist, number)

        # Return review data
        data = [reviewlist[number][0], reviewlist[number][1], reviewlist[number][2], reviewlist[number][3], reviewlist[number][4], reviewlist[number][5], reviewlist[number][6],
                reviewlist[number][7]]

        return jsonify(data)


# The kanji review page
@app.route("/review_kanji", methods=["GET", "POST"])
@login_required
def review_kanji():

    # If the method is get
    if request.method == "GET":
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

    # If the method is post
    else:

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


# The review words page
@app.route("/review_words", methods=["GET", "POST"])
@login_required
def review_words():
    # If the method is get
    if request.method == "GET":
        first = []
        reviewlist = []
        review = ""
        max = 0
        # Check user data regarding word reviews
        user_data = db_query("users", "SELECT last_word_review, rev_int FROM users WHERE id = '{}'".format(session["user_id"]))
        today = date.today()

        # Check if words have already been reviewed today
        reviewlimit = check_session(str(user_data[0][0]))

        # If words have not been reviewed, check if there are words to review
        if reviewlimit == "no":
            words = db_query("users", "SELECT type_id, date_due FROM study WHERE type = 'word' AND user_id = '{0}' AND date_due <= '{1}'".format(
                session["user_id"], today))

            # If there were no results:
            if not words:
                review = "done"

            else:
                # Append all entries to a list
                list = []
                review = "notdone"
                for entry in words:
                    list.append(entry[0])

                # Break the list up into the maximum review settings set by the user
                parts = [list[x:x+int(user_data[0][1])] for x in range(0, len(list), int(user_data[0][1]))]
                query = f"SELECT id, word, reading, meaning, type, jlpt FROM vocabulary WHERE id IN ({','.join(['{}']*len(parts[0]))})".format(
                    *parts[0])
                temp = db_query("dict", query)

                # Assemble the study list for this
                for row in temp:
                    list = [row[0], row[1], row[2], row[3], row[4], row[5]]
                    reviewlist.append(list)

                # Shuffle the list so the kanji do not come in the order in which they were first presented
                random.shuffle(reviewlist)
                for i in range(len(reviewlist)):
                    reviewlist[i].insert(0, i)

                # Get the first item and check the length of the list
                first.append(reviewlist[0])
                max = len(reviewlist)
        else:
            review = "done"

        return render_template("review_words.html", review=review, first=first, reviewlist=reviewlist, max=max)

    # If the method is post
    else:

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
                    file = "static/mp3/temp/" + str(i) + ".mp3"
                    if exists(file):
                        remove(file)

        # Once the list is empty, the user is done studying
        if not numberlist:
            for i in range(max):
                # Update the user DB according to the supermemo method
                data = db_query("users", "SELECT ef, review_count FROM study WHERE type = 'word' AND user_id = '{0}' AND type_id = '{1}'".format(
                    session["user_id"], reviewlist[i][1]))
                # Calculate new ef, new interval and the new due date by calling the super_memo function
                new_e, new_n, due_date = super_memo(data[0][0], data[0][1], int(efvalue[i]))
                db_insert("UPDATE study SET ef = '{0}', review_count = '{1}', date_due = '{2}' WHERE type = 'word' AND user_id = '{3}' AND type_id = '{4}'".format(
                    new_e, new_n, due_date, session["user_id"], reviewlist[i][1]))
            today = date.today()
            db_insert("UPDATE users SET last_word_review = '{0}' WHERE id = '{1}'".format(today, session["user_id"]))

            # The review session is finished
            data = "done"
            return jsonify(data)

        # Determine the next number using the function
        number = new_number(numberlist, number)

        # Return study data
        file = "static/mp3/temp/" + str(reviewlist[number][0]) + ".mp3"
        if exists(file):
            remove(file)
        tts = gTTS(reviewlist[number][3], lang='ja', slow='true')
        tts.save(file)

        # Wait for the file to be created
        while not exists(file):
            time.sleep(1)

        data = [reviewlist[number][0], reviewlist[number][1], reviewlist[number][2], reviewlist[number]
                [3], reviewlist[number][4], reviewlist[number][5], reviewlist[number][6], file]

        return jsonify(data)


# The kana page
@app.route("/kana", methods=["GET"])
def kana():
    return render_template("kana.html")


# The study page for kana
@app.route("/kana_study", methods=["GET", "POST"])
def study():
    # If the method is get, open the desired kana page
    if request.method == "GET":
        target = request.args.get("study")

        mono, di, monodia, didia, syllabary = get_kana(target)

        # Pick the first card to be shown
        card = [mono[0][0], mono[0][1], mono[0][2]]
        return render_template("kana_study.html", mono=mono, di=di, monodia=monodia, didia=didia, syllabary=syllabary, card=card)

    # If the user requested by post (meaning he is selecting a different kana)
    else:
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


# The review page for kana
@app.route("/kana_review", methods=["GET", "POST"])
def review():

    if request.method == "GET":
        # First, check what we are reviewing, hiragana or katakana, and query the correct data
        target = request.args["review"]
        if target == "hiragana":
            syllabary = "Hiragana"
            temp = db_query("dict", "SELECT kana, romaji, number FROM kana WHERE type = 'hiragana' ORDER BY RANDOM()")
        else:
            syllabary = "Katakana"
            temp = db_query("dict", "SELECT kana, romaji, number FROM kana WHERE type = 'katakana' ORDER BY RANDOM()")

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

        # Pick the first card to be shown
        card = [kana[0][0], kana[0][1], kana[0][2], kana[0][3]]

        return render_template("kana_review.html", kana=kana, syllabary=syllabary, card=card)

    if request.method == "POST":
        # Get the data from JSON
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


# The radicals page
@app.route("/radicals", methods=["GET", "POST"])
def radicals():
    # If the method is post, look up the specific radical and display all the relevant information
    if request.method == "POST":
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

    # If the method is get, display a list of all radicals.
    else:
        radicals = db_query("dict", "SELECT strokecount, title, id, english FROM radicals ORDER BY id, strokecount")
        # The number of possible radical strokes is a well known part of radical study so I hardcoded this here
        strokes = [*range(1, 18)]

        return render_template("radical_overview.html", radicals=radicals, strokes=strokes)


# The kanji page
@app.route("/kanji", methods=["GET", "POST"])
def kanji():
    # If the method is post, look up the specific kanji and display all the relevant information
    if request.method == "POST":
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
    # If the method is get, display a list of all kanji
    else:
        # Get a list sorted by grade
        grade = db_query("dict", "SELECT id, kanji, onyomi, kunyomi, meaning, grade, jlpt FROM kanji ORDER BY grade")
        # Get a list sorted by jlpt
        jlpt = db_query("dict", "SELECT id, kanji, onyomi, kunyomi, meaning, grade, jlpt FROM kanji ORDER BY jlpt DESC")
        return render_template("kanji_overview.html", grade=grade, jlpt=jlpt)


# The vocabulary page
@app.route("/vocabulary", methods=["GET", "POST"])
def vocabulary():
    # If the method is get, display a list of all words (this is very long and takes a moment)
    if request.method == "GET":
        vocabulary_kana = db_query("dict", "SELECT word, reading, meaning, jlpt FROM vocabulary ORDER BY reading")
        vocabulary_jlpt = db_query("dict", "SELECT word, reading, meaning, jlpt FROM vocabulary ORDER BY jlpt DESC, reading ASC")
        return render_template("vocabulary_list.html", kana=vocabulary_kana, jlpt=vocabulary_jlpt)

    # If the method is post, look up the specific word and display all the relevant information
    else:
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


# The explanation page
@app.route("/how_to_use")
def how_to():
    return render_template("how_to.html")


# The about page
@app.route("/about")
def about():
    return render_template("about.html")


# The acknowledgements page
@app.route("/acknowledgements")
def achknowledgements():
    return render_template("acknowledgements.html")