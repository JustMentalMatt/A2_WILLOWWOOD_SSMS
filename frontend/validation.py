# PUT VALIDATION METHODS IN HERE #

import re
import sqlite3
import tkinter as tk
import time

def auditlog(data):
    
    with open("frontend/uservar.txt", "r") as file:
        userVAR = file.read().strip()
        file.close()
        
    if userVAR == "":
        userVAR = "UNKNOWN"
    with open("auditlog.txt", "a") as file:
        file.write('{:<20}'.format(time.strftime('%Y-%m-%d %H:%M:%S')) + '{:<20}'.format(" | User: " + userVAR) + '{:<20}'.format(" | " + data) + "\n")
        file.close()


def validateDate(date):
    # Regular expression for YYYY-MM-DD format
    datePattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    if not datePattern.match(date):
        return False
    
    year, month, day = map(int, date.split('-'))
    
    if month < 1 or month > 12:
        return False
    if day < 1 or day > 31:
        return False
    if month in [4, 6, 9, 11] and day > 30:
        return False
    if month == 2:
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            if day > 29:
                return False
        elif day > 28:
            return False
    
    return True

def validateTime(time):
    # Regular expression for HH:MM:SS format
    timePattern = re.compile(r'^\d{2}:\d{2}:\d{2}$')
    if not timePattern.match(time):
        return False
    
    hours, minutes, seconds = map(int, time.split(':'))

    if hours < 0 or hours > 23:
        return False
    if minutes < 0 or minutes > 59:
        return False
    if seconds < 0 or seconds > 59:
        return False

    return True

def datetimeCheck(data):
    datetimePattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')

    if not datetimePattern.match(data):
        return False

    # Extract date and time components
    date_time = data.split(' ')
    date = date_time[0]
    time = date_time[1]

    if not validateDate(date):
        return False

    if not validateTime(time):
        return False

    return True

def validatePostcode(postcode):
    postcodePattern = re.compile(r'^[A-Z]{2}\d{2}\s\d[A-Z]{2}$')
    return postcodePattern.match(postcode)
    
def validateEmail(email):
    emailPattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    return emailPattern.match(email)
    
def validatePhone(phone):
    phonePattern = re.compile(r'^\d{11}$')
    return phonePattern.match(phone)
    
def validateName(name):
    namePattern = re.compile(r'^[A-Za-z]+ [A-Za-z]+$')
    return namePattern.match(name)
    
def validateUsername(username):
    usernamePattern = re.compile(r'^[A-Za-z0-9_]+$')
    return usernamePattern.match(username)

def presenceCheck(data):
    return data != None and data != "" and data != " " and data != "None" and data != "null"

def typeCheck(data, expectedType):
    return isinstance(data, expectedType)
    # expectedType: int, float, str, bool, list, dict, tuple, set, NoneType

def lookupCheck(value, lookupValues):
    return value in lookupValues

def lengthCheck(data, minLength=None, maxLength=None, exactLength=None):
    length = len(data)
    
    if exactLength is not None:
        return length == exactLength
    elif minLength is not None and maxLength is None:
        return length >= minLength
    elif maxLength is not None and minLength is None:
        return length <= maxLength
    elif minLength is not None and maxLength is not None:
        return minLength <= length <= maxLength
    else:
        return False

def rangeCheck(value, minValue=None, maxValue=None, exactValue=None):
    
    if isinstance(value, str):
        try:
            value = int(value)
        except ValueError:
            return False
    
    if exactValue is not None:
        return value == exactValue
    elif minValue is not None and maxValue is None:
        return value >= minValue
    elif maxValue is not None and minValue is None:
        return value <= maxValue
    elif minValue is not None and maxValue is not None:
        return minValue <= value <= maxValue
    else:
        return False

def dbPresenceCheck(value, table):
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT {value} FROM {table}")
        cursor.fetchall()
        return True
    except IndexError as e:
        print(e)
        return False
    
    
    
# Validation functions for each table
    
def UserValidation(Username, Password, FirstName, LastName, DOB, ContactNumber, Cmbo_Role, Cmbo_EnrollmentStatus):
    
    if not presenceCheck(Username):
        tk.messagebox.showerror("Error", "Username is empty")
        
    elif not presenceCheck(Password):
        tk.messagebox.showerror("Error", "Password is empty")
        
    elif not lengthCheck(Password, 8):
        tk.messagebox.showerror("Error", "Password must be at least 8 characters long")
        
    elif not presenceCheck(FirstName):
        tk.messagebox.showerror("Error", "First Name is empty")
        
    elif not presenceCheck(LastName):
        tk.messagebox.showerror("Error", "Last Name is empty")
        
    elif not presenceCheck(DOB):
        tk.messagebox.showerror("Error", "Date of Birth is empty")
        
    elif not presenceCheck(ContactNumber):
        tk.messagebox.showerror("Error", "Contact Number is empty")
        
    elif not presenceCheck(Cmbo_Role):
        tk.messagebox.showerror("Error", "Role is empty")
        
    elif not presenceCheck(Cmbo_EnrollmentStatus):
        tk.messagebox.showerror("Error", "Enrollment Status is empty")
    
    elif not validateDate(DOB):
        tk.messagebox.showerror("Error", "Invalid Date of Birth")
        
    elif not validatePhone(ContactNumber):
        tk.messagebox.showerror("Error", "Invalid Contact Number")
        
    else:
        return True
    
