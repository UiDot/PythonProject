def add_student(students, student_id, name, age, major):
    # Добавляет студента в словарь с ключом student_id и значениями имени, возраста и специальности.
    students[student_id] = {"name": name, "age": age, "major": major}

def update_student(students, student_id, name, age, major):
    # Обновляет данные студента, если он существует в словаре.
    if student_id in students:
        students[student_id] = {"name": name, "age": age, "major": major}
    else:
        # Выводит сообщение, если студент не найден.
        print("Студент не найден.")

def delete_student(students, student_id):
    # Удаляет данные студента из словаря по его ID, если он существует.
    if student_id in students:
        del students[student_id]
    else:
        # Выводит сообщение, если студент не найден.
        print("Студент не найден.")

def list_students(students):
    # Перечисляет всех студентов и их данные.
    for student_id, info in students.items():
        print(f"ID: {student_id}, Имя: {info['name']}, Возраст: {info['age']}, Специальность: {info['major']}")

def main():
    # Основная функция, управляющая программой.
    students = {}  # Инициализация пустого словаря для хранения данных студентов.

    while True:
        # Бесконечный цикл, выводящий меню и обрабатывающий пользовательский ввод.
        print("\n1. Добавить студента\n2. Обновить данные студента\n3. Удалить студента\n4. Показать всех студентов\n5. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            # Добавление нового студента.
            student_id = input("Введите ID студента: ")
            name = input("Введите имя студента: ")
            age = int(input("Введите возраст студента: "))
            major = input("Введите специальность студента: ")
            add_student(students, student_id, name, age, major)
        elif choice == '2':
            # Обновление данных существующего студента.
            student_id = input("Введите ID студента: ")
            name = input("Введите новое имя студента: ")
            age = int(input("Введите новый возраст студента: "))
            major = input("Введите новую специальность студента: ")
            update_student(students, student_id, name, age, major)  # !? Здесь должна быть update_student ?
        elif choice == '3':
            # Удаление студента.
            student_id = input("Введите ID студента для удаления: ")
            delete_student(students, student_id)
        elif choice == '4':
            # Вывод списка всех студентов.
            list_students(students)
        elif choice == '5':
            # Выход из программы.
            break
        else:
            # Обработка некорректного ввода.
            print("Неверный ввод. Пожалуйста, выберите корректный номер действия.")

if __name__ == "__main__":
    main()  # Запуск основной функции, если файл выполняется как основная программа.