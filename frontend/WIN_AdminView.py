import customtkinter as ctk
import tkinter as tk
from customtkinter import *
from CTkTable import CTkTable
from PIL import Image
import sqlite3


from SQL_AdminView import *


class mainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1056x645")
        self.resizable(False, False)
        self.title("Logged In - WILLOW WOOD INN")

        self.main = adminView(self)
        self.mainloop()

# class mainMenu(CTkToplevel):
#     def __init__(self, master=None):
#         super().__init__(master)
#         self.geometry("1056x645")
#         self.resizable(False, False)
#         self.title("Logged In - WILLOW WOOD INN")

#         self.main = adminView(self)


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
            
    def TableDestroy(self):
        frames = self.main_view.winfo_children()
        for frame in frames[1:len(frames)]:
            print(frame)
            frame.destroy()
        
        # frame = self.main_view.winfo_children()[1] # this is the scrollable frame; specific frame deletion, leaves others.
        # frame.destroy()                            # CHANGE OTHER CODE IN onSearch() IF CHANGING THIS TO THE ABOVE METHOD!


    def pageSwitch(self, page):
        self.pageDestroy()
        page()

    def menuFrame(self):
        title_frame = CTkFrame(self.main_view, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=2, pady=(2, 0))

        dat_img_backlogo = Image.open("./frontend/Resources/WILLOW_TITLE_LOGO.png")
        img_backlogo = CTkImage(dark_image=dat_img_backlogo, light_image=dat_img_backlogo, size=(720,240))
        CTkLabel(title_frame, text="", image=img_backlogo).pack(pady=(0, 0), anchor="n")
        
        dat_img_300caff = Image.open("./frontend/Resources/300mg_caff.jpg")
        #img_300caff = CTkImage(dark_image=dat_img_300caff, light_image=dat_img_300caff, size=(720,240))
        #CTkLabel(self.main_view, text="", image=img_300caff).pack(pady=(0, 0), anchor="n")
        
        text_frame = CTkFrame(self.main_view, fg_color="transparent", bg_color="#fff", width=480, height=490, corner_radius=0)
        text_frame.propagate(0)
        text_frame.pack(anchor="center", fill="x", pady=(30, 30), padx=27)
        
        CTkLabel(text_frame, text="\n\n\nWelcome to the Willow Wood Inn Management System.\nThis system is designed to help you manage your business.\nYou can use the sidebar to navigate to different parts of the system.\n\n\n\n\nYou are currently logged in as an ADMIN USER\nTread with care as you have all access rights!", font=("Trebuchet MS", 18), text_color="#000", bg_color="#fff").pack(anchor="center", side="top")

    def UserManagementFrame(self):

        title_frame = CTkFrame(self.main_view, fg_color="transparent", width=480, height=35)
        title_frame.propagate(0)
        title_frame.pack(anchor="n", fill="x", padx=15, pady=(29, 0))
        
        CTkLabel(title_frame, text="User Management", font=("Arial Black", 25), text_color="#DAF7A6").pack(anchor="nw", side="left")

        searchBar = CTkEntry(title_frame, width=250, height=35, font=("Arial Bold", 20), fg_color="#fff", bg_color="transparent", text_color="#000", placeholder_text="Search...")
        searchBar.pack(anchor="ne", side="right", padx=(0, 5), fill="x")
        searchBar.propagate(0)
        
        
        tableSelect = CTkComboBox(title_frame, values=["ALL USERS", "Management", "Supervisors", "Volunteers"], width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        tableSelect.propagate(0)
        tableSelect.pack(anchor="ne", side="right", padx=(0, 10),pady=(0,0), fill="x")


        def INIT_TABLE_AllUsers(search_query=None):
            
            global selectedRow
            selectedRow = None
            def TableClickEvent(cell):
                global selectedRow, e_ID, e_Username, e_Password, e_FirstName, e_LastName, e_DOB, e_ContactNumber, e_Role, e_EnrollmentStatus, e_HouseID, e_Message

                if selectedRow is not None:
                    table.deselect_row(selectedRow)

                selectedRow = cell["row"]
                print("Selected Row:", selectedRow)
                table.select_row(selectedRow)
                selectedData = table.get_row(selectedRow)

                global e_ID, e_Username, e_Password, e_FirstName, e_LastName, e_DOB, e_ContactNumber, e_Role, e_EnrollmentStatus, e_HouseID, e_Message, Cmbo_Role, Cmbo_EnrollmentStatus

                e_ID.set(selectedData[0])
                e_Username.set(selectedData[1])
                e_Password.set(selectedData[2])
                e_FirstName.set(selectedData[3])
                e_LastName.set(selectedData[4])
                e_DOB.set(selectedData[5])
                e_ContactNumber.set(selectedData[6])
                e_Role.set(selectedData[7])
                e_EnrollmentStatus.set(selectedData[8])
                e_HouseID.set(selectedData[9])
                e_Message.set(selectedData[10])

                Cmbo_Role.set(selectedData[7])
                Cmbo_EnrollmentStatus.set(selectedData[8])


            disp_column = SQL_AdminView_FetchUserTable()[0]
            rows = SQL_AdminView_FetchUserTable(search_query)[1] if search_query else SQL_AdminView_FetchUserTable()[1]
            tabData = [disp_column]
            tabData.extend(rows)
            
            tabFrame = CTkScrollableFrame(master=self.main_view, fg_color="transparent", border_color="#2A8C55",scrollbar_fg_color="transparent", border_width=2, width=480, height=300)
            tabFrame.pack(side="top", expand=False, fill="both", padx=10, pady=10)  
            
            table = CTkTable(master=tabFrame, values=tabData, command=TableClickEvent, colors=["#E6E6E6", "#EEEEEE"], header_color="#FFC300", hover_color="#B4B4B4", text_color="#000", width=50)
            table.edit_row(0, text_color="#000", hover_color="#2A8C55")
            table.configure(width=50, height=10)
            table.pack(expand=False, fill="both")

        INIT_TABLE_AllUsers()


        #place for sql queries
        def ApplyChangesButton():
            SqlID = e_ID.get()
            EditSQLTable(SqlID, e_Username.get(), e_Password.get(), e_FirstName.get(), e_LastName.get(), e_DOB.get(), e_ContactNumber.get(), Cmbo_Role.get(), Cmbo_EnrollmentStatus.get(), e_HouseID.get(), e_Message.get())
            self.TableDestroy()
            INIT_TABLE_AllUsers()
            optionsFrame()

        def optionsFrame():
            ###
            global e_ID, e_Username, e_Password, e_FirstName, e_LastName, e_DOB, e_ContactNumber, e_Role, e_EnrollmentStatus, e_HouseID, e_Message, Cmbo_Role, Cmbo_EnrollmentStatus
            e_ID = tk.StringVar()
            e_Username = tk.StringVar()
            e_Password = tk.StringVar()
            e_FirstName = tk.StringVar()
            e_LastName = tk.StringVar()
            e_DOB = tk.StringVar()
            e_ContactNumber = tk.StringVar()
            e_Role = tk.StringVar()
            e_EnrollmentStatus = tk.StringVar()
            e_HouseID = tk.StringVar()
            e_Message = tk.StringVar()
            Cmbo_Role = tk.StringVar()
            Cmbo_EnrollmentStatus = tk.StringVar()
            ###

            optionsFrame = CTkFrame(self.main_view, fg_color="transparent", width=480, height=300, border_color="#2A8C55", border_width=2)
            optionsFrame.propagate(0)
            optionsFrame.pack(anchor="n", fill="x", padx=10, pady=(20, 20)) 
            CTkLabel(optionsFrame, text="User Options", font=("Arial Black", 25), text_color="#DAF7A6", bg_color="transparent").pack(anchor="nw", side="top")
            CTkLabel(optionsFrame, text="  ID    Username   Password   F_Name     L_Name        DOB      C_Number      Role          E_Status         HouseID    Message", font=("Arial Bold", 15), text_color="#FFC300").pack(anchor="w", side="top", padx=(10, 0), pady=(5, 0))

            
            #CTkButton(optionsFrame, text="Add User", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 19), hover_color="#207244", command=lambda: addUserButton()).pack(anchor="w", ipady=5, pady=(1, 0))
            entryFrame = CTkFrame(optionsFrame, fg_color="transparent", width=480, height=30, border_color="#2A8C55", border_width=0)
            entryFrame.propagate(0)
            entryFrame.pack(anchor="n", fill="x", padx=5, pady=(0,0))
            CTkEntry(entryFrame, width=35, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=e_ID, state='readonly').pack(anchor="n", side="left", padx=(5, 2), fill="x")
            CTkEntry(entryFrame, width=75, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=e_Username).pack(anchor="n", side="left", padx=(2, 2), fill="x")
            CTkEntry(entryFrame, width=80, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=e_Password).pack(anchor="n", side="left", padx=(2, 2), fill="x")
            CTkEntry(entryFrame, width=75, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=e_FirstName).pack(anchor="n", side="left", padx=(2, 2), fill="x")
            CTkEntry(entryFrame, width=75, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=e_LastName).pack(anchor="n", side="left", padx=(2, 2), fill="x")
            CTkEntry(entryFrame, width=75, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=e_DOB).pack(anchor="n", side="left", padx=(2, 2), fill="x")
            
            CTkEntry(entryFrame, width=75, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=e_ContactNumber).pack(anchor="n", side="left", padx=(2, 2), fill="x")
            CTkComboBox(entryFrame, values=["USER", "SUPV", "MGMT"], width=75, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", variable=Cmbo_Role).pack(anchor="n", side="left", padx=(2, 2), fill="x")
            CTkComboBox(entryFrame, values=["Enrolled", "Not Enrolled", "Pending"], width=110, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", variable=Cmbo_EnrollmentStatus).pack(anchor="n", side="left", padx=(2, 2), fill="x")

            CTkEntry(entryFrame, width=75, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=e_HouseID).pack(anchor="n", side="left", padx=(2, 2), fill="x")
            CTkEntry(entryFrame, width=75, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=e_Message).pack(anchor="n", side="left", padx=(2, 5), fill="x")
            
            #CTkButton(optionsFrame, text="Delete User", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 19), hover_color="#207244").pack(anchor="w", ipady=5, pady=(15, 0))
            CTkButton(optionsFrame, text="Apply Changes", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 12), hover_color="#207244", height=10, width=15, command=ApplyChangesButton).pack(anchor="se", ipady=5, pady=(70, 10), padx=(0, 10))

        optionsFrame()

        

        def on_search():
            global search_query
            search_query = None if searchBar.get() == "" else searchBar.get()
            self.TableDestroy()
            #self.UserManagementFrame(search_query)     # this repacks the whole frame with searchbar, table and title - not ideal;
            INIT_TABLE_AllUsers(search_query)         # this just repacks the table - better ---> Make sure to switch the parameters in the function call if choosing to change method.
            optionsFrame()

        searchBar.bind("<Return>", lambda event: on_search())

    def GeneralRegisterFrame(self):

            title_frame = CTkFrame(self.main_view, fg_color="transparent", width=480, height=35)
            title_frame.propagate(0)
            title_frame.pack(anchor="n", fill="x", padx=15, pady=(29, 0))
            
            CTkLabel(title_frame, text="General Register", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", side="left")
            
            searchBar = CTkEntry(title_frame, width=250, height=35, font=("Arial Bold", 20), fg_color="#fff", bg_color="#2A8C55", text_color="#000", placeholder_text="Search...")
            searchBar.pack(anchor="ne", side="right", padx=(0, 5), fill="x")
            searchBar.propagate(0)
            

            def INIT_TABLE_GeneralRegister(search_query=None):
                
                disp_column = SQL_AdminView_FetchGeneralRegister()[0]
                rows = SQL_AdminView_FetchGeneralRegister(search_query)[1] if search_query else SQL_AdminView_FetchGeneralRegister()[1]
                tabData = [disp_column]
                tabData.extend(rows)
                
                tabFrame = CTkScrollableFrame(master=self.main_view, fg_color="transparent", border_color="#2A8C55",scrollbar_fg_color="transparent", border_width=2, width=480, height=300)
                tabFrame.pack(side="top", expand=False, fill="both", padx=10, pady=10)
                
                table = CTkTable(master=tabFrame, values=tabData, colors=["#E6E6E6", "#EEEEEE"], header_color="#2A8C55", hover_color="#B4B4B4", text_color="#000", width=75)
                table.edit_row(0, text_color="#000", hover_color="#2A8C55")
                table.pack(expand=True)

                
                
            INIT_TABLE_GeneralRegister()

            def on_search():
                global search_query
                search_query = None if searchBar.get() == "" else searchBar.get()
                self.TableDestroy()
                #self.UserManagementFrame(search_query)     # this repacks the whole frame with searchbar, table and title - not ideal;
                INIT_TABLE_GeneralRegister(search_query)         # this just repacks the table - better ---> Make sure to switch the parameters in the function call if choosing to change method.
            
            searchBar.bind("<Return>", lambda event: on_search())

    def AlertFrame(self):
        title_frame = CTkFrame(self.main_view, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=2, pady=(2, 0))

        dat_img_backlogo = Image.open("./frontend/Resources/funny-laugh.png")
        img_backlogo = CTkImage(dark_image=dat_img_backlogo, light_image=dat_img_backlogo, size=(720,1000))
        CTkLabel(title_frame, text="", image=img_backlogo).pack(pady=(0, 0), anchor="n")
        
        dat_img_300caff = Image.open("./frontend/Resources/300mg_caff.jpg")
        #img_300caff = CTkImage(dark_image=dat_img_300caff, light_image=dat_img_300caff, size=(720,240))
        #CTkLabel(self.main_view, text="", image=img_300caff).pack(pady=(0, 0), anchor="n")
        
        CTkLabel(title_frame, text="yo momma pigo", font=("Trebuchet MS", 18), text_color="#000", bg_color="#fff").pack(anchor="center", side="top")

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
        CTkButton(sidebar, text="General\nRegister", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19), hover_color="#207244",
                  command=lambda: self.pageSwitch(self.GeneralRegisterFrame)).pack(anchor="center", ipady=5, pady=(15, 0))
        CTkButton(sidebar, text="Alerts", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19), hover_color="#207244",
                  command=lambda: self.pageSwitch(self.AlertFrame)).pack(anchor="center", ipady=5, pady=(15, 0))
        CTkButton(sidebar, text="Profile", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 18), hover_color="#207244").pack(anchor="center", ipady=5, pady=(50, 0))

if __name__ == "__main__":
    mainMenu()