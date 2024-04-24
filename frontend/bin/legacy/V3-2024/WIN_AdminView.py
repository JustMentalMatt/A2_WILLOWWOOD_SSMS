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
        self.menuFrame()


    def pageDestroy():
        for frame in main_view.winfo_children():
            frame.destroy()

    def pageSwitch(self, page):
        self.pageDestroy(page)
        page()
        print("Switched to page: ", page)
    
    def menuFrame(self):
        main_view = CTkFrame(self, fg_color="#19383d",  width=900, height=650, corner_radius=0)
        main_view.pack_propagate(0)
        main_view.pack(side="left")

        title_frame = CTkFrame(main_view, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x",  padx=2, pady=(2, 0))
        
        dat_img_backlogo = Image.open("./frontend/Resources/WILLOW_TITLE_LOGO.png")
        img_backlogo = CTkImage(dark_image=dat_img_backlogo, light_image=dat_img_backlogo, size=(720,240))
        CTkLabel(title_frame, text="", image=img_backlogo).pack(pady=(0, 0), anchor="n")
        
        text_frame = CTkFrame(main_view, fg_color="transparent", bg_color="#fff", width=480, height=490, corner_radius=0)
        text_frame.propagate(0)
        text_frame.pack(anchor="center", fill="x", pady=(30, 30), padx=27)
        
        CTkLabel(text_frame, text='''Welcome to the Willow Wood Inn Management System.
                 \nThis system is designed to help you manage your business.
                 \nYou can use the sidebar to navigate to different parts of the system.''', 
                 font=("Trebuchet MS", 18), text_color="#000", bg_color="#fff").pack(anchor="center", side="top")
        
######
        
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
        
        main_view = CTkFrame(self, fg_color="#19383d",  width=680, height=450, corner_radius=0)
        main_view.pack_propagate(0)
        main_view.pack(anchor="ne")

        title_frame = CTkFrame(main_view, fg_color="transparent", width=480, height=450, corner_radius=30)
        title_frame.pack(anchor="n", fill="x",  padx=27, pady=(29, 0))

        CTkLabel(title_frame, text="AAAAAAA", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", side="left")
        
        
        UserManagementDatabase()
        
        

    def sidebarFrame(self):
            sidebar = CTkFrame(self, fg_color="#edebde",  width=176, height=650, corner_radius=0)
            sidebar.pack(fill="y", anchor="w", side="left")
            sidebar.pack_propagate(0)

            dat_img_mainLogo = Image.open("./frontend/Resources/WILLOW_LOGO.png")
            img_mainLogo = CTkImage(dark_image=dat_img_mainLogo, light_image=dat_img_mainLogo, size=(200,200))
            CTkLabel(sidebar, text="", image=img_mainLogo).pack(pady=(0, 0), anchor="center")
            
            CTkButton(sidebar, text="Menu", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 24), 
                      hover_color="#207244", command=lambda: self.pageSwitch(self.menuFrame)).pack(anchor="center", ipady=5, pady=(40, 0))
            CTkButton(sidebar, text="Dashboard", text_color="#19383d", fg_color="transparent", 
                      font=("Arial Bold", 19), hover_color="#207244").pack(anchor="center", ipady=5, pady=(15, 0))
            CTkButton(sidebar, text="User\nManagement", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19),
                      hover_color="#207244", command=lambda: self.pageSwitch(self.UserManagementFrame)).pack(anchor="center", ipady=5, pady=(15, 0))
            CTkButton(sidebar, text="Reports", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19),
                      hover_color="#207244").pack(anchor="center", ipady=5, pady=(15, 0))
            CTkButton(sidebar, text="Alerts", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 19),
                      hover_color="#207244").pack(anchor="center", ipady=5, pady=(15, 0))
            CTkButton(sidebar, text="Profile", text_color="#19383d", fg_color="transparent", font=("Arial Bold", 18),
                      hover_color="#207244").pack(anchor="center", ipady=5, pady=(50, 0))
            









# app = CTk()
# app.geometry("856x645")
# app.resizable(0,0)

# set_appearance_mode("light")

# sidebar_frame = CTkFrame(master=app, fg_color="#2A8C55",  width=176, height=650, corner_radius=0)
# sidebar_frame.pack_propagate(0)
# sidebar_frame.pack(fill="y", anchor="w", side="left")

