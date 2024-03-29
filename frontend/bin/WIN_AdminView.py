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
        self.title("Logged In - MANAGEMENT - WILLOW WOOD INN")

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

        self.user_management = UserManagement(self)
        self.menu = menuFrame(self)
        self.general_register = GeneralRegisterFrame(self)
        self.house_management = HouseManagementFrame(self)
        
        #self.sidebarFrame = UserManagement.sidebarFrame(self)
        self.menu.__init__(self)
        
    def onLogout(self):
            self.destroy()
            self.quit()
            # main_WIN_Login()

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
        if page == 1:
            self.user_management.MenuFrame()
        elif page == 2:
            pass

class menuFrame:
    
    def __init__(self, parent):
        self.parent = parent
        self.main_view = parent.main_view
    
        title_frame = CTkFrame(self.main_view, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=2, pady=(2, 0))

        dat_img_backlogo = Image.open("./frontend/Resources/WILLOW_TITLE_LOGO.png")
        img_backlogo = CTkImage(dark_image=dat_img_backlogo, light_image=dat_img_backlogo, size=(720,240))
        CTkLabel(title_frame, text="", image=img_backlogo).pack(pady=(0, 0), anchor="n")

        text_frame = CTkFrame(self.main_view, fg_color="transparent", bg_color="#fff", width=480, height=490, corner_radius=0)
        text_frame.propagate(0)
        text_frame.pack(anchor="center", fill="x", pady=(30, 30), padx=27)
        
        CTkLabel(text_frame, text="\n\n\nWelcome to the Willow Wood Inn Management System.\nThis system is designed to help you manage your business.\nYou can use the sidebar to navigate to different parts of the system.\n\n\n\n\nYou are currently logged in as an ADMIN USER\nTread with care as you have all access rights!", font=("Trebuchet MS", 18), text_color="#000", bg_color="#fff").pack(anchor="center", side="top")


# DEF TABLES #


