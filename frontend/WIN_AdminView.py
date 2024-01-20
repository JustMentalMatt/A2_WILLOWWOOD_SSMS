import customtkinter as ctk
import tkinter as tk
from customtkinter import *
from CTkTable import CTkTable
from PIL import Image
import sqlite3


class mainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1056x645")
        self.resizable(False, False)
        self.title("Logged In - WILLOW WOOD INN")

        self.main = adminView(self)
        self.mainloop()


class adminView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand=True, fill="both")

        self.main_view = CTkFrame(self, fg_color="#19383d", width=900, height=650, corner_radius=0)
        self.main_view.pack_propagate(0)
        self.main_view.pack(side="right")

        self.sidebarFrame()
        self.menuFrame()

    def pageDestroy(self):
        for frame in self.main_view.winfo_children():
            frame.destroy()

    def pageSwitch(self, page):
        self.pageDestroy()
        page()

    def menuFrame(self):
        title_frame = CTkFrame(self.main_view, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=2, pady=(2, 0))

        dat_img_backlogo = Image.open("./frontend/Resources/WILLOW_TITLE_LOGO.png")
        img_backlogo = CTkImage(dark_image=dat_img_backlogo, light_image=dat_img_backlogo, size=(720,240))
        CTkLabel(title_frame, text="", image=img_backlogo).pack(pady=(0, 0), anchor="n")
        
        text_frame = CTkFrame(self.main_view, fg_color="transparent", bg_color="#fff", width=480, height=490, corner_radius=0)
        text_frame.propagate(0)
        text_frame.pack(anchor="center", fill="x", pady=(30, 30), padx=27)
        
        CTkLabel(text_frame, text="Welcome to the Willow Wood Inn Management System.\nThis system is designed to help you manage your business.\nYou can use the sidebar to navigate to different parts of the system.\n\n\n\n\n\nHi!", font=("Trebuchet MS", 18), text_color="#000", bg_color="#fff").pack(anchor="center", side="top")

    def UserManagementFrame(self):
        
        def UserManagementDatabase():
            conn = sqlite3.connect('./backend/database.db')
            cursor = conn.cursor()

            disp_column = ["ID", "Name", "Email", "Joining_Date", "Username", "Password"] # iunclude coluims you only wanna show
            columnsSQL = ', '.join(disp_column) # for the sql wuarey
            cursor.execute(f'SELECT {columnsSQL} FROM Admin_Users') #yupada
            rows = cursor.fetchall() #this puts it in tabular form so u can just use it with the ctk table thing

            conn.close()

            tabData = [disp_column]
            tabData.extend(rows)
            
            tabFrame = CTkScrollableFrame(master=main_view, fg_color="transparent")
            tabFrame.pack(expand=True, fill="both", padx=27, pady=21)
            table = CTkTable(master=tabFrame, values=tabData, colors=["#E6E6E6", "#EEEEEE"], header_color="#2A8C55", hover_color="#B4B4B4", text_color="#000", width=85)
            table.edit_row(0, text_color="#000", hover_color="#2A8C55")
            table.pack(expand=True)
        
        title_frame = CTkFrame(self.main_view, fg_color="transparent", width=480, height=450, corner_radius=30)
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
        
        CTkLabel(title_frame, text="AAAAAAA", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", side="left")
        
        UserManagementDatabase()

        # Rest of the UserManagementFrame function...

    def sidebarFrame(self):
        sidebar = CTkFrame(self, fg_color="#edebde", width=176, height=650, corner_radius=0)
        sidebar.pack(fill="y", anchor="w", side="left")
        sidebar.pack_propagate(0)

        dat_img_mainLogo = Image.open("./frontend/Resources/WILLOW_LOGO.png")
        img_mainLogo = CTkImage(dark_image=dat_img_mainLogo, light_image=dat_img_mainLogo, size=(200,200))
        CTkLabel(sidebar, text="", image=img_mainLogo).pack(pady=(0, 0), anchor="center")
        
        CTkButton(sidebar, text="Menu", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 24), hover_color="#207244",
                    command=lambda: self.pageSwitch(self.menuFrame)).pack(anchor="center", ipady=5, pady=(40, 0))
        CTkButton(sidebar, text="Dashboard", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19), hover_color="#207244").pack(anchor="center", ipady=5, pady=(15, 0))
        CTkButton(sidebar, text="User\nManagement", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19), hover_color="#207244",
                    command=lambda: self.pageSwitch(self.UserManagementFrame)).pack(anchor="center", ipady=5, pady=(15, 0))
        CTkButton(sidebar, text="Reports", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19), hover_color="#207244").pack(anchor="center", ipady=5, pady=(15, 0))
        CTkButton(sidebar, text="Alerts", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19), hover_color="#207244").pack(anchor="center", ipady=5, pady=(15, 0))
        
        CTkButton(sidebar, text="Profile", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 18), hover_color="#207244").pack(anchor="center", ipady=5, pady=(50, 0))

if __name__ == "__main__":
    mainMenu()