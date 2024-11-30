import tkinter as tk
from PIL import Image, ImageTk
import pygame 
import pyodbc
from tkinter import messagebox

def close_dialog(dialog):
    dialog.destroy()

def load_db_config():  # sourcery skip: use-contextlib-suppress
    try:
        with open("db_config.txt", "r") as config_file:
            lines = config_file.readlines()
            if len(lines) >= 2:
                return lines[0].strip(), lines[1].strip()
    except FileNotFoundError:
        pass
    return None, None

def center_dialog(dialog):
    dialog.update_idletasks()  # Cập nhật các tác vụ chờ
    x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
    y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
    dialog.geometry(f"+{x}+{y}")  # Đặt vị trí cửa sổ

def show_success_dialog(parent, current_time, name, job_position):
    pygame.mixer.init()
    pygame.mixer.music.load("voice/succefully.mp3")
    pygame.mixer.music.play()

    success_dialog = tk.Toplevel(parent)
    success_dialog.title("Thông báo")
    success_dialog.geometry("300x200")
    center_dialog(success_dialog)
    success_dialog.grab_set()
    success_dialog.resizable(False, False)

    # Thay đổi background
    # bg_image = Image.open("bg/att_success_bg.jpg")
    # bg_image = bg_image.resize((300, 200), Image.LANCZOS)
    # backgr_photo = ImageTk.PhotoImage(bg_image)

    # backgr_label = tk.Label(success_dialog, image=backgr_photo)
    # backgr_label.image = backgr_photo
    # backgr_label.place(relwidth=1, relheight=1)

    # Icon cho dialog
    icon_image2 = Image.open("icon/success_icon.png")
    icon = ImageTk.PhotoImage(icon_image2)
    success_dialog.iconphoto(False, icon)

    # Frame header
    header_frame = tk.Frame(success_dialog)
    header_frame.pack(pady=10)

    # Icon
    icon_image = Image.open("icon/success.png")
    icon_image = icon_image.resize((50, 50), Image.LANCZOS)
    icon = ImageTk.PhotoImage(icon_image)
    icon_label = tk.Label(header_frame, image=icon)
    icon_label.image = icon
    icon_label.pack(side="left", padx=5)

    # Thông báo
    success_label = tk.Label(header_frame, text="Điểm danh thành công!", font=("Arial", 14, "bold"))
    success_label.pack(side="left")

    text1 = tk.Label(success_dialog, text=f"Ho tên: {name}", font=("Arial", 12))
    text1.pack(anchor="w", padx=20)

    text2 = tk.Label(success_dialog, text=f"Vai trò: {job_position}", font=("Arial", 12))
    text2.pack(anchor="w", padx=20)

    text3 = tk.Label(success_dialog, text=f"Thời gian: {current_time}", font=("Arial", 12))
    text3.pack(anchor="w", padx=20)

    # Nút OK
    ok_button = tk.Button(success_dialog, text="OK", command=lambda: close_dialog(success_dialog), width=10, height=2, bg="green")
    ok_button.pack(pady=10)

    success_dialog.after(3500, lambda: close_dialog(success_dialog))


def show_fail_dialog(parent):
    pygame.mixer.init()
    pygame.mixer.music.load("voice/fail.mp3")  # Thay đổi đường dẫn đến file âm thanh
    pygame.mixer.music.play()
    # Tạo cửa sổ dialog failed
    fail_dialog = tk.Toplevel(parent)
    fail_dialog.title("Thong bao")
    fail_dialog.geometry("300x200")
    center_dialog(fail_dialog)
    
    
    #thay bg for diaglog fail
    # bg2_image = Image.open("bg/att_failed_bg.jpg")  # Đường dẫn đến hình ảnh nền
    # bg2_image = bg2_image.resize((300, 200), Image.LANCZOS)  # Thay đổi kích thước hình ảnh
    # backgr2_photo = ImageTk.PhotoImage(bg2_image)
    
    # backgr_label = tk.Label(fail_dialog, image=backgr2_photo)
    # backgr_label.image = backgr2_photo
    # backgr_label.place(relwidth=1, relheight=1)
    
    
    fail_dialog.grab_set()
    fail_dialog.resizable(False, False)
    
    #thay bg success

    
    #icon_dialog
    icon_image3 = Image.open("icon/failed_icon.png")  # Đường dẫn đến icon mới
    icon2 = ImageTk.PhotoImage(icon_image3)
    fail_dialog.iconphoto(False, icon2)  # Đặt icon cho dialog
    
    # frame_header chứa icon và dòng chữ "Điểm danh thành công" ngang hàng
    header_frame2 = tk.Frame(fail_dialog)
    header_frame2.pack(pady=10)
    
    # Tạo icon và giữ tham chiếu để tránh bị xóa
    icon_image = Image.open("icon/failed.png")  
    icon_image = icon_image.resize((50, 50), Image.LANCZOS)
    icon = ImageTk.PhotoImage(icon_image)
    icon_label = tk.Label(header_frame2, image=icon)
    icon_label.image = icon  # Lưu tham chiếu đến icon
    icon_label.pack(side="left", padx=5)

    # Thông báo "Điểm danh thành công" nằm ngang hàng với icon
    fail_label = tk.Label(header_frame2, text="Diem danh that bai!", font=("Arial", 14, "bold"))
    fail_label.pack(side="left")
    
    # Thêm các dòng thông báo bổ sung
    text1 = tk.Label(fail_dialog, text="Vui long diem danh lai hoac", font=("Arial", 12))
    text1.pack(pady=5)
    text2 = tk.Label(fail_dialog, text="lien he quan tri vien!", font=("Arial", 12))
    text2.pack(pady=5)
    # text3 = tk.Label(fail_dialog, text=f"Thoi gian:", font=("Arial", 12))
    # text3.pack(anchor="w", padx=20)
    
    # Tạo nút OK
    ok_button = tk.Button(fail_dialog, text="OK", command=lambda: close_dialog(fail_dialog), width=10, height=2, bg="red")
    ok_button.pack(pady=10)
    
    # Đặt thời gian tự động đóng dialog sau 4 giây
    fail_dialog.after(4000, lambda: close_dialog(fail_dialog))
