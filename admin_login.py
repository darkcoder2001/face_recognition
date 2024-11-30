import tkinter as tk
from PIL import Image, ImageTk
import subprocess

import bcrypt
from tkinter import messagebox
import re
import random
import smtplib
from email.mime.text import MIMEText
import pyodbc
import os
import bcrypt

def center_dialog(dialog):
    dialog.update_idletasks()  
    x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
    y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
    dialog.geometry(f"+{x}+{y}")

def load_icon(path, size=(20, 20)):
    img = Image.open(path)
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)





def create_login_dialog():
    global username_entry, password_entry, login_dialog, username_icon, password_icon, login_icon, forgot_icon, save_password_var

    # Tạo cửa sổ con thay vì cửa sổ chính
    login_dialog = tk.Toplevel()
    login_dialog.title("Đăng Nhập Admin")
    login_dialog.geometry("500x300")
    login_dialog.resizable(False, False)
    login_dialog.grab_set()
    center_dialog(login_dialog)

    # Tải các icon
    username_icon = load_icon('icon_btn/username.png')
    password_icon = load_icon('icon_btn/password.png')
    login_icon = load_icon('icon_btn/login.png')
    forgot_icon = load_icon('icon_btn/fg_password.png')

    # Khung chứa tài khoản
    account_frame = tk.Frame(login_dialog)
    account_frame.pack(pady=(40, 0))

    # Nhãn "Tài Khoản" với icon và khoảng cách giữa icon và text
    tk.Label(account_frame, text="Tài Khoản:", font=("Arial", 12), image=username_icon, compound='left', padx=10).pack(side="left", padx=(10, 5), pady=(20))
    username_entry = tk.Entry(account_frame, width=30, font=("Arial", 14))
    username_entry.pack(side="left", padx=(0, 10))

    # Khung chứa mật khẩu
    password_frame = tk.Frame(login_dialog)
    password_frame.pack(pady=(10, 0))

    # Nhãn "Mật Khẩu" với icon và khoảng cách giữa icon và text
    tk.Label(password_frame, text="Mật Khẩu:", font=("Arial", 12), image=password_icon, compound='left', padx=10).pack(side="left", padx=(15, 5), pady=(20))
    password_entry = tk.Entry(password_frame, show="*", width=30, font=("Arial", 14))
    password_entry.pack(side="left", padx=(0, 10))

    # Khung chứa các nút
    button_frame = tk.Frame(login_dialog)
    button_frame.pack(pady=(25, 25))

    # Nút Đăng Nhập với icon và khoảng cách giữa icon và text
    login_button = tk.Button(button_frame, text="Đăng Nhập", command=on_login_button_click, image=login_icon, compound='left', padx=30, pady=10)
    login_button.pack(side="left", padx=20)

    # Nút Quên Mật Khẩu với icon và khoảng cách giữa icon và text
    forgot_button = tk.Button(button_frame, text="Quên mật khẩu", command=lambda: [forgot_password_dialog()], image=forgot_icon, compound='left', padx=30, pady=10)
    forgot_button.pack(side="left", padx=20)

    # Checkbutton lưu mật khẩu
    save_password_var = tk.BooleanVar()
    save_password_check = tk.Checkbutton(login_dialog, text="Lưu mật khẩu", variable=save_password_var)
    save_password_check.place(relx=0.3,rely=0.57)

    # Đọc thông tin đăng nhập từ file nếu có
    if os.path.exists("hacked.txt"):
        with open("hacked.txt", "r") as f:
            saved_data = f.read().splitlines()
            if len(saved_data) == 2:
                username_entry.insert(0, saved_data[0])
                password_entry.insert(0, saved_data[1])

    login_dialog.bind('<Return>', on_enter_key)


def close_dialog(dialog):
    dialog.destroy()

def validate_email(email):
    # Kiểm tra định dạng email
    pattern = r"[^@]+@[^@]+\.[^@]+"  # Email phải có ký tự trước và sau "@" và sau dấu "."
    return re.match(pattern, email)

