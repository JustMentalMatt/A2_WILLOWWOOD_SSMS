from customtkinter import *

from WIN_LoginMain import *
from WIN_AdminView import *
from WIN_SupervisorView import *
from WIN_VolunteerView import *

from validation import auditlog


# This class launches the view for Manager users
class AdminMenu(CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.geometry("1056x645")
        self.resizable(False, False)
        self.title(f"Logged In | Manager: {usernameVAR} | WILLOW WOOD INN")

        self.main = adminView(self)
        self.mainloop()


# This class launches the view for Supervisor users
class SupervisorMenu(CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.geometry("1056x645")
        self.resizable(False, False)
        self.title(f"Logged In | Supervisor: {usernameVAR} | WILLOW WOOD INN")

        self.main = supervisorView(self)
        self.mainloop()


# This class launches the view for Volunteer users
class VolunteerMenu(CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.geometry("1056x645")
        self.resizable(False, False)
        self.title(f"Logged In | Volunteer: {usernameVAR} | WILLOW WOOD INN")

        self.main = volunteerView(self)
        self.mainloop()


# This function determines the view to launch based on the user's role
def determineView(role):
    if role == 3:
        AdminMenu()
    elif role == 2:
        SupervisorMenu()
    elif role == 1:
        VolunteerMenu()
    else:
        print("main.py | User Role not found")


# This function is called when the user logs in, using values passed from WIN_LoginMain.py
def handle_login_result(successful, username, role):
    global usernameVAR
    usernameVAR = username
    if successful:
        print("main.py | Login Successful")
        print("main.py | Username:", username)
        print("main.py | Role:", role)

        # Write the username to a file for use in other modules
        with open("C:/Users/Matthew/Documents/FINAL_A2_WILLOWWOOD_SSMS/backend/uservar.txt", "w") as file:
            file.write(username)
            file.close()
        auditlog("User logged in")

        determineView(role)

    else:
        # If the login fails, clear the uservar.txt file
        print("main.py | Login Failed")
        with open("C:/Users/Matthew/Documents/FINAL_A2_WILLOWWOOD_SSMS/backend/.txt", "w") as file:
            file.write("")
            file.close()
        auditlog("Login attempt failed")
        tk.messagebox.showerror("Login Attempt", "No User found with the given credentials. Please try again.")


if __name__ == "__main__":
    mainApp(handle_login_result)
