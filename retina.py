import insightface
from insightface.app import FaceAnalysis
import cv2
import matplotlib.pyplot as plt

# Tải và khởi tạo model RetinaFace
app = FaceAnalysis(allowed_modules=['detection'])  # Chỉ cần module detection
app.prepare(ctx_id=0)  # ctx_id=0 dùng GPU, ctx_id=-1 dùng CPU

# Đọc ảnh
image_path = 'demo.jpg'
img = cv2.imread(image_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Phát hiện khuôn mặt
faces = app.get(img)

# Hiển thị khuôn mặt được phát hiện
for face in faces:
    box = face.bbox.astype(int)  # Tọa độ bounding box
    cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 2)

# Hiển thị ảnh với bounding boxes
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()

# In thông tin các khuôn mặt
for i, face in enumerate(faces):
    print(f"Face {i + 1}:")
    print(f"  Bounding Box: {face.bbox}")
    print(f"  Detection Score: {face.det_score}")
