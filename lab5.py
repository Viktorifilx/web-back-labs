from flask import Blueprint, render_template, request, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path


lab5 = Blueprint('lab5', __name__)


@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', username=session.get('login'))


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='filatova_viktoriya_knowledge_base',
            user='filatova_viktoriya_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    real_name = request.form.get('real_name')   
    password = request.form.get('password')

    if not (login and real_name and password):  
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error="Такой пользователь уже существует")

    password_hash = generate_password_hash(password)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "INSERT INTO users (login, password, real_name) VALUES (%s, %s, %s);",
            (login, password_hash, real_name)
        )
    else:
        cur.execute(
            "INSERT INTO users (login, password, real_name) VALUES (?, ?, ?);",
            (login, password_hash, real_name)
        )

    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)



@lab5.route('/lab5/success')
def success():
    return render_template('lab5/success.html')


@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login_value = request.form.get('login')
    password = request.form.get('password')

    if not (login_value and password):
        return render_template('lab5/login.html', error="Заполните поля")

    conn, cur = db_connect()

  
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login_value,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login_value,))

    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    session['login'] = login_value

    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login_value)


@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text or title.strip() == "" or article_text.strip() == "":
        return render_template(
            'lab5/create_article.html',
            error="Поля 'Тема' и 'Текст статьи' не могут быть пустыми."
        )

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    row = cur.fetchone()

    if row is None:
        db_close(conn, cur)
        return redirect('/lab5/login')

    login_id = row["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "INSERT INTO articles (login_id, title, article_text) "
            "VALUES (%s, %s, %s);",
            (login_id, title, article_text)
        )
    else:
        cur.execute(
            "INSERT INTO articles (login_id, title, article_text) "
            "VALUES (?, ?, ?);",
            (login_id, title, article_text)
        )

    db_close(conn, cur)
    return redirect('/lab5')


@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    row = cur.fetchone()
    if row is None:
        db_close(conn, cur)
        return redirect('/lab5/login')

    login_id = row["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "SELECT * FROM articles WHERE login_id=%s ORDER BY is_favorite DESC, id DESC;",
            (login_id,)
        )
    else:
        cur.execute(
            "SELECT * FROM articles WHERE login_id=? ORDER BY is_favorite DESC, id DESC;",
            (login_id,)
        )


    articles = cur.fetchall()
    db_close(conn, cur)

    if not articles:
        return render_template(
            'lab5/articles.html',
            articles=[],
            message="У вас пока нет ни одной статьи"
        )

    return render_template('lab5/articles.html', articles=articles)


@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    user_row = cur.fetchone()
    if not user_row:
        db_close(conn, cur)
        return redirect('/lab5/login')

    login_id = user_row['id']

    if request.method == 'GET':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(
                "SELECT * FROM articles WHERE id=%s AND login_id=%s;",
                (article_id, login_id)
            )
        else:
            cur.execute(
                "SELECT * FROM articles WHERE id=? AND login_id=?;",
                (article_id, login_id)
            )

        article = cur.fetchone()
        db_close(conn, cur)

        if not article:
            return redirect('/lab5/list')

        return render_template('lab5/edit_article.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text or title.strip() == "" or article_text.strip() == "":
        article = {'id': article_id, 'title': title, 'article_text': article_text}
        db_close(conn, cur)
        return render_template(
            'lab5/edit_article.html',
            article=article,
            error="Поля 'Тема' и 'Текст статьи' не могут быть пустыми."
        )

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "UPDATE articles SET title=%s, article_text=%s "
            "WHERE id=%s AND login_id=%s;",
            (title, article_text, article_id, login_id)
        )
    else:
        cur.execute(
            "UPDATE articles SET title=?, article_text=? "
            "WHERE id=? AND login_id=?;",
            (title, article_text, article_id, login_id)
        )

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    user_row = cur.fetchone()
    if not user_row:
        db_close(conn, cur)
        return redirect('/lab5/login')

    login_id = user_row['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "DELETE FROM articles WHERE id=%s AND login_id=%s;",
            (article_id, login_id)
        )
    else:
        cur.execute(
            "DELETE FROM articles WHERE id=? AND login_id=?;",
            (article_id, login_id)
        )

    db_close(conn, cur)
    return redirect('/lab5/list')



@lab5.route('/lab5/toggle_favorite/<int:article_id>', methods=['POST'])
def toggle_favorite(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET is_favorite = NOT is_favorite WHERE id=%s;", (article_id,))
    else:
        cur.execute("UPDATE articles SET is_favorite = CASE WHEN is_favorite=1 THEN 0 ELSE 1 END WHERE id=?;", (article_id,))

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/toggle_public/<int:article_id>', methods=['POST'])
def toggle_public(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET is_public = NOT is_public WHERE id=%s;", (article_id,))
    else:
        cur.execute("UPDATE articles SET is_public = CASE WHEN is_public=1 THEN 0 ELSE 1 END WHERE id=?;", (article_id,))

    db_close(conn, cur)
    return redirect('/lab5/list')



@lab5.route('/lab5/users')
def users():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, real_name FROM users ORDER BY id;")
    else:
        cur.execute("SELECT login, real_name FROM users ORDER BY id;")

    users = cur.fetchall()
    db_close(conn, cur)

    return render_template('lab5/users.html', users=users)


@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))

    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')

    user_id = user['id']

    if request.method == 'GET':
        real_name = user['real_name'] if user['real_name'] else ""
        db_close(conn, cur)
        return render_template('lab5/profile.html', real_name=real_name)

    real_name = request.form.get('real_name')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')

    if not real_name or real_name.strip() == "":
        db_close(conn, cur)
        return render_template(
            'lab5/profile.html',
            real_name=user['real_name'],
            error="Имя не может быть пустым"
        )

    if password or password_confirm:
        if password != password_confirm:
            db_close(conn, cur)
            return render_template(
                'lab5/profile.html',
                real_name=real_name,
                error="Пароль и подтверждение не совпадают"
            )

        password_hash = generate_password_hash(password)

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(
                "UPDATE users SET real_name=%s, password=%s WHERE id=%s;",
                (real_name, password_hash, user_id)
            )
        else:
            cur.execute(
                "UPDATE users SET real_name=?, password=? WHERE id=?;",
                (real_name, password_hash, user_id)
            )
    else:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(
                "UPDATE users SET real_name=%s WHERE id=%s;",
                (real_name, user_id)
            )
        else:
            cur.execute(
                "UPDATE users SET real_name=? WHERE id=?;",
                (real_name, user_id)
            )

    db_close(conn, cur)
    return render_template('lab5/profile_success.html', real_name=real_name)




@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5/login')



@lab5.route('/lab5/public')
def public_articles():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "SELECT a.title, a.article_text, u.login "
            "FROM articles a JOIN users u ON a.login_id = u.id "
            "WHERE a.is_public = TRUE ORDER BY a.id DESC;"
        )
    else:
        cur.execute(
            "SELECT a.title, a.article_text, u.login "
            "FROM articles a JOIN users u ON a.login_id = u.id "
            "WHERE a.is_public = 1 ORDER BY a.id DESC;"
        )

    articles = cur.fetchall()
    db_close(conn, cur)

    return render_template('lab5/public.html', articles=articles)

