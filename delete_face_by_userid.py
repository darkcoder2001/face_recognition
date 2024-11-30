import pickle

def delete_user_face_data(user_face_id):
    try:
        # Đọc dữ liệu từ file face_data.pkl
        with open("face_data.pkl", "rb") as f:
            face_data = pickle.load(f)
    except (FileNotFoundError, EOFError):
        print("Không tìm thấy file dữ liệu hoặc file rỗng!")
        return

    # Kiểm tra nếu user_face_id tồn tại trong dữ liệu và xóa nó
    if str(user_face_id) in face_data:
        del face_data[str(user_face_id)]  # Xóa userid khỏi dữ liệu
        # Ghi lại dữ liệu sau khi đã xóa vào file face_data.pkl
        with open("face_data.pkl", "wb") as f:
            pickle.dump(face_data, f)
        print(f"Dữ liệu của userid={user_face_id} đã được xóa thành công!")
    else:
        print(f"Không tìm thấy dữ liệu của userid={user_face_id} để xóa.")

if __name__ == "__main__":
    try:
        # Yêu cầu người dùng nhập vào userid cần xóa
        user_face_id = input("Nhập userid cần xóa: ")
        delete_user_face_data(user_face_id)
    except ValueError:
        print("Vui lòng nhập vào một số nguyên hợp lệ cho userid.")
