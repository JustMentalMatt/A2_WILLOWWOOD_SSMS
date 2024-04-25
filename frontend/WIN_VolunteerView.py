import customtkinter as ctk
import tkinter as tk
from customtkinter import *
from CTkTable import CTkTable
from PIL import Image
import sqlite3


from SQL_AdminView import *
from SQL_SupervisorView import *
from SQL_VolunteerView import *
from validation import auditlog

class volunteerView(ctk.CTkFrame):
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
        
        CTkLabel(text_frame, text="\n\n\nskibidi rizz simulator", font=("Trebuchet MS", 18), text_color="#000", bg_color="#fff").pack(anchor="center", side="top")

    def TaskFrame(self):
    
        title_frame = CTkFrame(self.main_view, fg_color="transparent", width=480, height=35)
        title_frame.propagate(0)
        title_frame.pack(anchor="n", fill="x", padx=15, pady=(29, 0))
        
        CTkLabel(title_frame, text="Volunteer Tasks", font=("Arial Black", 25), text_color="#DAF7A6").pack(anchor="nw", side="left")

        searchBar = CTkEntry(title_frame, width=250, height=35, font=("Arial Bold", 20), fg_color="#fff", bg_color="transparent", text_color="#000", placeholder_text="Search...")
        searchBar.pack(anchor="ne", side="right", padx=(0, 5), fill="x")
        searchBar.propagate(0)
        
        tableSelectVAR = tk.StringVar(value="TaskTable")


        class TaskTable:
            def __init__(self, parent):
                self.parent = parent
                self.main_view = parent.main_view
                self.INIT_table_Tasks(search_query=None)
                self.optionsFrame()
                
            def ClearFieldsButton(self):
                volunteerView.TableDestroy(self)
                TaskTable(self).INIT_table_Tasks(search_query=None)
                
            global selectedRow
            selectedRow = None
            
            def TableClickEvent(self, cell):
                global selectedRow, T_ID, T_Name, T_Capacity, T_Difficulty, T_Points, table

                if selectedRow is not None:
                    table.deselect_row(selectedRow)

                selectedRow = cell["row"]
                print("Selected Row:", selectedRow)
                table.select_row(selectedRow)
                selectedData = table.get_row(selectedRow)

                T_ID.set(selectedData[0])
                T_Name.set(selectedData[1])
                T_Capacity.set(selectedData[2])
                T_Difficulty.set(selectedData[3])
                T_Points.set(selectedData[4])

            def INIT_table_Tasks(self, search_query=None):
                
                volunteerView.TableDestroy(self)
                
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
                with open('TaskTable Export.txt', 'w') as f:
                    headings = result[0]
                    for heading in headings[0:]:
                        f.write('{:<20}'.format(heading))
                    f.write('\n')
                    for row in result[1]:
                        row_data = [str(item) if item is not None else '' for item in row]
                        for item in row_data[0:]:
                            f.write('{:<20}'.format(item))
                        f.write('\n')
                        
            def AssignTaskButton(self):
                global T_ID, T_Name, T_Capacity, T_Difficulty, T_Points
                if T_ID.get() == "":
                    tk.messagebox.showerror("Error", "Please select a task to enroll in.")
                else:
                    with open("frontend/uservar.txt", "r") as file:
                        userVAR = file.read().strip()
                        file.close()
                    SQL_VolunteerView_EnrollInTask(T_ID.get(), userVAR)
                    self.ClearFieldsButton()

            def optionsFrame(self):

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

                entryFrame = CTkFrame(optionsFrame, fg_color="transparent", width=480, height=30, border_color="#2A8C55", border_width=0)
                entryFrame.propagate(0)
                entryFrame.pack(anchor="n", fill="x", padx=5, pady=(0,0))
                CTkEntry(entryFrame, width=35, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=T_ID, state='readonly').pack(anchor="n", side="left", padx=(5, 2), fill="x")
                CTkEntry(entryFrame, width=75, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=T_Name, state='readonly').pack(anchor="n", side="left", padx=(2, 2), fill="x")
                CTkEntry(entryFrame, width=75, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=T_Capacity, state='readonly').pack(anchor="n", side="left", padx=(20, 2), fill="x")
                CTkEntry(entryFrame, width=45, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=T_Difficulty, state='readonly').pack(anchor="n", side="left", padx=(10, 2), fill="x")
                CTkEntry(entryFrame, width=45, height=25, font=("Arial Bold", 12), fg_color="#fff", bg_color="transparent", text_color="#000", textvariable=T_Points, state='readonly').pack(anchor="n", side="left", padx=(10, 2), fill="x")

                CTkButton(optionsFrame, text="Enroll in Task", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 12), hover_color="#207244", height=10, width=15, command=self.AssignTaskButton).pack(anchor="e", side="right", ipady=5, pady=(10, 10), padx=(0,10))
                CTkButton(optionsFrame, text="Export Table", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 12), hover_color="#207244", height=10, width=15, command=self.exportTable).pack(anchor="e", side="right", ipady=5, pady=(10, 10), padx=(0,10))


        def SwitchTable(tableSelectVAR):
            tableName = tableSelectVAR
            if tableName == "TaskTable":
                self.TableDestroy()
                TaskTable(self).INIT_table_Tasks(search_query=None)



        tableSelect = CTkComboBox(title_frame, values=["TaskTable"], command=SwitchTable, width=200, height=35, font=("Arial Bold", 15), fg_color="#fff", bg_color="transparent", text_color="#000", variable=tableSelectVAR)
        tableSelect.propagate(0)
        tableSelect.pack(anchor="ne", side="right", padx=(0, 10),pady=(0,0), fill="x")

        SwitchTable("TaskTable") # default table to display

        def on_search():
            search_query = None if searchBar.get() == "" else searchBar.get()
            
            if tableSelectVAR.get() == "TaskTable":
                TaskTableINST = TaskTable(parent=self)
                TaskTableINST.INIT_table_Tasks(search_query=search_query)




        searchBar.bind("<Return>", lambda event: on_search())
        
        
    def EnrolledTasksFrame(self):
    
        with open("frontend/uservar.txt", "r") as file:
            VolunteerUsername = file.read().strip()
            file.close()
    
        def exportTable():
            result = SQL_VolunteerView_FetchTasks(VolunteerUsername)
            with open(f'{VolunteerUsername} - Task Export.txt', 'w') as f:
                headings = "TaskID", "TaskName"
                for heading in headings[0:]:
                    f.write('{:<20}'.format(heading))
                f.write('\n')
                for row in result:
                    row_data = [str(item) if item is not None else '' for item in row]
                    for item in row_data[0:]:
                        f.write('{:<20}'.format(item))
                    f.write('\n')

        title_frame = CTkFrame(self.main_view, fg_color="transparent", width=480, height=35)
        title_frame.propagate(0)
        title_frame.pack(anchor="n", fill="x", padx=15, pady=(29, 0))
        
        CTkLabel(title_frame, text="My Tasks", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", side="left")
        
        searchBar = CTkEntry(title_frame, width=250, height=35, font=("Arial Bold", 20), fg_color="#fff", bg_color="#2A8C55", text_color="#000", placeholder_text="Search...")
        searchBar.pack(anchor="ne", side="right", padx=(0, 5), fill="x")
        searchBar.propagate(0)
        
        
        def INIT_TABLE_EnrolledTasks(search_query=None):
            
            disp_column = "TaskID", "TaskName"
            rows = SQL_VolunteerView_FetchTasks(VolunteerUsername, search_query) if search_query else SQL_VolunteerView_FetchTasks(VolunteerUsername)
            tabData = [disp_column]
            tabData.extend(rows)
            
            tabFrame = CTkScrollableFrame(master=self.main_view, fg_color="transparent", border_color="#2A8C55",scrollbar_fg_color="transparent", border_width=2, width=480, height=900)
            tabFrame.pack(side="top", expand=False, fill="both", padx=10, pady=10)
            
            table = CTkTable(master=tabFrame, values=tabData, colors=["#E6E6E6", "#EEEEEE"], header_color="#2A8C55", hover_color="#B4B4B4", text_color="#000", width=75)
            table.edit_row(0, text_color="#000", hover_color="#2A8C55")
            table.pack(expand=True)
            table.configure(width=420, height=30)
            
            
        INIT_TABLE_EnrolledTasks()
        
        CTkButton(title_frame, text="Export Tasks", text_color="#19383d", fg_color="#fff", font=("Arial Bold", 15), hover_color="#207244", command=lambda: exportTable()).pack(anchor="ne", side="right", ipady=5, pady=(0, 0), padx=(0, 10))

        def on_search():
            global search_query
            search_query = None if searchBar.get() == "" else searchBar.get()
            self.TableDestroy()
            INIT_TABLE_EnrolledTasks(search_query)
        
        searchBar.bind("<Return>", lambda event: on_search())
        

    def GeneralRegisterFrame(self):

        def exportTable():
            result = SQL_AdminView_FetchGeneralRegister()
            with open('GeneralRegister Export.txt', 'w') as f:
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


    def sidebarFrame(self):
        sidebar = CTkFrame(self, fg_color="#edebde", width=176, height=650, corner_radius=0)
        sidebar.pack(fill="y", anchor="w", side="left")
        sidebar.pack_propagate(0)

        dat_img_mainLogo = Image.open("./frontend/Resources/WILLOW_LOGO.png")
        img_mainLogo = CTkImage(dark_image=dat_img_mainLogo, light_image=dat_img_mainLogo, size=(200,200))
        CTkLabel(sidebar, text="", image=img_mainLogo).pack(pady=(0, 0), anchor="center")
        
        CTkButton(sidebar, text="Menu", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 24), hover_color="#207244",
                    command=lambda: self.pageSwitch(self.menuFrame)).pack(anchor="center", ipady=5, pady=(40, 0))
        CTkButton(sidebar, text="Volunteer\nTasks", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19), hover_color="#207244",
                    command=lambda: self.pageSwitch(self.TaskFrame)).pack(anchor="center", ipady=5, pady=(15, 0))
        CTkButton(sidebar, text="My\nTasks", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19), hover_color="#207244",
                  command=lambda: self.pageSwitch(self.EnrolledTasksFrame)).pack(anchor="center", ipady=5, pady=(15, 0))
        CTkButton(sidebar, text="General\nRegister", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19), hover_color="#207244",
                  command=lambda: self.pageSwitch(self.GeneralRegisterFrame)).pack(anchor="center", ipady=5, pady=(15, 0))
        CTkButton(sidebar, text="Logout", command=self.onLogout, text_color="#000", fg_color="transparent", font=("Arial Bold", 18), bg_color="#C70039", hover_color="#AD0000").pack(anchor="center", ipady=5, pady=(15, 0))
