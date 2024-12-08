import bcrypt

password = '123'
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

print(f"Hashed password: {hashed_password.decode('utf-8')}")
