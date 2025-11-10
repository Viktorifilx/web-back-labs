from flask import Blueprint, render_template, request, redirect, session
import psycopg2
from psycopg2.extras import RealDictCursor

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', username = session.get('login'))

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')

    conn = psycopg2.connect(
        host='127.0.0.1',
        database='filatova_viktoriya_knowledge_base',
        user='filatova_viktoriya_knowledge_base',
        password='123'
    )
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM users WHERE login='{login}';")
    if cur.fetchone():
        cur.close()
        conn.close()
        return render_template('lab5/register.html', error = "Такой пользователь уже существует")

    cur.execute(f"INSERT INTO users (login, password) VALUES ('{login}' , '{password}');")
    conn.commit()
    cur.close()
    conn.close()
    return render_template('lab5/success.html', login=login)

   

@lab5.route('/lab5/list')
def article_list():
    return render_template('lab5/list.html')

@lab5.route('/lab5/create')
def create_article():
    return render_template('lab5/create.html')

@lab5.route('/lab5/success')
def success():
    return render_template('lab5/success.html')

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login_value = request.form.get('login')
    password = request.form.get('password')

    # оба поля должны быть заполнены
    if not (login_value and password):
        return render_template('lab5/login.html', error="Заполните поля")

    conn = psycopg2.connect(
        host='127.0.0.1',
        database='filatova_viktoriya_knowledge_base',   # та же БД, что в register
        user='filatova_viktoriya_knowledge_base',        # или postgres, если так делала
        password='123'
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # безопасный запрос без f-строки
    cur.execute("SELECT * FROM users WHERE login = %s;", (login_value,))
    user = cur.fetchone()

    # пользователя нет
    if not user:
        cur.close()
        conn.close()
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')

    # пароль не совпал
    if user["password"] != password:
        cur.close()
        conn.close()
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')

    # успех: сохраняем логин в сессии
    session['login'] = login_value

    cur.close()
    conn.close()
    return render_template('lab5/success_login.html', login=login_value)