# logo_img_data = Image.open("./GUI_Design/Inventory_Management/Images/logo.png")
# logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(77.68, 85.42))

# CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

# analytics_img_data = Image.open("./GUI_Design/Inventory_Management/Images/analytics_icon.png")
# analytics_img = CTkImage(dark_image=analytics_img_data, light_image=analytics_img_data)

# CTkButton(master=sidebar_frame, image=analytics_img, text="Dashboard", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w").pack(anchor="center", ipady=5, pady=(60, 0))

# package_img_data = Image.open("./GUI_Design/Inventory_Management/Images/package_icon.png")
# package_img = CTkImage(dark_image=package_img_data, light_image=package_img_data)

# CTkButton(master=sidebar_frame, image=package_img, text="Orders", fg_color="#fff", font=("Arial Bold", 14), text_color="#2A8C55", hover_color="#eee", anchor="w").pack(anchor="center", ipady=5, pady=(16, 0))

# list_img_data = Image.open("./GUI_Design/Inventory_Management/Images/list_icon.png")
# list_img = CTkImage(dark_image=list_img_data, light_image=list_img_data)
# CTkButton(master=sidebar_frame, image=list_img, text="Orders", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w").pack(anchor="center", ipady=5, pady=(16, 0))

# returns_img_data = Image.open("./GUI_Design/Inventory_Management/Images/returns_icon.png")
# returns_img = CTkImage(dark_image=returns_img_data, light_image=returns_img_data)
# CTkButton(master=sidebar_frame, image=returns_img, text="Returns", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w").pack(anchor="center", ipady=5, pady=(16, 0))

# settings_img_data = Image.open("./GUI_Design/Inventory_Management/Images/settings_icon.png")
# settings_img = CTkImage(dark_image=settings_img_data, light_image=settings_img_data)
# CTkButton(master=sidebar_frame, image=settings_img, text="Settings", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w").pack(anchor="center", ipady=5, pady=(16, 0))

# person_img_data = Image.open("./GUI_Design/Inventory_Management/Images/person_icon.png")
# person_img = CTkImage(dark_image=person_img_data, light_image=person_img_data)
# CTkButton(master=sidebar_frame, image=person_img, text="Account", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w").pack(anchor="center", ipady=5, pady=(160, 0))

# main_view = CTkFrame(master=app, fg_color="#fff",  width=680, height=650, corner_radius=0)
# main_view.pack_propagate(0)
# main_view.pack(side="left")

# title_frame = CTkFrame(master=main_view, fg_color="transparent")
# title_frame.pack(anchor="n", fill="x",  padx=27, pady=(29, 0))

# CTkLabel(master=title_frame, text="Orders", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", side="left")

# CTkButton(master=title_frame, text="+ New Order",  font=("Arial Black", 15), text_color="#fff", fg_color="#2A8C55", hover_color="#207244").pack(anchor="ne", side="right")

# metrics_frame = CTkFrame(master=main_view, fg_color="transparent")
# metrics_frame.pack(anchor="n", fill="x",  padx=27, pady=(36, 0))

# orders_metric = CTkFrame(master=metrics_frame, fg_color="#2A8C55", width=200, height=60)
# orders_metric.grid_propagate(0)
# orders_metric.pack(side="left")

# logitics_img_data = Image.open("./GUI_Design/Inventory_Management/Images/logistics_icon.png")
# logistics_img = CTkImage(light_image=logitics_img_data, dark_image=logitics_img_data, size=(43, 43))

# CTkLabel(master=orders_metric, image=logistics_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)

# CTkLabel(master=orders_metric, text="Orders", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
# CTkLabel(master=orders_metric, text="123", text_color="#fff",font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))


# shipped_metric = CTkFrame(master=metrics_frame, fg_color="#2A8C55", width=200, height=60)
# shipped_metric.grid_propagate(0)
# shipped_metric.pack(side="left",expand=True, anchor="center")

# shipping_img_data = Image.open("./GUI_Design/Inventory_Management/Images/shipping_icon.png")
# shipping_img = CTkImage(light_image=shipping_img_data, dark_image=shipping_img_data, size=(43, 43))

# CTkLabel(master=shipped_metric, image=shipping_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)

