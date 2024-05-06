import sqlite3
from CTkTable import *
from customtkinter import *
import validation
import tkinter as tk

from validation import auditlog



def SQL_AdminView_FetchUserTable(search_query=None): #fetches all users from the database

            conn = sqlite3.connect('./backend/WillowInnDB.db')
            cursor = conn.cursor()

            disp_column = ["UserID", "Username", "Password", "FirstName", "LastName", "DOB", "ContactNumber", "EnrollmentStatus", "Message", "RoleID", "HouseID", "RoomID", "BedID"]
            columnsSQL = ', '.join(disp_column) 
            
            if search_query: # If there is a search query, filter results based on the search query
            # Add a WHERE clause to filter results based on the search query
                search_condition = f"UserID LIKE '{search_query}' OR Username LIKE '%{search_query}%' OR FirstName LIKE '%{search_query}%' OR LastName LIKE '%{search_query}%'"
                query = f"SELECT {columnsSQL} FROM UserTable WHERE {search_condition}"
            else: # if no search query, fetch all users
                query = f"SELECT {columnsSQL} FROM UserTable"
            
            cursor.execute(query)
            rows = cursor.fetchall() # In tabular format for CTkTable

            conn.close()
            return disp_column, rows
        
def SQL_AdminView_FetchGeneralRegister(search_query=None): #sorts users by enrollment status (pending and enrolled)

            conn = sqlite3.connect('./backend/WillowInnDB.db')
            cursor = conn.cursor()
            # Get the columns to display
            disp_column = ["UserID", "Username", "FirstName", "LastName", "RoleID", "EnrollmentStatus", "HouseID"]
            columnsSQL = ', '.join(disp_column)
            
            # Add a WHERE clause to filter results based on the search query
            if search_query: # If there is a search query, filter results based on the search query
                search_condition = f"(EnrollmentStatus = 'Pending' OR EnrollmentStatus = 'Enrolled') AND (Username LIKE '{search_query}%' OR FirstName LIKE '{search_query}%' OR LastName LIKE '{search_query}%')"
                query = f"SELECT {columnsSQL} FROM UserTable WHERE {search_condition}"
            else: # if no search query, fetch all users
                search_condition = f"EnrollmentStatus = 'Pending' OR EnrollmentStatus = 'Enrolled'"
                query = f"SELECT {columnsSQL} FROM UserTable WHERE {search_condition}"
            
            cursor.execute(query)
            rows = cursor.fetchall()

            conn.close()
            return disp_column, rows

def SQL_AdminView_FetchHouse(HouseID):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    disp_column = ["HouseID", "HouseName", "HouseAddress", "HousePhone", "HouseEmail"]
    columnsSQL = ', '.join(disp_column) # for the sql wuarey

    #get house supervosor name
    cursor.execute(f"SELECT FirstName, LastName FROM UserTable WHERE RoleID = '2' AND HouseID = {HouseID}")
    
    HouseSupervisor = cursor.fetchone()
    
    if HouseSupervisor == None:
        HouseSupervisor = "Unassigned"
    else:
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

    cursor.execute(f"SELECT {columnsSQL} FROM UserTable WHERE HouseID = {HouseID} AND RoleID = '1'")
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
        auditlog(f"Bed Unassigned from User")

    if user == "Unassigned":
        cursor.execute(f"UPDATE UserTable SET RoomID = '', BedID = '' WHERE UserID = {existingUser[0]}")
        auditlog(f"Bed Unassigned from User")
    else:
        FirstName, LastName = user.split()
        cursor.execute(f"UPDATE UserTable SET RoomID = {RoomID}, BedID = {BedID} WHERE FirstName = '{FirstName}' AND LastName = '{LastName}' AND HouseID = {HouseID}")
        auditlog(f"Bed Assigned to User")
    
    conn.commit()
    conn.close()

########## new @@@@@@@@@@@

