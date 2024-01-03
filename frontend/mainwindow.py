import customtkinter
import sqlite3
from tkinter import *
from tkinter import ttk
from sqliteui import AdminUsersTable_ENTRY
from sqliteui import DefaultUsersTable_ENTRY


loggedUserName = "[USERNAME]"


def mainWindow():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    root = customtkinter.CTk()
    root.geometry("1300x350") # original: 1280x720
    root.title("Database Viewer")
    root.resizable(False,False)
    
                                            # --------- Frames --------- #:
    
    # Title Box:
    titleboxFrame = customtkinter.CTkFrame(master=root)
    titleboxFrame.grid(column=0, columnspan=2, row=0, rowspan=1, ipadx=5, ipady=5, padx=20, pady=20, sticky="nsew")
    tb_title = customtkinter.CTkLabel(master=titleboxFrame, text="SQLite Database Viewer", font=("Roboto", 24, "underline",))
    tb_title.grid(column=0, row=0, ipadx=10, ipady=10, sticky="nsew")
    tb_text = customtkinter.CTkLabel(master=titleboxFrame, text=" Database Viewer", font=("Roboto", 12))
    tb_text.grid(column=0, columnspan=2, row=1, ipadx=10, sticky="w")
    
    # User Info Box:
    
    usrinfoFrame = customtkinter.CTkFrame(master=root)
    usrinfoFrame.grid(column=0, columnspan=2, row=2, rowspan=1, ipadx=5, ipady=5, padx=20, pady=10, sticky="nsew")
    usrName = customtkinter.CTkLabel(master=usrinfoFrame, text="¬ Logged in as: " + loggedUserName, font=("Roboto", 14))
    usrName.grid(column=0, row=0, ipadx=10, ipady=10, sticky="SW")
    authLevel_admin = True # This is temporary. Meant to be fetched from login_gui.py
    if authLevel_admin == True:
        authStatus = "Admin"
    else:
        authStatus = "User"
    usrAuth = customtkinter.CTkLabel(master=usrinfoFrame, text="¬ Auth Level:  " + authStatus, font=("Roboto", 14))
    usrAuth.grid(column=0, row=2, ipadx=10, sticky="SW")
        
    sqlUIFrame = customtkinter.CTkFrame(master=root)
    sqlUIFrame.grid(column=2, columnspan=5, row=0, rowspan=5, ipadx=5, ipady=5, padx=30, pady=20, sticky="NSEW")
    sqlUI = customtkinter.CTkLabel(master=sqlUIFrame,font=("Roboto", 130))
    sqlUI.grid(column=0, columnspan=5, row=0, rowspan=2, ipadx=10, ipady=10, sticky="NSEW")
    
    def admin_usersTable():
        conn = sqlite3.connect('./backend/database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Admin_Users")
        rows = c.fetchall()
        t = ttk.Treeview(sqlUI)
        t["columns"] = ("one", "two", "three", "four", "five")
        t.heading("#0", text="ID")
        t.column("#0", minwidth=50, width=50, stretch=YES)
        t.heading("one", text="Name")
        t.column("one", minwidth=150, width=150, stretch=YES)
        t.heading("two", text="Email")
        t.column("two", minwidth=200, width=200, stretch=YES)
        t.heading("three", text="Join Date")
        t.column("three", minwidth=150, width=150, stretch=YES)
        t.heading("four", text="Username")
        t.column("four", minwidth=150, width=150, stretch=YES)
        t.heading("five", text="Password")
        t.column("five", minwidth=150, width=150, stretch=YES)

        for row in rows:
            t.insert("", END, text=row[0], values=(row[1], row[2], row[3], row[4], row[5]))

        t.grid(column=0, columnspan=5, row=0, rowspan=2, padx=5, ipadx=10, ipady=10, sticky="NS")
        
        conn.commit()
        c.close()
    
    def default_usersTable():
        conn = sqlite3.connect('./backend/database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM default_users")
        rows = c.fetchall()
        t = ttk.Treeview(sqlUI)
        t["columns"] = ("one", "two", "three", "four", "five", "six")
        t.heading("#0", text="ID")
        t.column("#0", minwidth=50, width=50, stretch=YES)
        t.heading("one", text="Name")
        t.column("one", minwidth=150, width=150, stretch=YES)
        t.heading("two", text="Age")
        t.column("two", minwidth=200, width=200, stretch=YES)
        t.heading("three", text="Username")
        t.column("three", minwidth=150, width=150, stretch=YES)
        t.heading("four", text="Password")
        t.column("four", minwidth=150, width=150, stretch=YES)
        t.heading("five", text="Email")
        t.column("five", minwidth=150, width=150, stretch=YES)
        t.heading("six", text="Join Date")
        t.column("six", minwidth=150, width=150, stretch=YES)
    
   #admin_usersTable() # SQLUI - Loads data from database into table - (frontend\sqliteui.py)
    default_usersTable()
    
    def createRecord():
        #AdminUsersTable_ENTRY() # SQLUI - Create Records for Admin_Users Table - (frontend\sqliteui.py)
        DefaultUsersTable_ENTRY()
        
    createRecord_btn = customtkinter.CTkButton(master=root, text="Add Record", font=("Roboto", 16), command=createRecord)
    createRecord_btn.grid(column=3, row=4, columnspan=3, padx=5, ipadx=50, sticky="SW")
    
    def refreshTable():
        #admin_usersTable()
        default_usersTable()
    refreshTable_btn = customtkinter.CTkButton(master=root, text="Refresh", font=("Roboto", 16), command=refreshTable)
    refreshTable_btn.grid(column=3, row=4, columnspan=3, padx=5, ipadx=10, sticky="SE")
    
    # # Button Box:
    # btnboxFrame = customtkinter.CTkFrame(master=root)
    # btnboxFrame.grid(column=0, columnspan=3, row=0, rowspan=10, ipadx=20, ipady=20, padx=20, pady=20, sticky="nsew")
    

#########################################################################################################################


    # tableText = customtkinter.CTkLabel(master=btnboxFrame, text="Browse Tables:", font=("Roboto", 24))
    # tableText.grid(column=0, row=0, pady=(20, 0), sticky="nsew")
    
    # def optionmenu_callback(choice):
    #     print("optionmenu dropdown clicked:", choice)

    # combobox = customtkinter.CTkOptionMenu(master=frame, values=["Admin_Users", "Guest_Users"], command=optionmenu_callback) 
                                          
                                                                         
    # combobox.grid(row=1, column=1)
    # combobox.set("TABLES")  # set initial value
    
    
    root.mainloop()
    
#mainWindow()