import sqlite3
from CTkTable import *
from customtkinter import *



def SQL_AdminView_FetchUserTable(search_query=None): #fetches all users from the database
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
        
def SQL_AdminView_FetchGeneralRegister(search_query=None): #sorts users by enrollment status (pending and enrolled)

            conn = sqlite3.connect('./backend/WillowInnDB.db')
            cursor = conn.cursor()

            disp_column = ["UserID", "Username", "Password", "FirstName", "LastName", "DOB", "ContactNumber", "Role", "EnrollmentStatus", "HouseID"]
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

def EditUserSQL(SqlID, Username, Password, FirstName, LastName, DOB, ContactNumber, Cmbo_Role, Cmbo_EnrollmentStatus, HouseID, Message):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute(f"UPDATE UserTable SET Username = '{Username}', Password = '{Password}', FirstName = '{FirstName}', LastName = '{LastName}', DOB = '{DOB}', ContactNumber = '{ContactNumber}', Role = '{Cmbo_Role}', EnrollmentStatus = '{Cmbo_EnrollmentStatus}', HouseID = '{HouseID}', Message = '{Message}' WHERE UserID = '{SqlID}'")
    conn.commit()
    conn.close()

def DeleteUserSQL(SqlID):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM UserTable WHERE UserID = '{SqlID}'")
    conn.commit()
    conn.close()

def AddUserSQL(Username, Password, FirstName, LastName, DOB, ContactNumber, Cmbo_Role, Cmbo_EnrollmentStatus, HouseID, Message):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO UserTable (Username, Password, FirstName, LastName, DOB, ContactNumber, Role, EnrollmentStatus, HouseID, Message) VALUES ('{Username}', '{Password}', '{FirstName}', '{LastName}', '{DOB}', '{ContactNumber}', '{Cmbo_Role}', '{Cmbo_EnrollmentStatus}', '{HouseID}', '{Message}')")
    conn.commit()
    conn.close()