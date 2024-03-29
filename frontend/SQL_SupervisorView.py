import sqlite3
from CTkTable import *
from customtkinter import *

def SQL_SupervisorView_FetchUserTable(search_query=None): #fetches all users from the database
            conn = sqlite3.connect('./backend/WillowInnDB.db')
            cursor = conn.cursor()

            disp_column = ["UserID", "Username", "FirstName", "LastName", "ContactNumber", "DOB", "Role", "EnrollmentStatus", "HouseID"] # iunclude coluims you only wanna show
            columnsSQL = ', '.join(disp_column) # for the sql wuarey
            
            if search_query:
            # Add a WHERE clause to filter results based on the search query
                search_condition = f"UserID LIKE '{search_query}' OR Username LIKE '%{search_query}%' OR FirstName LIKE '%{search_query}%' OR LastName LIKE '%{search_query}%'"
                query = f"SELECT {columnsSQL} FROM UserTable WHERE {search_condition}"
            else:
                query = f"SELECT {columnsSQL} FROM UserTable"
            
            cursor.execute(query)
            rows = cursor.fetchall() #this puts it in tabular form so u can just use it with the ctk table thing

            conn.close()
            return disp_column, rows

def SQL_SupervisorView_FetchGeneralRegister(search_query=None): #sorts users by enrollment status (pending and enrolled)

            conn = sqlite3.connect('./backend/WillowInnDB.db')
            cursor = conn.cursor()

            disp_column = ["UserID", "Username", "FirstName", "LastName", "Role", "EnrollmentStatus", "HouseID"]
            columnsSQL = ', '.join(disp_column) # for the sql wuarey
            

            # Add a WHERE clause to filter results based on the search query
            if search_query:
                search_condition = f"(EnrollmentStatus = 'Pending' OR EnrollmentStatus = 'Enrolled') AND (Username LIKE '{search_query}%' OR FirstName LIKE '{search_query}%' OR LastName LIKE '{search_query}%')"
                query = f"SELECT {columnsSQL} FROM UserTable WHERE {search_condition}"
            else:
                search_condition = f"EnrollmentStatus = 'Pending' OR EnrollmentStatus = 'Enrolled'"
                query = f"SELECT {columnsSQL} FROM UserTable WHERE {search_condition}"
            
            #cursor.execute(f'SELECT {columnsSQL} FROM UserTable') #yupada
            cursor.execute(query)
            rows = cursor.fetchall() #this puts it in tabular form so u can just use it with the ctk table thing

            conn.close()
            return disp_column, rows