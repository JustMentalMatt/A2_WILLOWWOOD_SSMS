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

# def EditUserSQL(SqlID, Username, Password, FirstName, LastName, DOB, ContactNumber, Cmbo_Role, Cmbo_EnrollmentStatus, HouseID, Message):
#     conn = sqlite3.connect('./backend/WillowInnDB.db')
#     cursor = conn.cursor()

#     cursor.execute(f"UPDATE UserTable SET Username = '{Username}', Password = '{Password}', FirstName = '{FirstName}', LastName = '{LastName}', DOB = '{DOB}', ContactNumber = '{ContactNumber}', Role = '{Cmbo_Role}', EnrollmentStatus = '{Cmbo_EnrollmentStatus}', HouseID = '{HouseID}', Message = '{Message}' WHERE UserID = '{SqlID}'")
#     conn.commit()
#     conn.close()

# def DeleteUserSQL(SqlID):
#     conn = sqlite3.connect('./backend/WillowInnDB.db')
#     cursor = conn.cursor()

#     cursor.execute(f"DELETE FROM UserTable WHERE UserID = '{SqlID}'")
#     conn.commit()

#     #REORDER THE USERID
#     cursor.execute(f"UPDATE UserTable SET UserID = UserID - 1 WHERE UserID > '{SqlID}'")
#     conn.commit()

#     conn.close()

# def AddUserSQL(Username, Password, FirstName, LastName, DOB, ContactNumber, Cmbo_Role, Cmbo_EnrollmentStatus, HouseID, Message):
#     conn = sqlite3.connect('./backend/WillowInnDB.db')
#     cursor = conn.cursor()

#     cursor.execute('SELECT MAX(UserID) FROM UserTable')
#     conn.commit()

#     max_user_id = cursor.fetchone()[0]
#     # Calculate the new UserID by incrementing the maximum UserID
#     NewUID = max_user_id + 1 if max_user_id is not None else 1

#     cursor.execute(f"INSERT INTO UserTable (UserID, Username, Password, FirstName, LastName, DOB, ContactNumber, Role, EnrollmentStatus, HouseID, Message) VALUES ('{NewUID}', '{Username}', '{Password}', '{FirstName}', '{LastName}', '{DOB}', '{ContactNumber}', '{Cmbo_Role}', '{Cmbo_EnrollmentStatus}', '{HouseID}', '{Message}')")
#     conn.commit()
#     conn.close()

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

########## new @@@@@@@@@@@

def SQL_AdminView_FetchHouseTable(search_query=None):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    disp_column = ["HouseID", "HouseName", "HouseAddress", "HousePhone", "HouseEmail"]
    columnsSQL = ', '.join(disp_column) # for the sql wuarey

    if search_query:
        search_condition = f"HouseName LIKE '%{search_query}%' OR HouseAddress LIKE '%{search_query}%' OR HousePhone LIKE '%{search_query}%' OR HouseEmail LIKE '%{search_query}%'"
        query = f"SELECT {columnsSQL} FROM HouseTable WHERE {search_condition}"
    else:
        query = f"SELECT {columnsSQL} FROM HouseTable"

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return disp_column, rows

def SQL_AdminView_FetchEventsTable(search_query=None):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    disp_column = ["EventID", "EventName", "EventDate", "Capacity", "DifficultyLevel", "Points"]
    columnsSQL = ', '.join(disp_column) # for the sql wuarey

    if search_query:
        search_condition = f"EventName LIKE '%{search_query}%' OR EventDate LIKE '%{search_query}%' OR Capacity LIKE '%{search_query}%' OR DifficultyLevel LIKE '%{search_query}%' OR Points LIKE '%{search_query}%'"
        query = f"SELECT {columnsSQL} FROM EventTable WHERE {search_condition}"
    else:
        query = f"SELECT {columnsSQL} FROM EventTable"

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return disp_column, rows

def SQL_AdminView_FetchBookingTable(search_query=None):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    disp_column = ["BookingID", "EventID", "UserID", "BookingDate"]
    columnsSQL = ', '.join(disp_column) # for the sql wuarey
    
    if search_query:
        search_condition = f"EventID LIKE '{search_query}' OR UserID LIKE '{search_query}' OR BookingDate LIKE '{search_query}'"
        query = f"SELECT {columnsSQL} FROM BookingTable WHERE {search_condition}"
    else:
        query = f"SELECT {columnsSQL} FROM BookingTable"

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return disp_column, rows

