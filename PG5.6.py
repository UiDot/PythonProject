#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Консольная викторина для проверки школьных знаний 5 класса
"""

import random
import sys


class SchoolQuiz:
    def __init__(self):
        self.correct_answers = 0
        self.total_questions = 0

        # Математические вопросы - таблица умножения
        self.multiplication_questions = []
        for i in range(2, 10):
            for j in range(2, 10):
                self.multiplication_questions.append({
                    'question': f"{i} × {j} = ?",
                    'answer': i * j,
                    'type': 'math'
                })

        # Математические вопросы - сложение и вычитание
        self.addition_questions = []
        for _ in range(30):
            a = random.randint(10, 50)
            b = random.randint(10, 50)
            self.addition_questions.append({
                'question': f"{a} + {b} = ?",
                'answer': a + b,
                'type': 'math'
            })

        self.subtraction_questions = []
        for _ in range(30):
            a = random.randint(50, 100)
            b = random.randint(10, 49)
            self.subtraction_questions.append({
                'question': f"{a} - {b} = ?",
                'answer': a - b,
                'type': 'math'
            })

        # Текстовые вопросы по разным предметам
        self.text_questions = [
            # Русский язык
            {
                'question': "Сколько букв в русском алфавите?",
                'answer': "33",
                'type': 'text'
            },
            {
                'question': "Как называется главный член предложения, который обозначает действие?",
                'answer': "сказуемое",
                'type': 'text'
            },
            {
                'question': "Что такое синонимы?",
                'answer': "слова с одинаковым значением",
                'type': 'text'
            },

            # География
            {
                'question': "Столица России?",
                'answer': "москва",
                'type': 'text'
            },
            {
                'question': "Самая длинная река в России?",
                'answer': "обь",
                'type': 'text'
            },
            {
                'question': "На каком материке находится Россия?",
                'answer': "евразия",
                'type': 'text'
            },

            # Природоведение
            {
                'question': "Сколько планет в Солнечной системе?",
                'answer': "8",
                'type': 'text'
            },
            {
                'question': "Что производят растения в процессе фотосинтеза?",
                'answer': "кислород",
                'type': 'text'
            },
            {
                'question': "Как называется наука о животных?",
                'answer': "зоология",
                'type': 'text'
            },

            # История
            {
                'question': "В каком году началась Великая Отечественная война?",
                'answer': "1941",
                'type': 'text'
            },
            {
                'question': "Кто крестил Русь?",
                'answer': "владимир",
                'type': 'text'
            },

            # Литература
            {
                'question': "Кто написал сказку 'Колобок'?",
                'answer': "народ",
                'type': 'text'
            },
            {
                'question': "Автор сказки 'Золушка'?",
                'answer': "перро",
                'type': 'text'
            }
        ]

        # Объединяем все вопросы
        self.all_questions = (self.multiplication_questions +
                              self.addition_questions +
                              self.subtraction_questions +
                              self.text_questions)

    def clear_screen(self):
        """Очистка экрана"""
        print("\n" * 50)

    def show_welcome(self):
        """Показать приветствие"""
        print("=" * 60)
        print("🎓 ВИКТОРИНА ДЛЯ 5 КЛАССА 🎓")
        print("=" * 60)
        print("Добро пожаловать в викторину для проверки школьных знаний!")
        print("Здесь вас ждут вопросы по математике и другим предметам.")
        print("Отвечайте внимательно и не торопитесь!")
        print("=" * 60)
        print()

    def show_rules(self):
        """Показать правила"""
        print("📋 ПРАВИЛА ИГРЫ:")
        print("• Для математических примеров вводите только числа")
        print("• Для текстовых вопросов можно отвечать по-разному")
        print("• Для выхода из игры введите 'выход' или 'quit'")
        print("• Удачи! 🍀")
        print()

    def normalize_text_answer(self, answer):
        """Нормализация текстового ответа"""
        return answer.lower().strip().replace('ё', 'е')

    def check_answer(self, question, user_answer):
        """Проверка ответа"""
        if question['type'] == 'math':
            try:
                return int(user_answer) == question['answer']
            except ValueError:
                return False
        else:
            # Для текстовых вопросов делаем более гибкую проверку
            normalized_user = self.normalize_text_answer(user_answer)
            normalized_correct = self.normalize_text_answer(str(question['answer']))

            # Проверяем точное совпадение или содержание ключевых слов
            if normalized_user == normalized_correct:
                return True
            elif normalized_correct in normalized_user or normalized_user in normalized_correct:
                return True

            return False

    def ask_question(self, question):
        """Задать вопрос и получить ответ"""
        print(f"❓ {question['question']}")

        if question['type'] == 'math':
            print("   (введите число)")
        else:
            print("   (введите текстовый ответ)")

        user_answer = input("👉 Ваш ответ: ").strip()

        # Проверка на выход
        if user_answer.lower() in ['выход', 'quit', 'exit']:
            return None

        return user_answer

    def show_result(self, is_correct, correct_answer):
        """Показать результат ответа"""
        if is_correct:
            print("✅ Правильно! Молодец!")
        else:
            print(f"❌ Неправильно. Правильный ответ: {correct_answer}")
        print()

    def show_final_stats(self):
        """Показать финальную статистику"""
        print("=" * 60)
        print("📊 РЕЗУЛЬТАТЫ ВИКТОРИНЫ")
        print("=" * 60)
        print(f"Всего вопросов: {self.total_questions}")
        print(f"Правильных ответов: {self.correct_answers}")
        print(f"Неправильных ответов: {self.total_questions - self.correct_answers}")

        if self.total_questions > 0:
            percentage = (self.correct_answers / self.total_questions) * 100
            print(f"Процент правильных ответов: {percentage:.1f}%")

            if percentage >= 90:
                print("🏆 Отлично! Вы знаете материал на 'отлично'!")
            elif percentage >= 75:
                print("⭐ Хорошо! Есть небольшие пробелы, но в целом неплохо!")
            elif percentage >= 60:
                print("👍 Удовлетворительно. Стоит повторить материал.")
            else:
                print("📚 Нужно больше заниматься. Не расстраивайтесь!")

        print("=" * 60)
        print("Спасибо за игру! До встречи! 👋")

    def run(self):
        """Запустить викторину"""
        self.clear_screen()
        self.show_welcome()
        self.show_rules()

        # Спрашиваем, сколько вопросов хочет пользователь
        while True:
            try:
                num_questions = input("Сколько вопросов вы хотите (5-50)? [по умолчанию 10]: ").strip()
                if not num_questions:
                    num_questions = 10
                else:
                    num_questions = int(num_questions)

                if 5 <= num_questions <= 50:
                    break
                else:
                    print("Пожалуйста, введите число от 5 до 50.")
            except ValueError:
                print("Пожалуйста, введите корректное число.")

        print(f"\n🎯 Начинаем викторину! У вас {num_questions} вопросов.\n")

        # Выбираем случайные вопросы
        selected_questions = random.sample(self.all_questions, min(num_questions, len(self.all_questions)))

        # Основной цикл викторины
        for i, question in enumerate(selected_questions, 1):
            print(f"📝 Вопрос {i} из {num_questions}")
            print("-" * 40)

            user_answer = self.ask_question(question)

            # Проверка на выход
            if user_answer is None:
                print("\n👋 До свидания!")
                break

            # Проверка ответа
            is_correct = self.check_answer(question, user_answer)
            self.total_questions += 1

            if is_correct:
                self.correct_answers += 1

            self.show_result(is_correct, question['answer'])

            # Пауза между вопросами
            if i < len(selected_questions):
                input("Нажмите Enter для следующего вопроса...")
                print()

        # Показать итоговую статистику
        self.show_final_stats()


def main():
    """Главная функция"""
    try:
        quiz = SchoolQuiz()
        quiz.run()
    except KeyboardInterrupt:
        print("\n\n👋 Программа завершена пользователем. До свидания!")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {e}")
        print("Попробуйте запустить программу снова.")


if __name__ == "__main__":
    main()