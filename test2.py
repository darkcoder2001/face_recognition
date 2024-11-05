import tkinter as tk
from tkinter import ttk

# Hàm để lọc dữ liệu trong Treeview
def search_data():
    search_terms = [entry.get().lower() for entry in search_entries]  # Lấy ký tự tìm kiếm từ tất cả các ô
    for row in tree.get_children():  # Duyệt qua tất cả các hàng
        tree.delete(row)  # Xóa hàng hiện tại

    # Giả sử bạn có một danh sách dữ liệu ban đầu
    for item in original_data:  # original_data là danh sách chứa dữ liệu gốc
        # Kiểm tra tất cả các điều kiện tìm kiếm
        if all(item[i].lower().startswith(search_terms[i]) for i in range(len(search_terms))):
            tree.insert("", "end", values=item)  # Thêm hàng mới vào Treeview

# Dữ liệu mẫu
original_data = [
    ("John Doe", "admin"),
    ("Jane Smith", "user"),
    ("Alice Johnson", "admin"),
    ("Bob Brown", "user"),
]

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Tìm Kiếm trong Treeview")

# Tạo Treeview
tree = ttk.Treeview(root, columns=("Name", "Role"), show='headings')
tree.heading("Name", text="Name")
tree.heading("Role", text="Role")

tree.pack(pady=10)

# Chèn dữ liệu ban đầu vào Treeview
for item in original_data:
    tree.insert("", "end", values=item)

# Tạo khung cho ô tìm kiếm
search_frame = tk.Frame(root)
search_frame.pack(pady=5)

# Tạo ô tìm kiếm cho từng cột
search_entries = []
for column in tree["columns"]:
    label = tk.Label(search_frame, text=column)
    label.pack(side=tk.LEFT, padx=5)
    entry = tk.Entry(search_frame, width=15)
    entry.pack(side=tk.LEFT, padx=5)
    entry.bind("<KeyRelease>", lambda e: search_data())  # Liên kết sự kiện gõ phím
    search_entries.append(entry)

# Tạo lại Treeview để đảm bảo ô tìm kiếm nằm ngay giữa tiêu đề và giá trị
tree.update_idletasks()  # Cập nhật Treeview để lấy kích thước hiện tại
tree_width = tree.winfo_width()  # Lấy chiều rộng của Treeview
search_frame.place(relx=0.5, anchor="n", y=30)  # Đặt khung tìm kiếm ở giữa

# Chạy ứng dụng
root.mainloop()
