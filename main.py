import tkinter as tk
from time import strftime, time
# from PIL import ImageTk

from attention import show_success_dialog, show_fail_dialog
from admin_login import create_login_dialog
import pyodbc
from datetime import datetime, timedelta
from tkinter import messagebox
import threading
# from insightface import model_zoo
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image, ImageDraw, ImageFont,ImageTk
import cv2
from insightface.app import FaceAnalysis
import pickle
import os
import sys
import warnings
import numpy as np
warnings.simplefilter("ignore", FutureWarning)

recognized_user = None

def admin_login():
    stop_camera()
    create_login_dialog()

    
def close_window():
    # Đóng cửa sổ
    root.destroy()

def get_current_time():
    return datetime.now().strftime("%H:%M:%S")

def load_icon(path, size=(30, 30)):  # Kích thước mặc định cho icon
    img = Image.open(path)
    img = img.resize(size, Image.Resampling.LANCZOS)  # Thay đổi kích thước ảnh
    return ImageTk.PhotoImage(img)


#define_attention_success
def attention_success(user_id):
    # Lấy thông tin người dùng từ database
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

            # Truy vấn để lấy tên và vị trí công việc từ bảng user_manager
            sql_select = "SELECT Name, job_position FROM user_manager WHERE UserID = ?"
            cursor.execute(sql_select, (user_id,))
            result = cursor.fetchone()

            if result:
                name = result[0]
                job_position = result[1]
            else:
                name = "Không tìm thấy"
                job_position = "Không xác định"

            # Hiển thị thông báo thành công
            current_time = strftime('%H:%M:%S %p')
            show_success_dialog(root, current_time, name, job_position)

        except Exception as ex:
            print("Lỗi khi truy vấn dữ liệu:", ex)

        finally:
            cursor.close()
            connection.close()
    
#define_attention_fail
def attention_fail():
    show_fail_dialog(root)

#dong chuong trinh


