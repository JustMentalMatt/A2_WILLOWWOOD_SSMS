import customtkinter as ctk
import tkinter as tk
from customtkinter import *
from tkinter import ttk
from PIL import Image
import sqlite3

import validation
from validation import auditlog

globalUser = ""
globalPass = ""
globalLogin = False

class mainApp(ctk.CTk):
    def __init__(self, loginCallback):
        super().__init__()
        self.geometry("600x480")
        self.title("Login | Willow Wood Inn")
        self.resizable(False, False)

        self.main = loginGUI(self, loginCallback)

        self.mainloop()

class loginGUI(ctk.CTkFrame):

    def __init__(self, parent, loginCallback):
        super().__init__(parent)
        self.pack(expand=True, fill="both")

        self.loginCallback = loginCallback
        self.create_login_layout()


    # Creates the login layout frame, asking user to input their username and password.
    def create_login_layout(self):

        # This function switches the layout from the login layout to the register layout.
        def switch_to_register_layout():
            for widget in self.winfo_children():
                widget.destroy()
            self.create_register_layout()

        # This function is called when the user clicks the login button. It checks the user's credentials against the database.
        def onLogin():
            sqliteConnection = sqlite3.connect('./backend/WillowInnDB.db')
            cursor = sqliteConnection.cursor()

            print("LoginMain.py | Connected to SQLite")

            disp_column = ["Username", "Password","RoleID"]
            columnsSQL = ', '.join(disp_column)

            credential_fetch = f"SELECT {columnsSQL} FROM UserTable WHERE Username = '{userVar.get()}' AND Password = '{passVar.get()}'"
            cursor.execute(credential_fetch)
            results = cursor.fetchall()

            # If the user's credentials are correct, the global variables are set and the loginCallback function is called.
            # The loginCallback function is defined in main.py and is used to determine the user's role and open the appropriate view.
            for row in results:
                username = row[0]
                password = row[1]
                role = row[2]

                if userVar.get() == username and passVar.get() == password:
                    global globalUser
                    global globalLogin
                    globalUser = username
                    globalLogin = True
                    break
                else:
                    globalLogin = False

            if globalLogin:
                print("LoginMain.py | Login Callback")
                self.loginCallback(True, username, role)
            else:
                self.loginCallback(False, None, None)

        # These are the images used in the login layout.
        side_img_data = Image.open("./frontend/Resources/side-img.png")
        email_icon_data = Image.open("./frontend/Resources/email-icon.png")
        password_icon_data = Image.open("./frontend/Resources/password-icon.png")

        side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
        email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20, 20))
        password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17, 17))

        ctk.CTkLabel(self, text="", image=side_img).pack(expand=True, side="left")

        # This frame contains the login form.
        frame = ctk.CTkFrame(self, width=300, height=480, fg_color="#ffffff")
        frame.pack_propagate(0)
        frame.pack(expand=True, side="right")
        frame.sticky = "e"

        ctk.CTkLabel(master=frame, text="Welcome!", text_color="#274e13", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
        ctk.CTkLabel(master=frame, text="Sign in to your account", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))
        ctk.CTkLabel(master=frame, text="  Username:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
        userVar = ctk.CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        userVar.pack(anchor="w", padx=(25, 0))
        ctk.CTkLabel(master=frame, text="  Password:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
        passVar = ctk.CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*")
        passVar.pack(anchor="w", padx=(25, 0))
        ctk.CTkButton(master=frame, text="Login", fg_color="#274e13", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=onLogin).pack(anchor="w", pady=(40, 0), padx=(25, 0))
        ctk.CTkButton(master=frame, text="Register", fg_color="#EEEEEE", hover_color="#c4c2c2", font=("Arial Bold", 12), text_color="#274e13", width=225, command=switch_to_register_layout).pack(anchor="w", pady=(20, 0), padx=(25, 0))

    # Creates the register layout frame, asking user to input their details to create an account.
    def create_register_layout(self):

        # This function switches the layout from the register layout to the login layout.
        def switch_to_login_layout():
            for widget in self.winfo_children():
                widget.destroy()
            self.create_login_layout()

        side_img_data = Image.open("./frontend/Resources/side-img.png")
        side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))

        ctk.CTkLabel(self, text="", image=side_img).pack(expand=True, side="left")
        # This frame contains the register form.
        frame = ctk.CTkFrame(self, width=300, height=480, fg_color="#ffffff")
        frame.pack_propagate(0)
        frame.pack(expand=True, side="right")

        ctk.CTkLabel(master=frame, text="Register an Account", text_color="#274e13", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(20, 10), padx=(25, 0))
        ctk.CTkLabel(master=frame, text="""By registering an account you are agreeing to\nour terms and conditions.""", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 9)).pack(anchor="w", padx=(25, 0))
        ctk.CTkLabel(master=frame, text="  Full Name:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 11), compound="left").pack(anchor="w", pady=(10, 0), padx=(25, 0))
        NameVAR = ctk.CTkEntry(master=frame, placeholder_text="Daniel Adams", width=225, height=20, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        NameVAR.pack(anchor="w", padx=(25, 0))
        ctk.CTkLabel(master=frame, text="  Contact Number:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 11), compound="left").pack(anchor="w", pady=(10, 0), padx=(25, 0))
        ContactVAR = ctk.CTkEntry(master=frame, placeholder_text="07742978763", width=225, height=20, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        ContactVAR.pack(anchor="w", padx=(25, 0))
        ctk.CTkLabel(master=frame, text="  Username:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 11), compound="left").pack(anchor="w", pady=(10, 0), padx=(25, 0))
        UsernameVAR = ctk.CTkEntry(master=frame, placeholder_text="lizzo432", width=225, height=20, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        UsernameVAR.pack(anchor="w", padx=(25, 0))
        ctk.CTkLabel(master=frame, text="  Date of Birth:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 11), compound="left").pack(anchor="w", pady=(10, 0), padx=(25, 0))
        DOBVar = ctk.CTkEntry(master=frame, placeholder_text="YYYY-MM-DD", width=225, height=20, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        DOBVar.pack(anchor="w", padx=(25, 0))
        ctk.CTkLabel(master=frame, text="  Password:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 11), compound="left").pack(anchor="w", pady=(10, 0), padx=(25, 0))
        passVar = ctk.CTkEntry(master=frame, placeholder_text="supersecret123", width=225, height=20, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*")
        passVar.pack(anchor="w", padx=(25, 0))
        ctk.CTkButton(master=frame, text="Create Account", fg_color="#274e13", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=lambda: self.registerAccount(NameVAR.get(), ContactVAR.get(), UsernameVAR.get(), DOBVar.get(), passVar.get())).pack(anchor="w", pady=(20, 0), padx=(25, 0))
        ctk.CTkButton(master=frame, text="Back to Login", fg_color="#EEEEEE", hover_color="#c4c2c2", font=("Arial Bold", 12), text_color="#601E88", width=225, command=switch_to_login_layout).pack(anchor="w", pady=(10, 0), padx=(25, 0))

    # This function is called when the user clicks the create account button. 
    # It checks the user's input and inserts the data into the database.
    def registerAccount(self, fullName, contactNumber, username, dob, password):
        sqliteConnection = sqlite3.connect('./backend/WillowInnDB.db')
        cursor = sqliteConnection.cursor()
        
        # Validation Methods
        if fullName == "" or fullName == " ":
            tk.messagebox.showerror("Error", "Please Provide a Name")
        else:
            try:
                firstName = fullName.split()[0].capitalize()
                lastName = fullName.split()[1].capitalize()
            except IndexError:
                tk.messagebox.showerror("Error", "Please Provide a Full Name")
                return

            if not validation.validateName(fullName):
                tk.messagebox.showerror("Error", "Invalid Name")
                auditlog("Failed account creation")
            else:
                with open("./backend/uservar.txt", "w") as file:
                        file.write("UNKNOWN") 
                        file.close()

                if not validation.validatePhone(contactNumber):
                    tk.messagebox.showerror("Error", "Invalid Phone Number")
                    auditlog("Failed account creation")
                
                elif not validation.validateUsername(username):
                    tk.messagebox.showerror("Error", "Invalid Username")
                    auditlog("Failed account creation")
                    
                elif not validation.validateDate(dob):
                    tk.messagebox.showerror("Error", "Invalid Date of Birth")
                    auditlog("Failed account creation")
                    
                elif not validation.presenceCheck(password):
                    tk.messagebox.showerror("Error", "Please Provide a Password")
                    auditlog("Failed account creation")
                    
                elif not validation.lengthCheck(password, minLength=8):
                    tk.messagebox.showerror("Error", "Password must be at least 8 characters long")
                    auditlog("Failed account creation")
                    
                else:
                    # If all the user's input is valid, the data is inserted into the database.
                    print("LoginMain.py | Connected to SQLite")

                    insert = f"INSERT INTO UserTable (FirstName, LastName, ContactNumber, Username, DOB, Password, RoleID) VALUES ('{firstName}', '{lastName}', '{contactNumber}', '{username}', '{dob}', '{password}', 1)"
                    cursor.execute(insert)
                    sqliteConnection.commit()
                    print("LoginMain.py | Record inserted successfully into UserTable")
                    tk.messagebox.showinfo("Success", "Account Created Successfully")
                    
                    auditlog("Successful account creation") # Audit Log records the creation of a new account
                    
                    # The layout is switched back to the login layout.
                    for widget in self.winfo_children():
                        widget.destroy()
                        self.create_login_layout()

                    cursor.close()

                    print("LoginMain.py | SQLite connection is closed")
        
    