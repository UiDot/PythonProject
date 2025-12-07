# send_request.py

import requests

# Вставьте сюда ссылку, которую скопировали из браузера
url = "http://localhost:63342/PythonProject/goods.html?_ijt=okfv9lnscsckfrlgg90il4ie5h&_ij_reload=RELOAD_ON_SAVE"

# Отправляем GET-запрос
response = requests.get(url)

# Проверяем статус
if response.status_code == 200:
    print("✅ Запрос успешен!")
    print("Код ответа:", response.status_code)
    print("Тип контента:", response.headers.get('Content-Type'))
    print("\n--- HTML-контент ---")
    print(response.text)  # первые 500 символов
else:
    print(f"❌ Ошибка: {response.status_code}")