#can giua
def center_window(window):
    window.update_idletasks()  # Cập nhật các tác vụ chờ
    x = (window.winfo_screenwidth() // 2) - (window.winfo_width() // 2)
    y = (window.winfo_screenheight() // 2) - (window.winfo_height() // 2)
    window.geometry(f"+{x}+{y}")  # Đặt vị trí cửa sổ


# Bien toan cuc de luu thoi gian truoc do
last_time = time()

# Ham cap nhat thoi gian, ngay va FPS
def update_time():
    global last_time
    current_time = strftime('%H:%M:%S %p')  # Lay gio hien tai
    current_date = strftime('%d-%m-%Y')     # Lay ngay hien tai

    # # Tinh FPS
    # current_frame_time = time()
    # delta_time = current_frame_time - last_time
    # fps = 1 / delta_time if delta_time > 0 else 0
    # last_time = current_frame_time
    
    # Cap nhat cac nhan
    label_time.config(text=current_time)
    label_date.config(text=current_date)
    # label_fps.config(text=f"FPS: {fps:.2f}")
    
    # Cap nhat sau moi 1000ms (1 giay)
    label_time.after(1000, update_time)

# Tao cua so chinh
root = tk.Tk()
root.title("PHAN MEM DIEM DANH BANG KHUON MAT")
root.geometry("1000x800")
center_window(root)
root.resizable(False, False)

background_image = Image.open("bg/background.jpg")  # Đường dẫn đến hình ảnh JPEG
background_image = background_image.resize((1000, 800), Image.Resampling.LANCZOS)  # Thay đổi kích thước hình ảnh
background_photo = ImageTk.PhotoImage(background_image)


#icon_dialog_main
# icon_image2 = Image.open("icon/face_icon.png")  # Đường dẫn đến icon mới
icon_image2 = Image.open("logo/hau3.png") 
icon = ImageTk.PhotoImage(icon_image2)
root.iconphoto(False, icon)  # Đặt icon cho dialog

# Tạo nhãn để hiển thị hình ảnh nền
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

#frame_fps

# fps_frame = tk.Frame(root, bd=5, bg="blue")  # Khung với viền
# fps_frame.grid(row=0, column=0, padx=35, pady=10, sticky='w')


#frame time
time_frame = tk.Frame(root, bg="lightgray", bd=5, relief="sunken")  # Tạo khung với viền
time_frame.place(x=700, y=60, width=260, height=200)  # Đặt khung tại vị trí 


#frame_btn_adminlogin
button_frame = tk.Frame(root)
button_frame.place(x=700, y=285, width=260, height=230)

#icon_btn_adminlogin
icon_image = Image.open("icon/admin.png") 
icon_image = icon_image.resize((50, 50), Image.Resampling.LANCZOS)  # Thay đổi kích thước biểu tượng nếu cần
icon = ImageTk.PhotoImage(icon_image)

#tao nut adminlogin
admin_button = tk.Button(button_frame, text="ADMIN ĐĂNG NHẬP", image=icon, compound=tk.LEFT, command=admin_login,font=('calibri', 16), padx=10 )
admin_button.pack(expand=True, fill=tk.BOTH)


#frame_btn_attention
button2_frame = tk.Frame(root)
button2_frame.place(x=700, y=540, width=260, height=230)


#icon_btn_attention
icon2_image = Image.open("icon/face.png") 
icon2_image = icon2_image.resize((60, 60), Image.Resampling.LANCZOS)  # Thay đổi kích thước biểu tượng nếu cần
icon2 = ImageTk.PhotoImage(icon2_image)




# label_fps = tk.Label(fps_frame, font=('calibri', 20), background='blue', foreground='yellow')
# label_fps.pack(padx=5, pady=5)


# Tao nhan de hien thi gio
label_time = tk.Label(time_frame, font=('calibri',30, 'bold'), background='lightgray', foreground='black')
#label_time.pack(expand=True)

label_time.grid(row=0, column=0, padx=(20,20), pady=(40,10),sticky='nsew')  # Dat gio o hang 1, cot 0, duong dan sang trai

# Tao nhan de hien thi ngay
label_date = tk.Label(time_frame, font=('calibri', 25), background='lightgray', foreground='black')
#label_time.pack(expand=True)

label_date.grid(row=1, column=0, padx=(10,10), pady=(10,30),sticky='nsew')  # Dat ngay o hang 2, cot 0, duong dan sang trai

# Goi ham cap nhat thoi gian, ngay va FPS
update_time()

def load_db_config():  # sourcery skip: use-contextlib-suppress
    try:
        with open("db_config.txt", "r") as config_file:
            lines = config_file.readlines()
            if len(lines) >= 2:
                return lines[0].strip(), lines[1].strip()
    except FileNotFoundError:
        pass
    return None, None

# def attention():
#     # Kiểm tra xem camera có đang bật không
#     if not camera_active:  # Giả sử bạn có biến camera_active để kiểm tra trạng thái camera
#         messagebox.showerror("Lỗi", "Camera chưa được bật, vui lòng bật camera và thử lại.")
#         return  # Dừng lại nếu camera chưa bật

#     # Kết nối đến cơ sở dữ liệu SQL Server
#     server_name, database_name = load_db_config()
#     if server_name and database_name:
#         try:
#             connection = pyodbc.connect(
#                 'DRIVER={SQL Server};' +
#                 f'Server={server_name};' +
#                 f'Database={database_name};' +
#                 'Trusted_Connection=True'
#             )
#             cursor = connection.cursor()

#             # Lấy khuôn mặt từ camera và so sánh với dữ liệu đã lưu
#             # Giả sử bạn có hàm detect_face và face_data chứa dữ liệu khuôn mặt đã đăng ký
#             face_embedding, _ = detect_face(frame)

#             if face_embedding is not None:
#                 highest_similarity = 0
#                 name = "Không rõ"
#                 user_id = None
#                 job_position = None

#                 # So sánh với các khuôn mặt đã đăng ký
#                 for stored_name, stored_data in face_data.items():
#                     stored_embedding = np.array(stored_data['embedding'])
                    
#                     # Sử dụng cosine_similarity từ sklearn để tính similarity
#                     similarity = cosine_similarity([face_embedding], [stored_embedding])[0][0]

#                     if similarity > highest_similarity:
#                         highest_similarity = similarity
#                         name = stored_name
#                         user_id = stored_data['userid']

#                 # Kiểm tra độ tin cậy, nếu trên 70% thì lấy thông tin từ cơ sở dữ liệu
#                 if highest_similarity > 0.65:
#                     # Lấy thông tin name và job_position từ bảng user_manager
#                     sql_query = """
#                     SELECT name, job_position
#                     FROM user_manager
#                     WHERE UserID = ? 
#                     """
#                     cursor.execute(sql_query, (user_id,))
#                     result = cursor.fetchone()

#                     if result:
#                         name = result[0]  # Tên người dùng
#                         job_position = result[1]  # Chức vụ người dùng
#                     else:
#                         pass
#                 else:
#                     print("Khuôn mặt chưa đăng ký hoặc độ tin cậy không đủ.")

#             # Thiết lập các giá trị cho điểm danh
#             attention_date = datetime.now()  # Ngày hiện tại
#             checkin_time = datetime.now()  # Thời gian check-in
#             checkout_time = checkin_time + timedelta(minutes=5)  # Thời gian check-out
#             status = "Muon"  # Trạng thái

#             # Câu lệnh SQL để thêm bản ghi mới vào bảng attention_manager
#             sql_insert = """
#             INSERT INTO attention_manager (UserID, Name, job_position, AttentionDate, CheckInTime, CheckOutTime, Status)
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#             """

#             # Thực thi câu lệnh để thêm dữ liệu vào bảng
#             cursor.execute(sql_insert, (user_id, name, job_position, attention_date, checkin_time, checkout_time, status))

#             # Lưu thay đổi
#             connection.commit()
#             attention_success(user_id)
#             cursor.close()
#             connection.close()

#         except Exception as ex:
#             # Xử lý lỗi và hiển thị thông báo
#             attention_fail()
#             print("Đã xảy ra lỗi khi điểm danh:", ex)
#             return  # Dừng lại nếu có lỗi xảy ra


from datetime import datetime

def attention():
    global recognized_user  # Biến lưu thông tin nhận diện tạm thời

    # Kiểm tra xem camera có đang bật không
    if not camera_active:  # Giả sử bạn có biến camera_active để kiểm tra trạng thái camera
        messagebox.showerror("Lỗi", "Camera chưa được bật, vui lòng bật camera và thử lại.")
        return  # Dừng lại nếu camera chưa bật
    if recognized_user is None:
        messagebox.showinfo("Thông báo", "Khuôn mặt chưa đăng ký hoặc \nKhông phát hiện bất kì khuôn mặt nào!")
        return  # Dừng lại nếu không phát hiện khuôn mặt

    # Kết nối đến cơ sở dữ liệu SQL Server
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

            # Kiểm tra thông tin nhận diện
            if recognized_user and recognized_user["similarity"] > 0.65:
                user_id = recognized_user["userid"]
                name = recognized_user["name"]

                # Lấy thông tin từ bảng user_manager
                sql_query = """
                SELECT job_position
                FROM user_manager
                WHERE UserID = ?
                """
                cursor.execute(sql_query, (user_id,))
                result = cursor.fetchone()
                job_position = result[0] if result else None


                # Thiết lập ngày hiện tại
                attention_date = datetime.now().date().strftime('%Y-%m-%d')
                current_time = datetime.now()

                # Kiểm tra tất cả bản ghi của ngày hôm nay
                sql_check = """
                SELECT AttentionID, CheckInTime, CheckOutTime
                FROM attention_manager
                WHERE UserID = ? AND AttentionDate = ?
                """
                cursor.execute(sql_check, (user_id, attention_date))
                records = cursor.fetchall()  # Lấy tất cả bản ghi của người dùng trong ngày

                if not records:
                    # Nếu không có bản ghi trong ngày, tạo mới
                    sql_insert = """
                    INSERT INTO attention_manager (UserID, Name, job_position, AttentionDate, CheckInTime, CheckOutTime, Status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """
                    cursor.execute(sql_insert, (user_id, name, job_position, attention_date, current_time, None, "Muon"))
                    print("create")
                    connection.commit()
                else:
                    # Nếu có ít nhất một bản ghi, kiểm tra và cập nhật
                    for record in records:
                        attention_id, checkin_time, checkout_time = record
                        # print(f"CheckOutTime: {checkout_time}")

                        if checkin_time and checkout_time is None:
                            print("update")
                            # Cập nhật CheckOutTime nếu đã có CheckInTime và chưa có CheckOutTime
                            sql_update = """
                            UPDATE attention_manager
                            SET CheckOutTime = ?
                            WHERE AttentionID = ? 
                            """
                            # AND CheckOutTime IS NULL
                            cursor.execute(sql_update, (current_time, attention_id))
                            connection.commit()
                            break

                        elif checkin_time and checkout_time:
                            print("create2")
                            # Nếu đã có cả CheckInTime và CheckOutTime, thêm bản ghi mới (nếu cần)
                            sql_insert = """
                            INSERT INTO attention_manager (UserID, Name, job_position, AttentionDate, CheckInTime, CheckOutTime, Status)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            """
                            cursor.execute(sql_insert, (user_id, name, job_position, attention_date, current_time, None, "Muon"))
                            connection.commit()
                            break

                # Lưu thay đổi
                # connection.commit()
                attention_success(user_id)
            else:
                # Nếu nhận diện không thành công, xử lý lại nhận diện
                face_embedding, _ = detect_face(frame)

                if face_embedding is not None:
                    highest_similarity = 0
                    name = "Không rõ danh tính"
                    user_id = None
                    job_position = None

                    # So sánh với các khuôn mặt đã đăng ký
                    for stored_name, stored_data in face_data.items():
                        stored_embedding = np.array(stored_data['embedding'])

                        # Sử dụng cosine_similarity từ sklearn để tính similarity
                        similarity = cosine_similarity([face_embedding], [stored_embedding])[0][0]

                        if similarity > highest_similarity:
                            highest_similarity = similarity
                            name = stored_name
                            user_id = stored_data['userid']

                    if highest_similarity > 0.65:
                        sql_query = """
                        SELECT name, job_position
                        FROM user_manager
                        WHERE UserID = ? 
                        """
                        cursor.execute(sql_query, (user_id,))
                        result = cursor.fetchone()

                        if result:
                            name = result[0]
                            job_position = result[1]
                    else:
                        print("Khuôn mặt chưa đăng ký hoặc độ tin cậy không đủ.")

            cursor.close()
            connection.close()

        except Exception as ex:
            attention_fail()
            print("Đã xảy ra lỗi khi điểm danh:", ex)
            return


#tao nut attention

# att_button = tk.Button(button2_frame, text="ĐIỂM DANH", image=icon2, compound=tk.LEFT, command=lambda:(attention(),attention_success()),font=('calibri', 30), padx=10 )
att_button = tk.Button(button2_frame, text="ĐIỂM DANH", image=icon2, compound=tk.LEFT, command=attention,font=('calibri', 25), padx=10 )
# att_button = tk.Button(button2_frame, text="ĐIỂM DANH", image=icon2, compound=tk.LEFT, command=lambda: random_dialog(root, get_current_time()),font=('calibri', 30), padx=10 )
# att_button.pack(expand=True, pady=20)
att_button.pack(expand=True, fill=tk.BOTH)

#camera

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

insightface_path = os.path.join(os.getcwd(), 'insightface')  
if insightface_path not in sys.path:
    sys.path.append(insightface_path)
    
face_recognition_app = FaceAnalysis()
face_recognition_app.prepare(ctx_id=0)

default_background = Image.open("bg/waiting.jpg")
default_background = default_background.resize((640, 640))
default_img = ImageTk.PhotoImage(default_background)

camera_frame = tk.Label(root, image=default_img, anchor="n")
camera_frame.place(x=35, y=60, width=640, height=640)
camera_frame.imgtk = default_img  # Giữ tham chiếu đến ảnh

# Biến lưu trạng thái camera
cap = None
camera_active = False
frame = None  # Lưu frame hiện tại từ camera
face_data = {}  # Dữ liệu khuôn mặt đã lưu (tên và embedding)

# Tải dữ liệu khuôn mặt từ file 'face_data.pkl' nếu tồn tại
def load_face_data():
    global face_data
    if os.path.exists("face_data.pkl"):
        try:
            with open("face_data.pkl", "rb") as f:
                face_data = pickle.load(f)
        except EOFError:
            # Nếu file trống, khởi tạo face_data là dictionary trống
            print("File face_data.pkl trống, khởi tạo dữ liệu mới.")
            face_data = {}
    else:
        # Nếu file không tồn tại, khởi tạo face_data là dictionary trống
        print("Không tìm thấy file face_data.pkl, khởi tạo dữ liệu mới.")
        face_data = {}

# Lưu dữ liệu khuôn mặt vào file 'face_data.pkl'
def save_face_data():
    with open('face_data.pkl', 'wb') as f:
        pickle.dump(face_data, f)


# def detect_face(frame):
#     global face_recognition_app
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
#     # Phát hiện khuôn mặt sử dụng Haar Cascade
#     faces = face_cascade.detectMultiScale(gray, 1.1, 4)

#     if len(faces) > 0:
#         for (x, y, w, h) in faces:
#             # Vẽ khung vuông quanh khuôn mặt
#             cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
#         # Lấy đặc trưng khuôn mặt
#         face_embedding = face_recognition_app.get(frame)
#         if len(face_embedding) > 0:
#             return face_embedding[0].embedding, faces
#     return None, None

def detect_face(frame):

    # Chuyển hình ảnh từ BGR sang RGB vì InsightFace yêu cầu
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Phát hiện khuôn mặt
    faces = face_recognition_app.get(img_rgb)

    if len(faces) > 0:
        for face in faces:
            # Lấy bounding box
            box = face.bbox.astype(int)
            
            # Vẽ khung vuông quanh khuôn mặt
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 2)
            
            # Trích xuất embedding của khuôn mặt
            embedding = face.embedding  # Vector đặc trưng khuôn mặt
            return embedding, faces  # Trả về embedding và thông tin khuôn mặt
    
    return None, None


def start_camera():
    global cap, camera_active
    # Kiểm tra nếu camera đã bật
    if camera_active:
        messagebox.showinfo("Thông báo", "Camera đang bật!")
        return

    # Hiển thị thông báo ngay lập tức
    dialog = tk.Toplevel(root)
    dialog.title("Thông báo")
    dialog.geometry("300x150")
    message = tk.Label(dialog, text="Camera đang khởi động, vui lòng chờ từ 5-10s")
    message.pack(pady=20)
    center_window(dialog)
    ok_button = tk.Button(dialog, text="OK", command=dialog.destroy,width=10)
    ok_button.pack(pady=10)
    
    # Đóng dialog sau 2 giây nếu không bấm OK
    dialog.after(2000, dialog.destroy)
    threading.Thread(target=open_camera_thread, daemon=True).start()

    # Khởi động camera
def open_camera_thread():
    global cap, camera_active
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Lỗi", "Không tìm thấy camera! Vui lòng kiểm tra lại!")
        return

    camera_active = True
    update_camera()


# Cập nhật khung hình camera
# def update_camera():
#     global cap, camera_active, frame
#     if camera_active:
#         ret, frame = cap.read()
#         if not ret:
#             messagebox.showerror("Lỗi", "Không thể đọc từ camera!")
#             stop_camera()
#             return
#         frame = cv2.flip(frame, 1)
#         frame = cv2.resize(frame, (640, 640))

#         # Gọi hàm nhận diện khuôn mặt
#         face_embedding, faces = detect_face(frame)
#         if face_embedding is not None:
#             name = "Unknown"
#             userid = None
#             highest_similarity = 0

#             # Tính cosine similarity và tìm mức độ tương đồng cao nhất
#             for stored_name, stored_data in face_data.items():
#                 stored_embedding = np.array(stored_data['embedding'])
#                 similarity = cosine_similarity([face_embedding], [stored_embedding])[0][0]  # cosine similarity
#                 # print(similarity)
#                 if similarity > highest_similarity:
#                     highest_similarity = similarity
#                     name = stored_data['name']
#                     userid = stored_data['userid']

#             # Kiểm tra ngưỡng nhận diện
#             if highest_similarity > 0.65:
#                 display_text = f"Xin chào, {name}!!"
#             else:
#                 display_text = "Khuôn mặt chưa được đăng ký!"

#         else:
#             display_text = "Không tìm thấy khuôn mặt nào!"

#         # Chuyển đổi khung hình `frame` sang đối tượng `PIL` để vẽ chuỗi tiếng Việt
#         pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
#         draw = ImageDraw.Draw(pil_image)

#         # Tạo font Unicode cho tiếng Việt (có thể điều chỉnh kích thước và font)
#         try:
#             font = ImageFont.truetype("arial.ttf", 24)
#         except IOError:
#             font = ImageFont.load_default()

#         # Vẽ chuỗi tiếng Việt lên hình ảnh
#         draw.text((10, 30), display_text, font=font, fill=(255, 255, 255))

#         # Chuyển đổi lại hình ảnh sang `frame` của OpenCV
#         frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

#         # Hiển thị hình ảnh lên giao diện Tkinter
#         img = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
#         camera_frame.imgtk = img
#         camera_frame.config(image=img)

#         # Gọi lại hàm update_camera sau 5ms
#         camera_frame.after(5, update_camera)

def update_camera():
    global cap, camera_active, frame, recognized_user
    if camera_active:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Lỗi", "Không thể đọc từ camera!")
            stop_camera()
            return
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (640, 640))

        # Nhận diện khuôn mặt
        face_embedding, faces = detect_face(frame)
        recognized_user = None  # Reset thông tin nhận diện mỗi lần cập nhật

        if faces is None or len(faces) == 0:
            # Nếu không phát hiện khuôn mặt nào
            display_text = "Không tìm thấy khuôn mặt nào!"
        else:
            # Nếu phát hiện khuôn mặt
            if face_embedding is not None:
                highest_similarity = 0
                user_info = {"userid": None, "name": "Unknown", "similarity": 0}
                for stored_name, stored_data in face_data.items():
                    stored_embedding = np.array(stored_data['embedding'])
                    similarity = cosine_similarity([face_embedding], [stored_embedding])[0][0]
                    if similarity > highest_similarity:
                        highest_similarity = similarity
                        user_info = {
                            "userid": stored_data["userid"],
                            "name": stored_data["name"],
                            "similarity": similarity
                        }

                # Cập nhật thông tin nhận diện nếu độ tương đồng vượt ngưỡng
                if highest_similarity > 0.65:
                    recognized_user = user_info
                    display_text = f"Xin chào, {recognized_user['name']}!"
                else:
                    recognized_user = None
                    display_text = "Khuôn mặt chưa đăng ký!"  # Nếu không tìm thấy người đã đăng ký

        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except IOError:
            font = ImageFont.load_default()
        draw.text((10, 30), display_text, font=font, fill=(255, 255, 255))
        frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        # Hiển thị khung hình trên giao diện
        img = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        camera_frame.imgtk = img
        camera_frame.config(image=img)

        # Gọi lại hàm update_camera sau 5ms
        camera_frame.after(5, update_camera)

