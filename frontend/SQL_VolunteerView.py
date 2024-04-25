import sqlite3
from CTkTable import *
from customtkinter import *
import validation
import tkinter as tk
import datetime

from validation import auditlog


def SQL_VolunteerView_EnrollInTask(TaskID, VolunteerUsername):
    
    TaskID = int(TaskID)
    
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT MAX(BookingID) FROM BookingTable')
    conn.commit()

    max_booking_id = cursor.fetchone()[0]
    NewBookingID = max_booking_id + 1 if max_booking_id is not None else 1
    
    UserID = cursor.execute(f"SELECT UserID FROM UserTable WHERE Username = '{VolunteerUsername}'")
    conn.commit()
    UserID = cursor.fetchone()
        
    cursor.execute(f"SELECT UserID FROM BookingTable WHERE TaskID = {TaskID}")
    conn.commit()
    existingUser = cursor.fetchone()
    if existingUser:
        tk.messagebox.showerror("Error", "User already enrolled in this task")
    else:
        cursor.execute(f"INSERT INTO BookingTable (BookingID, TaskID, UserID, BookingDate) VALUES ({NewBookingID}, {TaskID}, {UserID[0]}, CURRENT_TIMESTAMP)")
        conn.commit()
        
        conn.close()
        auditlog(f"User {VolunteerUsername} enrolled in task {TaskID}")
        tk.messagebox.showinfo("Success", f"User {VolunteerUsername} enrolled in task {TaskID}")
        
def SQL_VolunteerView_FetchTasks(VolunteerUsername, search_query=None):
    
    conn = sqlite3.connect('./backend/WillowInnDB.db')
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT UserID FROM UserTable WHERE Username = '{VolunteerUsername}'")
    conn.commit()
    UserID = cursor.fetchone()
    
    cursor.execute(f"SELECT TaskID, TaskName FROM TaskTable WHERE TaskID IN (SELECT TaskID FROM BookingTable WHERE UserID = {UserID[0]})")
    conn.commit()
    
    tasks = cursor.fetchall()
    
    conn.close()
    
    if search_query is not None:
        tasks = [task for task in tasks if search_query.lower() in task[1].lower()]
    
    return tasks

