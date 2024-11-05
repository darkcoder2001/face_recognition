import tkinter as tk
from tkinter import ttk
import datetime
import subprocess
from PIL import Image, ImageTk  # Import thư viện để làm việc với ảnh
from admin_login import create_login_dialog


login_dialog_open = False

def close_dialog(dialog):
    dialog.destroy()
    
def update_time():
    now = datetime.datetime.now()
    time_label.config(text=now.strftime("%H:%M:%S"))
    date_label.config(text=now.strftime("%d/%m/%Y"))
    manager_admin.after(1000, update_time)

def center_dialog(dialog):
    dialog.update_idletasks()  # Cập nhật các tác vụ chờ
    x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
    y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
    dialog.geometry(f"+{x}+{y}")  # Đặt vị trí cửa sổ

def show_user_management():
    # Ẩn menu khác
    attendance_frame.pack_forget()
    catalog_frame.pack_forget()
    user_management_frame.pack(fill='both', expand=True)

def show_attendance_management():
    # Ẩn menu khác
    user_management_frame.pack_forget()
    catalog_frame.pack_forget()
    attendance_frame.pack(fill='both', expand=True)


def show_catalog_management():
    user_management_frame.pack_forget()
    attendance_frame.pack_forget()
    catalog_frame.pack(fill='both', expand=True)


manager_admin = tk.Toplevel()
manager_admin.geometry("1000x800")
manager_admin.title("Quản lý Admin")
manager_admin.grab_set()
manager_admin.resizable(False, False)    
center_dialog(manager_admin)


#doi icon cho frame chinh
icon_image = Image.open('icon_btn/setting.png')  # Thay đổi đường dẫn đến file icon của bạn
icon_image = icon_image.resize((20, 20), Image.LANCZOS)  # Kích thước icon
icon_photo = ImageTk.PhotoImage(icon_image)  # Tạo đối tượng PhotoImage
manager_admin.iconphoto(True, icon_photo)  # Đặt icon cho cửa sổ chính

#def tao icon cho nut
def load_icon(path, size=(30, 30)):  # Kích thước mặc định cho icon
    img = Image.open(path)
    img = img.resize(size, Image.LANCZOS)  # Thay đổi kích thước ảnh
    return ImageTk.PhotoImage(img)

def show_info():
    print("Xem thông tin")  # Hàm xử lý cho "Xem thông tin"

# def logout():
#     print("Đăng xuất")
#     manager_admin.destroy()
#     # manager_admin.destroy()
#     create_login_dialog()
#     # subprocess.Popen(["python", "admin_login.py"])
    
#     # Hàm xử lý cho "Đăng xuất"
#     # 

def logout():
    global login_dialog_open
    print("Đăng xuất")
    manager_admin.destroy()
    if not login_dialog_open:  # Chỉ mở cửa sổ đăng nhập nếu chưa mở
        create_login_dialog()
        login_dialog_open = True  # Đánh dấu rằng cửa sổ đăng nhập đã mở
        subprocess.Popen(["python", "admin_login.py"])
  


# Tạo icon cho các nút
user_manager_icon = load_icon('icon_btn/userbtn.png')  # Thay đổi đường dẫn đến file icon của bạn
att_manager_icon = load_icon('icon_btn/user2btn.png')  # Thay đổi đường dẫn đến file icon của bạn
catalog_icon = load_icon('icon_btn/catabtn.png')  # Thay đổi đường dẫn đến file icon của bạn

#tao icon cho cac nut chuc nang nho khac
add_btn = load_icon('icon_btn/add_btn.png')
edit_btn = load_icon('icon_btn/edit_btn.png')
delete_btn = load_icon('icon_btn/remove_btn.png')   
search_btn = load_icon('icon_btn/search_btn.png')
filter_btn = load_icon('icon_btn/filter_btn.png')
export_btn = load_icon('icon_btn/export_btn.png')
# Header
header_frame = tk.Frame(manager_admin, width=250,bd=20,bg='lightblue')
header_frame.pack(fill='x')

separator = tk.Frame(manager_admin, height=2, bd=1, bg='black')  # Đường kẻ ngang với màu đen
separator.pack(fill='x')

# Thời gian và ngày hiện tại
time_label = tk.Label(header_frame, font=("Arial", 16))
time_label.pack(side="left", padx=50)
date_label = tk.Label(header_frame, font=("Arial", 16))
date_label.pack(side="left", padx=50)
# greeting_label = tk.Label(header_frame, text="Xin chào, ADMIN", font=("Arial", 18))
# greeting_label.pack(side="right", padx=50)

admin_button = tk.Menubutton(header_frame, text="ADMIN", font=("Arial", 18),padx=10,pady=10,width=8,relief="raised", bd=2)
admin_button.menu = tk.Menu(admin_button, tearoff=0)
admin_button['menu'] = admin_button.menu
admin_button.menu.add_command(label="Xem thông tin", command=show_info)
admin_button.menu.add_separator()
admin_button.menu.add_command(label="Đăng xuất", command=logout)
admin_button.pack(side="right", padx=50)



# Menu bên trái
menu_frame = tk.Frame(manager_admin,width=200, bd=20)
menu_frame.pack(side="left", fill='y')

user_management_button = tk.Button(menu_frame, text="Quản lý người dùng", command=show_user_management, height=130, width=200,image=user_manager_icon, compound='left',padx=15)
user_management_button.pack(fill='both',padx=20, pady=(40, 40))

