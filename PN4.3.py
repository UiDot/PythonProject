
from abc import ABC, abstractmethod


# Абстрактный класс для вопросов (абстракция)
class Question(ABC):
    def __init__(self, text, points):
        self._text = text  # Инкапсуляция: приватное поле
        self._points = points

    @abstractmethod
    def ask(self):
        """Спрашивает вопрос и возвращает набранные очки."""
        pass

# Обычный вопрос с одним правильным ответом
class SingleChoiceQuestion(Question):
    def __init__(self, text, options, correct_answer, points):
        super().__init__(text, points)  # Наследование
        self._options = options  # Список вариантов ответа
        self._correct_answer = correct_answer  # Индекс правильного ответа (1-based)

    def ask(self):  # Полиморфизм
        print(f"\n{self._text}")
        for i, option in enumerate(self._options, 1):
            print(f"{i}. {option}")
        answer = input("Ваш ответ (номер): ")
        if answer.isdigit() and int(answer) == self._correct_answer:
            print("Правильно!")
            return self._points
        print("Неправильно!")
        return 0

# Вопрос с несколькими правильными ответами
class MultiChoiceQuestion(Question):
    def __init__(self, text, options, correct_answers, points):
        super().__init__(text, points)  # Наследование
        self._options = options
        self._correct_answers = correct_answers  # Список индексов правильных ответов

    def ask(self):  # Полиморфизм
        print(f"\n{self._text}")
        for i, option in enumerate(self._options, 1):
            print(f"{i}. {option}")
        answers = input("Введите номера правильных ответов (через запятую): ").split(",")
        try:
            answers = [int(a) for a in answers if a.strip().isdigit()]
            if sorted(answers) == sorted(self._correct_answers):
                print("Правильно!")
                return self._points
            print("Неправильно!")
            return 0
        except ValueError:
            print("Ошибка ввода!")
            return 0

# Класс викторины
class Quiz:
    def __init__(self):
        self._questions = []  # Список вопросов
        self._score = 0  # Очки игрока

    def add_question(self, question):
        """Добавляет вопрос в викторину."""
        self._questions.append(question)
        print(f"Добавлен вопрос: {question._text}")

    def run(self):
        """Запускает викторину."""
        self._score = 0
        print("\nДобро пожаловать в викторину!")
        for question in self._questions:
            self._score += question.ask()
        print(f"\nВикторина завершена! Ваш результат: {self._score} очков")

# Основная программа с консольным меню
def main():
    quiz = Quiz()
    # Пример вопросов
    quiz.add_question(SingleChoiceQuestion("Какой цвет неба?", ["Красный", "Синий", "Зелёный"], 2, 10))
    quiz.add_question(SingleChoiceQuestion("Столица Франции?", ["Париж", "Лондон", "Москва"], 1, 10))
    quiz.add_question(MultiChoiceQuestion("Какие числа чётные?", ["1", "2", "3", "4"], [2, 4], 20))
    quiz.add_question(SingleChoiceQuestion("Сколько планет в Солнечной системе?", ["7", "8", "9"], 2, 10))
    quiz.add_question(MultiChoiceQuestion("Какие животные млекопитающие?", ["Крокодил", "Дельфин", "Питон", "Кит"], [2, 4], 20))

    while True:
        print("\n=== Викторина ===")
        print("1. Начать викторину")
        print("2. Добавить вопрос (с одним ответом)")
        print("3. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            quiz.run()
        elif choice == "2":
            text = input("Введите текст вопроса: ")
            if not text:
                print("Вопрос не может быть пустым!")
                continue
            options = []
            for i in range(1, 4):
                opt = input(f"Введите вариант ответа {i}: ")
                if opt:
                    options.append(opt)
                else:
                    print("Вариант не может бытфь пустым!")
                    break
            if len(options) != 3:
                print("Нужно ровно 3 варианта ответа!")
                continue
            correct = input("Введите номер правильного ответа (1-3): ")
            if correct.isdigit() and 1 <= int(correct) <= 3:
                qw = SingleChoiceQuestion(text, options, correct, 10)

                quiz.add_question(qw)
if __name__=="__main__":
    main()