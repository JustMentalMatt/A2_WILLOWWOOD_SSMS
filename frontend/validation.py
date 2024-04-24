# PUT VALIDATION METHODS IN HERE #

import re
import sqlite3

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