attendance_management_button = tk.Button(menu_frame, text="Quản lý dữ liệu điểm danh", command=show_attendance_management,height=130, width=200,image=att_manager_icon, compound='left',padx=15)
attendance_management_button.pack(fill='both',padx=20, pady=(30, 40))

catalog_button = tk.Button(menu_frame, text="Quản lý vai trò người dùng", command=show_catalog_management,height=130, width=200,image=catalog_icon, compound='left',padx=15)
catalog_button.pack(fill='both',padx=20, pady=(30, 40))

# Khung quản lý người dùng
user_management_frame = tk.Frame(manager_admin, width=1000, height=850)
user_management_frame.pack(fill='both', expand=True)

# Nút chức năng quản lý người dùng
user_function_frame = tk.Frame(user_management_frame)
user_function_frame.pack(side="top", anchor="ne", padx=10, pady=10)

add_button = tk.Button(user_function_frame, text="Thêm",image=add_btn, compound='left',padx=15)
add_button.pack(side="left", padx=20)

edit_button = tk.Button(user_function_frame, text="Sửa",image=edit_btn, compound='left',padx=15)
edit_button.pack(side="left", padx=20)

delete_button = tk.Button(user_function_frame, text="Xóa",image=delete_btn, compound='left',padx=15)
delete_button.pack(side="left", padx=20)

search_button = tk.Button(user_function_frame, text="Tìm kiếm",image=search_btn, compound='left',padx=15)
search_button.pack(side="left", padx=20)

# Cột dữ liệu
columns = ('ID', 'Tên', 'Vai trò', 'Ghi chú')
user_treeview = ttk.Treeview(user_management_frame, columns=columns, show='headings')
for col in columns:
    user_treeview.heading(col, text=col)
user_treeview.column('ID', width=50)  # Độ rộng cho cột ID
user_treeview.column('Tên', width=200)  # Độ rộng cho cột Tên
user_treeview.column('Vai trò', width=100)  # Độ rộng cho cột Vai trò
user_treeview.column('Ghi chú', width=200)  # Độ rộng cho cột Ghi chú
user_treeview.pack(fill='both', expand=True)



# Khung quản lý dữ liệu điểm danh
attendance_frame = tk.Frame(manager_admin, width=1000, height=850)

# Nút chức năng quản lý dữ liệu điểm danh
attendance_function_frame = tk.Frame(attendance_frame)
attendance_function_frame.pack(side="top", anchor="ne", padx=10, pady=10)

filter_button = tk.Button(attendance_function_frame, text="Lọc",image=filter_btn, compound='left',padx=15)
filter_button.pack(side="left", padx=20)

export_button = tk.Button(attendance_function_frame, text="Xuất Excel",image=export_btn, compound='left',padx=15)
export_button.pack(side="left", padx=20)

# Cột dữ liệu
attendance_columns = ('ID', 'Tên', 'Vai trò', 'Ngày', 'Giờ')
attendance_treeview = ttk.Treeview(attendance_frame, columns=attendance_columns, show='headings')
for col in attendance_columns:
    attendance_treeview.heading(col, text=col)
attendance_treeview.column('ID', width=50)  # Độ rộng cho cột ID
attendance_treeview.column('Tên', width=200)  # Độ rộng cho cột Tên
attendance_treeview.column('Vai trò', width=100)  # Độ rộng cho cột Vai trò
attendance_treeview.column('Ngày', width=100)  # Độ rộng cho cột Vai trò
attendance_treeview.column('Giờ', width=200)  # Độ rộng cho cột Ghi chú
attendance_treeview.pack(fill='both', expand=True)

# Khung danh muc
catalog_frame = tk.Frame(manager_admin, width=1000, height=850)

# Nút chức năng danh muc
catalog_function_frame = tk.Frame(catalog_frame)
catalog_function_frame.pack(side="top", anchor="ne", padx=10, pady=10)

filter_button = tk.Button(catalog_function_frame, text="Thêm",image=add_btn, compound='left',padx=15)
filter_button.pack(side="left", padx=20)

export_button = tk.Button(catalog_function_frame, text="Sửa",image=edit_btn, compound='left',padx=15)
export_button.pack(side="left", padx=20)

export_button = tk.Button(catalog_function_frame, text="Xoá",image=delete_btn, compound='left',padx=15)
export_button.pack(side="left", padx=20)

export_button = tk.Button(catalog_function_frame, text="Tìm kiếm",image=search_btn, compound='left',padx=15)
export_button.pack(side="left", padx=20)

# Cột dữ liệu danh muc
catalog_columns = ('STT','Vai trò','Thời gian làm việc')
catalog_treeview = ttk.Treeview(catalog_frame, columns=catalog_columns, show='headings')
for col in catalog_columns:
    catalog_treeview.heading(col, text=col)
catalog_treeview.column('STT', width=50)  # Độ rộng cho cột Vai trò
catalog_treeview.column('Vai trò', width=100)  # Độ rộng cho cột Vai trò
catalog_treeview.column('Thời gian làm việc', width=100)  # Độ rộng cho cột Vai trò
catalog_treeview.pack(fill='both', expand=True)

# Cập nhật thời gian
update_time()

manager_admin.mainloop()
