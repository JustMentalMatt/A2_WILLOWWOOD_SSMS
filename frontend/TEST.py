import customtkinter as ctk
import tkinter as tk
from customtkinter import *
from CTkTable import CTkTable
from PIL import Image
import sqlite3


from SQL_AdminView import *

# import customtkinter
# from CTkTable import *

# root = customtkinter.CTk()

# def show(cell):
#     print("row:", cell["row"])
#     print("column:", cell["column"])
#     print("value:", cell["value"])
          
# value = [[1,2,3,4,5],
#          [1,2,3,4,5],
#          [1,2,3,4,5],
#          [1,2,3,4,5],
#          [1,2,3,4,5],]

# frame = customtkinter.CTkFrame(root)
# frame.pack(expand=True, fill="both")

# table = CTkTable(master=frame, row=5, column=5, values=value, height=100, command=show)
# table.pack(expand=True, fill="both", padx=20, pady=20)

# root.mainloop()

######################


class adminView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand=True, fill="both")

        self.main_view = CTkFrame(self, fg_color="#19383d", width=900, height=650, corner_radius=0)
        self.main_view.pack_propagate(0)
        self.main_view.pack(side="right")

        self.sidebarFrame = UserManagement.sidebarFrame(self)
        self.menuFrame()
        
        self.user_management = UserManagement(self)
        self.sidebarFrame = UserManagement(self)
        
    def pageSwitch(self, page):
        self.pageDestroy()
        page()
            
class UserManagement:
    def __init__(self, parent):
        self.parent = parent
        self.main_view = parent.main_view
        #self.optionsFrame()
        
    def sidebarFrame(self):
        sidebar = CTkFrame(self, fg_color="#edebde", width=176, height=650, corner_radius=0)
        sidebar.pack(fill="y", anchor="w", side="left")
        sidebar.pack_propagate(0)

        dat_img_mainLogo = Image.open("./frontend/Resources/WILLOW_LOGO.png")
        img_mainLogo = CTkImage(dark_image=dat_img_mainLogo, light_image=dat_img_mainLogo, size=(200,200))
        CTkLabel(sidebar, text="", image=img_mainLogo).pack(pady=(0, 0), anchor="center")
        
        CTkButton(sidebar, text="User\nManagement", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19), hover_color="#207244",
                    command=lambda: adminView.pageSwitch(UserManagement)).pack(anchor="center", ipady=5, pady=(15, 0))
    