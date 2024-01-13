import sqlite3
import customtkinter
import tkinter
from tkinter import ttk

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

def AdminUsersTable_ENTRY():

    root = customtkinter.CTkToplevel()
    root.geometry("360x280")
    root.title("Admin Users - Record Entry")
    root.resizable(False,False)
    
    # id, name, email, joining_date, password, username
    tab_id = customtkinter.CTkEntry(master=root, width=30) 
    tab_id.grid(column=1, row=0, pady=5, sticky="WE")
    tab_id_label = customtkinter.CTkLabel(master=root, text="ID:", font=("Roboto", 16))
    tab_id_label.grid(column=0, row=0)
    #
    tab_name = customtkinter.CTkEntry(master=root, width=30) 
    tab_name.grid(column=1, row=1, pady=5, sticky="WE")
    tab_name_label = customtkinter.CTkLabel(master=root, text="Name:", font=("Roboto", 16))
    tab_name_label.grid(column=0, row=1)
    #
    tab_email = customtkinter.CTkEntry(master=root, width=30) 
    tab_email.grid(column=1, row=2, pady=5, sticky="WE")
    tab_email_label = customtkinter.CTkLabel(master=root, text="Email:", font=("Roboto", 16))
    tab_email_label.grid(column=0, row=2)
    #
    tab_birthDate = customtkinter.CTkEntry(master=root, width=30) 
    tab_birthDate.grid(column=1, row=3, pady=5, sticky="WE")
    tab_birthDate_label = customtkinter.CTkLabel(master=root, text="Birthday:", font=("Roboto", 16))
    tab_birthDate_label.grid(column=0, row=3)
    #
    tab_pass = customtkinter.CTkEntry(master=root, width=30) 
    tab_pass.grid(column=1, row=4, pady=5, sticky="WE")
    tab_pass_label = customtkinter.CTkLabel(master=root, text="Password:", font=("Roboto", 16))
    tab_pass_label.grid(column=0, row=4)
    #
    tab_usrName = customtkinter.CTkEntry(master=root, width=30) 
    tab_usrName.grid(column=1, row=5, pady=5, sticky="WE")
    tab_usrName_label = customtkinter.CTkLabel(master=root, text="Username:", font=("Roboto", 16))
    tab_usrName_label.grid(column=0, row=5)

def DefaultUsersTable_ENTRY():

    root = customtkinter.CTkToplevel()
    root.geometry("360x280")
    root.title("Admin Users - Record Entry")
    root.resizable(False,False)
    
    # id, name, age, username, password, email, join date 
    tab_id = customtkinter.CTkEntry(master=root, width=30) 
    tab_id.grid(column=1, row=0, pady=5, sticky="WE")
    tab_id_label = customtkinter.CTkLabel(master=root, text="ID:", font=("Roboto", 16))
    tab_id_label.grid(column=0, row=0)
    #
    tab_name = customtkinter.CTkEntry(master=root, width=30) 
    tab_name.grid(column=1, row=1, pady=5, sticky="WE")
    tab_name_label = customtkinter.CTkLabel(master=root, text="Name:", font=("Roboto", 16))
    tab_name_label.grid(column=0, row=1)
    #
    tab_age = customtkinter.CTkEntry(master=root, width=30) 
    tab_age.grid(column=1, row=2, pady=5, sticky="WE")
    tab_age_label = customtkinter.CTkLabel(master=root, text="Age:", font=("Roboto", 16))
    tab_age_label.grid(column=0, row=2)
    #
    tab_usrName = customtkinter.CTkEntry(master=root, width=30) 
    tab_usrName.grid(column=1, row=3, pady=5, sticky="WE")
    tab_usrName_label = customtkinter.CTkLabel(master=root, text="Username:", font=("Roboto", 16))
    tab_usrName_label.grid(column=0, row=3)

    tab_pass = customtkinter.CTkEntry(master=root, width=30) 
    tab_pass.grid(column=1, row=4, pady=5, sticky="WE")
    tab_pass_label = customtkinter.CTkLabel(master=root, text="Password:", font=("Roboto", 16))
    tab_pass_label.grid(column=0, row=4)

    tab_email = customtkinter.CTkEntry(master=root, width=30) 
    tab_email.grid(column=1, row=5, pady=5, sticky="WE")
    tab_email_label = customtkinter.CTkLabel(master=root, text="Email:", font=("Roboto", 16))
    tab_email_label.grid(column=0, row=5)

    tab_birthDate = customtkinter.CTkEntry(master=root, width=30) 
    tab_birthDate.grid(column=1, row=6, pady=5, sticky="WE")
    tab_birthDate_label = customtkinter.CTkLabel(master=root, text="Birthday:", font=("Roboto", 16))
    tab_birthDate_label.grid(column=0, row=6)

    
    #Btn
    def submit():
        
        sqliteConnection = sqlite3.connect('./backend/database.db')
        cursor = sqliteConnection.cursor()
        
        try:
            cursor.execute("INSERT INTO Admin_Users VALUES (:id, :name, :email, :birthDate, :password, :username)",
                {  
                    'id': tab_id.get(),
                    'name': tab_name.get(),
                    'email': tab_email.get(),
                    'birthDate': tab_birthDate.get(),
                    'password': tab_pass.get(),
                    'username': tab_usrName.get()
                })
        
            sqliteConnection.commit()
            cursor.close()
        except:
            pass
        
        tab_id.delete(0, customtkinter.END)
        tab_name.delete(0, customtkinter.END)
        tab_email.delete(0, customtkinter.END)
        tab_birthDate.delete(0, customtkinter.END)
        tab_pass.delete(0, customtkinter.END)
        tab_usrName.delete(0, customtkinter.END)
    
    submit_btn = customtkinter.CTkButton(master=root, text="Add Record", font=("Roboto", 16), command=submit)
    submit_btn.grid(column=0, row=6, columnspan=2, pady=10, padx=5, ipadx=100)
    
    root.mainloop()
    
        
#AdminUsersTable_ENTRY()