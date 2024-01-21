import customtkinter as ctk
import sqlite3
from tkinter import *
from tkinter import ttk


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

login_window = ctk.CTk()
login_window.geometry("400x350")

def login():

    new_window = ctk.CTkToplevel(login_window) 
    new_window.title("Login Window") 
    new_window.geometry("400x350") 

    sqliteConnection = sqlite3.connect('./backend/database.db')
    cursor = sqliteConnection.cursor()
    credential_fetch = "SELECT username, password FROM Admin_Users"
    cursor.execute(credential_fetch)
    results = cursor.fetchall()
    
    for row in results:
        username = row[0]
        password = row[1]

        if entry1.get() == username and entry2.get() == password:
            print("Login Successful")
            return username #Returns the Logged in Username
        
frame = ctk.CTkFrame(master=login_window)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = ctk.CTkLabel(master=frame, text="Login System", font=("Roboto", 24))
label.pack(pady=12, padx=10)

entry1 = ctk.CTkEntry(master=frame, placeholder_text="Username")
entry1.pack(pady=12, padx=10)

entry2 = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
entry2.pack(pady=12, padx=10)

button = ctk.CTkButton(master=frame, text="Login", command=login)
button.pack(pady=12, padx=10)


login_window.mainloop()





ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.geometry("1300x350") # original: 1280x720
root.title("Database Viewer")
root.resizable(False,False)



                                        # --------- Frames --------- #:loggedUserName = login()
# Title Box:
titleboxFrame = ctk.CTkFrame(master=root)
titleboxFrame.grid(column=0, columnspan=2, row=0, rowspan=1, ipadx=5, ipady=5, padx=20, pady=20, sticky="nsew")
tb_title = ctk.CTkLabel(master=titleboxFrame, text="SQLite Database Viewer", font=("Roboto", 24, "underline",))
tb_title.grid(column=0, row=0, ipadx=10, ipady=10, sticky="nsew")
tb_text = ctk.CTkLabel(master=titleboxFrame, text=" Database Viewer", font=("Roboto", 12))
tb_text.grid(column=0, columnspan=2, row=1, ipadx=10, sticky="w")

# User Info Box:
loggedUserName = "Admin"
usrinfoFrame = ctk.CTkFrame(master=root)
usrinfoFrame.grid(column=0, columnspan=2, row=2, rowspan=1, ipadx=5, ipady=5, padx=20, pady=10, sticky="nsew")
usrName = ctk.CTkLabel(master=usrinfoFrame, text="¬ Logged in as: " + loggedUserName, font=("Roboto", 14))
usrName.grid(column=0, row=0, ipadx=10, ipady=10, sticky="SW")

authLevel_admin = True # This is temporary. Meant to be fetched from login_gui.py
if authLevel_admin == True:
    authStatus = "Admin"
else:
    authStatus = "User"
usrAuth = ctk.CTkLabel(master=usrinfoFrame, text="¬ Auth Level:  " + authStatus, font=("Roboto", 14))
usrAuth.grid(column=0, row=2, ipadx=10, sticky="SW")
    
sqlUIFrame = ctk.CTkFrame(master=root)
sqlUIFrame.grid(column=2, columnspan=5, row=0, rowspan=5, ipadx=5, ipady=5, padx=30, pady=20, sticky="NSEW")
sqlUI = ctk.CTkLabel(master=sqlUIFrame,font=("Roboto", 130))
sqlUI.grid(column=0, columnspan=5, row=0, rowspan=2, ipadx=10, ipady=10, sticky="NSEW")

root.mainloop()