# CTkLabel(master=shipped_metric, text="Shipping", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
# CTkLabel(master=shipped_metric, text="91", text_color="#fff",font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))

# delivered_metric = CTkFrame(master=metrics_frame, fg_color="#2A8C55", width=200, height=60)
# delivered_metric.grid_propagate(0)
# delivered_metric.pack(side="right",)

# delivered_img_data = Image.open("./GUI_Design/Inventory_Management/Images/delivered_icon.png")
# delivered_img = CTkImage(light_image=delivered_img_data, dark_image=delivered_img_data, size=(43, 43))

# CTkLabel(master=delivered_metric, image=delivered_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)

# CTkLabel(master=delivered_metric, text="Delivered", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
# CTkLabel(master=delivered_metric, text="23", text_color="#fff",font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))

# search_container = CTkFrame(master=main_view, height=50, fg_color="#F0F0F0")
# search_container.pack(fill="x", pady=(45, 0), padx=27)

# CTkEntry(master=search_container, width=305, placeholder_text="Search Order", border_color="#2A8C55", border_width=2).pack(side="left", padx=(13, 0), pady=15)

# CTkComboBox(master=search_container, width=125, values=["Date", "Most Recent Order", "Least Recent Order"], button_color="#2A8C55", border_color="#2A8C55", border_width=2, button_hover_color="#207244",dropdown_hover_color="#207244" , dropdown_fg_color="#2A8C55", dropdown_text_color="#fff").pack(side="left", padx=(13, 0), pady=15)
# CTkComboBox(master=search_container, width=125, values=["Status", "Processing", "Confirmed", "Packing", "Shipping", "Delivered", "Cancelled"], button_color="#2A8C55", border_color="#2A8C55", border_width=2, button_hover_color="#207244",dropdown_hover_color="#207244" , dropdown_fg_color="#2A8C55", dropdown_text_color="#fff").pack(side="left", padx=(13, 0), pady=15)

# table_data = [
#     ["Order ID", "Item Name", "Customer", "Address", "Status", "Quantity"],
#     ['3833', 'Smartphone', 'Alice', '123 Main St', 'Confirmed', '8'],
#     ['6432', 'Laptop', 'Bob', '456 Elm St', 'Packing', '5'],
#     ['2180', 'Tablet', 'Crystal', '789 Oak St', 'Delivered', '1'],
#     ['5438', 'Headphones', 'John', '101 Pine St', 'Confirmed', '9'],
#     ['9144', 'Camera', 'David', '202 Cedar St', 'Processing', '2'],
#     ['7689', 'Printer', 'Alice', '303 Maple St', 'Cancelled', '2'],
#     ['1323', 'Smartwatch', 'Crystal', '404 Birch St', 'Shipping', '6'],
#     ['7391', 'Keyboard', 'John', '505 Redwood St', 'Cancelled', '10'],
#     ['4915', 'Monitor', 'Alice', '606 Fir St', 'Shipping', '6'],
#     ['5548', 'External Hard Drive', 'David', '707 Oak St', 'Delivered', '10'],
#     ['5485', 'Table Lamp', 'Crystal', '808 Pine St', 'Confirmed', '4'],
#     ['7764', 'Desk Chair', 'Bob', '909 Cedar St', 'Processing', '9'],
#     ['8252', 'Coffee Maker', 'John', '1010 Elm St', 'Confirmed', '6'],
#     ['2377', 'Blender', 'David', '1111 Redwood St', 'Shipping', '2'],
#     ['5287', 'Toaster', 'Alice', '1212 Maple St', 'Processing', '1'],
#     ['7739', 'Microwave', 'Crystal', '1313 Cedar St', 'Confirmed', '8'],
#     ['3129', 'Refrigerator', 'John', '1414 Oak St', 'Processing', '5'],
#     ['4789', 'Vacuum Cleaner', 'Bob', '1515 Pine St', 'Cancelled', '10']
# ]

# table_frame = CTkScrollableFrame(master=main_view, fg_color="transparent")
# table_frame.pack(expand=True, fill="both", padx=27, pady=21)
# table = CTkTable(master=table_frame, values=table_data, colors=["#E6E6E6", "#EEEEEE"], header_color="#2A8C55", hover_color="#B4B4B4")
# table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
# table.pack(expand=True)

# app.mainloop()

if __name__ == "__main__":
    mainMenu()