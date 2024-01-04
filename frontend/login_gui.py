import customtkinter as ctk
import sqlite3

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

login_window = ctk.CTk()
login_window.geometry("400x350")

def login():
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
        
        else:
            return None
            #root.destroy()
            #mainWindow() 


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

login_window.title("Database Login System")
login_window.resizable(False,False)
login_window.mainloop()