def SQL_AdminView_FetchHouseTable(search_query=None):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    disp_column = ["HouseID", "HouseName", "HouseAddress", "HousePhone", "HouseEmail"]
    columnsSQL = ', '.join(disp_column)

    if search_query: # If there is a search query, filter results based on the search query
        search_condition = f"HouseName LIKE '%{search_query}%' OR HouseAddress LIKE '%{search_query}%' OR HousePhone LIKE '%{search_query}%' OR HouseEmail LIKE '%{search_query}%'"
        query = f"SELECT {columnsSQL} FROM HouseTable WHERE {search_condition}"
    else: # if no search query, fetch all users
        query = f"SELECT {columnsSQL} FROM HouseTable"

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return disp_column, rows

def SQL_AdminView_FetchTaskTable(search_query=None):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    disp_column = ["TaskID", "TaskName", "Capacity", "DifficultyLevel", "Points"]
    columnsSQL = ', '.join(disp_column) # for the sql wuarey

    if search_query: # If there is a search query, filter results based on the search query
        search_condition = f"TaskName LIKE '%{search_query}%' OR Capacity LIKE '%{search_query}%' OR DifficultyLevel LIKE '%{search_query}%' OR Points LIKE '%{search_query}%'"
        query = f"SELECT {columnsSQL} FROM TaskTable WHERE {search_condition}"
    else: # if no search query, fetch all users
        query = f"SELECT {columnsSQL} FROM TaskTable"

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return disp_column, rows

def SQL_AdminView_FetchBookingTable(search_query=None):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()
    # Get the columns to display
    disp_column = ["BookingID", "TaskID", "UserID", "BookingDate"]
    columnsSQL = ', '.join(disp_column) # for the sql wuarey
    
    if search_query: # If there is a search query, filter results based on the search query
        search_condition = f"TaskID LIKE '{search_query}' OR UserID LIKE '{search_query}' OR BookingDate LIKE '{search_query}'"
        query = f"SELECT {columnsSQL} FROM BookingTable WHERE {search_condition}"
    else: # if no search query, fetch all users
        query = f"SELECT {columnsSQL} FROM BookingTable"

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return disp_column, rows

def SQL_AdminView_FetchRoomTable(search_query=None):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()
    # Get the columns to display
    disp_column = ["RoomID", "RoomNumber", "RoomType", "RoomCapacity", "HouseID"]
    columnsSQL = ', '.join(disp_column) # for the sql wuarey

    if search_query: # If there is a search query, filter results based on the search query
        search_condition = f"RoomNumber LIKE '{search_query}' OR RoomType LIKE '{search_query}' OR RoomCapacity LIKE '{search_query}' OR HouseID LIKE '{search_query}'"
        query = f"SELECT {columnsSQL} FROM RoomTable WHERE {search_condition}"
    else: # if no search query, fetch all users
        query = f"SELECT {columnsSQL} FROM RoomTable"
    
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return disp_column, rows

def SQL_AdminView_FetchBedTable(search_query=None):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()
    # Get the columns to display
    disp_column = ["BedID", "RoomID", "BedNumber", "BedStatus"]
    columnsSQL = ', '.join(disp_column)

    if search_query: # If there is a search query, filter results based on the search query
        search_condition = f"RoomID LIKE '{search_query}' OR BedNumber LIKE '{search_query}' OR BedStatus LIKE '{search_query}'"
        query = f"SELECT {columnsSQL} FROM BedTable WHERE {search_condition}"
    else: # if no search query, fetch all records
        query = f"SELECT {columnsSQL} FROM BedTable"

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return disp_column, rows

#### House Buttons ###

def EditHouseSQL(HouseID, HouseName, HouseAddress, HousePhone, HouseEmail):
    
    if validation.HouseValidation(HouseName, HouseAddress, HousePhone, HouseEmail):
    
        conn = sqlite3.connect('./backend/WillowInnDB.db')
        cursor = conn.cursor()

        cursor.execute(f"UPDATE HouseTable SET HouseName = '{HouseName}', HouseAddress = '{HouseAddress}', HousePhone = '{HousePhone}', HouseEmail = '{HouseEmail}' WHERE HouseID = '{HouseID}'")
        conn.commit()
        conn.close()
        
        # Dialog box to show success message
        tk.messagebox.showinfo("Success", "House Edited Successfully")
        auditlog("House Edited")
        return True
    else:
        auditlog("House Edit Failed")
        return False

