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

            # Kiểm tra xem đã có thông tin nhận diện trước đó chưa
            if recognized_user and recognized_user["similarity"] > 0.65:
                # Sử dụng thông tin từ recognized_user
                user_id = recognized_user["userid"]
                name = recognized_user["name"]
                job_position = None

                # Lấy thông tin từ bảng user_manager
                sql_query = """
                SELECT job_position
                FROM user_manager
                WHERE UserID = ?
                """
                cursor.execute(sql_query, (user_id,))
                result = cursor.fetchone()

                if result:
                    job_position = result[0]
            else:
                # Nhận diện lại nếu thông tin tạm thời không khả dụng hoặc không đủ độ tin cậy
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

                    # Kiểm tra độ tin cậy, nếu trên 70% thì lấy thông tin từ cơ sở dữ liệu
                    if highest_similarity > 0.65:
                        # Lấy thông tin name và job_position từ bảng user_manager
                        sql_query = """
                        SELECT name, job_position
                        FROM user_manager
                        WHERE UserID = ? 
                        """
                        cursor.execute(sql_query, (user_id,))
                        result = cursor.fetchone()

                        if result:
                            name = result[0]  # Tên người dùng
                            job_position = result[1]  # Chức vụ người dùng
                        else:
                            pass
                    else:
                        print("Khuôn mặt chưa đăng ký hoặc độ tin cậy không đủ.")

            # Thiết lập các giá trị cho điểm danh
            attention_date = datetime.now()  # Ngày hiện tại
            checkin_time = datetime.now()  # Thời gian check-in
            checkout_time = checkin_time + timedelta(minutes=5)  # Thời gian check-out
            status = "Muon"  # Trạng thái

            # Câu lệnh SQL để thêm bản ghi mới vào bảng attention_manager
            sql_insert = """
            INSERT INTO attention_manager (UserID, Name, job_position, AttentionDate, CheckInTime, CheckOutTime, Status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """

            # Thực thi câu lệnh để thêm dữ liệu vào bảng
            cursor.execute(sql_insert, (user_id, name, job_position, attention_date, checkin_time, checkout_time, status))

            # Lưu thay đổi
            connection.commit()
            attention_success(user_id)
            print(f"user_id: {user_id}")
            print(f"attention_date: {attention_date}")
            print(f"checkin_time: {checkin_time}")
            print(f"checkout_time: {checkout_time}")
            print(f"status: {status}")
            cursor.close()
            connection.close()

        except Exception as ex:
            # Xử lý lỗi và hiển thị thông báo
            attention_fail()
            print("Đã xảy ra lỗi khi điểm danh:", ex)
            return  # Dừng lại nếu có lỗi xảy ra
