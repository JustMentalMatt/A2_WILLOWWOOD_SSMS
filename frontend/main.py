import customtkinter as ctk
import tkinter as tk
from customtkinter import *
from CTkTable import CTkTable
from PIL import Image
import sqlite3
from threading import Thread

from WIN_AdminView import *
from WIN_LoginMain import *

# # login
# class LoginMenu(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         self.geometry("600x480")
#         self.title("i love jesus better than icecream")
#         self.resizable(False, False)

#         self.main = loginGUI(self)
#         self.mainloop()
        
#     def get_login_info(self):
#         return self.main.logged_in, self.main.username
        
# # admin-view
class AdminMenu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1056x645")
        self.resizable(False, False)
        self.title("Logged In - MANAGEMENT - WILLOW WOOD INN")

        self.main = adminView(self)
        self.mainloop()
                
# LoggedIn = True

# def tickle_my_pickle():

#     if LoggedIn == True:
#         AdminMenu()
#     else:
#         print("You are not authorized to access this page.")
           
# tickle_my_pickle()

from WIN_LoginMain import mainApp as LoginMenu


LoggedIn = True 
def initiate_login():
    if LoggedIn:
        object = LoginMenu(handle_login_result)
        global t
        t = Thread(target=object)  # Create a thread to run AdminMenu
        t.start()
    else:
        print("Program Disabled. Please contact the administrator.")

def viewManager(role):

    if role == 3:
        AdminMenu()
    elif role == 2:
        print("main.py | Manager")
    elif role == 1:
        print("main.py | Volunteer")
    else:
        print("main.py | User Role not found")

def handle_login_result(successful, username, role):
    if successful:
        print("main.py | Login Successful")
        print("main.py | Username:", username)
        print("main.py | Role:", role)
        viewManager(role)
    else:
        print("main.py | Login Failed")

if __name__ == "__main__":
    initiate_login()