def AddHouseSQL(HouseName, HouseAddress, HousePhone, HouseEmail):
    
    if validation.HouseValidation(HouseName, HouseAddress, HousePhone, HouseEmail):
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
        
        tk.messagebox.showinfo("Success", "House Added Successfully")
        auditlog("House Added")
        return True
    else:
        auditlog("House Add Failed")
        return False

def DeleteHouseSQL(HouseID):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM HouseTable WHERE HouseID = '{HouseID}'")
    conn.commit()

    conn.close()
    auditlog("House Deleted")

#### Event ---TASK--- Buttons ###

def EditTaskSQL(TaskID, TaskName, Capacity, DifficultyLevel, Points):
    
    if validation.TaskValidation(TaskName, Capacity, DifficultyLevel, Points):
        
        conn = sqlite3.connect('./backend/WillowInnDB.db')
        cursor = conn.cursor()

        cursor.execute(f"UPDATE TaskTable SET TaskName = '{TaskName}', Capacity = '{Capacity}', DifficultyLevel = '{DifficultyLevel}', Points = '{Points}' WHERE TaskID = '{TaskID}'")
        conn.commit()
        conn.close()
        
        tk.messagebox.showinfo("Success", "Task Edited Successfully")
        auditlog("Task Edited")
        return True
    else:
        auditlog("Task Edit Failed")
        return False
    
def AddTaskSQL(TaskName, Capacity, DifficultyLevel, Points):
    
    if validation.TaskValidation(TaskName, Capacity, DifficultyLevel, Points):
        conn = sqlite3.connect('./backend/WillowInnDB.db')
        cursor = conn.cursor()

        cursor.execute('SELECT MAX(TaskID) FROM TaskTable')
        conn.commit()

        max_task_id = cursor.fetchone()[0]
        # Calculate the new EventID by incrementing the maximum EventID
        NewTID = max_task_id + 1 if max_task_id is not None else 1

        cursor.execute(f"INSERT INTO TaskTable (TaskID, TaskName, Capacity, DifficultyLevel, Points) VALUES ('{NewTID}', '{TaskName}', '{Capacity}', '{DifficultyLevel}', '{Points}')")
        conn.commit()
        conn.close()
        # Dialog box to show success message
        tk.messagebox.showinfo("Success", "Task Added Successfully")
        auditlog("Task Added")
        return True
    else:
        auditlog("Task Add Failed")
        return False
    
    
def DeleteTaskSQL(TaskID):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM TaskTable WHERE TaskID = '{TaskID}'")
    conn.commit()

    conn.close()
    auditlog("Task Deleted")
    
#### Booking Buttons ###

def EditBookingSQL(BookingID, TaskID, UserID, BookingDate):
    # Check if the booking is valid
    if validation.BookingValidaion(TaskID, UserID, BookingDate):
        # If true, update the booking
        conn = sqlite3.connect('./backend/WillowInnDB.db')
        cursor = conn.cursor()

        cursor.execute(f"UPDATE BookingTable SET TaskID = '{TaskID}', UserID = '{UserID}', BookingDate = '{BookingDate}' WHERE BookingID = '{BookingID}'")
        conn.commit()
        conn.close()
        
        tk.messagebox.showinfo("Success", "Booking Edited Successfully")
        auditlog("Booking Edited") # Log the editing of the booking
        return True
    else:
        auditlog("Booking Edit Failed") # Log the failure of the booking edit
        return False

    
def AddBookingSQL(TaskID, UserID, BookingDate):
    
    if validation.BookingValidaion(TaskID, UserID, BookingDate):
        conn = sqlite3.connect('./backend/WillowInnDB.db')
        cursor = conn.cursor()
        # Get the maximum BookingID
        cursor.execute('SELECT MAX(BookingID) FROM BookingTable')
        conn.commit()

        max_booking_id = cursor.fetchone()[0]
        # Calculate the new BookingID by incrementing the maximum BookingID
        NewBID = max_booking_id + 1 if max_booking_id is not None else 1
        # Create a new booking
        cursor.execute(f"INSERT INTO BookingTable (BookingID, TaskID, UserID, BookingDate) VALUES ({NewBID}, {TaskID}, {UserID[0]}, CURRENT_TIMESTAMP)")
        conn.commit()
        conn.close()
        # Dialog box to show success message
        tk.messagebox.showinfo("Success", "Booking Added Successfully")
        auditlog("Booking Added")
        return True
    else:
        auditlog("Booking Add Failed")
        return False
    
