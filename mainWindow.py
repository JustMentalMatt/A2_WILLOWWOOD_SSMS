import customtkinter as ctk
import tkinter as tk
from customtkinter import *
from tkinter import ttk
from PIL import Image
import sqlite3


class mainApp(ctk.CTk):
	def __init__(self):
        # main window setup
		super().__init__()
		self.geometry("600x480")
		self.title("i love jesus better than icecream")
		self.resizable(False,False)

		self.main = loginGUI(self)

		self.mainloop()


class loginGUI(ctk.CTkFrame):
      
	def __init__(self, parent):
		super().__init__(parent)
		self.pack(expand=True, fill="both")
		self.create_layout()
	
	def create_layout(self):
		side_img_data = Image.open("./GUI_Design/Login/Images/side-img.gif")
		email_icon_data = Image.open("./GUI_Design/Login/Images/email-icon.png")
		password_icon_data = Image.open("./GUI_Design/Login/Images/password-icon.png")

		side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
		email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20,20))
		password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17,17))

		ctk.CTkLabel(self, text="", image=side_img).pack(expand=True, side="left")

		frame = ctk.CTkFrame(self, width=300, height=480, fg_color="#ffffff")
		frame.pack_propagate(0)
		frame.pack(expand=True, side="right")
		frame.sticky = "e"

		ctk.CTkLabel(
			master=frame,
			text="Welcome Back!",
			text_color="#37007a",
			anchor="w",
			justify="left",
			font=("Arial Bold", 24),
		).pack(anchor="w", pady=(50, 5), padx=(25, 0))

		ctk.CTkLabel(
			master=frame,
			text="Sign in to your account",
			text_color="#7E7E7E",
			anchor="w",
			justify="left",
			font=("Arial Bold", 12),
		).pack(anchor="w", padx=(25, 0))

		ctk.CTkLabel(
			master=frame,
			text="  Email:",
			text_color="#601E88",
			anchor="w",
			justify="left",
			font=("Arial Bold", 14),
            image=email_icon,
			compound="left",
		).pack(anchor="w", pady=(38, 0), padx=(25, 0))

		ctk.CTkEntry(
			master=frame,
			width=225,
			fg_color="#EEEEEE",
			border_color="#601E88",
			border_width=1,
			text_color="#000000",
		).pack(anchor="w", padx=(25, 0))

		ctk.CTkLabel(
			master=frame,
			text="  Password:",
			text_color="#601E88",
			anchor="w",
			justify="left",
			font=("Arial Bold", 14),
            image=password_icon,
			compound="left",
		).pack(anchor="w", pady=(21, 0), padx=(25, 0))

		ctk.CTkEntry(
			master=frame,
			width=225,
			fg_color="#EEEEEE",
			border_color="#601E88",
			border_width=1,
			text_color="#000000",
			show="*",
		).pack(anchor="w", padx=(25, 0))

		ctk.CTkButton(
			master=frame,
			text="Login",
			fg_color="#37007a",
			hover_color="#E44982",
			font=("Arial Bold", 12),
			text_color="#ffffff",
			width=225,
		).pack(anchor="w", pady=(40, 0), padx=(25, 0))

		ctk.CTkButton(
			master=frame,
			text="Register",
			fg_color="#EEEEEE",
			hover_color="#c4c2c2",
			font=("Arial Bold", 12),
			text_color="#601E88",
			width=225,
		).pack(anchor="w", pady=(20, 0), padx=(25, 0))


if __name__ == "__main__":
    mainApp()
