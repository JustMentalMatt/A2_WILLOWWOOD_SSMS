import customtkinter as ctk
import tkinter as tk
from customtkinter import *
from CTkTable import CTkTable
from PIL import Image
import sqlite3


# from SQL_AdminView import *
from WIN_AdminView import *

yo_momma = True


class mainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1056x645")
        self.resizable(False, False)
        self.title("Logged In - MANAGEMENT - WILLOW WOOD INN")

        self.main = adminView(self)
        self.mainloop()
                
def tickle_my_pickle():
    if yo_momma == True:
        mainMenu()
    else:
        print("You are not authorized to access this page.")
           
tickle_my_pickle()