class UserManagement:
    
    def __init__(self, parent):
        self.parent = parent
        self.main_view = parent.main_view


    def INIT_TABLE_AllUsers(self, search_query=None):
        
        global selectedRow
        selectedRow = None
        def TableClickEvent(cell):
            global selectedRow, e_ID, e_Username, e_Password, e_FirstName, e_LastName, e_DOB, e_ContactNumber, e_RoleID, e_EnrollmentStatus, e_Message, e_HouseID, e_RoomID, e_BedID

            if selectedRow is not None:
                table.deselect_row(selectedRow)

            selectedRow = cell["row"]
            print("Selected Row:", selectedRow)
            table.select_row(selectedRow)
            selectedData = table.get_row(selectedRow)

            global e_ID, e_Username, e_Password, e_FirstName, e_LastName, e_DOB, e_ContactNumber, e_RoleID, e_EnrollmentStatus, e_Message, e_HouseID, e_RoomID, e_BedID, Cmbo_Role, Cmbo_EnrollmentStatus

            e_ID.set(selectedData[0])
            e_Username.set(selectedData[1])
            e_Password.set(selectedData[2])
            e_FirstName.set(selectedData[3])
            e_LastName.set(selectedData[4])
            e_DOB.set(selectedData[5])
            e_ContactNumber.set(selectedData[6])
            e_EnrollmentStatus.set(selectedData[7])
            e_Message.set(selectedData[8])
            e_RoleID.set(selectedData[9])
            e_HouseID.set(selectedData[10])
            e_RoomID.set(selectedData[11])
            e_BedID.set(selectedData[12])


            Cmbo_Role.set(selectedData[13])
            Cmbo_EnrollmentStatus.set(selectedData[9])

        disp_column = SQL_AdminView_FetchUserTable()[0]
        rows = SQL_AdminView_FetchUserTable(search_query)[1] if search_query else SQL_AdminView_FetchUserTable()[1]
        tabData = [disp_column]
        tabData.extend(rows)
        
        tabFrame = CTkScrollableFrame(master=self.main_view, fg_color="transparent", border_color="#2A8C55",scrollbar_fg_color="transparent", border_width=2, width=480, height=350)
        tabFrame.pack(side="top", expand=False, fill="both", padx=10, pady=10)  
        
        table = CTkTable(master=tabFrame, values=tabData, command=TableClickEvent, colors=["#E6E6E6", "#EEEEEE"], font=("Arial Bold", 10), header_color="#FFC300", hover_color="#B4B4B4", text_color="#000", width=50)
        table.edit_row(0, text_color="#000", hover_color="#2A8C55")
        table.configure(width=30, height=20)
        table.pack(expand=False, fill="both")

    def optionsFrame(self):
        ###
        global e_ID, e_Username, e_Password, e_FirstName, e_LastName, e_DOB, e_ContactNumber, e_RoleID, e_EnrollmentStatus, e_Message, e_HouseID, e_RoomID, e_BedID, Cmbo_Role, Cmbo_EnrollmentStatus
        self.e_ID = tk.StringVar()
        self.e_Username = tk.StringVar()
        self.e_Password = tk.StringVar()
        self.e_FirstName = tk.StringVar()
        self.e_LastName = tk.StringVar()
        self.e_DOB = tk.StringVar()
        self.e_ContactNumber = tk.StringVar()
        self.e_EnrollmentStatus = tk.StringVar()
        self.e_Message = tk.StringVar()
        self.e_RoleID = tk.StringVar()
        self.e_HouseID = tk.StringVar()
        self.e_RoomID = tk.StringVar()
        self.e_BedID = tk.StringVar()
        self.Cmbo_Role = tk.StringVar()
        self.Cmbo_EnrollmentStatus = tk.StringVar()
        ###

        optionsFrame = CTkFrame(self.main_view, fg_color="transparent", width=480, height=300, border_color="#2A8C55", border_width=2)
        optionsFrame.propagate(0)
        optionsFrame.pack(anchor="n", fill="x", padx=10, pady=(20, 20)) 
        CTkLabel(optionsFrame, text="User Options", font=("Arial Black", 25), bg_color="transparent", text_color="#DAF7A6").pack(anchor="nw", side="top")
        CTkLabel(optionsFrame, text="  ID    Username   Password   F_Name     L_Name        DOB      C_Number      Role          E_Status         HouseID    Message", font=("Arial Bold", 15), text_color="#FFC300").pack(anchor="w", side="top", padx=(10, 0), pady=(5, 0))

        #CTkButton(optionsFrame, text="Add User", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 19), hover_color="#207244", command=lambda: addUserButton()).pack(anchor="w", ipady=5, pady=(1, 0))
        entryFrame = CTkFrame(optionsFrame, fg_color="transparent", width=480, height=30, border_color="#2A8C55", border_width=0)
        entryFrame.propagate(0)
        entryFrame.pack(anchor="n", fill="x", padx=5, pady=(0,0))
        CTkEntry(entryFrame, width=35, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=self.e_ID, state='readonly').pack(anchor="n", side="left", padx=(5, 2), fill="x")
        CTkEntry(entryFrame, width=75, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=self.e_Username).pack(anchor="n", side="left", padx=(2, 2), fill="x")
        CTkEntry(entryFrame, width=80, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=self.e_Password).pack(anchor="n", side="left", padx=(2, 2), fill="x")
        CTkEntry(entryFrame, width=75, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=self.e_FirstName).pack(anchor="n", side="left", padx=(2, 2), fill="x")
        CTkEntry(entryFrame, width=75, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=self.e_LastName).pack(anchor="n", side="left", padx=(2, 2), fill="x")
        CTkEntry(entryFrame, width=75, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=self.e_DOB).pack(anchor="n", side="left", padx=(2, 2), fill="x")
        
        CTkEntry(entryFrame, width=75, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=self.e_ContactNumber).pack(anchor="n", side="left", padx=(2, 2), fill="x")
        CTkComboBox(entryFrame, values=["USER", "SUPV", "MGMT"], width=75, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", variable=self.Cmbo_Role).pack(anchor="n", side="left", padx=(2, 2), fill="x")
        CTkComboBox(entryFrame, values=["Enrolled", "Not Enrolled", "Pending"], width=110, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", variable=self.Cmbo_EnrollmentStatus).pack(anchor="n", side="left", padx=(2, 2), fill="x")

        CTkEntry(entryFrame, width=75, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=self.e_HouseID).pack(anchor="n", side="left", padx=(2, 2), fill="x")
        CTkEntry(entryFrame, width=75, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=self.e_Message).pack(anchor="n", side="left", padx=(2, 5), fill="x")
        
        #CTkButton(optionsFrame, text="Delete User", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 19), hover_color="#207244").pack(anchor="w", ipady=5, pady=(15, 0))
        CTkButton(optionsFrame, text="Apply Changes", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 12), hover_color="#207244", height=10, width=15, command=self.EditUserButton).pack(anchor="e", side="right", ipady=5, pady=(10, 10), padx=(0,10))
        CTkButton(optionsFrame, text="Add User", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 12), hover_color="#207244", height=10, width=15, command=self.AddUserButton).pack(anchor="w", side="left", ipady=5, pady=(10, 10), padx=(10,0))
        CTkButton(optionsFrame, text="Delete User", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 12), hover_color="#207244", height=10, width=15, command=self.DeleteUserButton).pack(anchor="w", side="left", ipady=5, pady=(10, 10), padx=(10,0))
        CTkButton(optionsFrame, text="Clear Fields", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 12), hover_color="#207244", height=10, width=15, command=self.ClearFieldsButton).pack(anchor="e", side="right", ipady=5, pady=(10, 10), padx=(0,10))

    def LoadTable(self, tableSelectVAR):
        print(tableSelectVAR)
        tableName = tableSelectVAR
        if tableName == "UserTable":
            self.parent.TableDestroy()
            self.INIT_TABLE_AllUsers()
            self.optionsFrame()

    def EditUserButton(self):
        SqlID = self.e_ID.get()
        EditUserSQL(SqlID, self.e_Username.get(), self.e_Password.get(), self.e_FirstName.get(), self.e_LastName.get(), self.e_DOB.get(), self.e_ContactNumber.get(), self.Cmbo_Role.get(), self.Cmbo_EnrollmentStatus.get(), self.e_HouseID.get(), self.e_Message.get())
        self.parent.TableDestroy()
        self.parent.INIT_TABLE_AllUsers()
        self.optionsFrame()

    def AddUserButton(self):
        if self.e_Username.get() == "":
            tk.messagebox.showerror("User Addition", "No user selected to add.")
            return
        else:
            try:
                AddUserSQL(self.e_Username.get(), self.e_Password.get(), self.e_FirstName.get(), self.e_LastName.get(), self.e_DOB.get(), self.e_ContactNumber.get(), self.Cmbo_Role.get(), self.Cmbo_EnrollmentStatus.get(), self.e_HouseID.get(), self.e_Message.get())
                self.parent.TableDestroy()
                self.parent.INIT_TABLE_AllUsers()
                self.optionsFrame()
            except sqlite3.IntegrityError:
                tk.messagebox.showerror("User Addition", "User already exists.")
                return
            except sqlite3.OperationalError:
                tk.messagebox.showerror("User Addition", "Database Locked - Restart the application.")
                return
            except sqlite3.DatabaseError:
                tk.messagebox.showerror("User Addition", "Database error - restart the application.")
                return

    def DeleteUserButton(self):
        if self.e_Username.get() == "":
            tk.messagebox.showerror("User Deletion", "No user selected to delete.")
            return
        
        answer = tk.messagebox.askyesno("User Deletion", f"Are you sure you want to PERMANENTLY DELETE [{self.e_Username.get()}]?\nThis action cannot be undone.", icon="warning")
        if answer:
            SqlID = self.e_ID.get()
            DeleteUserSQL(SqlID)
            self.parent.TableDestroy()
            self.parent.INIT_TABLE_AllUsers()
            self.optionsFrame()
    
    def ClearFieldsButton(self):
        self.parent.TableDestroy()
        self.parent.INIT_TABLE_AllUsers()
        self.optionsFrame()

    def on_search(self, event):
        search_query = None if self.searchBar.get() == "" else self.searchBar.get()
        self.parent.TableDestroy()
        self.parent.INIT_TABLE_AllUsers(search_query)
        self.optionsFrame()
    
