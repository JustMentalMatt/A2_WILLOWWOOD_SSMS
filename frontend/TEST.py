# import customtkinter as ctk
# import tkinter as tk
# from customtkinter import *
# from CTkTable import CTkTable
# from PIL import Image
# import sqlite3


# from SQL_AdminView import *

# # import customtkinter
# # from CTkTable import *

# # root = customtkinter.CTk()

# # def show(cell):
# #     print("row:", cell["row"])
# #     print("column:", cell["column"])
# #     print("value:", cell["value"])
          
# # value = [[1,2,3,4,5],
# #          [1,2,3,4,5],
# #          [1,2,3,4,5],
# #          [1,2,3,4,5],
# #          [1,2,3,4,5],]

# # frame = customtkinter.CTkFrame(root)
# # frame.pack(expand=True, fill="both")

# # table = CTkTable(master=frame, row=5, column=5, values=value, height=100, command=show)
# # table.pack(expand=True, fill="both", padx=20, pady=20)

# # root.mainloop()

# ######################


# class adminView(ctk.CTkFrame):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.pack(expand=True, fill="both")

#         self.main_view = CTkFrame(self, fg_color="#19383d", width=900, height=650, corner_radius=0)
#         self.main_view.pack_propagate(0)
#         self.main_view.pack(side="right")

#         self.sidebarFrame = UserManagement.sidebarFrame(self)
#         self.menuFrame()
        
#         self.user_management = UserManagement(self)
#         self.sidebarFrame = UserManagement(self)
        
#     def pageSwitch(self, page):
#         self.pageDestroy()
#         page()
            
# class UserManagement:
#     def __init__(self, parent):
#         self.parent = parent
#         self.main_view = parent.main_view
#         #self.optionsFrame()
        
#     def sidebarFrame(self):
#         sidebar = CTkFrame(self, fg_color="#edebde", width=176, height=650, corner_radius=0)
#         sidebar.pack(fill="y", anchor="w", side="left")
#         sidebar.pack_propagate(0)

#         dat_img_mainLogo = Image.open("./frontend/Resources/WILLOW_LOGO.png")
#         img_mainLogo = CTkImage(dark_image=dat_img_mainLogo, light_image=dat_img_mainLogo, size=(200,200))
#         CTkLabel(sidebar, text="", image=img_mainLogo).pack(pady=(0, 0), anchor="center")
        
#         CTkButton(sidebar, text="User\nManagement", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19), hover_color="#207244",
#                     command=lambda: adminView.pageSwitch(UserManagement)).pack(anchor="center", ipady=5, pady=(15, 0))
    

###############


        # this is from another document but imported...
        def SQL_AdminView_FetchUserTable(search_query=None): #fetches all users from the database
    
            print("SQL search_query:", search_query)
            conn = sqlite3.connect('./backend/WillowInnDB.db')
            cursor = conn.cursor()

            disp_column = ["UserID", "Username", "Password", "FirstName", "LastName", "DOB", "ContactNumber", "EnrollmentStatus", "Message", "RoleID", "HouseID", "RoomID", "BedID"] # iunclude coluims you only wanna show
            columnsSQL = ', '.join(disp_column) # for the sql wuarey
            
            if search_query:
            # Add a WHERE clause to filter results based on the search query
                search_condition = f"UserID LIKE '{search_query}' OR Username LIKE '%{search_query}%' OR FirstName LIKE '%{search_query}%' OR LastName LIKE '%{search_query}%'"
                query = f"SELECT {columnsSQL} FROM UserTable WHERE {search_condition}"
            else:
                query = f"SELECT {columnsSQL} FROM UserTable"
            
            
            #cursor.execute(f'SELECT {columnsSQL} FROM UserTable') #yupada
            cursor.execute(query)
            rows = cursor.fetchall() #this puts it in tabular form so u can just use it with the ctk table thing

            conn.close()
            return disp_column, rows


        # this is from the main program
        searchBar = CTkEntry(title_frame, width=250, height=35, font=("Arial Bold", 20), fg_color="#fff", bg_color="transparent", text_color="#000", placeholder_text="Search...")

        class UserTable:
            def __init__(self, parent):
                self.parent = parent
                self.main_view = parent.main_view
                self.INIT_TABLE_AllUsers(search_query=None)
                self.optionsFrame()
                
            def INIT_TABLE_AllUsers(self, search_query=None):
                    
                print(f"{search_query} - Search Query")
                
                global table
                disp_column = SQL_AdminView_FetchUserTable()[0]
                rows = SQL_AdminView_FetchUserTable(search_query)[1] if search_query else SQL_AdminView_FetchUserTable()[1]
                tabData = [disp_column]
                tabData.extend(rows)
                
                tabFrame = CTkScrollableFrame(master=self.main_view, fg_color="transparent", border_color="#2A8C55",scrollbar_fg_color="transparent", border_width=2, width=480, height=350)
                tabFrame.pack(side="top", expand=False, fill="both", padx=10, pady=10)
                
                table = CTkTable(master=tabFrame, values=tabData, command=self.TableClickEvent, colors=["#E6E6E6", "#EEEEEE"], header_color="#FFC300", hover_color="#B4B4B4", text_color="#000", width=75)
                table.edit_row(0, text_color="#000", hover_color="#2A8C55")
                table.pack(expand=False)
                table.configure(width=45, height=20)
                
                
        def on_search():
    
            search_query = None if searchBar.get() == "" else searchBar.get()
            
            if tableSelectVAR.get() == "UserTable":
                self.TableDestroy()
                UserTableINST = UserTable(parent=self)
                UserTableINST.INIT_TABLE_AllUsers(search_query=search_query)
                print("UserTable")
                print(search_query)

        searchBar.bind("<Return>", lambda event: on_search())