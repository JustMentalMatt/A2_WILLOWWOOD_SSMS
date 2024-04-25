import sqlite3
from CTkTable import *
from customtkinter import *
import validation
import tkinter as tk

from validation import auditlog


def SQL_SupervisorView_FetchUserTable(search_query=None):

        conn = sqlite3.connect('./backend/WillowInnDB.db')
        cursor = conn.cursor()

        disp_column = ["UserID", "Username", "FirstName", "LastName", "DOB", "ContactNumber", "EnrollmentStatus", "Message", "RoleID", "HouseID", "RoomID", "BedID"] # iunclude coluims you only wanna show
        columnsSQL = ', '.join(disp_column) # for the sql wuarey
        
        if search_query:
        # Add a WHERE clause to filter results based on the search query
            search_condition = f"UserID LIKE '{search_query}' OR Username LIKE '%{search_query}%' OR FirstName LIKE '%{search_query}%' OR LastName LIKE '%{search_query}%'"
            query = f"SELECT {columnsSQL} FROM UserTable WHERE {search_condition}"
        else:
            query = f"SELECT {columnsSQL} FROM UserTable"
        
        
        #cursor.execute(f'SELECT {columnsSQL} FROM UserTable') #yupada
        cursor.execute(query)
        rows = cursor.fetchall() #this puts it in tabular form so u can just use it with the ctk table thing

        conn.close()
        return disp_column, rows
    
def SQL_SupervisorView_FetchHouseID():

    with open("frontend/uservar.txt", "r") as file:
        userVAR = file.read().strip()
        file.close()
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT HouseID FROM UserTable WHERE Username = "{userVAR}"')
    rows = cursor.fetchall()
    conn.close()
    
    result = rows[0][0]

    if result != "" or " ":
        return result
    else:
        return None
