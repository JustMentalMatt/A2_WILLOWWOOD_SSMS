import customtkinter as ctk
import tkinter as tk
from customtkinter import *
from CTkTable import CTkTable
from PIL import Image
import sqlite3


from SQL_AdminView import *
from SQL_SupervisorView import *

class supervisorView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand=True, fill="both")

        self.main_view = CTkFrame(self, fg_color="#19383d", 
                                  width=900, height=650, corner_radius=0)
        self.main_view.pack_propagate(0)
        self.main_view.pack(side="right")
        self.focus()
        self.sidebarFrame()
        self.menuFrame()

    def onLogout(self):
            self.destroy()
            self.quit()

    def pageDestroy(self):
        for frame in self.main_view.winfo_children():
            frame.destroy()
            
    def TableDestroy(self):
        frames = self.main_view.winfo_children()
        for frame in frames[1:len(frames)]:
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
        
        CTkLabel(text_frame, text="\n\n\nWelcome to the Willow Wood Inn Management System.\nYou can use the sidebar to navigate to different parts of the system.\n\n\n\n\nYou are currently logged in as a SUPERVISOR USER\nHead over to the [House Management] menu to manage your house\n or browse task and user details using the [System Management] menu.", font=("Trebuchet MS", 18), text_color="#000", bg_color="#fff").pack(anchor="center", side="top")

    def UserManagementFrame(self):
    
        title_frame = CTkFrame(self.main_view, fg_color="transparent", width=480, height=35)
        title_frame.propagate(0)
        title_frame.pack(anchor="n", fill="x", padx=15, pady=(29, 0))
        
        CTkLabel(title_frame, text="System Management", font=("Arial Black", 25), text_color="#DAF7A6").pack(anchor="nw", side="left")

        searchBar = CTkEntry(title_frame, width=250, height=35, font=("Arial Bold", 20), fg_color="#fff", bg_color="transparent", text_color="#000", placeholder_text="Search...")
        searchBar.pack(anchor="ne", side="right", padx=(0, 5), fill="x")
        searchBar.propagate(0)
        
        tableSelectVAR = tk.StringVar(value="UserTable")

        class UserTable:
            def __init__(self, parent):
                self.parent = parent
                self.main_view = parent.main_view
                self.INIT_TABLE_AllUsers(search_query=None)
                self.optionsFrame()

                
            def EditUserButton(self):
                EditUserSQL(e_ID.get(), e_Username.get(), e_Password.get(), e_FirstName.get(), e_LastName.get(), e_DOB.get(), e_ContactNumber.get(), Cmbo_Role.get(), Cmbo_EnrollmentStatus.get(), e_Message.get(), e_HouseID.get(), e_RoomID.get(), e_BedID.get())
                supervisorView.TableDestroy(self)
                UserTable(self).INIT_TABLE_AllUsers(search_query=None)
                
            def AddUserButton(self):
                global e_ID, e_Username, e_Password, e_FirstName, e_LastName, e_DOB, e_ContactNumber, e_RoleID, e_EnrollmentStatus, e_Message, e_HouseID, e_RoomID, e_BedID, Cmbo_Role, Cmbo_EnrollmentStatus
                if e_Username.get() == "":
                    tk.messagebox.showerror("User Addition", "No User selected to add.")
                    return
                else:
                    try:
                        AddUserSQL(e_Username.get(), e_Password.get(), e_FirstName.get(), e_LastName.get(), e_DOB.get(), e_ContactNumber.get(), Cmbo_Role.get(), Cmbo_EnrollmentStatus.get(), e_Message.get(), e_HouseID.get(), e_RoomID.get(), e_BedID.get())
                        supervisorView.TableDestroy(self)
                        UserTable(self).INIT_TABLE_AllUsers(search_query=None)
                    except sqlite3.IntegrityError:
                        tk.messagebox.showerror("User Addition", "Integrity Error.")
                        return
                    except sqlite3.OperationalError:
                        tk.messagebox.showerror("User Addition", "Database Locked - Restart the application.")
                        return
                    except sqlite3.DatabaseError:
                        tk.messagebox.showerror("User Addition", "Database Error - Restart the application.")
                        return
                    
            def DeleteUserButton(self):
                global e_Username
                if e_Username.get() == "":
                    tk.messagebox.showerror("User Deletion", "No User selected to delete.")
                    return
                
                answer = tk.messagebox.askyesno("User Deletion", f"Are you sure you want to PERMANENTLY DELETE [{e_Username.get()}]?\nThis action cannot be undone.", icon="warning")
                if answer:
                    DeleteUserSQL(e_ID.get())
                    supervisorView.TableDestroy(self)
                    UserTable(self).INIT_TABLE_AllUsers(search_query=None)
                    
            def ClearFieldsButton(self):
                supervisorView.TableDestroy(self)
                UserTable(self).INIT_TABLE_AllUsers(search_query=None)
                
            global selectedRow
            selectedRow = None
            
            def TableClickEvent(self, cell):
                global selectedRow, e_ID, e_Username, e_Password, e_FirstName, e_LastName, e_DOB, e_ContactNumber, e_RoleID, e_EnrollmentStatus, e_HouseID, e_Message, e_RoomID, e_BedID, table, Cmbo_Role, Cmbo_EnrollmentStatus

                if selectedRow is not None:
                    table.deselect_row(selectedRow)

                selectedRow = cell["row"]
                table.select_row(selectedRow)
                selectedData = table.get_row(selectedRow)

                e_ID.set(selectedData[0])
                e_Username.set(selectedData[1])
                e_Password.set(selectedData[2])
                e_FirstName.set(selectedData[3])
                e_LastName.set(selectedData[4])
                e_DOB.set(selectedData[5])
                e_ContactNumber.set(selectedData[6])
                e_HouseID.set(selectedData[10])
                e_Message.set(selectedData[8])
                e_RoomID.set(selectedData[11])
                e_BedID.set(selectedData[12])
                
                Cmbo_Role.set(selectedData[9])
                Cmbo_EnrollmentStatus.set(selectedData[7])
                
            def INIT_TABLE_AllUsers(self, search_query=None):
                

                supervisorView.TableDestroy(self)
                                
                global table
                global result
                result = SQL_SupervisorView_FetchUserTable(search_query)
                disp_column = result[0]
                rows = result[1]
                
                tabData = [disp_column]
                tabData.extend(rows)
                
                tabFrame = CTkScrollableFrame(master=self.main_view, fg_color="transparent", border_color="#2A8C55",scrollbar_fg_color="transparent", border_width=2, width=480, height=350)
                tabFrame.pack(side="top", expand=False, fill="both", padx=10, pady=10)
                
                table = CTkTable(master=tabFrame, values=tabData, command=self.TableClickEvent, colors=["#E6E6E6", "#EEEEEE"], header_color="#FFC300", hover_color="#B4B4B4", text_color="#000", width=75)
                
                table.edit_column(2, text_color=["#E6E6E6", "#EEEEEE"], hover_color="#FFFFFF", bg_color="#FFFFFF")
                
                table.edit_row(0, text_color="#000", hover_color="#2A8C55", bg_color="#FFC300")
                table.pack(expand=False)
                table.configure(width=45, height=20)
                
                self.optionsFrame()

            def exportTable(self):
                global result
                with open('./UserTable Export.txt', 'w') as f:
                    headings = result[0]
                    for heading in headings[0:]:
                        f.write('{:<20}'.format(heading))
                    f.write('\n')
                    for row in result[1]:
                        row_data = [str(item) if item is not None else '' for item in row]
                        for item in row_data[0:]:
                            f.write('{:<20}'.format(item))
                        f.write('\n')

                
            def optionsFrame(self):
                global e_ID, e_Username, e_Password, e_FirstName, e_LastName, e_DOB, e_ContactNumber, e_RoleID, e_EnrollmentStatus, e_HouseID, e_Message, e_RoomID, e_BedID, Cmbo_Role, Cmbo_EnrollmentStatus
                
                global table
                
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
                e_RoomID = tk.StringVar()
                e_BedID = tk.StringVar()
                Cmbo_Role = tk.StringVar()
                Cmbo_EnrollmentStatus = tk.StringVar()
                
                optionsFrame = CTkFrame(self.main_view, fg_color="transparent", width=480, height=300, border_color="#2A8C55", border_width=2)
                optionsFrame.propagate(0)
                optionsFrame.pack(anchor="n", fill="x", padx=10, pady=(20, 20))
                CTkLabel(optionsFrame, text="User Options", font=("Arial Black", 20), bg_color="transparent", text_color="#DAF7A6").pack(anchor="nw", side="top")
                CTkLabel(optionsFrame, text="  ID       Username         Password           F_Name             L_Name              DOB          C_Number   Role     E_Status            HouseID   Message RoomID  BedID", font=("Arial Bold", 12), text_color="#FFC300").pack(anchor="w", side="top", padx=(10, 0), pady=(5, 0))
                
                entryFrame = CTkFrame(optionsFrame, fg_color="transparent", width=480, height=30, border_color="#2A8C55", border_width=0)
                entryFrame.propagate(0)
                entryFrame.pack(anchor="n", fill="x", padx=5, pady=(0,0))
                CTkEntry(entryFrame, width=25, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=e_ID, state='readonly').pack(anchor="n", side="left", padx=(5, 2), fill="x")
                CTkEntry(entryFrame, width=55, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=e_Username, state='readonly').pack(anchor="n", side="left", padx=(15, 2), fill="x")
                CTkEntry(entryFrame, width=55, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=e_Password,  show="*", border_color="#ff0000").pack(anchor="n", side="left", padx=(15, 2), fill="x")
                CTkEntry(entryFrame, width=65, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=e_FirstName, state='readonly').pack(anchor="n", side="left", padx=(20, 2), fill="x")
                CTkEntry(entryFrame, width=65, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=e_LastName, state='readonly').pack(anchor="n", side="left", padx=(20, 2), fill="x")
                CTkEntry(entryFrame, width=80, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=e_DOB, state='readonly').pack(anchor="n", side="left", padx=(2, 2), fill="x")
                CTkEntry(entryFrame, width=65, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=e_ContactNumber, border_color="#ff0000").pack(anchor="n", side="left", padx=(2, 2), fill="x")
                
                CTkEntry(entryFrame, width=15, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=Cmbo_Role, state='readonly').pack(anchor="n", side="left", padx=(2, 2), fill="x")
                CTkComboBox(entryFrame, values=["Enrolled", "Not Enrolled", "Pending"], width=110, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", variable=Cmbo_EnrollmentStatus, border_color="#ff0000").pack(anchor="n", side="left", padx=(2, 2), fill="x")
                
                CTkEntry(entryFrame, width=25, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=e_HouseID, state='readonly').pack(anchor="n", side="left", padx=(2, 2), fill="x")
                CTkEntry(entryFrame, width=75, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=e_Message, border_color="#ff0000").pack(anchor="n", side="left", padx=(2, 5), fill="x")
                CTkEntry(entryFrame, width=25, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=e_RoomID, state='readonly').pack(anchor="n", side="left", padx=(2, 5), fill="x")
                CTkEntry(entryFrame, width=25, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=e_BedID, state='readonly').pack(anchor="n", side="left", padx=(2, 5), fill="x")
                
                CTkButton(optionsFrame, text="Apply Changes", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 12), hover_color="#207244", height=10, width=15, command=self.EditUserButton).pack(anchor="e", side="right", ipady=5, pady=(10, 10), padx=(0,10))
                CTkButton(optionsFrame, text="Add User", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 12), hover_color="#207244", height=10, width=15, command=self.AddUserButton).pack(anchor="w", side="left", ipady=5, pady=(10, 10), padx=(10,0))
                CTkButton(optionsFrame, text="Delete User", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 12), hover_color="#207244", height=10, width=15, command=self.DeleteUserButton).pack(anchor="w", side="left", ipady=5, pady=(10, 10), padx=(10,0))
                CTkButton(optionsFrame, text="Clear Fields", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 12), hover_color="#207244", height=10, width=15, command=self.ClearFieldsButton).pack(anchor="e", side="right", ipady=5, pady=(10, 10), padx=(0,10))
                CTkButton(optionsFrame, text="Export Table", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 12), hover_color="#207244", height=10, width=15, command=self.exportTable).pack(anchor="e", side="right", ipady=5, pady=(10, 10), padx=(0,10))
                CTkButton(optionsFrame, text="Refresh Table", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 12), hover_color="#207244", height=10, width=15, command=lambda: table.draw_table()).pack(anchor="e", side="right", ipady=5, pady=(10, 10), padx=(0,10))


        class HouseTable:
            def __init__(self, parent):
                self.parent = parent
                self.main_view = parent.main_view
                self.INIT_table_House(search_query=None)
                self.optionsFrame()

            global selectedRow
            selectedRow = None
            
            def TableClickEvent(self, cell):
                global selectedRow, h_ID, h_Name, h_Address, h_Telephone, h_Email, table

                if selectedRow is not None:
                    table.deselect_row(selectedRow)

                selectedRow = cell["row"]
                table.select_row(selectedRow)
                selectedData = table.get_row(selectedRow)

                h_ID.set(selectedData[0])
                h_Name.set(selectedData[1])
                h_Address.set(selectedData[2])
                h_Telephone.set(selectedData[3])
                h_Email.set(selectedData[4])

            def INIT_table_House(self, search_query=None):
                
                supervisorView.TableDestroy(self)
                
                global table
                global result
                result = SQL_AdminView_FetchHouseTable(search_query)
                disp_column = result[0]
                rows = result[1]
                
                tabData = [disp_column]
                tabData.extend(rows)
                
                tabFrame = CTkScrollableFrame(master=self.main_view, fg_color="transparent", border_color="#2A8C55",scrollbar_fg_color="transparent", border_width=2, width=480, height=350)
                tabFrame.pack(side="top", expand=False, fill="both", padx=10, pady=10)
                
                table = CTkTable(master=tabFrame, values=tabData, command=self.TableClickEvent, colors=["#E6E6E6", "#EEEEEE"], header_color="#FFC300", hover_color="#B4B4B4", text_color="#000", width=75)
                table.edit_row(0, text_color="#000", hover_color="#2A8C55")
                table.pack(expand=True)
                table.configure(width=170, height=40)
                
                self.optionsFrame()
            
            def exportTable(self):
                global result
                with open('./HouseTable Export.txt', 'w') as f:
                    headings = result[0]
                    for heading in headings[0:]:
                        f.write('{:<20}'.format(heading))
                    f.write('\n')
                    for row in result[1]:
                        row_data = [str(item) if item is not None else '' for item in row]
                        for item in row_data[0:]:
                            f.write('{:<20}'.format(item))
                        f.write('\n')
            
            def optionsFrame(self):
                ###
                global h_ID, h_Name, h_Address, h_Telephone, h_Email
                
                h_ID = tk.StringVar()
                h_Name = tk.StringVar()
                h_Address = tk.StringVar()
                h_Telephone = tk.StringVar()
                h_Email = tk.StringVar()
                

                optionsFrame = CTkFrame(self.main_view, fg_color="transparent", width=480, height=300, border_color="#2A8C55", border_width=2)
                optionsFrame.propagate(0)
                optionsFrame.pack(anchor="n", fill="x", padx=10, pady=(20, 20)) 
                CTkLabel(optionsFrame, text="House Options", font=("Arial Black", 25), bg_color="transparent", text_color="#DAF7A6").pack(anchor="nw", side="top")
                CTkLabel(optionsFrame, text="  ID        Name         Address    Telephone    Email        ", font=("Arial Bold", 15), text_color="#FFC300").pack(anchor="w", side="top", padx=(10, 0), pady=(5, 0))

                
                #CTkButton(optionsFrame, text="Add User", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 19), hover_color="#207244", command=lambda: addUserButton()).pack(anchor="w", ipady=5, pady=(1, 0))
                entryFrame = CTkFrame(optionsFrame, fg_color="transparent", width=480, height=30, border_color="#2A8C55", border_width=0)
                entryFrame.propagate(0)
                entryFrame.pack(anchor="n", fill="x", padx=5, pady=(0,0))

               
                CTkButton(optionsFrame, text="Export Table", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 12), hover_color="#207244", height=10, width=15, command=self.exportTable).pack(anchor="e", side="right", ipady=5, pady=(10, 10), padx=(0,10))

        class TaskTable:
            def __init__(self, parent):
                self.parent = parent
                self.main_view = parent.main_view
                self.INIT_table_Tasks(search_query=None)
                self.optionsFrame()

            def EditTaskButton(self):
                EditTaskSQL(T_ID.get(), T_Name.get(), T_Capacity.get(), T_Difficulty.get(), T_Points.get())
                supervisorView.TableDestroy(self)
                TaskTable(self).INIT_table_Tasks(search_query=None)
            
            def AddTaskButton(self):
                    
                    global T_ID, T_Name, T_Capacity, T_Difficulty, T_Points
                    if T_Name.get() == "":
                        tk.messagebox.showerror("Task Addition", "No Task selected to add.")
                        return
                    else:
                        try:
                            AddTaskSQL(T_Name.get(), T_Capacity.get(), T_Difficulty.get(), T_Points.get())
                            supervisorView.TableDestroy(self)
                            TaskTable(self)
                        except sqlite3.IntegrityError:
                            tk.messagebox.showerror("Task Addition", "Integrity Error.")
                            return
                        except sqlite3.OperationalError:
                            tk.messagebox.showerror("Task Addition", "Database Locked - Restart the application.")
                            return
                        except sqlite3.DatabaseError:
                            tk.messagebox.showerror("Task Addition", "Database Error - Restart the application.")
                            return
                        
            def DeleteTaskButton(self):
                global T_Name
                if T_Name.get() == "":
                    tk.messagebox.showerror("Task Deletion", "No Task selected to delete.")
                    return
                
                answer = tk.messagebox.askyesno("Task Deletion", f"Are you sure you want to PERMANENTLY DELETE [{T_Name.get()}]?\nThis action cannot be undone.", icon="warning")
                if answer:
                    DeleteTaskSQL(T_ID.get())
                    supervisorView.TableDestroy(self)
                    TaskTable(self).INIT_table_Tasks(search_query=None)

                    
            def ClearFieldsButton(self):
                supervisorView.TableDestroy(self)
                TaskTable(self).INIT_table_Tasks(search_query=None)
                
            global selectedRow
            selectedRow = None
            
            def TableClickEvent(self, cell):
                global selectedRow, T_ID, T_Name, T_Capacity, T_Difficulty, T_Points, table

                if selectedRow is not None:
                    table.deselect_row(selectedRow)

                selectedRow = cell["row"]
                table.select_row(selectedRow)
                selectedData = table.get_row(selectedRow)

                T_ID.set(selectedData[0])
                T_Name.set(selectedData[1])
                T_Capacity.set(selectedData[2])
                T_Difficulty.set(selectedData[3])
                T_Points.set(selectedData[4])

            def INIT_table_Tasks(self, search_query=None):
                
                supervisorView.TableDestroy(self)
                
                global table
                global result
                result = SQL_AdminView_FetchTaskTable(search_query)
                disp_column = result[0]
                rows = result[1]
                
                tabData = [disp_column]
                tabData.extend(rows)
                
                tabFrame = CTkScrollableFrame(master=self.main_view, fg_color="transparent", border_color="#2A8C55",scrollbar_fg_color="transparent", border_width=2, width=480, height=350)
                tabFrame.pack(side="top", expand=False, fill="both", padx=10, pady=10)
                
                table = CTkTable(master=tabFrame, values=tabData, command=self.TableClickEvent, colors=["#E6E6E6", "#EEEEEE"], header_color="#FFC300", hover_color="#B4B4B4", text_color="#000", width=75)
                table.edit_row(0, text_color="#000", hover_color="#2A8C55")
                table.configure(width=140, height=40)
                table.pack(expand=True)
                
                self.optionsFrame()
                
            def exportTable(self):
                global result
                with open('./TaskTable Export.txt', 'w') as f:
                    headings = result[0]
                    for heading in headings[0:]:
                        f.write('{:<20}'.format(heading))
                    f.write('\n')
                    for row in result[1]:
                        row_data = [str(item) if item is not None else '' for item in row]
                        for item in row_data[0:]:
                            f.write('{:<20}'.format(item))
                        f.write('\n')

            def optionsFrame(self):
                ###
                global selectedRow, T_ID, T_Name, T_Points, T_Capacity, T_Difficulty, table
                T_ID = tk.StringVar()
                T_Name = tk.StringVar()
                T_Points = tk.StringVar()
                T_Capacity = tk.StringVar()
                T_Difficulty = tk.StringVar()
                
                optionsFrame = CTkFrame(self.main_view, fg_color="transparent", width=480, height=300, border_color="#2A8C55", border_width=2)
                optionsFrame.propagate(0)
                optionsFrame.pack(anchor="n", fill="x", padx=10, pady=(20, 20)) 
                CTkLabel(optionsFrame, text="Task Options", font=("Arial Black", 25), bg_color="transparent", text_color="#DAF7A6").pack(anchor="nw", side="top")
                CTkLabel(optionsFrame, text="  ID        Name          Capacity     Difficulty    Points       ", font=("Arial Bold", 15), text_color="#FFC300").pack(anchor="w", side="top", padx=(10, 0), pady=(5, 0))

                
                #CTkButton(optionsFrame, text="Add User", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 19), hover_color="#207244", command=lambda: addUserButton()).pack(anchor="w", ipady=5, pady=(1, 0))
                entryFrame = CTkFrame(optionsFrame, fg_color="transparent", width=480, height=30, border_color="#2A8C55", border_width=0)
                entryFrame.propagate(0)
                entryFrame.pack(anchor="n", fill="x", padx=5, pady=(0,0))
                CTkEntry(entryFrame, width=35, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=T_ID, state='readonly').pack(anchor="n", side="left", padx=(5, 2), fill="x")
                CTkEntry(entryFrame, width=75, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=T_Name).pack(anchor="n", side="left", padx=(2, 2), fill="x")
                CTkEntry(entryFrame, width=75, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=T_Capacity).pack(anchor="n", side="left", padx=(20, 2), fill="x")
                CTkEntry(entryFrame, width=45, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=T_Difficulty).pack(anchor="n", side="left", padx=(10, 2), fill="x")
                CTkEntry(entryFrame, width=45, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=T_Points).pack(anchor="n", side="left", padx=(10, 2), fill="x")


                CTkButton(optionsFrame, text="Apply Changes", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 12), hover_color="#207244", height=10, width=15, command=self.EditTaskButton).pack(anchor="e", side="right", ipady=5, pady=(10, 10), padx=(0,10))
                CTkButton(optionsFrame, text="Add Task", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 12), hover_color="#207244", height=10, width=15, command=self.AddTaskButton).pack(anchor="w", side="left", ipady=5, pady=(10, 10), padx=(10,0))
                CTkButton(optionsFrame, text="Delete Task", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 12), hover_color="#207244", height=10, width=15, command=self.DeleteTaskButton).pack(anchor="w", side="left", ipady=5, pady=(10, 10), padx=(10,0))
                CTkButton(optionsFrame, text="Clear Fields", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 12), hover_color="#207244", height=10, width=15, command=self.ClearFieldsButton).pack(anchor="e", side="right", ipady=5, pady=(10, 10), padx=(0,10))
                CTkButton(optionsFrame, text="Export Table", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 12), hover_color="#207244", height=10, width=15, command=self.exportTable).pack(anchor="e", side="right", ipady=5, pady=(10, 10), padx=(0,10))

        class BookingTable:
            def __init__(self, parent):
                self.parent = parent
                self.main_view = parent.main_view
                self.INIT_table_Booking(search_query=None)
                self.optionsFrame()

            def EditBookingButton(self):
                EditBookingSQL(B_ID.get(), B_TaskID.get(), B_UserID.get(), B_Date.get())
                supervisorView.TableDestroy(self)
                BookingTable(self).INIT_table_Booking(search_query=None)
                
            def AddBookingButton(self):
                        
                global B_ID, B_TaskID, B_UserID, B_Date
                if B_TaskID.get() == "":
                    tk.messagebox.showerror("Booking Addition", "No Booking selected to add.")
                    return
                else:
                    try:
                        AddBookingSQL(B_TaskID.get(), B_UserID.get(), B_Date.get())
                        supervisorView.TableDestroy(self)
                        BookingTable(self).INIT_table_Booking(search_query=None)
                    except sqlite3.IntegrityError:
                        tk.messagebox.showerror("Booking Addition", "Integrity Error.")
                        return
                    except sqlite3.OperationalError:
                        tk.messagebox.showerror("Booking Addition", "Database Locked - Restart the application.")
                        return
                    except sqlite3.DatabaseError:
                        tk.messagebox.showerror("Booking Addition", "Database Error - Restart the application.")
                        return
            
            def DeleteBookingButton(self):
                global B_TaskID
                if B_TaskID.get() == "":
                    tk.messagebox.showerror("Booking Deletion", "No Booking selected to delete.")
                    return
                
                answer = tk.messagebox.askyesno("Booking Deletion", f"Are you sure you want to PERMANENTLY DELETE the booking for [{B_Date.get()}]?\nThis action cannot be undone.", icon="warning")
                if answer:
                    DeleteBookingSQL(B_ID.get())
                    supervisorView.TableDestroy(self)
                    BookingTable(self).INIT_table_Booking(search_query=None)
                    
            def ClearFieldsButton(self):
                supervisorView.TableDestroy(self)
                BookingTable(self).INIT_table_Booking(search_query=None)

            global selectedRow
            selectedRow = None
            
            def TableClickEvent(self, cell):
                global selectedRow, B_ID, B_TaskID, B_UserID, B_Date, table

                if selectedRow is not None:
                    table.deselect_row(selectedRow)

                selectedRow = cell["row"]
                table.select_row(selectedRow)
                selectedData = table.get_row(selectedRow)

                B_ID.set(selectedData[0])
                B_TaskID.set(selectedData[1])
                B_UserID.set(selectedData[2])
                B_Date.set(selectedData[3])

            def INIT_table_Booking(self, search_query=None):
                
                supervisorView.TableDestroy(self)
                
                global table
                global result
                result = SQL_AdminView_FetchBookingTable(search_query)
                disp_column = result[0]
                rows = result[1]
                
                tabData = [disp_column]
                tabData.extend(rows)
                
                tabFrame = CTkScrollableFrame(master=self.main_view, fg_color="transparent", border_color="#2A8C55",scrollbar_fg_color="transparent", border_width=2, width=480, height=350)
                tabFrame.pack(side="top", expand=False, fill="both", padx=10, pady=10)
                
                table = CTkTable(master=tabFrame, values=tabData, command=self.TableClickEvent, colors=["#E6E6E6", "#EEEEEE"], header_color="#FFC300", hover_color="#B4B4B4", text_color="#000", width=75)
                table.edit_row(0, text_color="#000", hover_color="#2A8C55")
                table.pack(expand=True)
                table.configure(width=210, height=30)
                
                self.optionsFrame()
            
            def exportTable(self):
                global result
                with open('./BookingTable Export.txt', 'w') as f:
                    headings = result[0]
                    for heading in headings[0:]:
                        f.write('{:<20}'.format(heading))
                    f.write('\n')
                    for row in result[1]:
                        row_data = [str(item) if item is not None else '' for item in row]
                        for item in row_data[0:]:
                            f.write('{:<20}'.format(item))
                        f.write('\n')

            def optionsFrame(self):
                # These variables are used to store the data from the table
                global selectedRow, B_ID, B_TaskID, B_UserID, B_Date, table
                B_ID = tk.StringVar()
                B_UserID = tk.StringVar()
                B_TaskID = tk.StringVar()
                B_Date = tk.StringVar()
                
                optionsFrame = CTkFrame(self.main_view, fg_color="transparent", width=480, height=300, border_color="#2A8C55", border_width=2)
                optionsFrame.propagate(0)
                optionsFrame.pack(anchor="n", fill="x", padx=10, pady=(20, 20))
                CTkLabel(optionsFrame, text="Booking Options", font=("Arial Black", 25), bg_color="transparent", text_color="#DAF7A6").pack(anchor="nw", side="top")
                
                entryFrame = CTkFrame(optionsFrame, fg_color="transparent", width=480, height=30, border_color="#2A8C55", border_width=0)
                entryFrame.propagate(0)
                entryFrame.pack(anchor="n", fill="x", padx=5, pady=(0,0))
                
                # reduced buttons limit supervisor access to only the necessary functions
                CTkButton(optionsFrame, text="Delete Booking", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 26), hover_color="#207244", height=40, width=45, command=self.DeleteBookingButton).pack(anchor="center", side="left", ipady=5, pady=(0, 50), padx=(10,0))
                CTkButton(optionsFrame, text="Export Table", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 26), hover_color="#207244", height=40, width=45, command=self.exportTable).pack(anchor="center", side="right", ipady=5, pady=(0, 50), padx=(0,10))

        def SwitchTable(tableSelectVAR):
            tableName = tableSelectVAR
            if tableName == "UserTable":
                self.TableDestroy()
                UserTable(self).INIT_TABLE_AllUsers(search_query=None)
            elif tableName == "HouseTable":
                self.TableDestroy()
                HouseTable(self).INIT_table_House(search_query=None)
            elif tableName == "TaskTable":
                self.TableDestroy()
                TaskTable(self).INIT_table_Tasks(search_query=None)
            elif tableName == "BookingTable":
                self.TableDestroy()
                BookingTable(self).INIT_table_Booking(search_query=None)


        tableSelect = CTkComboBox(title_frame, values=["UserTable", "HouseTable", "TaskTable", "BookingTable"], command=SwitchTable, width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000", variable=tableSelectVAR)
        tableSelect.propagate(0)
        tableSelect.pack(anchor="ne", side="right", padx=(0, 10),pady=(0,0), fill="x")

        SwitchTable("UserTable") # default table to display

        def on_search():
            search_query = None if searchBar.get() == "" else searchBar.get()
            
            if tableSelectVAR.get() == "UserTable":
                UserTableINST = UserTable(parent=self)
                UserTableINST.INIT_TABLE_AllUsers(search_query=search_query)
            elif tableSelectVAR.get() == "HouseTable":
                HouseTableINST = HouseTable(parent=self)
                HouseTableINST.INIT_table_House(search_query=search_query)
            elif tableSelectVAR.get() == "TaskTable":
                TaskTableINST = TaskTable(parent=self)
                TaskTableINST.INIT_table_Tasks(search_query=search_query)
            elif tableSelectVAR.get() == "BookingTable":
                BookingTableINST = BookingTable(parent=self)
                BookingTableINST.INIT_table_Booking(search_query=search_query)



        searchBar.bind("<Return>", lambda event: on_search())
        

    def GeneralRegisterFrame(self):

        def exportTable():
            result = SQL_AdminView_FetchGeneralRegister()
            with open('./GeneralRegister Export.txt', 'w') as f:
                headings = result[0]
                for heading in headings[0:]:
                    f.write('{:<20}'.format(heading))
                f.write('\n')
                for row in result[1]:
                    row_data = [str(item) if item is not None else '' for item in row]
                    for item in row_data[0:]:
                        f.write('{:<20}'.format(item))
                    f.write('\n')

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
            
            tabFrame = CTkScrollableFrame(master=self.main_view, fg_color="transparent", border_color="#2A8C55",scrollbar_fg_color="transparent", border_width=2, width=480, height=900)
            tabFrame.pack(side="top", expand=False, fill="both", padx=10, pady=10)
            
            table = CTkTable(master=tabFrame, values=tabData, colors=["#E6E6E6", "#EEEEEE"], header_color="#2A8C55", hover_color="#B4B4B4", text_color="#000", width=75)
            table.edit_row(0, text_color="#000", hover_color="#2A8C55")
            table.pack(expand=True)
            table.configure(width=120, height=30)
            
            
        INIT_TABLE_GeneralRegister()
        
        CTkButton(title_frame, text="Export Table", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 15), hover_color="#207244", command=lambda: exportTable()).pack(anchor="ne", side="right", ipady=5, pady=(0, 0), padx=(0, 10))

        def on_search():
            global search_query
            search_query = None if searchBar.get() == "" else searchBar.get()
            self.TableDestroy()
            INIT_TABLE_GeneralRegister(search_query)
        
        searchBar.bind("<Return>", lambda event: on_search())

    def HouseManagementFrame(self):
        # House Management Frame
        title_frame = CTkFrame(self.main_view, fg_color="transparent", width=480, height=35)
        title_frame.propagate(0)
        title_frame.pack(anchor="n", fill="x", padx=15, pady=(29, 0))
        
        CTkLabel(title_frame, text="House Management", bg_color="transparent", font=("Arial Black", 32), text_color="#DAF7A6").pack(anchor="nw", side="left")

        HouseFrame = CTkScrollableFrame(master=self.main_view, fg_color="transparent", border_color="#2A8C55",scrollbar_fg_color="transparent", border_width=0, width=480, height=600)
        HouseFrame.pack(side="top", expand=False, fill="both", padx=10, pady=10)

        H = CTkFrame(HouseFrame, fg_color="transparent", width=480, height=380, border_color="#FF5733", border_width=5)
        H.propagate(0)
        H.pack(anchor="n", fill="x", padx=10, pady=(20, 20))
        
        # Gets the ID of the currently logged in Supervisor's House
        SupervisorHouseID = SQL_SupervisorView_FetchHouseID()
        
        # If the Supervisor is not assigned to a House, display an error message
        if SupervisorHouseID == None or SupervisorHouseID == "" or SupervisorHouseID == " ":
            CTkLabel(H, text="No House Assigned\n Please contact an Administrator.", font=("Arial Black", 25), text_color="#FFC300", bg_color="transparent").pack(anchor="center", pady=(5, 0), padx=(10, 0))
        else: # If the Supervisor is assigned to a House, display the House Management options, specific to that users assigned House.
            CTkLabel(H, text= f"House {SupervisorHouseID} Management", font=("Arial Black", 25), text_color="#FFC300", bg_color="transparent").pack(anchor="nw", side="top", pady=(5, 0), padx=(10, 0))
            
            # House Management Table - Reusing the code from WIN_AdminView.py, however it is modified 
            # to only display the House that the Supervisor is assigned to, by changing the HouseID parameter.
            def INIT_TABLE_House():
                
                disp_column = SQL_AdminView_FetchHouse(HouseID=SupervisorHouseID)[0]
                rows = SQL_AdminView_FetchHouse(HouseID=SupervisorHouseID)[1]

                tabData = [disp_column]
                tabData.extend(rows)
                
                tabFrame = CTkFrame(master=H, fg_color="transparent", border_width=0, width=480, height=30)
                tabFrame.pack(side="top", expand=False, fill="both", padx=10, pady=10)
                
                table = CTkTable(master=tabFrame, values=tabData, colors=["#E6E6E6", "#EEEEEE"], header_color="#2A8C55", hover_color="#B4B4B4", text_color="#000", width=75)
                table.edit_row(0, text_color="#000", hover_color="#2A8C55")
                table.pack(expand=True)

                dividerFrame1 = CTkFrame(H, fg_color="transparent", width=240, height=390, border_color="#fff", border_width=2)
                dividerFrame1.propagate(0)
                dividerFrame1.pack(side="left", anchor="n", fill="x", padx=25, pady=(20, 20))

                dividerFrame2 = CTkFrame(H, fg_color="transparent", width=240, height=370, border_color="#fff", border_width=2)
                dividerFrame2.propagate(0)
                dividerFrame2.pack(side="left", anchor="n", fill="x", padx=10, pady=(20, 20))

                dividerFrame3 = CTkFrame(H, fg_color="transparent", width=240, height=370, border_color="#fff", border_width=2)
                dividerFrame3.propagate(0)
                dividerFrame3.pack(side="left", anchor="n", fill="x", padx=10, pady=(20, 20))

                CTkLabel(dividerFrame1, text="Room 1", font=("Arial Black", 20), text_color="#DAF7A6", bg_color="transparent").pack(anchor="nw", side="top", pady=(5, 0), padx=(10, 0))
                CTkLabel(dividerFrame2, text="Room 2", font=("Arial Black", 20), text_color="#DAF7A6", bg_color="transparent").pack(anchor="nw", side="top", pady=(5, 0), padx=(10, 0))
                CTkLabel(dividerFrame3, text="Room 3", font=("Arial Black", 20), text_color="#DAF7A6", bg_color="transparent").pack(anchor="nw", side="top", pady=(5, 0), padx=(10, 0))

                def AssignBed(user, RoomID, BedID):
                    SQLAdminView_AssignBed(user, RoomID, BedID, HouseID=SupervisorHouseID)

                def FetchAssignedUser(room_id, bed_id):
                    return SQLAdminView_FetchAssignedUser(room_id, bed_id, house_id=SupervisorHouseID)

                HouseResidents = SQLAdminView_FetchHouseResidents(HouseID=SupervisorHouseID)
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


            INIT_TABLE_House()


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
        CTkButton(sidebar, text="System\nManagement", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19), hover_color="#207244",
                    command=lambda: self.pageSwitch(self.UserManagementFrame)).pack(anchor="center", ipady=5, pady=(15, 0))
        CTkButton(sidebar, text="General\nRegister", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19), hover_color="#207244",
                  command=lambda: self.pageSwitch(self.GeneralRegisterFrame)).pack(anchor="center", ipady=5, pady=(15, 0))
        CTkButton(sidebar, text="House\nManagement", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19), hover_color="#207244",
                  command=lambda: self.pageSwitch(self.HouseManagementFrame)).pack(anchor="center", ipady=5, pady=(15, 0))
        CTkButton(sidebar, text="Logout", command=self.onLogout, text_color="#000", fg_color="transparent", font=("Arial Bold", 18), bg_color="#C70039", hover_color="#AD0000").pack(anchor="center", ipady=5, pady=(15, 0))
