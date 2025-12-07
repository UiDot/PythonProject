import sqlite3


# Создаем подключение
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# параметр PRIMARY KEY означает, что это поле будет основным идентификатором в таблице
# параметр AUTOINCREMENT означает, что при вставки данных этот параметр будет создаваться сам и увеличиваться на единицу
# в sqlite символьный тип всегда TEXT
# NOT NULL означает, что поле нельзя оставлять пустым
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL
)
""")

# Добавляем пользователей
cursor.execute("""
INSERT INTO users (username) VALUES
("John"),
("Tom")
""")
conn.commit()

# Выводим пользователей
print('Только добавили')
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
for user in users:
    print(f"User_id:  {user[0]} User name: {user[1]}")

# Удаляем пользователя
cursor.execute('DELETE FROM users WHERE username = "John"')
conn.commit()

# Выводим пользователей
print('Удалили John')
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
for user in users:
    print(f"User_id:  {user[0]} User name: {user[1]}")

# обновляем пользователя
cursor.execute('UPDATE users SET username = "John" WHERE username = "Tom"')
conn.commit()

# Выводим пользователей
print('Обновили Tom')
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
for user in users:
    print(f"User_id:  {user[0]} User name: {user[1]}")

# Закрываем подключение
conn.close()