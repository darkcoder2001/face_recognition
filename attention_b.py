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