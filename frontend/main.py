
from customtkinter import *
from threading import Thread
import time

from WIN_LoginMain import *
from WIN_AdminView import *
from WIN_SupervisorView import *
from WIN_VolunteerView import *


def auditlog(data):

    with open("frontend/uservar.txt", "r") as file:
        userVAR = file.read().strip()
        file.close()
        
    if userVAR == "":
        userVAR = "UNKNOWN"
    with open("auditlog.txt", "a") as file:
        file.write('{:<20}'.format(time.strftime('%Y-%m-%d %H:%M:%S')) + '{:<20}'.format(" | User: " + userVAR) + '{:<20}'.format(" | " + data) + "\n")
        file.close()

class AdminMenu(CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.geometry("1056x645")
        self.resizable(False, False)
        self.title(f"Logged In | Manager: {usernameVAR} | WILLOW WOOD INN")

        self.main = adminView(self)
        self.mainloop()

class SupervisorMenu(CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.geometry("1056x645")
        self.resizable(False, False)
        self.title(f"Logged In | Supervisor: {usernameVAR} | WILLOW WOOD INN")

        self.main = supervisorView(self)
        self.mainloop()

class VolunteerMenu(CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.geometry("1056x645")
        self.resizable(False, False)
        self.title(f"Logged In | Volunteer: {usernameVAR} | WILLOW WOOD INN")

        self.main = volunteerView(self)
        self.mainloop()

LoggedIn = True 
def initiate_login():
    if LoggedIn:
        object = mainApp(handle_login_result)
        global t
        t = Thread(target=object)  # Create a thread to run AdminMenu
        t.start()
    else:
        print("Program Disabled. Please contact the administrator.")

def determineView(role):
    if role == 3:
        AdminMenu()
    elif role == 2:
        SupervisorMenu()
    elif role == 1:
        VolunteerMenu()
    else:
        print("main.py | User Role not found")

def handle_login_result(successful, username, role):
    global usernameVAR
    usernameVAR = username
    if successful:
        print("main.py | Login Successful")
        print("main.py | Username:", username)
        print("main.py | Role:", role)
        
        determineView(role)
        
        with open("frontend/uservar.txt", "w") as file:
            file.write(username)
            file.close()
        auditlog("User logged in")
    else:
        print("main.py | Login Failed")
        with open("frontend/uservar.txt", "w") as file:
            file.write("")
            file.close()
        auditlog("Login attempt failed")
        tk.messagebox.showerror("Login Attempt", "No User found with the given credentials. Please try again.")

if __name__ == "__main__":
    initiate_login()