def SQL_AdminView_FetchRoomTable(search_query=None):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    disp_column = ["RoomID", "RoomNumber", "RoomType", "RoomCapacity", "HouseID"]
    columnsSQL = ', '.join(disp_column) # for the sql wuarey

    if search_query:
        search_condition = f"RoomNumber LIKE '{search_query}' OR RoomType LIKE '{search_query}' OR RoomCapacity LIKE '{search_query}' OR HouseID LIKE '{search_query}'"
        query = f"SELECT {columnsSQL} FROM RoomTable WHERE {search_condition}"
    else:
        query = f"SELECT {columnsSQL} FROM RoomTable"
    
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return disp_column, rows

def SQL_AdminView_FetchBedTable(search_query=None):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    disp_column = ["BedID", "RoomID", "BedNumber", "BedStatus"]
    columnsSQL = ', '.join(disp_column) # for the sql wuarey

    if search_query:
        search_condition = f"RoomID LIKE '{search_query}' OR BedNumber LIKE '{search_query}' OR BedStatus LIKE '{search_query}'"
        query = f"SELECT {columnsSQL} FROM BedTable WHERE {search_condition}"
    else:
        query = f"SELECT {columnsSQL} FROM BedTable"

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return disp_column, rows

#### House Buttons ###

def EditHouseSQL(HouseID, HouseName, HouseAddress, HousePhone, HouseEmail):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute(f"UPDATE HouseTable SET HouseName = '{HouseName}', HouseAddress = '{HouseAddress}', HousePhone = '{HousePhone}', HouseEmail = '{HouseEmail}' WHERE HouseID = '{HouseID}'")
    conn.commit()
    conn.close()

def AddHouseSQL(HouseName, HouseAddress, HousePhone, HouseEmail):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute('SELECT MAX(HouseID) FROM HouseTable')
    conn.commit()

    max_house_id = cursor.fetchone()[0]
    # Calculate the new HouseID by incrementing the maximum HouseID
    NewHID = max_house_id + 1 if max_house_id is not None else 1

    cursor.execute(f"INSERT INTO HouseTable (HouseID, HouseName, HouseAddress, HousePhone, HouseEmail) VALUES ('{NewHID}', '{HouseName}', '{HouseAddress}', '{HousePhone}', '{HouseEmail}')")
    conn.commit()
    conn.close()

def DeleteHouseSQL(HouseID):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM HouseTable WHERE HouseID = '{HouseID}'")
    conn.commit()

    conn.close()

#### Event Buttons ###

def EditEventSQL(EventID, EventName, EventDate, Capacity, DifficultyLevel, Points):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute(f"UPDATE EventTable SET EventName = '{EventName}', EventDate = '{EventDate}', Capacity = '{Capacity}', DifficultyLevel = '{DifficultyLevel}', Points = '{Points}' WHERE EventID = '{EventID}'")
    conn.commit()
    conn.close()
    
def AddEventSQL(EventName, EventDate, Capacity, DifficultyLevel, Points):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute('SELECT MAX(EventID) FROM EventTable')
    conn.commit()

    max_event_id = cursor.fetchone()[0]
    # Calculate the new EventID by incrementing the maximum EventID
    NewEID = max_event_id + 1 if max_event_id is not None else 1

    cursor.execute(f"INSERT INTO EventTable (EventID, EventName, EventDate, Capacity, DifficultyLevel, Points) VALUES ('{NewEID}', '{EventName}', '{EventDate}', '{Capacity}', '{DifficultyLevel}', '{Points}')")
    conn.commit()
    conn.close()
    
def DeleteEventSQL(EventID):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM EventTable WHERE EventID = '{EventID}'")
    conn.commit()

    conn.close()
    
#### Booking Buttons ###

def EditBookingSQL(BookingID, EventID, UserID, BookingDate):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute(f"UPDATE BookingTable SET EventID = '{EventID}', UserID = '{UserID}', BookingDate = '{BookingDate}' WHERE BookingID = '{BookingID}'")
    conn.commit()
    conn.close()
    
def AddBookingSQL(EventID, UserID, BookingDate):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute('SELECT MAX(BookingID) FROM BookingTable')
    conn.commit()

    max_booking_id = cursor.fetchone()[0]
    # Calculate the new BookingID by incrementing the maximum BookingID
    NewBID = max_booking_id + 1 if max_booking_id is not None else 1

    cursor.execute(f"INSERT INTO BookingTable (BookingID, EventID, UserID, BookingDate) VALUES ('{NewBID}', '{EventID}', '{UserID}', '{BookingDate}')")
    conn.commit()
    conn.close()
    