def HouseValidation(HouseName, HouseAddress, HousePhone, HouseEmail):
    
    if not presenceCheck(HouseName):
        tk.messagebox.showerror("Error", "House Name is empty")
        
    elif not presenceCheck(HouseAddress):
        tk.messagebox.showerror("Error", "House Address is empty")
        
    elif not presenceCheck(HousePhone):
        tk.messagebox.showerror("Error", "House Phone is empty")
        
    elif not presenceCheck(HouseEmail):
        tk.messagebox.showerror("Error", "House Email is empty")
        
    elif not validatePhone(HousePhone):
        tk.messagebox.showerror("Error", "Invalid House Phone")
        
    elif not validateEmail(HouseEmail):
        tk.messagebox.showerror("Error", "Invalid House Email")
        
    else:
        return True
    
def TaskValidation(TaskName, Capacity, DifficultyLevel, Points):
    
    if not presenceCheck(TaskName):
        tk.messagebox.showerror("Error", "Task Name is empty")
        
    elif not presenceCheck(Capacity):
        tk.messagebox.showerror("Error", "Capacity is empty")
        
    elif not presenceCheck(DifficultyLevel):
        tk.messagebox.showerror("Error", "Difficulty Level is empty")
        
    elif not presenceCheck(Points):
        tk.messagebox.showerror("Error", "Points is empty")
        
    elif not rangeCheck(Capacity, 1):
        tk.messagebox.showerror("Error", "Capacity must be at least 1")
        
    elif not lookupCheck(DifficultyLevel, ["Easy", "Moderate", "Hard"]):
        tk.messagebox.showerror("Error", "Invalid Difficulty Level")
        
    elif not rangeCheck(Points, 1):
        tk.messagebox.showerror("Error", "Points must be at least 1")
        
    else:
        return True
    
def BookingValidaion(TaskID, UserID, BookingDate):

    if not presenceCheck(TaskID):
        tk.messagebox.showerror("Error", "Task ID is empty")
    
    elif not presenceCheck(UserID):
        tk.messagebox.showerror("Error", "User ID is empty")
    
    elif not presenceCheck(BookingDate):
        tk.messagebox.showerror("Error", "Booking Date is empty")
    
    elif not datetimeCheck(BookingDate):
        tk.messagebox.showerror("Error", "Invalid Booking Date")
    
    else:
        return True
    
def RoomValidation(RoomNumber, RoomType, RoomCapacity, HouseID):
    
    if not presenceCheck(RoomNumber):
        tk.messagebox.showerror("Error", "Room Number is empty")
        
    elif not presenceCheck(RoomType):
        tk.messagebox.showerror("Error", "Room Type is empty")
        
    elif not presenceCheck(RoomCapacity):
        tk.messagebox.showerror("Error", "Room Capacity is empty")
        
    elif not presenceCheck(HouseID):
        tk.messagebox.showerror("Error", "House ID is empty")
        
    elif not lookupCheck(RoomType, ["Single", "Double", "Triple", "Quad", "Queen", "King", "Twin", "Double-Double", "Studio", "Suite", "Mini-Suite", "Cabana", "Villa", "Condo", "Penthouse", "Duplex", "Triplex", "Quadplex", "Quintuplex"]):
        tk.messagebox.showerror("Error", "Invalid Room Type")
        
    elif not rangeCheck(RoomCapacity, 1):
        tk.messagebox.showerror("Error", "Room Capacity must be at least 1")
        
    else:
        return True
    
def BedValidation(RoomID, BedNumber, BedStatus):
    
    if not presenceCheck(RoomID):
        tk.messagebox.showerror("Error", "Room ID is empty")
        
    elif not presenceCheck(BedNumber):
        tk.messagebox.showerror("Error", "Bed Number is empty")
        
    elif not presenceCheck(BedStatus):
        tk.messagebox.showerror("Error", "Bed Status is empty")
        
    elif not rangeCheck(BedNumber, 1):
        tk.messagebox.showerror("Error", "Bed Number must be at least 1")
        
    elif not lookupCheck(BedStatus, ["Available", "Occupied", "Reserved"]):
        tk.messagebox.showerror("Error", "Invalid Bed Status")
        
    else:
        return True