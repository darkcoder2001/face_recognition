
# CREATE TABLE
import customtkinter
import tkinter
import pyodbc

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")

app= customtkinter.CTk()
app.geometry("500x500")
app.title("add tables")

entry_table_name = customtkinter.CTkEntry(app,placeholder_text='enter table name',width=190)
entry_table_name.place(relx=0.1,rely=0.1)

entry_column1 = customtkinter.CTkEntry(app,placeholder_text='column1',width=190)
entry_column1.place(relx=0.1,rely=0.2)

entry_column2 = customtkinter.CTkEntry(app,placeholder_text='column2',width=190)
entry_column2.place(relx=0.1,rely=0.3)

entry_column3 = customtkinter.CTkEntry(app,placeholder_text='column3',width=190)
entry_column3.place(relx=0.1,rely=0.4)

def create():
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};'+
                                     'Server=ADMIN;'+
                                     f'Database={entry_database.get()};'+
                                     'Trusted_Connection=True')
        connection.autocommit = True
        sql_stmt = f"create table {entry_table_name.get()}\
                    ({entry_column1.get()} {radio_val_col1.get()},\
                    {entry_column2.get()} {radio_val_col2.get()},\
                    {entry_column3.get()} {radio_val_col3.get()})"
        connection.execute(sql_stmt)           
        info_label.configure(text="Table created successfully")
    except pyodbc.Error as ex:
        print('connect failed',ex)
        info_label.configure(text="Connect failed")
        

entry_database = customtkinter.CTkEntry(app,placeholder_text="enter name db")
entry_database.place(relx=0.1,rely=0.7)

create_Button = customtkinter.CTkButton(app,text="create column",command= create)
create_Button.place(relx=0.1,rely=0.5)
#column1
radio_val_col1 = tkinter.StringVar(value="")
col1_rd_varchar50= customtkinter.CTkRadioButton(app,text="varchar(50)",
                                                variable=radio_val_col1,
                                                value="varchar(50)")
col1_rd_varchar50.place(relx=0.5,rely=0.2)

col1_rd_int= customtkinter.CTkRadioButton(app,text="integer",
                                                variable=radio_val_col1,
                                                value="integer")
col1_rd_int.place(relx=0.7,rely=0.2)

#column2
radio_val_col2 = tkinter.StringVar(value="")
col2_rd_varchar50= customtkinter.CTkRadioButton(app,text="varchar(50)",
                                                variable=radio_val_col2,
                                                value="varchar(50)")
col2_rd_varchar50.place(relx=0.5,rely=0.3)

col2_rd_int= customtkinter.CTkRadioButton(app,text="integer",
                                                variable=radio_val_col2,
                                                value="integer")
col2_rd_int.place(relx=0.7,rely=0.3)

#column3
radio_val_col3 = tkinter.StringVar(value="")
col3_rd_varchar50= customtkinter.CTkRadioButton(app,text="varchar(50)",
                                                variable=radio_val_col3,
                                                value="varchar(50)")
col3_rd_varchar50.place(relx=0.5,rely=0.4)

col3_rd_int= customtkinter.CTkRadioButton(app,text="integer",
                                                variable=radio_val_col3,
                                                value="integer")
col3_rd_int.place(relx=0.7,rely=0.4)

info_label = customtkinter.CTkLabel(app,text="duc")
info_label.place(relx=0.1, rely=0.6)
app.mainloop()


# #INSERT INTO

# import customtkinter
# import tkinter
# import pyodbc

# customtkinter.set_appearance_mode("system")
# customtkinter.set_default_color_theme("blue")

# app= customtkinter.CTk()
# app.geometry("500x500")
# app.title("insert into")

# entry_database = customtkinter.CTkEntry(app,placeholder_text="enter name db",width=190)
# entry_database.place(relx=0.1,rely=0.1)

# entry_table_name = customtkinter.CTkEntry(app,placeholder_text='table name',width=190)
# entry_table_name.place(relx=0.1,rely=0.2)

# entry_id = customtkinter.CTkEntry(app,placeholder_text='ID',width=190)
# entry_id.place(relx=0.1,rely=0.3)

# entry_firstname = customtkinter.CTkEntry(app,placeholder_text='first name',width=190)
# entry_firstname.place(relx=0.1,rely=0.4)

# entry_lastname = customtkinter.CTkEntry(app,placeholder_text='last name',width=190)
# entry_lastname.place(relx=0.1,rely=0.5)

# def insert():
#     try:
#         connection = pyodbc.connect('DRIVER={SQL Server};'+
#                                      'Server=ADMIN;'+
#                                      f'Database={entry_database.get()};'+
#                                      'Trusted_Connection=True')
#         connection.autocommit = True
#         sql_stmt = f"INSERT INTO {entry_table_name.get()} VALUES ({entry_id.get()}, '{entry_firstname.get()}', '{entry_lastname.get()}')"
#         connection.execute(sql_stmt)
#         info_label.configure(text="Insert successfully")
        