def load_db_config():
    try:
        with open("db_config.txt", "r") as config_file:
            lines = config_file.readlines()
            if len(lines) >= 2:
                return lines[0].strip(), lines[1].strip()
    except FileNotFoundError:
        pass
    return None, None

def hash_password(password):
    # Mã hóa mật khẩu với salt tự động tạo
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def forgot_password_dialog():
    # Tạo cửa sổ dialog nhập email và username
    forgot_pw_dialog = tk.Toplevel()
    forgot_pw_dialog.title("Quên mật khẩu")
    forgot_pw_dialog.geometry("400x250")
    forgot_pw_dialog.resizable(False, False)
    forgot_pw_dialog.grab_set()
    center_dialog(forgot_pw_dialog)

    # Dòng nhắc nhập username
    label_username = tk.Label(forgot_pw_dialog, text="Nhập Username:", font=("Arial", 12))
    label_username.pack(pady=10)

    # Ô nhập username
    username_entry = tk.Entry(forgot_pw_dialog, font=("Arial", 12), width=30)
    username_entry.pack(pady=5)

    # Dòng nhắc nhập email
    label_email = tk.Label(forgot_pw_dialog, text="Nhập email:", font=("Arial", 12))
    label_email.pack(pady=10)

    # Ô nhập email
    email_entry = tk.Entry(forgot_pw_dialog, font=("Arial", 12), width=30)
    email_entry.pack(pady=5)

    def submit_info():
        username = username_entry.get()
        email = email_entry.get()
        
        if not validate_email(email):
            messagebox.showerror("Lỗi", "Email không hợp lệ. Vui lòng nhập lại!")
            return
        
        # Kiểm tra xem username và email có tồn tại trong hệ thống không
        if check_user_exists(username, email):  # Hàm này sẽ kiểm tra trong cơ sở dữ liệu
            # Tạo mật khẩu ngẫu nhiên
            new_password = str(random.randint(100000, 999999))
            send_email(email, new_password)  # Gửi email với mật khẩu mới
            messagebox.showinfo("Thông báo", "Chúng tôi đã gửi mật khẩu mới về email của bạn, vui lòng kiểm tra!")
            update_password(username, new_password)
            hashed_password = hash_password(new_password)
            hashed_password_str = hashed_password.decode('utf-8')
            update_password(username, hashed_password_str)
            close_dialog(forgot_pw_dialog)
            # login_dialog.deiconify()
        else:
            messagebox.showerror("Lỗi", "Username hoặc email không tồn tại trong hệ thống!")

    # Nút OK để xác nhận thông tin
    ok_button = tk.Button(forgot_pw_dialog, text="OK", command=submit_info, width=10, height=2, bg="green")
    ok_button.pack(pady=10)

def check_user_exists(username, email):
    # Kết nối đến cơ sở dữ liệu để kiểm tra sự tồn tại của username và email
    server_name, database_name = load_db_config()
    if server_name and database_name:
        try:
            connection = pyodbc.connect(
                'DRIVER={SQL Server};' +
                f'Server={server_name};' +
                f'Database={database_name};' +
                'Trusted_Connection=True'
            )
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM user_manager WHERE Username = ? AND Email = ?", (username, email))
            exists = cursor.fetchone()[0] > 0
            cursor.close()
            connection.close()
            return exists
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi", "Lỗi kiểm tra sự tồn tại của người dùng")
            return False

def update_password(username, new_hashed_password):
    # Kết nối đến cơ sở dữ liệu để cập nhật mật khẩu
    server_name, database_name = load_db_config()
    if server_name and database_name:
        try:
            connection = pyodbc.connect(
                'DRIVER={SQL Server};' +
                f'Server={server_name};' +
                f'Database={database_name};' +
                'Trusted_Connection=True'
            )
            cursor = connection.cursor()
            cursor.execute("UPDATE user_manager SET Password = ? WHERE Username = ?", (new_hashed_password, username))
            connection.commit()  # Lưu thay đổi
            cursor.close()
            connection.close()
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi", "Cập nhật mật khẩu thất bại!")