def DeleteBookingSQL(BookingID):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()
    # Delete the booking
    cursor.execute(f"DELETE FROM BookingTable WHERE BookingID = '{BookingID}'")
    conn.commit()

    conn.close()
    auditlog("Booking Deleted") # Log the deletion of the booking
    
#### Room Buttons ###

def EditRoomSQL(RoomID, RoomNumber, RoomType, RoomCapacity, HouseID):
    # Check if the room is valid
    if validation.RoomValidation(RoomNumber, RoomType, RoomCapacity, HouseID):
        
        conn = sqlite3.connect('./backend/WillowInnDB.db')
        cursor = conn.cursor()
        # Update the room
        cursor.execute(f"UPDATE RoomTable SET RoomNumber = '{RoomNumber}', RoomType = '{RoomType}', RoomCapacity = '{RoomCapacity}', HouseID = '{HouseID}' WHERE RoomID = '{RoomID}'")
        conn.commit()
        conn.close()
        
        tk.messagebox.showinfo("Success", "Room Edited Successfully")
        auditlog("Room Edited") # Log the editing of the room
        return True
    else:
        auditlog("Room Edit Failed") # Log the failure of the room edit
        return False
 
    
def AddRoomSQL(RoomNumber, RoomType, RoomCapacity, HouseID):
    # Check if the room is valid
    if validation.RoomValidation(RoomNumber, RoomType, RoomCapacity, HouseID):
        conn = sqlite3.connect('./backend/WillowInnDB.db')
        cursor = conn.cursor()

        cursor.execute('SELECT MAX(RoomID) FROM RoomTable')
        conn.commit()

        max_room_id = cursor.fetchone()[0]
        # Calculate the new RoomID by incrementing the maximum RoomID
        NewRID = max_room_id + 1 if max_room_id is not None else 1
        # Create a new room
        cursor.execute(f"INSERT INTO RoomTable (RoomID, RoomNumber, RoomType, RoomCapacity, HouseID) VALUES ('{NewRID}', '{RoomNumber}', '{RoomType}', '{RoomCapacity}', '{HouseID}')")
        conn.commit()
        conn.close()
        
        tk.messagebox.showinfo("Success", "Room Added Successfully")
        auditlog("Room Added") # Log the addition of the room
        return True
    else:
        auditlog("Room Add Failed") # Log the failure of the room addition
        return False
    
def DeleteRoomSQL(RoomID):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()
    # Delete the room
    cursor.execute(f"DELETE FROM RoomTable WHERE RoomID = '{RoomID}'")
    conn.commit()

    conn.close()
    auditlog("Room Deleted") # Log the deletion of the room
    
#### Bed Buttons ###

def EditBedSQL(BedID, RoomID, BedNumber, BedStatus):
    # Check if the bed is valid
    if validation.BedValidation(RoomID, BedNumber, BedStatus):
        
        conn = sqlite3.connect('./backend/WillowInnDB.db')
        cursor = conn.cursor()
        # Update the bed
        cursor.execute(f"UPDATE BedTable SET RoomID = '{RoomID}', BedNumber = '{BedNumber}', BedStatus = '{BedStatus}' WHERE BedID = '{BedID}'")
        conn.commit()
        conn.close()
        # Dialog box to show success message
        tk.messagebox.showinfo("Success", "Bed Edited Successfully")
        auditlog("Bed Edited") # Log the editing of the bed
        return True
    else:
        auditlog("Bed Edit Failed") # Log the failure of the bed edit
        return False
    