#     except pyodbc.Error as ex:
#         print('connect failed',ex)
#         info_label.configure(text="Insert failed")



# insert_button = customtkinter.CTkButton(app,text="Insert",
#                                         command= insert,
#                                         fg_color="green")
# insert_button.place(relx=0.1,rely=0.6)

# info_label = customtkinter.CTkLabel(app,text="")
# info_label.place(relx=0.1,rely=0.7)

# app.mainloop()

#SHOW RESULTS

# import customtkinter
# import tkinter
# import pyodbc

# # customtkinter.set_appearance_mode("system")
# # customtkinter.set_default_color_theme("blue")

# # app = customtkinter.CTk()
# # app.geometry("500x500")
# # app.title("show results")

# try:
#     connection = pyodbc.connect('DRIVER={SQL Server};'+
#                                      'Server=ADMIN;'+
#                                      f'Database=ductran;'+
#                                      'Trusted_Connection=True')
#     cursor = connection.cursor()
    
#     cursor.execute("SELECT * from table2")
    
#     for data in cursor:
#         print(data[0],data[1],data[2])
        
# except pyodbc.Error as ex:
#     print('Failed',ex)
#     # info_label.configure(text="Show failed")
    

# import pyodbc
# import customtkinter

# customtkinter.set_appearance_mode("system")
# customtkinter.set_default_color_theme("blue")
# app = customtkinter.CTk()
# app.geometry("500x500")
# app.title("Show Full GUI")

# # Entry widgets
# entry_database = customtkinter.CTkEntry(app, placeholder_text="Enter database name", width=190)
# entry_database.place(relx=0.1, rely=0.1)

# entry_table_name = customtkinter.CTkEntry(app, placeholder_text='Enter table name', width=190)
# entry_table_name.place(relx=0.1, rely=0.2)

# id_name = customtkinter.CTkEntry(app, placeholder_text='Enter ID', width=190)
# id_name.place(relx=0.1, rely=0.3)

# # Textbox for displaying all results
# info_textbox = customtkinter.CTkTextbox(app, width=400, height=250)
# info_textbox.place(relx=0.1, rely=0.4)

# def select():
#     try:
#         # Connect to the database
#         connection = pyodbc.connect('DRIVER={SQL SERVER};' +
#                                     'Server=ADMIN;' +
#                                     f'Database={entry_database.get()};' +
#                                     'Trusted_Connection=True')
        
#         cursor = connection.cursor()
        
#         # Execute SQL query
#         cursor.execute(f"SELECT * FROM {entry_table_name.get()} WHERE name = '{id_name.get()}'")
        
#         # Clear previous content in textbox
#         info_textbox.delete("1.0", customtkinter.END)
        
#         # Loop through and display all rows
#         rows = cursor.fetchall()
#         if rows:
#             for data in rows:
#                 # Format and insert data into textbox
#                 row_text = " | ".join([str(item) for item in data]) + "\n"
#                 info_textbox.insert(customtkinter.END, row_text)
#         else:
#             info_textbox.insert(customtkinter.END, "No matching records found.")
#     except pyodbc.Error as ex:
#         print("Failed", ex)
#         info_textbox.insert(customtkinter.END, "No data or table found.")

# def delete_data():
#     try:
#         # Connect to the database
#         connection = pyodbc.connect('DRIVER={SQL SERVER};' +
#                                     'Server=ADMIN;' +
#                                     f'Database={entry_database.get()};' +
#                                     'Trusted_Connection=True')
        
#         cursor = connection.cursor()
        
#         # Execute DELETE query
#         cursor.execute(f"DELETE FROM {entry_table_name.get()} WHERE name = '{id_name.get()}'")
        
#         # Commit changes to the database
#         if cursor.rowcount == 0:
#             info_textbox.insert(customtkinter.END, "No data to delete.\n")
#         else:
#             connection.commit()
#             info_textbox.insert(customtkinter.END, "Data deleted successfully.\n")
#     except pyodbc.Error as ex:
#         print("Failed", ex)
#         info_textbox.insert(customtkinter.END, "Failed to delete data.\n")

# # Button to trigger select function
# select_button = customtkinter.CTkButton(app, text="Select",
#                                         command=select,
#                                         fg_color="green")
# select_button.place(relx=0.1, rely=0.7)

# # Button to trigger delete function
# delete_button = customtkinter.CTkButton(app, text="Delete",
#                                         command=delete_data,
#                                         fg_color="red")
# delete_button.place(relx=0.4, rely=0.7)

# app.mainloop()