def DeleteBookingSQL(BookingID):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM BookingTable WHERE BookingID = '{BookingID}'")
    conn.commit()

    conn.close()
    
#### Room Buttons ###

def EditRoomSQL(RoomID, RoomNumber, RoomType, RoomCapacity, HouseID):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute(f"UPDATE RoomTable SET RoomNumber = '{RoomNumber}', RoomType = '{RoomType}', RoomCapacity = '{RoomCapacity}', HouseID = '{HouseID}' WHERE RoomID = '{RoomID}'")
    conn.commit()
    conn.close()
    
def AddRoomSQL(RoomNumber, RoomType, RoomCapacity, HouseID):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute('SELECT MAX(RoomID) FROM RoomTable')
    conn.commit()

    max_room_id = cursor.fetchone()[0]
    # Calculate the new RoomID by incrementing the maximum RoomID
    NewRID = max_room_id + 1 if max_room_id is not None else 1

    cursor.execute(f"INSERT INTO RoomTable (RoomID, RoomNumber, RoomType, RoomCapacity, HouseID) VALUES ('{NewRID}', '{RoomNumber}', '{RoomType}', '{RoomCapacity}', '{HouseID}')")
    conn.commit()
    conn.close()
    
def DeleteRoomSQL(RoomID):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM RoomTable WHERE RoomID = '{RoomID}'")
    conn.commit()

    conn.close()
    
#### Bed Buttons ###

def EditBedSQL(BedID, RoomID, BedNumber, BedStatus):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute(f"UPDATE BedTable SET RoomID = '{RoomID}', BedNumber = '{BedNumber}', BedStatus = '{BedStatus}' WHERE BedID = '{BedID}'")
    conn.commit()
    conn.close()
    
def AddBedSQL(RoomID, BedNumber, BedStatus):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute('SELECT MAX(BedID) FROM BedTable')
    conn.commit()

    max_bed_id = cursor.fetchone()[0]
    # Calculate the new BedID by incrementing the maximum BedID
    NewBID = max_bed_id + 1 if max_bed_id is not None else 1

    cursor.execute(f"INSERT INTO BedTable (BedID, RoomID, BedNumber, BedStatus) VALUES ('{NewBID}', '{RoomID}', '{BedNumber}', '{BedStatus}')")
    conn.commit()
    conn.close()
    
def DeleteBedSQL(BedID):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM BedTable WHERE BedID = '{BedID}'")
    conn.commit()

    conn.close()

#### User Buttons ###

def EditUserSQL(SqlID, Username, Password, FirstName, LastName, DOB, ContactNumber, Cmbo_Role, Cmbo_EnrollmentStatus, Message, HouseID, RoomID, BedID):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute(f"UPDATE UserTable SET Username = '{Username}', Password = '{Password}', FirstName = '{FirstName}', LastName = '{LastName}', DOB = '{DOB}', ContactNumber = '{ContactNumber}', RoleID = '{Cmbo_Role}', EnrollmentStatus = '{Cmbo_EnrollmentStatus}', HouseID = '{HouseID}', Message = '{Message}' WHERE UserID = '{SqlID}'")
    conn.commit()
    conn.close()
    
def AddUserSQL(Username, Password, FirstName, LastName, DOB, ContactNumber, Cmbo_Role, Cmbo_EnrollmentStatus, Message, HouseID, RoomID, BedID):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute('SELECT MAX(UserID) FROM UserTable')
    conn.commit()

    max_user_id = cursor.fetchone()[0]
    # Calculate the new UserID by incrementing the maximum UserID
    NewUID = max_user_id + 1 if max_user_id is not None else 1

    cursor.execute(f"INSERT INTO UserTable (UserID, Username, Password, FirstName, LastName, DOB, ContactNumber, RoleID, EnrollmentStatus, Message, HouseID, RoomID, BedID) VALUES ('{NewUID}', '{Username}', '{Password}', '{FirstName}', '{LastName}', '{DOB}', '{ContactNumber}', '{Cmbo_Role}', '{Cmbo_EnrollmentStatus}', '{Message}', '{HouseID}', '{RoomID}', '{BedID}')")
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