import sqlite3
from CTkTable import *
from customtkinter import *
import tkinter as tk

from validation import auditlog


def SQL_VolunteerView_EnrollInTask(TaskID, VolunteerUsername):
    # Convert TaskID to int
    TaskID = int(TaskID)
    conn = sqlite3.connect('C:/Users/Matthew/Documents/FINAL_A2_WILLOWWOOD_SSMS/backend/WillowInnDB.db')
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(BookingID) FROM BookingTable')
    conn.commit()
    # Get the max BookingID from the BookingTable
    max_booking_id = cursor.fetchone()[0]
    NewBookingID = max_booking_id + 1 if max_booking_id is not None else 1
    # Get the UserID of the Volunteer
    UserID = cursor.execute(f"SELECT UserID FROM UserTable WHERE Username = '{VolunteerUsername}'")
    conn.commit()
    UserID = cursor.fetchone()
    # Check if the user is already enrolled in the task
    cursor.execute(f"SELECT * FROM BookingTable WHERE TaskID = {TaskID} AND UserID = {UserID[0]}")
    conn.commit()
    existingUser = cursor.fetchone()
    if existingUser: # If the user is already enrolled in the task show an error message
        tk.messagebox.showerror("Error", "User already enrolled in this task")
    else: # If the user is not already enrolled in the task, enroll them
        cursor.execute(f"INSERT INTO BookingTable (BookingID, TaskID, UserID, BookingDate) VALUES ({NewBookingID}, {TaskID}, {UserID[0]}, CURRENT_TIMESTAMP)")
        conn.commit()
        conn.close()
        # Show a success message
        auditlog(f"User {VolunteerUsername} enrolled in task {TaskID}")
        tk.messagebox.showinfo("Success", f"User {VolunteerUsername} enrolled in task {TaskID}")
        
def SQL_VolunteerView_FetchTasks(VolunteerUsername, search_query=None):
    
    conn = sqlite3.connect('C:/Users/Matthew/Documents/FINAL_A2_WILLOWWOOD_SSMS/backend/WillowInnDB.db')
    cursor = conn.cursor()
    # Get the UserID of the Volunteer
    cursor.execute(f"SELECT UserID FROM UserTable WHERE Username = '{VolunteerUsername}'")
    conn.commit()
    UserID = cursor.fetchone()
    # Get the TaskID and TaskName of the tasks the Volunteer is enrolled in
    cursor.execute(f"SELECT TaskID, TaskName FROM TaskTable WHERE TaskID IN (SELECT TaskID FROM BookingTable WHERE UserID = {UserID[0]})")
    conn.commit()
    
    tasks = cursor.fetchall()
    
    conn.close()
    
    if search_query is not None: # If a search query is provided, filter the tasks
        tasks = [task for task in tasks if search_query.lower() in task[1].lower()]
    
    return tasks

def SQL_VolunteerView_EnrollmentStatus(VolunteerUsername):
    
    conn = sqlite3.connect('C:/Users/Matthew/Documents/FINAL_A2_WILLOWWOOD_SSMS/backend/WillowInnDB.db')
    cursor = conn.cursor()
    # Get the UserID of the Volunteer
    cursor.execute(f"SELECT UserID FROM UserTable WHERE Username = '{VolunteerUsername}'")
    conn.commit()
    UserID = cursor.fetchone()
    # Get the EnrollmentStatus of the Volunteer
    cursor.execute(f"SELECT EnrollmentStatus FROM UserTable WHERE UserID = {UserID[0]}")
    conn.commit()
    EnrollmentStatus = cursor.fetchone()
    conn.close()
    
    return EnrollmentStatus[0]

def SQL_VolunteerView_HouseStatus(VolunteerUsername):

    conn = sqlite3.connect('C:/Users/Matthew/Documents/FINAL_A2_WILLOWWOOD_SSMS/backend/WillowInnDB.db')
    cursor = conn.cursor()
    # Get the HouseID of the Volunteer if they are assigned to a house
    cursor.execute(f"SELECT HouseID FROM UserTable WHERE Username = '{VolunteerUsername}'")
    conn.commit()
    
    status = cursor.fetchall()
    
    conn.close()
    
    return status
    
def SQL_VolunteerView_EnrollUser(VolunteerUsername):
        
        conn = sqlite3.connect('C:/Users/Matthew/Documents/FINAL_A2_WILLOWWOOD_SSMS/backend/WillowInnDB.db')
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT UserID FROM UserTable WHERE Username = '{VolunteerUsername}'")
        conn.commit()
        UserID = cursor.fetchone()
        
        cursor.execute(f"UPDATE UserTable SET EnrollmentStatus = 'Enrolled' WHERE UserID = {UserID[0]}")
        conn.commit()
        
        conn.close()
    
def SQL_VolunteerView_AssignUserHouse(VolunteerUsername, house):
        
        conn = sqlite3.connect('C:/Users/Matthew/Documents/FINAL_A2_WILLOWWOOD_SSMS/backend/WillowInnDB.db')
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT UserID FROM UserTable WHERE Username = '{VolunteerUsername}'")
        conn.commit()
        UserID = cursor.fetchone()
        
        cursor.execute(f"UPDATE UserTable SET HouseID = {house} WHERE UserID = {UserID[0]}")
        conn.commit()
        
        conn.close()
        
        tk.messagebox.showinfo("Success", f"User {VolunteerUsername} assigned to house {house}")
        auditlog(f"User {VolunteerUsername} assigned to house {house}")