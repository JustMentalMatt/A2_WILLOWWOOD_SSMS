import sqlite3
from CTkTable import *
from customtkinter import *



def SQL_AdminView_FetchUserTable(search_query=None): #fetches all users from the database
            conn = sqlite3.connect('./backend/WillowInnDB.db')
            cursor = conn.cursor()

            disp_column = ["UserID", "Username", "Password", "FirstName", "LastName", "DOB", "ContactNumber", "EnrollmentStatus", "Message", "RoleID", "HouseID", "RoomID", "BedID"] # iunclude coluims you only wanna show
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

    #REORDER THE USERID
    cursor.execute(f"UPDATE UserTable SET UserID = UserID - 1 WHERE UserID > '{SqlID}'")
    conn.commit()

    conn.close()

def AddUserSQL(Username, Password, FirstName, LastName, DOB, ContactNumber, Cmbo_Role, Cmbo_EnrollmentStatus, HouseID, Message):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute('SELECT MAX(UserID) FROM UserTable')
    conn.commit()

    max_user_id = cursor.fetchone()[0]
    # Calculate the new UserID by incrementing the maximum UserID
    NewUID = max_user_id + 1 if max_user_id is not None else 1

    cursor.execute(f"INSERT INTO UserTable (UserID, Username, Password, FirstName, LastName, DOB, ContactNumber, Role, EnrollmentStatus, HouseID, Message) VALUES ('{NewUID}', '{Username}', '{Password}', '{FirstName}', '{LastName}', '{DOB}', '{ContactNumber}', '{Cmbo_Role}', '{Cmbo_EnrollmentStatus}', '{HouseID}', '{Message}')")
    conn.commit()
    conn.close()

def SQL_AdminView_FetchHouse(HouseID):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    disp_column = ["HouseID", "HouseName", "HouseAddress", "HousePhone", "HouseEmail"]
    columnsSQL = ', '.join(disp_column) # for the sql wuarey

    #get house supervosor name
    cursor.execute(f"SELECT FirstName, LastName FROM UserTable WHERE Role = 'SUPV' AND HouseID = {HouseID}")
    HouseSupervisor = cursor.fetchone()
    HouseSupervisor = f"{HouseSupervisor[0]} {HouseSupervisor[1]}"
    conn.commit()
    cursor.execute(f"UPDATE HouseTable SET HouseSupervisor = '{HouseSupervisor}' WHERE HouseID = {HouseID}")
    conn.commit()

    cursor.execute(f"SELECT {columnsSQL} FROM HouseTable WHERE HouseID = {HouseID}")
    rows = cursor.fetchall()
    conn.close()

    disp_column = ["HouseID", "HouseName", "HouseAddress", "HousePhone", "HouseEmail", "HouseSupervisor"]
    combinedrows = [rows[0] + (HouseSupervisor,)]

    return disp_column, combinedrows, HouseSupervisor

def SQLAdminView_FetchHouseResidents(HouseID):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    disp_column = ["FirstName", "LastName"]
    columnsSQL = ', '.join(disp_column) # for the sql wuarey

    cursor.execute(f"SELECT {columnsSQL} FROM UserTable WHERE HouseID = {HouseID} AND Role = 'USER'")
    residents = cursor.fetchall()
    conn.close()

    residents = [" ".join(resident) for resident in residents]
    residents.insert(0, "Unassigned")
    return residents

def SQLAdminView_FetchAssignedUser(room_id, bed_id, house_id):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    disp_column = ["FirstName", "LastName"]
    columnsSQL = ', '.join(disp_column) # for the sql wuarey

    cursor.execute(f"SELECT {columnsSQL} FROM UserTable WHERE HouseID = {house_id} AND RoomID = {room_id} AND BedID = {bed_id}")
    assigned_user = cursor.fetchone()
    conn.close()

    if assigned_user:
        return " ".join(assigned_user)
    else:
        return "Unassigned"

