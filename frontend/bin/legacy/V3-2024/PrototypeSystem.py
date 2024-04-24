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
        self.resizable(False,False)
        self.title("Logged In - WILLOW WOOD INN")

        self.main = adminView(self)
        self.mainloop()
        

class adminView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand=True, fill="both")
        self.sidebarFrame()

        self.optionsFrame()
        self.UserManagementFrame()
        # self.HouseMagementFrame()
        # self.TaskManagementFrame()


    def pageDestroy(self):
        # Destroy all widgets in the frame
        for widget in self.winfo_children():
            widget.destroy()

    def pageSwitch(self, page):
        self.pageDestroy()
        page()
    
    def UserManagementFrame(self):
        
        def UserManagementDatabase():
            conn = sqlite3.connect('./frontend/bin/legacy/V3-2024/WillowInn-PrototypeDB/SampleDB.sqlite')
            cursor = conn.cursor()

            disp_column = ["UserID", "Username", "Password", "FirstName", "LastName",
                           "DOB", "ContactNumber", "RoleID", "EnrollmentStatus", "HouseID"]
            columnsSQL = ', '.join(disp_column)
            cursor.execute(f'SELECT {columnsSQL} FROM UserTable')
            rows = cursor.fetchall()

            conn.close()

            tabData = [disp_column]
            tabData.extend(rows)
            
            tabFrame = CTkScrollableFrame(master=main_view, fg_color="transparent")
            tabFrame.pack(expand=True, fill="both", padx=27, pady=5)
            table = CTkTable(master=tabFrame, values=tabData, colors=["#E6E6E6", "#EEEEEE"], header_color="#2A8C55",
                             hover_color="#B4B4B4", text_color="#000", corner_radius=0)
            table.edit_row(0, text_color="#000", hover_color="#2A8C55")
            table.pack(expand=False)
            table.configure(height=30, width=10)
            table.edit_column(0, width=10)
        
        main_view = CTkFrame(self, fg_color="#19383d",  width=980, height=450, corner_radius=0, border_color="#fff", border_width=2)
        main_view.pack_propagate(0)
        main_view.pack(anchor="nw", side="left")

        title_frame = CTkFrame(main_view, fg_color="transparent", width=680, height=450, corner_radius=30)
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

        CTkLabel(title_frame, text="User Table", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="n", side="top")

        UserManagementDatabase()
        
    def HouseMagementFrame(self):
            
            def HouseManagementDatabase():
                conn = sqlite3.connect('./frontend/bin/legacy/V3-2024/WillowInn-PrototypeDB/SampleDB.sqlite')
                cursor = conn.cursor()

                disp_column = ["HouseID", "HouseName", "HouseAddress", "HousePhone", "HouseEmail", "HouseSupervisor"]
                columnsSQL = ', '.join(disp_column)
                cursor.execute(f'SELECT {columnsSQL} FROM HouseTable')
                rows = cursor.fetchall()

                conn.close()

                tabData = [disp_column]
                tabData.extend(rows)
                
                tabFrame = CTkScrollableFrame(master=main_view, fg_color="transparent")
                tabFrame.pack(expand=True, fill="both", padx=27, pady=5)
                table = CTkTable(master=tabFrame, values=tabData, colors=["#E6E6E6", "#EEEEEE"], header_color="#2A8C55",
                                hover_color="#B4B4B4", text_color="#000", corner_radius=0)
                table.edit_row(0, text_color="#000", hover_color="#2A8C55")
                table.pack(expand=False)
                table.configure(height=30, width=10)
                table.edit_column(0, width=10)
            
            main_view = CTkFrame(self, fg_color="#19383d",  width=980, height=450, corner_radius=0, border_color="#fff", border_width=2)
            main_view.pack_propagate(0)
            main_view.pack(anchor="nw", side="left")

            title_frame = CTkFrame(main_view, fg_color="transparent", width=680, height=450, corner_radius=30)
            title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

            CTkLabel(title_frame, text="House Table", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="n", side="top")

            HouseManagementDatabase()

    def TaskManagementFrame(self):
            
            def TaskManagementDatabase():
                conn = sqlite3.connect('./frontend/bin/legacy/V3-2024/WillowInn-PrototypeDB/SampleDB.sqlite')
                cursor = conn.cursor()

                disp_column = ["TaskID", "TaskName", "EventID", "Capacity", "DifficultyLevel", "Points"]
                columnsSQL = ', '.join(disp_column)
                cursor.execute(f'SELECT {columnsSQL} FROM TaskTable')
                rows = cursor.fetchall()

                conn.close()

                tabData = [disp_column]
                tabData.extend(rows)
                
                tabFrame = CTkScrollableFrame(master=main_view, fg_color="transparent")
                tabFrame.pack(expand=True, fill="both", padx=27, pady=5)
                table = CTkTable(master=tabFrame, values=tabData, colors=["#E6E6E6", "#EEEEEE"], header_color="#2A8C55",
                                hover_color="#B4B4B4", text_color="#000", corner_radius=0)
                table.edit_row(0, text_color="#000", hover_color="#2A8C55")
                table.pack(expand=False)
                table.configure(height=30, width=10)
                table.edit_column(0, width=10)
            
            main_view = CTkFrame(self, fg_color="#19383d",  width=980, height=450, corner_radius=0, border_color="#fff", border_width=2)
            main_view.pack_propagate(0)
            main_view.pack(anchor="nw", side="left")

            title_frame = CTkFrame(main_view, fg_color="transparent", width=680, height=450, corner_radius=30)
            title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

            CTkLabel(title_frame, text="Task Table", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="n", side="top")

            TaskManagementDatabase()

    def sidebarFrame(self):
            sidebar = CTkFrame(self, fg_color="#edebde",  width=176, height=650, corner_radius=0)
            sidebar.pack(fill="y", anchor="w", side="left")
            sidebar.pack_propagate(0)

            CTkButton(sidebar, text="Table Selector\n----------------", text_color="#7c3f00", fg_color="transparent", font=("Arial Bold", 24), 
                      hover_color="#207244", command=lambda: self.pageSwitch(self.menuFrame)).pack(anchor="center", ipady=5, pady=(150, 0))
            CTkButton(sidebar, text="User\nManagement", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19), 
                      hover_color="#207244", command=lambda: self.pageSwitch(self.menuFrame)).pack(anchor="center", ipady=5, pady=(40, 0))
            CTkButton(sidebar, text="House\nManagement", text_color="#19383d", fg_color="transparent", 
                      font=("Arial Bold", 19), hover_color="#207244").pack(anchor="center", ipady=5, pady=(15, 0))
            CTkButton(sidebar, text="Task\nManagement", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19),
                      hover_color="#207244", command=lambda: self.pageSwitch(self.UserManagementFrame)).pack(anchor="center", ipady=5, pady=(15, 0))

    def test(self):
        print("Test")
        main_view = CTkFrame(self, fg_color="#19383d",  width=80, height=45, corner_radius=0, border_color="#fff", border_width=2)
        main_view.pack_propagate(0)
        main_view.pack(anchor="se", side="bottom")


    def optionsFrame(self): # User Management Options

        global e_ID, e_Username, e_Password, e_FirstName, e_LastName, e_DOB, e_ContactNumber, e_RoleID, e_EnrollmentStatus, e_HouseID, e_Message, Cmbo_Role, Cmbo_EnrollmentStatus
        e_ID = tk.StringVar()
        e_Username = tk.StringVar()
        e_Password = tk.StringVar()
        e_FirstName = tk.StringVar()
        e_LastName = tk.StringVar()
        e_DOB = tk.StringVar()
        e_ContactNumber = tk.StringVar()
        e_EnrollmentStatus = tk.StringVar()
        e_RoleID = tk.StringVar()
        e_Message = tk.StringVar()
        e_HouseID = tk.StringVar()
        Cmbo_Role = tk.StringVar()
        Cmbo_EnrollmentStatus = tk.StringVar()
        
        optionsFrame = CTkFrame(master=self, fg_color="transparent", width=100, height=180, border_color="#fff", border_width=2)
        optionsFrame.propagate(0)
        optionsFrame.pack(anchor="n", side="bottom", fill="x", padx=10, pady=(20, 20))

        # CTkLabel(optionsFrame, text="User Options", font=("Arial Black", 20), bg_color="transparent", text_color="#fff").pack(anchor="nw", side="top")
        CTkLabel(optionsFrame, text='''  ID       Username         Password            F_Name             L_Name           DOB           C_Number     RoleID          E_Status          HouseID   ''', font=("Arial Bold", 12), 
                 text_color="#FFC300").pack(anchor="w", side="top", padx=(10, 0), pady=(5, 0))
        
        entryFrame = CTkFrame(optionsFrame, fg_color="transparent", width=480, height=30, border_color="#2A8C55", border_width=0)
        entryFrame.propagate(0)
        entryFrame.pack(anchor="n", fill="x", padx=5, pady=(0,0))
        CTkEntry(entryFrame, width=25, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", 
                 text_color="#000", textvariable=e_ID).pack(anchor="n", side="left", padx=(5, 2), fill="x")
        CTkEntry(entryFrame, width=55, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", 
                 text_color="#000", textvariable=e_Username).pack(anchor="n", side="left", padx=(15, 2), fill="x")
        CTkEntry(entryFrame, width=70, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", 
                 text_color="#000", textvariable=e_Password).pack(anchor="n", side="left", padx=(20, 2), fill="x")
        CTkEntry(entryFrame, width=65, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", 
                 text_color="#000", textvariable=e_FirstName).pack(anchor="n", side="left", padx=(20, 2), fill="x")
        CTkEntry(entryFrame, width=65, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", 
                 text_color="#000", textvariable=e_LastName).pack(anchor="n", side="left", padx=(20, 2), fill="x")
        CTkEntry(entryFrame, width=80, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", 
                 text_color="#000", textvariable=e_DOB).pack(anchor="n", side="left", padx=(2, 2), fill="x")
        CTkEntry(entryFrame, width=65, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", 
                 text_color="#000", textvariable=e_ContactNumber).pack(anchor="n", side="left", padx=(2, 2), fill="x")
        
        CTkComboBox(entryFrame, values=["1", "2", "3"], width=5, height=25, font=("Arial Bold", 12), fg_color="#fff", 
                    bg_color="transparent", text_color="#000", variable=Cmbo_Role).pack(anchor="n", side="left", padx=(2, 2), fill="x")
        CTkComboBox(entryFrame, values=["Enrolled", "Not Enrolled", "Pending"], width=110, height=25, font=("Arial Bold", 12), 
                    fg_color="#fff", bg_color="transparent", text_color="#000", variable=Cmbo_EnrollmentStatus).pack(anchor="n", side="left", padx=(2, 2), fill="x")
        
        CTkEntry(entryFrame, width=25, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", 
                 textvariable=e_HouseID).pack(anchor="n", side="left", padx=(2, 2), fill="x")

        CTkLabel(optionsFrame, text="Options:", font=("Arial Black", 24), bg_color="transparent", 
                 text_color="#ECEAE2").pack(anchor="e", side="left", padx=(10,0))
        CTkButton(optionsFrame, text="Add User", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 16), hover_color="#207244", 
                  height=10, width=15, command=self.AddUserButton).pack(anchor="e", side="left", ipady=5, pady=(10, 10), padx=(20,10))
        CTkButton(optionsFrame, text="Delete User", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 16), hover_color="#207244", 
                  height=10, width=15, command=self.DeleteUserButton).pack(anchor="e", side="left", ipady=5, pady=(10, 10), padx=(10,10))
        CTkButton(optionsFrame, text="Clear Fields", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 16), hover_color="#207244", 
                  height=10, width=15, command=self.ClearFieldsButton).pack(anchor="e", side="left", ipady=5, pady=(10, 10), padx=(10,10))
    def AddUserSQL(self):
        pass
    def DeleteUserSQL(self):
        pass
    
    def AddUserButton(self):
        # self.AddUserSQL(e_Username.get(), e_Password.get(), e_FirstName.get(), 
        #                 e_LastName.get(), e_DOB.get(), 
        #                 e_ContactNumber.get(), Cmbo_Role.get(), 
        #                 Cmbo_EnrollmentStatus.get(), e_Message.get(), e_HouseID.get())
        # self.pageDestroy()
        # self.UserManagementFrame()
        pass
        
    def DeleteUserButton(self):
        # self.DeleteUserSQL(e_ID.get())
        # self.pageDestroy()
        # self.UserManagementFrame()
        pass
        
    def ClearFieldsButton(self):
        pass
    
    
    # def optionsFrame(self): # House Management Options
    
    #     global e_ID, e_Username, e_Password, e_FirstName, e_LastName, e_DOB, e_ContactNumber, e_RoleID, e_EnrollmentStatus, e_HouseID, e_Message, Cmbo_Role, Cmbo_EnrollmentStatus
    #     e_ID = tk.StringVar()
    #     e_Username = tk.StringVar()
    #     e_Password = tk.StringVar()
    #     e_FirstName = tk.StringVar()
    #     e_LastName = tk.StringVar()
    #     e_DOB = tk.StringVar()
    #     e_ContactNumber = tk.StringVar()
    #     e_EnrollmentStatus = tk.StringVar()
    #     e_RoleID = tk.StringVar()
    #     e_Message = tk.StringVar()
    #     e_HouseID = tk.StringVar()
    #     Cmbo_Role = tk.StringVar()
    #     Cmbo_EnrollmentStatus = tk.StringVar()
        
    #     optionsFrame = CTkFrame(master=self, fg_color="transparent", width=100, height=180, border_color="#fff", border_width=2)
    #     optionsFrame.propagate(0)
    #     optionsFrame.pack(anchor="n", side="bottom", fill="x", padx=10, pady=(20, 20))

    #     # CTkLabel(optionsFrame, text="User Options", font=("Arial Black", 20), bg_color="transparent", text_color="#fff").pack(anchor="nw", side="top")
    #     CTkLabel(optionsFrame, text='''  ID            Name              Address             Telephone             Email           Supervisor''', font=("Arial Bold", 12), 
    #              text_color="#FFC300").pack(anchor="w", side="top", padx=(10, 0), pady=(5, 0))
        
    #     entryFrame = CTkFrame(optionsFrame, fg_color="transparent", width=480, height=30, border_color="#2A8C55", border_width=0)
    #     entryFrame.propagate(0)
    #     entryFrame.pack(anchor="n", fill="x", padx=5, pady=(0,0))
    #     CTkEntry(entryFrame, width=25, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", 
    #              text_color="#000", textvariable=e_ID, state='readonly').pack(anchor="n", side="left", padx=(5, 2), fill="x")
    #     CTkEntry(entryFrame, width=55, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", 
    #              text_color="#000", textvariable=e_Username).pack(anchor="n", side="left", padx=(15, 2), fill="x")
    #     CTkEntry(entryFrame, width=70, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", 
    #              text_color="#000", textvariable=e_Password).pack(anchor="n", side="left", padx=(20, 2), fill="x")
    #     CTkEntry(entryFrame, width=65, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", 
    #              text_color="#000", textvariable=e_FirstName).pack(anchor="n", side="left", padx=(20, 2), fill="x")
    #     CTkEntry(entryFrame, width=65, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", 
    #              text_color="#000", textvariable=e_LastName).pack(anchor="n", side="left", padx=(20, 2), fill="x")
    #     CTkEntry(entryFrame, width=80, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", 
    #              text_color="#000", textvariable=e_DOB).pack(anchor="n", side="left", padx=(2, 2), fill="x")

    #     CTkLabel(optionsFrame, text="Options:", font=("Arial Black", 24), bg_color="transparent", 
    #              text_color="#ECEAE2").pack(anchor="e", side="left", padx=(10,0))
    #     CTkButton(optionsFrame, text="Add House", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 16), hover_color="#207244", 
    #               height=10, width=15, command=self.AddHouseButton).pack(anchor="e", side="left", ipady=5, pady=(10, 10), padx=(20,10))
    #     CTkButton(optionsFrame, text="Delete House", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 16), hover_color="#207244", 
    #               height=10, width=15, command=self.DeleteHouseButton).pack(anchor="e", side="left", ipady=5, pady=(10, 10), padx=(10,10))
    #     CTkButton(optionsFrame, text="Clear Fields", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 16), hover_color="#207244", 
    #               height=10, width=15, command=self.ClearFieldsButton).pack(anchor="e", side="left", ipady=5, pady=(10, 10), padx=(10,10))
        
    def AddHouseButton(self):
        pass
    def DeleteHouseButton(self):
        pass
    

    # def optionsFrame(self): # Task Management Options

    #     global e_ID, e_Username, e_Password, e_FirstName, e_LastName, e_DOB, e_ContactNumber, e_RoleID, e_EnrollmentStatus, e_HouseID, e_Message, Cmbo_Role, Cmbo_EnrollmentStatus
    #     e_ID = tk.StringVar()
    #     e_Username = tk.StringVar()
    #     e_Password = tk.StringVar()
    #     e_FirstName = tk.StringVar()
    #     e_LastName = tk.StringVar()
    #     e_DOB = tk.StringVar()
    #     e_ContactNumber = tk.StringVar()
    #     e_EnrollmentStatus = tk.StringVar()
    #     e_RoleID = tk.StringVar()
    #     e_Message = tk.StringVar()
    #     e_HouseID = tk.StringVar()
    #     Cmbo_Role = tk.StringVar()
    #     Cmbo_EnrollmentStatus = tk.StringVar()

    #     optionsFrame = CTkFrame(master=self, fg_color="transparent", width=100, height=180, border_color="#fff", border_width=2)
    #     optionsFrame.propagate(0)
    #     optionsFrame.pack(anchor="n", side="bottom", fill="x", padx=10, pady=(20, 20))

    #     # CTkLabel(optionsFrame, text="User Options", font=("Arial Black", 20), bg_color="transparent", text_color="#fff").pack(anchor="nw", side="top")
    #     CTkLabel(optionsFrame, text='''  ID            Name              EventID                Capacity             Difficulty           Points''', font=("Arial Bold", 12), 
    #             text_color="#FFC300").pack(anchor="w", side="top", padx=(10, 0), pady=(5, 0))

    #     entryFrame = CTkFrame(optionsFrame, fg_color="transparent", width=480, height=30, border_color="#2A8C55", border_width=0)
    #     entryFrame.propagate(0)
    #     entryFrame.pack(anchor="n", fill="x", padx=5, pady=(0,0))
    #     CTkEntry(entryFrame, width=25, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", 
    #             text_color="#000", textvariable=e_ID, state='readonly').pack(anchor="n", side="left", padx=(5, 2), fill="x")
    #     CTkEntry(entryFrame, width=55, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", 
    #             text_color="#000", textvariable=e_Username).pack(anchor="n", side="left", padx=(15, 2), fill="x")
    #     CTkEntry(entryFrame, width=70, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", 
    #             text_color="#000", textvariable=e_Password).pack(anchor="n", side="left", padx=(20, 2), fill="x")
    #     CTkEntry(entryFrame, width=65, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", 
    #             text_color="#000", textvariable=e_FirstName).pack(anchor="n", side="left", padx=(20, 2), fill="x")
    #     CTkEntry(entryFrame, width=65, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", 
    #             text_color="#000", textvariable=e_LastName).pack(anchor="n", side="left", padx=(20, 2), fill="x")
    #     CTkEntry(entryFrame, width=80, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", 
    #             text_color="#000", textvariable=e_DOB).pack(anchor="n", side="left", padx=(2, 2), fill="x")

    #     CTkLabel(optionsFrame, text="Options:", font=("Arial Black", 24), bg_color="transparent", 
    #             text_color="#ECEAE2").pack(anchor="e", side="left", padx=(10,0))
    #     CTkButton(optionsFrame, text="Add Task", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 16), hover_color="#207244", 
    #             height=10, width=15, command=self.AddHouseButton).pack(anchor="e", side="left", ipady=5, pady=(10, 10), padx=(20,10))
    #     CTkButton(optionsFrame, text="Delete Task", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 16), hover_color="#207244", 
    #             height=10, width=15, command=self.DeleteHouseButton).pack(anchor="e", side="left", ipady=5, pady=(10, 10), padx=(10,10))
    #     CTkButton(optionsFrame, text="Clear Fields", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 16), hover_color="#207244", 
    #             height=10, width=15, command=self.ClearFieldsButton).pack(anchor="e", side="left", ipady=5, pady=(10, 10), padx=(10,10))

    
    
if __name__ == "__main__":
    mainMenu()