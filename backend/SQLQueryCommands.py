import sqlite3
import traceback
import sys

def createDatabase():
    try:
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")

        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        print("SQLite Database Version is: ", record)
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to the database", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The databse connection has closed")

def createTable():
    try:
        sqliteConnection = sqlite3.connect('database.db')
        sqlite_create_table_query = '''CREATE TABLE Admin_Users (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    email text NOT NULL UNIQUE,
                                    joining_date datetime,
                                    password REAL NOT NULL,
                                    username TEXT NOT NULL);'''

        cursor = sqliteConnection.cursor()
        print("Successfully Connected to the databae")
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("Datase table created")

        cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a database table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("Database connection has closed")

def insertData():
    try:
        sqliteConnection = sqlite3.connect('./database.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to the database")

        sqlite_insert_query = """INSERT INTO default_users (id, name, age, username, password, email, join_date)  VALUES  (1, 'Sandra Adams', 24, 'sadams1', 'passsecur3', 'sadams@user.net', '12/12/2020')"""

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Record inserted successfully into Admin_Users table ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into database table")
        print("Exception class is: ", error.__class__)
        print("Exception is", error.args)
        print('Printing detailed SQLite exception traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The database connection has closed")
            
def rowCount():
    try:
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        print("Connected to the database")

        sqlite_select_query = """SELECT count(*) from Admin_Users"""
        cursor.execute(sqlite_select_query)
        totalRows = cursor.fetchone()
        print("Total rows are:  ", totalRows)
        cursor.close()

    except sqlite3.Error as error:
            print("Failed to read data from database table", error)
    finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("The databse connection is closed")
                print("Total Rows affected since the database connection was opened: ", sqliteConnection.total_changes)

def showTables():
    try:
        sqliteConnection = sqlite3.connect('./database.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to the database")

        sqlite_insert_query = """SHOW TABLES"""

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Record inserted successfully into Admin_Users table ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
            print("Failed to read data from database table", error)

showTables()