def send_email(to_email, new_password):
    # Gửi email với mật khẩu mới
    subject = "Yêu cầu khôi phục mật khẩu"
    body = f"Mật khẩu mới của bạn là: {new_password}"
    
    # Cấu hình thông tin máy chủ email
    smtp_server = "smtp.gmail.com"  # Thay đổi theo máy chủ email của bạn
    smtp_port = 587
    from_email = "ducpctn@gmail.com"  # Thay đổi thành email của bạn
    from_password = "tdfw mesp xbut fdpu"
    # Tạo đối tượng email
    msg = MIMEText(body)
    msg["Subject"] = subject
    # msg["From"] = from_email
    msg["From"] = "Face_recognition_recovery_password <no-reply@facerecognition.com>"
    msg["To"] = to_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, from_password)
            server.sendmail(from_email, to_email, msg.as_string())
    except Exception as e:
        messagebox.showerror("Lỗi", "Gửi email thất bại!")
    

# def center_dialog(dialog):
#     dialog.update_idletasks()  # Cập nhật các tác vụ chờ
#     x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
#     y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
#     dialog.geometry(f"+{x}+{y}")  # Đặt vị trí cửa sổ

def login_success_dialog():
    # Tạo cửa sổ dialog thành công
    login_success_dialog = tk.Toplevel()
    login_success_dialog.title("Thông báo")
    login_success_dialog.geometry("300x200")
    center_dialog(login_success_dialog)
    login_success_dialog.grab_set()
    login_success_dialog.resizable(False, False)
    
    # Thay background
    bg_image = Image.open("bg/att_success_bg.jpg")  # Đường dẫn đến hình ảnh nền
    bg_image = bg_image.resize((300, 200), Image.LANCZOS)  # Thay đổi kích thước hình ảnh
    backgr_photo = ImageTk.PhotoImage(bg_image)
    
    backgr_label = tk.Label(login_success_dialog, image=backgr_photo)
    backgr_label.image = backgr_photo
    backgr_label.place(relwidth=1, relheight=1)
    
    # Icon dialog
    icon_image2 = Image.open("icon/success_icon.png")  # Đường dẫn đến icon mới
    icon = ImageTk.PhotoImage(icon_image2)
    login_success_dialog.iconphoto(False, icon)  # Đặt icon cho dialog
    
    # Frame header chứa icon và dòng chữ "Điểm danh thành công"
    header_frame = tk.Frame(login_success_dialog)
    header_frame.pack(pady=10)
    
    # Tạo icon và giữ tham chiếu để tránh bị xóa
    icon_image = Image.open("icon/success.png")  
    icon_image = icon_image.resize((50, 50), Image.LANCZOS)
    icon = ImageTk.PhotoImage(icon_image)
    icon_label = tk.Label(header_frame, image=icon)
    icon_label.image = icon  # Lưu tham chiếu đến icon
    icon_label.pack(side="left", padx=5)    

    # Thông báo "Điểm danh thành công" nằm ngang hàng với icon
    success_label = tk.Label(header_frame, text="Đăng nhập thành công!", font=("Arial", 14, "bold"))
    success_label.pack(side="left")
    
    # Tạo nút OK
    ok_button = tk.Button(login_success_dialog, text="OK", command=lambda: close_dialog(login_success_dialog), width=10, height=2, bg="green")
    ok_button.pack(pady=10)
    
    # Đặt thời gian tự động đóng dialog sau 4 giây
    login_success_dialog.after(2000, lambda: close_dialog(login_success_dialog))

