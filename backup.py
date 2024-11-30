def fetch_report_data(time_period, selected_time, selected_job, selected_user):
    server_name, database_name = load_db_config()
    if not server_name or not database_name:
        messagebox.showerror("Lỗi cấu hình", "Kiểm tra lại servername hoặc database!")
        return {}

    try:
        connection = pyodbc.connect(
            f"DRIVER={{SQL Server}};Server={server_name};Database={database_name};Trusted_Connection=True"
        )
        cursor = connection.cursor()

        data = {}

        # Xử lý các tham số chọn công việc và người dùng
        query = "SELECT COUNT(*) FROM attention_manager WHERE status = 'Muon'"
        params = []

        # Thêm điều kiện job_position nếu không chọn "Tất cả"
        if selected_job != "Tất cả":
            query += " AND job_position = ?"
            params.append(selected_job)

        # Thêm điều kiện name nếu không chọn "Tất cả"
        if selected_user != "Tất cả":
            query += " AND name = ?"
            params.append(selected_user)

        # Xử lý ngày, tuần hoặc tháng
        if time_period == "Ngày":
            selected_date = arrow.get(selected_time, "DD/MM/YYYY")
            for i in range(7):
                current_date = selected_date.shift(days=-i).format("YYYY-MM-DD")
                cursor.execute(query + " AND AttentionDate = ?", params + [current_date])
                count = cursor.fetchone()[0]
                data[current_date] = count

        elif time_period == "Tuần":
            selected_date = arrow.get(selected_time, "DD/MM/YYYY")
            week_number = selected_date.isocalendar()[1]
            for i in range(5):
                current_week_number = week_number - i
                if current_week_number < 1:
                    current_week_number = 52 + current_week_number
                data[f"Tuần {current_week_number}"] = 0
                start_of_week = selected_date.shift(weeks=-i).floor('week').format("YYYY-MM-DD")
                end_of_week = selected_date.shift(weeks=-i).ceil('week').format("YYYY-MM-DD")
                cursor.execute(query + " AND AttentionDate BETWEEN ? AND ?", params + [start_of_week, end_of_week])
                count = cursor.fetchone()[0]
                data[f"Tuần {current_week_number}"] = count

        elif time_period == "Tháng":
            if "Tháng" in selected_time:
                month = selected_time.replace("Tháng ", "").strip()
                current_year = arrow.now().year
                formatted_date = f"{int(month):02d}/{current_year}"
                selected_date = arrow.get(formatted_date, "MM/YYYY")
            else:
                formatted_date = selected_time
                selected_date = arrow.get(selected_time, "MM/YYYY")

            for i in range(5):
                start_of_month = selected_date.shift(months=-i).floor('month').format("YYYY-MM-DD")
                end_of_month = selected_date.shift(months=-i).ceil('month').format("YYYY-MM-DD")
                cursor.execute(query + " AND AttentionDate BETWEEN ? AND ?", params + [start_of_month, end_of_month])
                count = cursor.fetchone()[0]
                data[f"Tháng {selected_date.shift(months=-i).format('MM/YYYY')}"] = count

        # Sắp xếp dữ liệu theo thứ tự thời gian từ bé đến lớn
        sorted_data = OrderedDict(sorted(data.items(), key=lambda x: x[0]))

        connection.close()
        return sorted_data

    except pyodbc.Error as ex:
        messagebox.showerror("Lỗi SQL", f"Lỗi khi truy vấn: {ex}")
        return {}



def display_report():
    time_period = combo1.get()  # Lấy giá trị "Ngày", "Tuần", hoặc "Tháng"
    selected_time = combo2.get()  # Lấy giá trị thời gian đã chọn
    selected_job = combo3.get()  # Lấy vị trí công việc đã chọn
    selected_user = combo4.get()  # Lấy người dùng đã chọn

    if selected_job == "Tất cả" and selected_user == "Tất cả" and time_period == "Tất cả" and selected_time == "Tất cả":
        messagebox.showerror("Lỗi", "Vui lòng chọn 1 trường dữ liệu!")
        return

    # Kiểm tra nếu đã chọn "Ngày", "Tuần" hoặc "Tháng" mà không chọn thời gian phù hợp
    if (time_period in ["Ngày", "Tuần", "Tháng"]) and selected_time == "Tất cả":
        messagebox.showerror("Lỗi", f"Vui lòng chọn 1 thời gian {time_period} phù hợp!")
        return
    
    if time_period == "Tất cả" and (selected_job != "Tất cả" or selected_user != "Tất cả"):
        messagebox.showwarning("Thông báo", "Vui lòng chọn điều kiện thời gian!")
        return

    # Fetch dữ liệu báo cáo từ DB
    records = fetch_report_data(time_period, selected_time, selected_job, selected_user)

    if not records:
        messagebox.showinfo("Thông báo", "Không có dữ liệu để hiển thị")
        return

    # Phân tích dữ liệu và chuẩn bị vẽ biểu đồ
    dates = list(records.keys())
    counts = list(records.values()) 

    # Tạo một figure và vẽ biểu đồ
    fig, ax = plt.subplots(figsize=(7, 5))  # Tạo một figure mới
    ax.bar(dates, counts, color='blue')  # Vẽ biểu đồ thanh (bar chart)
    ax.set_xlabel('Thời gian')  # Nhãn trục X
    ax.set_ylabel('Số lần đi muộn')  # Nhãn trục Y

    # Cập nhật tiêu đề theo thời gian từ bé đến lớn
    if time_period == "Ngày":
        ax.set_title(f"Số lần đi muộn từ {dates[0]} đến {dates[-1]}")  # Hiển thị ngày từ đầu đến cuối
    elif time_period == "Tuần":
        ax.set_title(f"Số lần đi muộn từ {dates[0]} đến {dates[-1]}")  # Hiển thị tuần từ đầu đến cuối
    elif time_period == "Tháng":
        ax.set_title(f"Số lần đi muộn từ {dates[0]} đến {dates[-1]}")  # Hiển thị tháng từ đầu đến cuối

    # Tìm giá trị lớn nhất trong counts
    max_count = max(counts)

    # Tô màu các cột có giá trị bằng giá trị lớn nhất
    for i, count in enumerate(counts):
        if count == max_count:
            ax.patches[i].set_color('red')  # Đổi màu các cột có giá trị lớn nhất thành đỏ

    # Cải thiện hiển thị: xoay nhãn trên trục X để dễ đọc hơn
    plt.xticks(rotation=45, ha='right', fontsize=10)  # Xoay nhãn và giảm kích thước font

    # Điều chỉnh khoảng cách dưới cùng để nhãn không bị cắt
    plt.subplots_adjust(bottom=0.2)  # Điều chỉnh khoảng cách dưới cùng
    plt.tight_layout()

    # Hiển thị số trên các cột
    for i, count in enumerate(counts):
        ax.text(i, count + 0.1, str(count), ha='center', va='bottom', fontsize=10)

    # Đặt biểu đồ vào trong report_frame
    canvas = FigureCanvasTkAgg(fig, master=report_frame)  # Kết nối figure với Tkinter frame
    canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10)  # Đặt canvas vào giao diện
    canvas.draw()  # Vẽ biểu đồ