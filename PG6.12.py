import asyncio
from googletrans import Translator, LANGUAGES

async def translate_text(text, dest_language='en'):
    translator = Translator()
    translation = await translator.translate(text, dest=dest_language)
    return translation.text

def print_supported_languages():
    print("Доступные языки:")
    for code, name in LANGUAGES.items():
        print(f"{code}: {name}")

async def main():
    print("Добро пожаловать в переводчик!")

    show_languages = input("Хотите увидеть список доступных языков? (да/нет): ").strip().lower()
    if show_languages == 'да':
        print_supported_languages()  # Выводим список доступных языков

    text = input("Введите текст для перевода: ")
    lang = input("Введите код языка перевода (например, 'en' для английского, 'es' для испанского): ")

    if lang not in LANGUAGES:
        print("Ошибка: указанный язык не поддерживается.")
        return

    translated_text = await translate_text(text, dest_language=lang)
    print(f"Переведенный текст: {translated_text}")

if __name__ == "__main__":
    asyncio.run(main())
