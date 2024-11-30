import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Dữ liệu mẫu
dates = ["2021-01-01", "2021-01-02", "2021-01-03"]
counts = [5, 10, 3]

# Tạo biểu đồ thanh
fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(dates, counts, color='blue')

# Tìm cột có giá trị lớn nhất
max_height = max(counts)
max_index = counts.index(max_height)

# Tô màu đỏ cho cột có giá trị lớn nhất
bars[max_index].set_color('red')

# Thêm chú thích cho mỗi cột
for bar in bars:
    yval = bar.get_height()  # Lấy chiều cao của mỗi cột
    ax.annotate(f'{yval}',  # Chú thích là giá trị chiều cao của cột
                xy=(bar.get_x() + bar.get_width() / 2, yval),  # Vị trí chú thích
                xytext=(0, 3),  # Dịch chuyển chú thích một chút lên trên
                textcoords="offset points",  # Đảm bảo tọa độ dịch chuyển là theo điểm
                ha='center',  # Căn giữa chú thích
                va='bottom',  # Căn dưới cho chú thích
                fontsize=10,  # Kích thước chữ
                color='black')  # Màu sắc của chữ

# Thêm chú thích dưới biểu đồ
# Thêm một hình vuông màu đỏ (trong khung chú thích)


# Đặt tiêu đề và nhãn
ax.set_title('Số lần đi muộn trong các ngày')
ax.set_xlabel('Ngày')
ax.set_ylabel('Số lần')
legend_patch = patches.Patch(color='red', label='Giá trị lớn nhất')
# Hiển thị chú thích dưới biểu đồ
plt.legend(handles=[legend_patch], loc='lower center', bbox_to_anchor=(0.5, -0.1), fontsize=12)

# Hiển thị biểu đồ
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
