import sqlite3
from CTkTable import *
from customtkinter import *



def SQL_AdminView_fetchadminusers():
            conn = sqlite3.connect('./backend/WillowInnDB.db')
            cursor = conn.cursor()

            disp_column = ["UserID", "Username", "Password", "FirstName", "LastName", "DOB", "ContactNumber", "Role", "EnrollmentStatus", "HouseID", "Message"] # iunclude coluims you only wanna show
            columnsSQL = ', '.join(disp_column) # for the sql wuarey
            cursor.execute(f'SELECT {columnsSQL} FROM UserTable') #yupada
            rows = cursor.fetchall() #this puts it in tabular form so u can just use it with the ctk table thing

            conn.close()
            return disp_column, rows