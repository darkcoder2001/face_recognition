import bcrypt

# Mật khẩu cần mã hóa
password = "my_secure_password"

# Mã hóa mật khẩu
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# In mật khẩu đã mã hóa ra màn hình
print("Mật khẩu đã mã hóa:", hashed_password)
