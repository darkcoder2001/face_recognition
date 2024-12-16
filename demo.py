from insightface.app import FaceAnalysis
import cv2

# Khởi tạo ứng dụng InsightFace
app = FaceAnalysis(name='buffalo_l')  # Sử dụng mô hình 'buffalo_l'
app.prepare(ctx_id=0, det_size=(640, 640))

# Đọc ảnh đầu vào
img_path = 'demo.jpg'
img = cv2.imread(img_path)

# Phân tích khuôn mặt
faces = app.get(img)
for face in faces:
    print(f"Bounding Box: {face.bbox}")
    print(f"Gender: {'Male' if face.gender > 0.5 else 'Female'}")
    print(f"Age: {face.age}")
