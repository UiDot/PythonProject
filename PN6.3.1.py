
import sqlite3

# подключение к базе
conn = sqlite3.connect("diary.db")
cursor = conn.cursor()

# создание таблицы
cursor.execute("""
CREATE TABLE IF NOT EXISTS diary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# функции
def add_entry(title, content):
    cursor.execute("INSERT INTO diary (title, content) VALUES (?, ?)", (title, content))
    conn.commit()

def view_entries():
    cursor.execute("SELECT id, title, created_at FROM diary ORDER BY created_at DESC")
    return cursor.fetchall()

def read_entry(entry_id):
    cursor.execute("SELECT title, content, created_at FROM diary WHERE id=?", (entry_id,))
    return cursor.fetchone()

def delete_entry(entry_id):
    cursor.execute("DELETE FROM diary WHERE id=?", (entry_id,))
    conn.commit()

# основной цикл
while True:
    print("\n📓 Дневник")
    print("1. Добавить запись")
    print("2. Посмотреть все записи")
    print("3. Прочитать запись")
    print("4. Удалить запись")
    print("5. Выйти")

    choice = input("Выберите действие: ")

    if choice == "1":
        title = input("Заголовок: ")
        content = input("Текст: ")
        add_entry(title, content)
        print("✅ Запись добавлена.")

    elif choice == "2":
        entries = view_entries()
        if entries:
            for e in entries:
                print(f"{e[0]}. {e[1]} ({e[2]})")
        else:
            print("Записей пока нет.")

    elif choice == "3":
        entry_id = input("Введите ID записи: ")
        entry = read_entry(entry_id)
        if entry:
            print(f"\n{entry[0]} ({entry[2]})\n{entry[1]}")
        else:
            print("❌ Запись не найдена.")

    elif choice == "4":
        entry_id = input("Введите ID записи для удаления: ")
        delete_entry(entry_id)
        print("🗑 Запись удалена.")

    elif choice == "5":
        print("👋 До свидания!")
        break

    else:
        print("❌ Неверный выбор. Попробуйте снова.")

# закрытие соединения
conn.close()