
from abc import ABC, abstractmethod

# Абстрактный класс для медиа
class Media(ABC):

    def __init__(self, pages, title, author):
        # Указываем все стандартные поля в родительском классе
        self._is_rented = False
        self._pages = pages
        self._title = title
        self._author = author

    @abstractmethod
    def display_info(self):
        ...

    def rent(self):  # Одинаковый для всех метод
        if self._is_rented:
            print('Этот экземпляр уже кем то арендован')
        else:
            self._is_rented = True

    def unrent(self):  # Одинаковый для всех метод
        self._is_rented = False

    def could_be_rented(self):  # Одинаковый для всех метод
        return not self._is_rented


# Класс для книги
class Book(Media):  # Указываем на абстрактный класс/наследуем
    def __init__(self, title, author,pages):
        super().__init__(pages, title, author )

    def display_info(self):
        return f"Книга: {self._title} от {self._author}, {self._pages} страниц"


# Класс для журнала (для демонстрации полиморфизма)
class Magazine(Media):  # Указываем на абстрактный класс/наследуем
    def __init__(self, title, author, pages, issue):
        super().__init__(pages, title, author)
        self._issue = issue

    def display_info(self):
        return f"Журнал: {self._title} от {self._author}, страниц - {self._pages}, выпуск {self._issue}"


# Библиотека как список объектов
library = [
    Book("Изучаем Python", "Эрик Маттес", 544),
    Magazine("Наука и жизнь", "Разные авторы", 202, 2001),
    Book("Чистый код", "Роберт Мартин", 464)
]


# Консольное меню
def main():
    while True:
        print("\nБиблиотека книг")
        print("1. Показать все книги")
        print("2. Арендовать книгу")
        print("3. Вернуть книгу")
        print("4. Выход")
        choice = input("Выберите действие (1-2): ")

        if choice == "1":
            print("\nСписок книг:")
            for item in library:
                print(item.display_info())  # Полиморфизм
        elif choice == "2":
            not_rented = []
            for index, item in enumerate(library):
                if item.could_be_rented():
                    not_rented.append(item)
                    print(f'{index+1}. {item.display_info()}')
            choice = int(input('Введите номер книги, которую хотите арендовать'))
            not_rented[choice - 1].rent()
        elif choice == "3":
            rented = []
            for index, item in enumerate(library):
                if not item.could_be_rented():
                    rented.append(item)
                    print(f'{index + 1}. {item.display_info()}')
            choice = int(input('Введите номер книги, которую хотите вернуть'))
            rented[choice - 1].unrent()
        elif choice == "4":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
