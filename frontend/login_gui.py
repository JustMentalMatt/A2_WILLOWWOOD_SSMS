import customtkinter
import sqlite3
from mainwindow import mainWindow

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("400x350")

def login():
    sqliteConnection = sqlite3.connect('./backend/database.db')
    cursor = sqliteConnection.cursor()
    credential_fetch = "SELECT username, password FROM Admin_Users"
    cursor.execute(credential_fetch)
    results = cursor.fetchall()
    
    for row in results:
        global username
        username = row[0]
        password = row[1]
        
        if entry1.get() == username and entry2.get() == password:
            print("Login Successful")
            UserStatus = str(username)
            root.destroy()
            mainWindow()         
    return

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Login System", font=("Roboto", 24))
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
entry1.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
entry2.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Login", command=login)
button.pack(pady=12, padx=10)

root.title("Database Login System")
root.resizable(False,False)
root.mainloop()