def AddBedSQL(RoomID, BedNumber, BedStatus):
    # Check if the bed is valid
    if validation.BedValidation(RoomID, BedNumber, BedStatus):
        conn = sqlite3.connect('./backend/WillowInnDB.db')
        cursor = conn.cursor()
        # Get the maximum BedID
        cursor.execute('SELECT MAX(BedID) FROM BedTable')
        conn.commit()

        max_bed_id = cursor.fetchone()[0]
        # Calculate the new BedID by incrementing the maximum BedID
        NewBID = max_bed_id + 1 if max_bed_id is not None else 1
        # Create a new bed
        cursor.execute(f"INSERT INTO BedTable (BedID, RoomID, BedNumber, BedStatus) VALUES ('{NewBID}', '{RoomID}', '{BedNumber}', '{BedStatus}')")
        conn.commit()
        conn.close()
        
        tk.messagebox.showinfo("Success", "Bed Added Successfully")
        auditlog("Bed Added") # Log the addition of the bed
        return True
    else:
        auditlog("Bed Add Failed") # Log the failure of the bed addition
        return False
    
def DeleteBedSQL(BedID):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()
    # Delete the bed
    cursor.execute(f"DELETE FROM BedTable WHERE BedID = '{BedID}'")
    conn.commit()

    conn.close()
    auditlog("Bed Deleted") # Log the deletion of the bed

#### User Buttons ###

def EditUserSQL(SqlID, Username, Password, FirstName, LastName, DOB, ContactNumber, Cmbo_Role, Cmbo_EnrollmentStatus, Message, HouseID, RoomID, BedID):
    
    if validation.UserValidation(Username, Password, FirstName, LastName, DOB, ContactNumber, Cmbo_Role, Cmbo_EnrollmentStatus, HouseID, notEdit=False):
        
        conn = sqlite3.connect('./backend/WillowInnDB.db')
        cursor = conn.cursor()

        cursor.execute(f"UPDATE UserTable SET Username = '{Username}', Password = '{Password}', FirstName = '{FirstName}', LastName = '{LastName}', DOB = '{DOB}', ContactNumber = '{ContactNumber}', RoleID = '{Cmbo_Role}', EnrollmentStatus = '{Cmbo_EnrollmentStatus}', Message = '{Message}', HouseID = '{HouseID}' WHERE UserID = '{SqlID}'")
        conn.commit()
        conn.close()
        
        tk.messagebox.showinfo("Success", "User Edited Successfully")
        auditlog("User Edited")
        return True
    else:
        auditlog("User Edit Failed")
        return False
    
def AddUserSQL(Username, Password, FirstName, LastName, DOB, ContactNumber, Cmbo_Role, Cmbo_EnrollmentStatus, Message, HouseID, RoomID, BedID):
    
    if validation.UserValidation(Username, Password, FirstName, LastName, DOB, ContactNumber, Cmbo_Role, Cmbo_EnrollmentStatus, HouseID):
        conn = sqlite3.connect('./backend/WillowInnDB.db')
        cursor = conn.cursor()
        # Get the maximum UserID
        cursor.execute('SELECT MAX(UserID) FROM UserTable')
        conn.commit()

        max_user_id = cursor.fetchone()[0]
        # Calculate the new UserID by incrementing the maximum UserID
        NewUID = max_user_id + 1 if max_user_id is not None else 1

        cursor.execute(f"INSERT INTO UserTable (UserID, Username, Password, FirstName, LastName, DOB, ContactNumber, RoleID, EnrollmentStatus, Message, HouseID, RoomID, BedID) VALUES ('{NewUID}', '{Username}', '{Password}', '{FirstName}', '{LastName}', '{DOB}', '{ContactNumber}', '{Cmbo_Role}', '{Cmbo_EnrollmentStatus}', '{Message}', '{HouseID}', '{RoomID}', '{BedID}')")
        conn.commit()
        conn.close()
        
        tk.messagebox.showinfo("Success", "User Added Successfully")
        auditlog("User Added")
        return True
    else:
        auditlog("User Add Failed")
        return False
    
def DeleteUserSQL(SqlID):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM UserTable WHERE UserID = '{SqlID}'")
    conn.commit()

    conn.close()
    auditlog("User Deleted")
    
    

























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