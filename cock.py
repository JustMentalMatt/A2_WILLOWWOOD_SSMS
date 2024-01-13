import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk

ctk.set_appearance_mode("System")
appWidth, appHeight = 600, 325

#im = Image.open("hopper.ppm")

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Add Customer")
        self.geometry(f"{appWidth}x{appHeight}")    

        appearance_mode = ctk.get_appearance_mode()
        if appearance_mode == "Dark":
            headerLogo = Image.open("./GUI_Design/Inventory_Management/Images/analytics_icon.png")
        else:
            headerLogo = Image.open("./GUI_Design/Inventory_Management/Images/delivered_icon.png")

        self.MatchettsLogo = ctk.CTkImage(headerLogo, headerLogo, size=(200, 200))
        self.logo = ctk.CTkLabel(self, image=self.MatchettsLogo, text="Add Customer", text_color="#2A8C55", font=("Arial Bold", 20), compound="top").pack(side=ctk.LEFT)



if __name__ == "__main__":
    app = App()
    app.mainloop()