def stop_camera():
    global cap, camera_active
    if cap is not None:
        cap.release()
    camera_active = False
    camera_frame.config(image=default_img)

def show_help():
    help_message = "Nếu bạn cần trợ giúp, liên hệ với chúng tôi!\nMr. Đức\nSĐT: 01234896811\nEmail: ducpctn@gmail.com"
    messagebox.showinfo("Trợ giúp", help_message)

start_attention_btn = load_icon('icon_btn/start.png')
stop_attention_btn = load_icon('icon_btn/stop.png')
help_btn = load_icon('icon_btn/help.png')


button_frame = tk.Frame(root, bg="lightblue")
button_frame.place(x=35, y=700, width=640, height=70)

camera_button = tk.Button(button_frame, text="Bắt đầu điểm danh", command=start_camera,image=start_attention_btn, font=("Arial", 12),compound="left",padx=10)
camera_button.grid(row=0, column=0, padx=(25,20), pady=20)

stop_button = tk.Button(button_frame, text="Dừng điểm danh", command=stop_camera,image=stop_attention_btn, font=("Arial", 12),compound="left",padx=10)
stop_button.grid(row=0, column=1, padx=20, pady=20)

help_button = tk.Button(button_frame, text="Trợ giúp", command=show_help,image=help_btn, font=("Arial", 12),compound="left",padx=10)
help_button.grid(row=0, column=2, padx=20, pady=20)

def on_closing():
    stop_camera()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
load_face_data()
root.mainloop()


# Bat dau vong lap su kien
# root.mainloop()
# cap.release()
# cv2.destroyAllWindows()