import sqlite3
from CTkTable import *
from customtkinter import *



def SQL_AdminView_FetchUserTable(search_query=None):
            conn = sqlite3.connect('./backend/WillowInnDB.db')
            cursor = conn.cursor()

            disp_column = ["UserID", "Username", "Password", "FirstName", "LastName", "DOB", "ContactNumber", "Role", "EnrollmentStatus", "HouseID", "Message"] # iunclude coluims you only wanna show
            columnsSQL = ', '.join(disp_column) # for the sql wuarey
            
            if search_query:
            # Add a WHERE clause to filter results based on the search query
                search_condition = f"Username LIKE '%{search_query}%' OR FirstName LIKE '%{search_query}%' OR LastName LIKE '%{search_query}%'"
                query = f"SELECT {columnsSQL} FROM UserTable WHERE {search_condition}"
            else:
                query = f"SELECT {columnsSQL} FROM UserTable"
            
            
            #cursor.execute(f'SELECT {columnsSQL} FROM UserTable') #yupada
            cursor.execute(query)
            rows = cursor.fetchall() #this puts it in tabular form so u can just use it with the ctk table thing

            conn.close()
            return disp_column, rows
        
