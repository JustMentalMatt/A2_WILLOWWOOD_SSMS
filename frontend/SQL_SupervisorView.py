import sqlite3
from CTkTable import *
from customtkinter import *
import validation
import tkinter as tk

from validation import auditlog


def SUPVEditUserSQL(SqlID, Username, Password, FirstName, LastName, DOB, ContactNumber, Cmbo_Role, Cmbo_EnrollmentStatus, Message, HouseID, RoomID, BedID):
   
    if validation.UserValidation(Username, Password, FirstName, LastName, DOB, ContactNumber, Cmbo_Role, Cmbo_EnrollmentStatus, HouseID):
        
        conn = sqlite3.connect('./backend/WillowInnDB.db')
        cursor = conn.cursor()

        cursor.execute(f"UPDATE UserTable SET Username = '{Username}', Password = '{Password}', FirstName = '{FirstName}', LastName = '{LastName}', DOB = '{DOB}', ContactNumber = '{ContactNumber}', RoleID = '{Cmbo_Role}', EnrollmentStatus = '{Cmbo_EnrollmentStatus}', Message = '{Message}', HouseID = '{HouseID}' WHERE UserID = '{SqlID}'")
        conn.commit()
        conn.close()
        
        tk.messagebox.showinfo("Success", "User Edited Successfully")
        auditlog("User Edited")
    else:
        auditlog("User Edit Failed")