def SQLAdminView_AssignBed(user, RoomID, BedID, HouseID):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT UserID FROM UserTable WHERE RoomID = {RoomID} AND BedID = {BedID} AND HouseID = {HouseID}")
    existingUser = cursor.fetchone()
    if existingUser:
        cursor.execute(f"UPDATE UserTable SET RoomID = '', BedID = '' WHERE UserID = {existingUser[0]}")

    if user == "Unassigned":
        cursor.execute(f"UPDATE UserTable SET RoomID = '', BedID = '' WHERE UserID = {existingUser[0]}")
    else:
        FirstName, LastName = user.split()
        cursor.execute(f"UPDATE UserTable SET RoomID = {RoomID}, BedID = {BedID} WHERE FirstName = '{FirstName}' AND LastName = '{LastName}' AND HouseID = {HouseID}")
    
    conn.commit()
    conn.close()

def SQL_AdminView_FetchHouse2(HouseID):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    disp_column = ["HouseID", "HouseName", "HouseAddress", "HousePhone", "HouseEmail"]
    columnsSQL = ', '.join(disp_column) # for the sql wuarey

    #get house supervosor name
    cursor.execute(f"SELECT FirstName, LastName FROM UserTable WHERE Role = 'SUPV' AND HouseID = 2")
    HouseSupervisor = cursor.fetchone()
    HouseSupervisor = f"{HouseSupervisor[0]} {HouseSupervisor[1]}"
    conn.commit()
    cursor.execute(f"UPDATE HouseTable SET HouseSupervisor = '{HouseSupervisor}' WHERE HouseID = 2")
    conn.commit()

    cursor.execute(f"SELECT {columnsSQL} FROM HouseTable WHERE HouseID = 2")
    rows = cursor.fetchall()
    conn.close()

    disp_column = ["HouseID", "HouseName", "HouseAddress", "HousePhone", "HouseEmail", "HouseSupervisor"]
    combinedrows = [rows[0] + (HouseSupervisor,)]

    return disp_column, combinedrows, HouseSupervisor

def SQLAdminView_FetchHouse2Residents():
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    disp_column = ["FirstName", "LastName"]
    columnsSQL = ', '.join(disp_column) # for the sql wuarey

    cursor.execute(f"SELECT {columnsSQL} FROM UserTable WHERE HouseID = 2 AND Role = 'USER'")
    residents = cursor.fetchall()
    conn.close()

    residents = [" ".join(resident) for resident in residents]
    residents.insert(0, "Unassigned")
    return residents


####################################################################################################################

# def ChangeTableView(Option):

#     def SQLChangeTableView(search_query=None):
#         conn = sqlite3.connect('./backend/WillowInnDB.db')
#         cursor = conn.cursor()

#         disp_column = ["UserID", "Username", "Password", "FirstName", "LastName", "DOB", "ContactNumber", "Role", "EnrollmentStatus", "HouseID", "Message"] # iunclude coluims you only wanna show
#         columnsSQL = ', '.join(disp_column) # for the sql wuarey
        
#         if search_query:
#         # Add a WHERE clause to filter results based on the search query
#             search_condition = f"Role LIKE '{search_query}'"
#             query = f"SELECT {columnsSQL} FROM UserTable WHERE {search_condition}"
#         else:
#             query = f"SELECT {columnsSQL} FROM UserTable"
        
#         #cursor.execute(f'SELECT {columnsSQL} FROM UserTable') #yupada
#         cursor.execute(query)
#         rows = cursor.fetchall() #this puts it in tabular form so u can just use it with the ctk table thing
#         conn.close()

#         return disp_column, rows

#     if Option == "ALL USERS":
#         return SQLChangeTableView(search_query=None)
#     elif Option == "Supervisors":
#         return SQLChangeTableView(search_query="SUPV")
#     elif Option == "Management":
#         return SQLChangeTableView(search_query="MGMT")
#     elif Option == "Volunteers":
#         return SQLChangeTableView(search_query="USER")

####################################################################################################################

# def MANUALREORDER():
#     conn = sqlite3.connect('./backend/WillowInnDB.db')
#     cursor = conn.cursor()

#     cursor.execute(f"UPDATE UserTable SET UserID = UserID - 1 WHERE UserID > 15")
#     conn.commit()
#     conn.close()

# MANUALREORDER() #this is for the manual reorder of the user id, this is only for testing purposes