class GeneralRegisterFrame:

    def __init__(self, parent):
        self.parent = parent
        self.main_view = parent.main_view

        title_frame = CTkFrame(self.main_view, fg_color="transparent", width=480, height=35)
        title_frame.propagate(0)
        title_frame.pack(anchor="n", fill="x", padx=15, pady=(29, 0))
        
        CTkLabel(title_frame, text="General Register", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", side="left")
        
        searchBar = CTkEntry(title_frame, width=250, height=35, font=("Arial Bold", 20), fg_color="#fff", bg_color="#2A8C55", text_color="#000", placeholder_text="Search...")
        searchBar.pack(anchor="ne", side="right", padx=(0, 5), fill="x")
        searchBar.propagate(0)
        

    def INIT_TABLE_GeneralRegister(self, search_query=None):
        
        disp_column = SQL_AdminView_FetchGeneralRegister()[0]
        rows = SQL_AdminView_FetchGeneralRegister(search_query)[1] if search_query else SQL_AdminView_FetchGeneralRegister()[1]
        tabData = [disp_column]
        tabData.extend(rows)
        
        tabFrame = CTkScrollableFrame(master=self.main_view, fg_color="transparent", border_color="#2A8C55",scrollbar_fg_color="transparent", border_width=2, width=480, height=900)
        tabFrame.pack(side="top", expand=False, fill="both", padx=10, pady=10)
        
        table = CTkTable(master=tabFrame, values=tabData, colors=["#E6E6E6", "#EEEEEE"], header_color="#2A8C55", hover_color="#B4B4B4", text_color="#000", width=75)
        table.edit_row(0, text_color="#000", hover_color="#2A8C55")
        table.pack(expand=True)
        table.configure(width=75, height=30)

            
            
        self.INIT_TABLE_GeneralRegister()

    def on_search(self):
        global search_query
        search_query = None if self.searchBar.get() == "" else self.searchBar.get()
        self.TableDestroy()
        #self.UserManagementFrame(search_query)     # this repacks the whole frame with searchbar, table and title - not ideal;
        self.INIT_TABLE_GeneralRegister(search_query)         # this just repacks the table - better ---> Make sure to switch the parameters in the function call if choosing to change method.
    
    # searchBar.bind("<Return>", lambda event: on_search())

class HouseManagementFrame:
    
    def __init__(self, parent):
        self.parent = parent
        self.main_view = parent.main_view
    
        title_frame = CTkFrame(self.main_view, fg_color="transparent", width=480, height=35)
        title_frame.propagate(0)
        title_frame.pack(anchor="n", fill="x", padx=15, pady=(29, 0))
        
        CTkLabel(title_frame, text="House Management", bg_color="transparent", font=("Arial Black", 32), text_color="#DAF7A6").pack(anchor="nw", side="left")

        HouseFrame = CTkScrollableFrame(master=self.main_view, fg_color="transparent", border_color="#2A8C55",scrollbar_fg_color="transparent", border_width=0, width=480, height=600)
        HouseFrame.pack(side="top", expand=False, fill="both", padx=10, pady=10)

        H1 = CTkFrame(HouseFrame, fg_color="transparent", width=480, height=380, border_color="#FF5733", border_width=5)
        H1.propagate(0)
        H1.pack(anchor="n", fill="x", padx=10, pady=(20, 20))
        CTkLabel(H1, text="House 1", font=("Arial Black", 25), text_color="#FFC300", bg_color="transparent").pack(anchor="nw", side="top", pady=(5, 0), padx=(10, 0))
    
        H2 = CTkFrame(HouseFrame, fg_color="transparent", width=480, height=380, border_color="#FF5733", border_width=5)
        H2.propagate(0)
        H2.pack(anchor="n", fill="x", padx=10, pady=(20, 20))
        CTkLabel(H2, text="House 2", font=("Arial Black", 25), text_color="#FFC300", bg_color="transparent").pack(anchor="nw", side="top", pady=(5, 0), padx=(10, 0))
    
        H3 = CTkFrame(HouseFrame, fg_color="transparent", width=480, height=380, border_color="#FF5733", border_width=5)
        H3.propagate(0)
        H3.pack(anchor="n", fill="x", padx=10, pady=(20, 20))
        CTkLabel(H3, text="House 3", font=("Arial Black", 25), text_color="#FFC300", bg_color="transparent").pack(anchor="nw", side="top", pady=(5, 0), padx=(10, 0))
        
        H4 = CTkFrame(HouseFrame, fg_color="transparent", width=480, height=380, border_color="#FF5733", border_width=5)
        H4.propagate(0)
        H4.pack(anchor="n", fill="x", padx=10, pady=(20, 20))
        CTkLabel(H4, text="House 4", font=("Arial Black", 25), text_color="#FFC300", bg_color="transparent").pack(anchor="nw", side="top", pady=(5, 0), padx=(10, 0))
        
        self.INIT_TABLE_House1()
        self.INIT_TABLE_House2()
        self.INIT_TABLE_House3()
        self.INIT_TABLE_House4()
        
        
    def INIT_TABLE_House1():
        disp_column = SQL_AdminView_FetchHouse(HouseID=1)[0]
        rows = SQL_AdminView_FetchHouse(HouseID=1)[1]

        tabData = [disp_column]
        tabData.extend(rows)
        
        tabFrame = CTkFrame(master=H1, fg_color="transparent", border_width=0, width=480, height=30)
        tabFrame.pack(side="top", expand=False, fill="both", padx=10, pady=10)
        
        table = CTkTable(master=tabFrame, values=tabData, colors=["#E6E6E6", "#EEEEEE"], header_color="#2A8C55", hover_color="#B4B4B4", text_color="#000", width=75)
        table.edit_row(0, text_color="#000", hover_color="#2A8C55")
        table.pack(expand=True)

        dividerFrame1 = CTkFrame(H1, fg_color="transparent", width=240, height=390, border_color="#fff", border_width=2)
        dividerFrame1.propagate(0)
        dividerFrame1.pack(side="left", anchor="n", fill="x", padx=25, pady=(20, 20))

        dividerFrame2 = CTkFrame(H1, fg_color="transparent", width=240, height=370, border_color="#fff", border_width=2)
        dividerFrame2.propagate(0)
        dividerFrame2.pack(side="left", anchor="n", fill="x", padx=10, pady=(20, 20))

        dividerFrame3 = CTkFrame(H1, fg_color="transparent", width=240, height=370, border_color="#fff", border_width=2)
        dividerFrame3.propagate(0)
        dividerFrame3.pack(side="left", anchor="n", fill="x", padx=10, pady=(20, 20))

        CTkLabel(dividerFrame1, text="Room 1", font=("Arial Black", 20), text_color="#DAF7A6", bg_color="transparent").pack(anchor="nw", side="top", pady=(5, 0), padx=(10, 0))
        CTkLabel(dividerFrame2, text="Room 2", font=("Arial Black", 20), text_color="#DAF7A6", bg_color="transparent").pack(anchor="nw", side="top", pady=(5, 0), padx=(10, 0))
        CTkLabel(dividerFrame3, text="Room 3", font=("Arial Black", 20), text_color="#DAF7A6", bg_color="transparent").pack(anchor="nw", side="top", pady=(5, 0), padx=(10, 0))

        def AssignBed(user, RoomID, BedID):
            SQLAdminView_AssignBed(user, RoomID, BedID, HouseID=1)


        def FetchAssignedUser(room_id, bed_id):
            return SQLAdminView_FetchAssignedUser(room_id, bed_id, house_id=1)

        HouseResidents = SQLAdminView_FetchHouseResidents(HouseID=1)
        C1 = CTkComboBox(dividerFrame1, values=HouseResidents, command=lambda user="", room_id="1", bed_id="1": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C1.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C1.set(FetchAssignedUser(1, 1))

        C2 = CTkComboBox(dividerFrame1, values=HouseResidents, command=lambda user="", room_id="1", bed_id="2": AssignBed(user, room_id, bed_id),width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C2.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C2.set(FetchAssignedUser(1, 2))

        C3 = CTkComboBox(dividerFrame1, values=HouseResidents, command=lambda user="", room_id="1", bed_id="3": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C3.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C3.set(FetchAssignedUser(1, 3))

        C4 = CTkComboBox(dividerFrame1, values=HouseResidents, command=lambda user="", room_id="1", bed_id="4": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C4.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C4.set(FetchAssignedUser(1, 4))

        C5 = CTkComboBox(dividerFrame2, values=HouseResidents, command=lambda user="", room_id="2", bed_id="1": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C5.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C5.set(FetchAssignedUser(2, 1))

        C6 = CTkComboBox(dividerFrame2, values=HouseResidents, command=lambda user="", room_id="2", bed_id="2": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C6.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C6.set(FetchAssignedUser(2, 2))

        C7 = CTkComboBox(dividerFrame2, values=HouseResidents, command=lambda user="", room_id="2", bed_id="3": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C7.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C7.set(FetchAssignedUser(2, 3))

        C8 = CTkComboBox(dividerFrame2, values=HouseResidents, command=lambda user="", room_id="2", bed_id="4": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C8.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C8.set(FetchAssignedUser(2, 4))

        C9 = CTkComboBox(dividerFrame3, values=HouseResidents, command=lambda user="", room_id="3", bed_id="1": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C9.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C9.set(FetchAssignedUser(3, 1))

        C10 = CTkComboBox(dividerFrame3, values=HouseResidents, command=lambda user="", room_id="3", bed_id="2": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C10.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C10.set(FetchAssignedUser(3, 2))

        C11 = CTkComboBox(dividerFrame3, values=HouseResidents, command=lambda user="", room_id="3", bed_id="3": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C11.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C11.set(FetchAssignedUser(3, 3))

        C12 = CTkComboBox(dividerFrame3, values=HouseResidents, command=lambda user="", room_id="3", bed_id="4": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C12.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C12.set(FetchAssignedUser(3, 4))


    def INIT_TABLE_House2():
        disp_column = SQL_AdminView_FetchHouse(HouseID=2)[0]
        rows = SQL_AdminView_FetchHouse(HouseID=2)[1]

        tabData = [disp_column]
        tabData.extend(rows)
        
        tabFrame = CTkFrame(master=H2, fg_color="transparent", border_width=0, width=480, height=30)
        tabFrame.pack(side="top", expand=False, fill="both", padx=10, pady=10)
        
        table = CTkTable(master=tabFrame, values=tabData, colors=["#E6E6E6", "#EEEEEE"], header_color="#2A8C55", hover_color="#B4B4B4", text_color="#000", width=75)
        table.edit_row(0, text_color="#000", hover_color="#2A8C55")
        table.pack(expand=True)

        dividerFrame1 = CTkFrame(H2, fg_color="transparent", width=240, height=390, border_color="#fff", border_width=2)
        dividerFrame1.propagate(0)
        dividerFrame1.pack(side="left", anchor="n", fill="x", padx=25, pady=(20, 20))

        dividerFrame2 = CTkFrame(H2, fg_color="transparent", width=240, height=370, border_color="#fff", border_width=2)
        dividerFrame2.propagate(0)
        dividerFrame2.pack(side="left", anchor="n", fill="x", padx=10, pady=(20, 20))

        dividerFrame3 = CTkFrame(H2, fg_color="transparent", width=240, height=370, border_color="#fff", border_width=2)
        dividerFrame3.propagate(0)
        dividerFrame3.pack(side="left", anchor="n", fill="x", padx=10, pady=(20, 20))

        CTkLabel(dividerFrame1, text="Room 1", font=("Arial Black", 20), text_color="#DAF7A6", bg_color="transparent").pack(anchor="nw", side="top", pady=(5, 0), padx=(10, 0))
        CTkLabel(dividerFrame2, text="Room 2", font=("Arial Black", 20), text_color="#DAF7A6", bg_color="transparent").pack(anchor="nw", side="top", pady=(5, 0), padx=(10, 0))
        CTkLabel(dividerFrame3, text="Room 3", font=("Arial Black", 20), text_color="#DAF7A6", bg_color="transparent").pack(anchor="nw", side="top", pady=(5, 0), padx=(10, 0))

        def AssignBed(user, RoomID, BedID):
            SQLAdminView_AssignBed(user, RoomID, BedID, HouseID=2)


        def FetchAssignedUser(room_id, bed_id):
            return SQLAdminView_FetchAssignedUser(room_id, bed_id, house_id=2)

        HouseResidents = SQLAdminView_FetchHouseResidents(HouseID=2)
        C1 = CTkComboBox(dividerFrame1, values=HouseResidents, command=lambda user="", room_id="1", bed_id="1": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C1.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C1.set(FetchAssignedUser(1, 1))

        C2 = CTkComboBox(dividerFrame1, values=HouseResidents, command=lambda user="", room_id="1", bed_id="2": AssignBed(user, room_id, bed_id),width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C2.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C2.set(FetchAssignedUser(1, 2))

        C3 = CTkComboBox(dividerFrame1, values=HouseResidents, command=lambda user="", room_id="1", bed_id="3": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C3.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C3.set(FetchAssignedUser(1, 3))

        C4 = CTkComboBox(dividerFrame1, values=HouseResidents, command=lambda user="", room_id="1", bed_id="4": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C4.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C4.set(FetchAssignedUser(1, 4))

        C5 = CTkComboBox(dividerFrame2, values=HouseResidents, command=lambda user="", room_id="2", bed_id="1": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C5.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C5.set(FetchAssignedUser(2, 1))

        C6 = CTkComboBox(dividerFrame2, values=HouseResidents, command=lambda user="", room_id="2", bed_id="2": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C6.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C6.set(FetchAssignedUser(2, 2))

        C7 = CTkComboBox(dividerFrame2, values=HouseResidents, command=lambda user="", room_id="2", bed_id="3": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C7.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C7.set(FetchAssignedUser(2, 3))

        C8 = CTkComboBox(dividerFrame2, values=HouseResidents, command=lambda user="", room_id="2", bed_id="4": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C8.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C8.set(FetchAssignedUser(2, 4))

        C9 = CTkComboBox(dividerFrame3, values=HouseResidents, command=lambda user="", room_id="3", bed_id="1": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C9.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C9.set(FetchAssignedUser(3, 1))

        C10 = CTkComboBox(dividerFrame3, values=HouseResidents, command=lambda user="", room_id="3", bed_id="2": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C10.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C10.set(FetchAssignedUser(3, 2))

        C11 = CTkComboBox(dividerFrame3, values=HouseResidents, command=lambda user="", room_id="3", bed_id="3": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C11.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C11.set(FetchAssignedUser(3, 3))

        C12 = CTkComboBox(dividerFrame3, values=HouseResidents, command=lambda user="", room_id="3", bed_id="4": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C12.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C12.set(FetchAssignedUser(3, 4))


    def INIT_TABLE_House3():
        disp_column = SQL_AdminView_FetchHouse(HouseID=3)[0]
        rows = SQL_AdminView_FetchHouse(HouseID=3)[1]

        tabData = [disp_column]
        tabData.extend(rows)
        
        tabFrame = CTkFrame(master=H3, fg_color="transparent", border_width=0, width=480, height=30)
        tabFrame.pack(side="top", expand=False, fill="both", padx=10, pady=10)
        
        table = CTkTable(master=tabFrame, values=tabData, colors=["#E6E6E6", "#EEEEEE"], header_color="#2A8C55", hover_color="#B4B4B4", text_color="#000", width=75)
        table.edit_row(0, text_color="#000", hover_color="#2A8C55")
        table.pack(expand=True)

        dividerFrame1 = CTkFrame(H3, fg_color="transparent", width=240, height=390, border_color="#fff", border_width=2)
        dividerFrame1.propagate(0)
        dividerFrame1.pack(side="left", anchor="n", fill="x", padx=25, pady=(20, 20))

        dividerFrame2 = CTkFrame(H3, fg_color="transparent", width=240, height=370, border_color="#fff", border_width=2)
        dividerFrame2.propagate(0)
        dividerFrame2.pack(side="left", anchor="n", fill="x", padx=10, pady=(20, 20))

        dividerFrame3 = CTkFrame(H3, fg_color="transparent", width=240, height=370, border_color="#fff", border_width=2)
        dividerFrame3.propagate(0)
        dividerFrame3.pack(side="left", anchor="n", fill="x", padx=10, pady=(20, 20))

        CTkLabel(dividerFrame1, text="Room 1", font=("Arial Black", 20), text_color="#DAF7A6", bg_color="transparent").pack(anchor="nw", side="top", pady=(5, 0), padx=(10, 0))
        CTkLabel(dividerFrame2, text="Room 2", font=("Arial Black", 20), text_color="#DAF7A6", bg_color="transparent").pack(anchor="nw", side="top", pady=(5, 0), padx=(10, 0))
        CTkLabel(dividerFrame3, text="Room 3", font=("Arial Black", 20), text_color="#DAF7A6", bg_color="transparent").pack(anchor="nw", side="top", pady=(5, 0), padx=(10, 0))

        def AssignBed(user, RoomID, BedID):
            SQLAdminView_AssignBed(user, RoomID, BedID, HouseID=3)


        def FetchAssignedUser(room_id, bed_id):
            return SQLAdminView_FetchAssignedUser(room_id, bed_id, house_id=3)

        HouseResidents = SQLAdminView_FetchHouseResidents(HouseID=3)
        C1 = CTkComboBox(dividerFrame1, values=HouseResidents, command=lambda user="", room_id="1", bed_id="1": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C1.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C1.set(FetchAssignedUser(1, 1))

        C2 = CTkComboBox(dividerFrame1, values=HouseResidents, command=lambda user="", room_id="1", bed_id="2": AssignBed(user, room_id, bed_id),width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C2.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C2.set(FetchAssignedUser(1, 2))

        C3 = CTkComboBox(dividerFrame1, values=HouseResidents, command=lambda user="", room_id="1", bed_id="3": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C3.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C3.set(FetchAssignedUser(1, 3))

        C4 = CTkComboBox(dividerFrame1, values=HouseResidents, command=lambda user="", room_id="1", bed_id="4": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C4.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C4.set(FetchAssignedUser(1, 4))

        C5 = CTkComboBox(dividerFrame2, values=HouseResidents, command=lambda user="", room_id="2", bed_id="1": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C5.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C5.set(FetchAssignedUser(2, 1))

        C6 = CTkComboBox(dividerFrame2, values=HouseResidents, command=lambda user="", room_id="2", bed_id="2": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C6.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C6.set(FetchAssignedUser(2, 2))

        C7 = CTkComboBox(dividerFrame2, values=HouseResidents, command=lambda user="", room_id="2", bed_id="3": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C7.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C7.set(FetchAssignedUser(2, 3))

        C8 = CTkComboBox(dividerFrame2, values=HouseResidents, command=lambda user="", room_id="2", bed_id="4": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C8.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C8.set(FetchAssignedUser(2, 4))

        C9 = CTkComboBox(dividerFrame3, values=HouseResidents, command=lambda user="", room_id="3", bed_id="1": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C9.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C9.set(FetchAssignedUser(3, 1))

        C10 = CTkComboBox(dividerFrame3, values=HouseResidents, command=lambda user="", room_id="3", bed_id="2": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C10.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C10.set(FetchAssignedUser(3, 2))

        C11 = CTkComboBox(dividerFrame3, values=HouseResidents, command=lambda user="", room_id="3", bed_id="3": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C11.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C11.set(FetchAssignedUser(3, 3))

        C12 = CTkComboBox(dividerFrame3, values=HouseResidents, command=lambda user="", room_id="3", bed_id="4": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C12.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C12.set(FetchAssignedUser(3, 4))


    def INIT_TABLE_House4():
        disp_column = SQL_AdminView_FetchHouse(HouseID=4)[0]
        rows = SQL_AdminView_FetchHouse(HouseID=4)[1]

        tabData = [disp_column]
        tabData.extend(rows)
        
        tabFrame = CTkFrame(master=H4, fg_color="transparent", border_width=0, width=480, height=30)
        tabFrame.pack(side="top", expand=False, fill="both", padx=10, pady=10)
        
        table = CTkTable(master=tabFrame, values=tabData, colors=["#E6E6E6", "#EEEEEE"], header_color="#2A8C55", hover_color="#B4B4B4", text_color="#000", width=75)
        table.edit_row(0, text_color="#000", hover_color="#2A8C55")
        table.pack(expand=True)

        dividerFrame1 = CTkFrame(H4, fg_color="transparent", width=240, height=390, border_color="#fff", border_width=2)
        dividerFrame1.propagate(0)
        dividerFrame1.pack(side="left", anchor="n", fill="x", padx=25, pady=(20, 20))

        dividerFrame2 = CTkFrame(H4, fg_color="transparent", width=240, height=370, border_color="#fff", border_width=2)
        dividerFrame2.propagate(0)
        dividerFrame2.pack(side="left", anchor="n", fill="x", padx=10, pady=(20, 20))

        dividerFrame3 = CTkFrame(H4, fg_color="transparent", width=240, height=370, border_color="#fff", border_width=2)
        dividerFrame3.propagate(0)
        dividerFrame3.pack(side="left", anchor="n", fill="x", padx=10, pady=(20, 20))

        CTkLabel(dividerFrame1, text="Room 1", font=("Arial Black", 20), text_color="#DAF7A6", bg_color="transparent").pack(anchor="nw", side="top", pady=(5, 0), padx=(10, 0))
        CTkLabel(dividerFrame2, text="Room 2", font=("Arial Black", 20), text_color="#DAF7A6", bg_color="transparent").pack(anchor="nw", side="top", pady=(5, 0), padx=(10, 0))
        CTkLabel(dividerFrame3, text="Room 3", font=("Arial Black", 20), text_color="#DAF7A6", bg_color="transparent").pack(anchor="nw", side="top", pady=(5, 0), padx=(10, 0))

        def AssignBed(user, RoomID, BedID):
            SQLAdminView_AssignBed(user, RoomID, BedID, HouseID=4)


        def FetchAssignedUser(room_id, bed_id):
            return SQLAdminView_FetchAssignedUser(room_id, bed_id, house_id=4)

        HouseResidents = SQLAdminView_FetchHouseResidents(HouseID=4)
        C1 = CTkComboBox(dividerFrame1, values=HouseResidents, command=lambda user="", room_id="1", bed_id="1": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C1.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C1.set(FetchAssignedUser(1, 1))

        C2 = CTkComboBox(dividerFrame1, values=HouseResidents, command=lambda user="", room_id="1", bed_id="2": AssignBed(user, room_id, bed_id),width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C2.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C2.set(FetchAssignedUser(1, 2))

        C3 = CTkComboBox(dividerFrame1, values=HouseResidents, command=lambda user="", room_id="1", bed_id="3": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C3.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C3.set(FetchAssignedUser(1, 3))

        C4 = CTkComboBox(dividerFrame1, values=HouseResidents, command=lambda user="", room_id="1", bed_id="4": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C4.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C4.set(FetchAssignedUser(1, 4))

        C5 = CTkComboBox(dividerFrame2, values=HouseResidents, command=lambda user="", room_id="2", bed_id="1": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C5.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C5.set(FetchAssignedUser(2, 1))

        C6 = CTkComboBox(dividerFrame2, values=HouseResidents, command=lambda user="", room_id="2", bed_id="2": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C6.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C6.set(FetchAssignedUser(2, 2))

        C7 = CTkComboBox(dividerFrame2, values=HouseResidents, command=lambda user="", room_id="2", bed_id="3": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C7.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C7.set(FetchAssignedUser(2, 3))

        C8 = CTkComboBox(dividerFrame2, values=HouseResidents, command=lambda user="", room_id="2", bed_id="4": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C8.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C8.set(FetchAssignedUser(2, 4))

        C9 = CTkComboBox(dividerFrame3, values=HouseResidents, command=lambda user="", room_id="3", bed_id="1": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C9.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C9.set(FetchAssignedUser(3, 1))

        C10 = CTkComboBox(dividerFrame3, values=HouseResidents, command=lambda user="", room_id="3", bed_id="2": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C10.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C10.set(FetchAssignedUser(3, 2))

        C11 = CTkComboBox(dividerFrame3, values=HouseResidents, command=lambda user="", room_id="3", bed_id="3": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C11.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C11.set(FetchAssignedUser(3, 3))

        C12 = CTkComboBox(dividerFrame3, values=HouseResidents, command=lambda user="", room_id="3", bed_id="4": AssignBed(user, room_id, bed_id), width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000")
        C12.pack(anchor="n", side="top", padx=(10, 10), pady=(5, 0))
        C12.set(FetchAssignedUser(3, 4))

class sidebarFrame:
        
        def __init__(self, parent):
            self.parent = parent
            self.main_view = parent.main_view
            
            sidebar = CTkFrame(self, fg_color="#edebde", width=176, height=650, corner_radius=0)
            sidebar.pack(fill="y", anchor="w", side="left")
            sidebar.pack_propagate(0)

            c = UserManagement(self)
            dat_img_mainLogo = Image.open("./frontend/Resources/WILLOW_LOGO.png")
            img_mainLogo = CTkImage(dark_image=dat_img_mainLogo, light_image=dat_img_mainLogo, size=(200,200))
            CTkLabel(sidebar, text="", image=img_mainLogo).pack(pady=(0, 0), anchor="center")
            
            CTkButton(sidebar, text="Menu", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 24), hover_color="#207244",
                        command=lambda: adminView.pageSwitch(self, page=1)).pack(anchor="center", ipady=5, pady=(40, 0))
            CTkButton(sidebar, text="Dashboard", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19), hover_color="#207244").pack(anchor="center", ipady=5, pady=(15, 0))
            CTkButton(sidebar, text="User\nManagement", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19), hover_color="#207244",
                        command=lambda: adminView.pageSwitch(self, page=2)).pack(anchor="center", ipady=5, pady=(15, 0))
            CTkButton(sidebar, text="General\nRegister", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19), hover_color="#207244",
                    command=lambda: adminView.pageSwitch(self, page=3)).pack(anchor="center", ipady=5, pady=(15, 0))
            CTkButton(sidebar, text="House\nManagement", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19), hover_color="#207244",
                    command=lambda: adminView.pageSwitch(self, page=4)).pack(anchor="center", ipady=5, pady=(15, 0))
            CTkButton(sidebar, text="Logout", command=self.onLogout, text_color="#000", fg_color="transparent", font=("Arial Bold", 18), bg_color="#C70039", hover_color="#AD0000").pack(anchor="center", ipady=5, pady=(15, 0))

if __name__ == "__main__":
    mainMenu()