def fail_login_dialog():
    # Tạo cửa sổ dialog failed
    fail_login_dialog = tk.Toplevel()
    fail_login_dialog.title("Thông báo")
    fail_login_dialog.geometry("300x200")
    center_dialog(fail_login_dialog)
    fail_login_dialog.grab_set()
    fail_login_dialog.resizable(False, False)
    
    # Icon dialog
    icon_image3 = Image.open("icon/failed_icon.png")  # Đường dẫn đến icon mới
    icon2 = ImageTk.PhotoImage(icon_image3)
    fail_login_dialog.iconphoto(False, icon2)  # Đặt icon cho dialog
    
    # Frame header chứa icon và dòng chữ "Điểm danh thất bại"
    header_frame2 = tk.Frame(fail_login_dialog)
    header_frame2.pack(pady=10)
    
    # Tạo icon và giữ tham chiếu để tránh bị xóa
    icon_image = Image.open("icon/failed.png")  
    icon_image = icon_image.resize((50, 50), Image.LANCZOS)
    icon = ImageTk.PhotoImage(icon_image)
    icon_label = tk.Label(header_frame2, image=icon)
    icon_label.image = icon  # Lưu tham chiếu đến icon
    icon_label.pack(side="left", padx=5)

    # Thông báo "Điểm danh thất bại" nằm ngang hàng với icon
    fail_label = tk.Label(header_frame2, text="Đăng nhập thất bại!", font=("Arial", 14, "bold"))
    fail_label.pack(side="left")
    
    # Thêm các dòng thông báo bổ sung
    text1 = tk.Label(fail_login_dialog, text="Vui lòng kiểm tra lại hoặc", font=("Arial", 12))
    text1.pack(pady=5)
    text2 = tk.Label(fail_login_dialog, text="Nhấn quên mật khẩu!", font=("Arial", 12))
    text2.pack(pady=5)
    
    # Nút OK
    ok_button = tk.Button(fail_login_dialog, text="OK", command=lambda: close_dialog(fail_login_dialog), width=12, height=4, bg="red")
    ok_button.pack(pady=7, side="left", padx=20)
    
    # Nút quên mật khẩu
    forgot_pw_button = tk.Button(fail_login_dialog, text="Quên mật khẩu", command=lambda: [close_dialog(fail_login_dialog), forgot_password_dialog()], width=12, height=4, bg="blue")
    forgot_pw_button.pack(side="right", pady=7, padx=20)
    
    # Đặt thời gian tự động đóng dialog sau 4 giây
    fail_login_dialog.after(4000, lambda: close_dialog(fail_login_dialog))



# def login_check():
#     username = username_entry.get()
#     password = password_entry.get()
#     if username == password and username != "":
#         print("Đăng Nhập Thành Công")
#         login_dialog.destroy()
#         # login_success_dialog()
       
#         subprocess.Popen(["python", "admin.py"])
#     else:
#         fail_login_dialog()

# Bạn có thể gọi create_login_dialog() từ một file khác mà không cần gọi lại mainloop()

# Biến toàn cục để lưu userID
userid = 0

def login_check(username, password):
    global userid  # Sử dụng biến toàn cục

    server_name, database_name = load_db_config()

    if server_name and database_name:
        try:
            connection = pyodbc.connect(
                'DRIVER={SQL Server};' +
                f'Server={server_name};' +
                f'Database={database_name};' +
                'Trusted_Connection=True'
            )
            cursor = connection.cursor()

            cursor.execute("""
                SELECT UserID, Password
                FROM user_manager
                WHERE Username = ? AND Role = 'admin'
            """, (username,))
            result = cursor.fetchone()

            if result:  # Nếu tìm thấy username và role là admin
                stored_userid, stored_password = result
                # print(stored_userid)  # Lấy UserID và Password từ kết quả
                try:
                    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                        # Lưu UserID vào biến toàn cục và vào file tạm thời
                        userid = stored_userid
                        with open("userid.txt", "w") as f:
                            f.write(str(userid))  # Lưu userid vào file

                        subprocess.Popen(["python", "admin.py"])  # Mở file admin.py
                        login_dialog.destroy()

                        # Lưu thông tin đăng nhập nếu checkbox "Lưu mật khẩu" được chọn
                        if save_password_var.get():
                            with open("hacked.txt", "w") as f:
                                f.write(f"{username}\n{password}")
                        else:
                            if os.path.exists("hacked.txt"):
                                os.remove("hacked.txt")
                    else:
                        fail_login_dialog()
                except ValueError:
                    fail_login_dialog()

            else:
                fail_login_dialog()

            cursor.close()
            connection.close()

        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi", "Lỗi kiểm tra đăng nhập")

def on_login_button_click():
    username = username_entry.get()
    password = password_entry.get()
    login_check(username, password)

def on_enter_key(event):
    on_login_button_click()
    
