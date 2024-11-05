import tkinter as tk
from tkinter import ttk

# def search_data():
#     search_terms = [entry.get().lower() for entry in search_entries]  # Lấy ký tự tìm kiếm từ tất cả các ô
#     for row in tree.get_children():  # Duyệt qua tất cả các hàng
#         tree.delete(row)  # Xóa hàng hiện tại

#     # Giả sử bạn có một danh sách dữ liệu ban đầu
#     for item in original_data:  # original_data là danh sách chứa dữ liệu gốc
#         # Kiểm tra tất cả các điều kiện tìm kiếm
#         if all(item[i].lower().startswith(search_terms[i]) for i in range(len(search_terms))):
#             tree.insert("", "end", values=item)  # Thêm hàng mới vào Treeview

# search_entries = []
# for column in tree["columns"]:
#     label = tk.Label(search_frame, text=column)
#     label.pack(side=tk.LEFT, padx=5)
#     entry = tk.Entry(search_frame, width=15)
#     entry.pack(side=tk.LEFT, padx=5)
#     entry.bind("<KeyRelease>", lambda e: search_data())  # Liên kết sự kiện gõ phím
#     search_entries.append(entry)

class TreeViewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Treeview Example")

        # Tạo Treeview với 3 cột
        self.tree = ttk.Treeview(root, columns=("ID", "Tên", "Vai trò"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tên", text="Tên")
        self.tree.heading("Vai trò", text="Vai trò")

        # Đặt chiều rộng cho các cột
        self.tree.column("ID", width=100)
        self.tree.column("Tên", width=200)
        self.tree.column("Vai trò", width=200)

        # Hiển thị Treeview
        self.tree.pack(padx=10, pady=10)

        # Dữ liệu mẫu
        self.data = [
            (1, "Nguyễn Văn A", "Sinh viên"),
            (2, "Trần Thị B", "Giảng viên"),
            (3, "Lê Văn C", "Nhân viên"),
            (4, "Phạm Thị D", "Sinh viên"),
        ]

        # Hiển thị dữ liệu vào Treeview
        self.show_data(self.data)

        # Thêm một hàng rỗng sau khi thêm tiêu đề
        self.tree.insert("", 0, values=("", "", ""))  # Chèn hàng rỗng vào vị trí thứ 1

    def show_data(self, data):
        # Xóa tất cả các mục hiện tại trong Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Thêm dữ liệu vào Treeview
        for row in data:
            self.tree.insert("", tk.END, values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = TreeViewApp(root)
    root.mainloop()