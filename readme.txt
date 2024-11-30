B1: restore DB face_recognition.bak
B2: thay tên ServerName(dòng đầu tiên) trong file db_config.txt (thay bằng tên servername của máy hiện tại)
B3: Cài đặt các thư viện cần thiết ở bằng cách chạy pip install -r install.txt
B4: run file main.py
B5: bấm admin login with username/password = admin1/123456
B6: Tạo 1 bản ghi => Thêm khuôn mặt cho bản ghi đó => quay về main test chức năng điểm danh
B7: Kiểm tra các chức năng khác của ứng dụng

*Các chức năng của phần mềm
- Với user: Điểm danh khuôn mặt đã đăng kí
- Với ADMIN: đăng nhập/quên mật khẩu/quản lý dữ liệu(xuất Excel...)/quản lý người dùng...
*Công nghệ:
- ngôn ngữ: python
- phát hiện và nhận diện khuôn mặt: opencv và insightface
- điểm danh khuôn mặt: cosine similarity