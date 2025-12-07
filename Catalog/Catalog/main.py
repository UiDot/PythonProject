
import json
from flask import request, redirect, url_for

film_storage_path = "db.json"
loginpass = "base.json"
app = flask.Flask(__name__)

# Инициализация данных
loginbase = {"admin": "123"}  # Пример: ключ = логин, значение = пароль
data = [
    {"title": "Главы государств", "description": "...", "rate": "6.5", "image": "/static/film1.jpg"},
    {"title": "Шрек", "description": "...", "rate": "8.2", "image": "/static/shrek.jpg"}
]

# Загрузка данных из файлов
try:
    with open(loginpass, "r", encoding="utf-8") as f:
        loginbase = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    loginbase = {"admin": "123"}

try:
    with open(film_storage_path, "r", encoding="utf-8") as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = []


# Сохранение данных в файлы
def save_data():
    with open(loginpass, "w", encoding="utf-8") as f:
        json.dump(loginbase, f, ensure_ascii=False)
    with open(film_storage_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


# Главная страница
@app.route('/')
def catalog():
    return flask.render_template('catalog.html', title="Каталог", films=data)


# Страница авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        # Проверка логина и пароля
        if login in loginbase and loginbase[login] == password:
            return redirect(url_for('catalog'))
        else:
            return flask.render_template('login.html', error="Неверный логин или пароль")

    return flask.render_template('login.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        # Проверка логина и пароля
        if login in loginbase and loginbase[login] == password:
            return redirect(url_for('catalog'))
        else:
            return flask.render_template('login.html', error="Неверный логин или пароль")

    return flask.render_template('login.html')

# Страница "О нас"
@app.route('/about')
@app.route('/info')
def info():
    return flask.render_template('about.html', title="О нас")


if __name__ == '__main__':
    app.run(port=5001, debug=True)