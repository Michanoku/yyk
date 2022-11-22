import sqlite3


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