from flask import Blueprint, render_template, request, jsonify, abort, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from datetime import date


lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')

def db_connect():
    if current_app.config.get('DB_TYPE') == 'postgres':
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


MIN_YEAR = 1895
MAX_YEAR = date.today().year


def validate_and_normalize_film(data: dict):
    errors = {}

    title = (data.get("title") or "").strip()
    title_ru = (data.get("title_ru") or "").strip()
    description = (data.get("description") or "").strip()
    year_raw = data.get("year")

    if not title_ru:
        errors["title_ru"] = "Русское название не должно быть пустым"

    if not title and not title_ru:
        errors["title"] = "Название на оригинальном языке обязательно, если нет русского"

    if year_raw is None or str(year_raw).strip() == "":
        errors["year"] = "Год обязателен"
        year = None
    else:
        try:
            year = int(year_raw)
            if year < MIN_YEAR or year > MAX_YEAR:
                errors["year"] = f"Год должен быть от {MIN_YEAR} до {MAX_YEAR}"
        except ValueError:
            errors["year"] = "Год должен быть числом"
            year = None

    if not description:
        errors["description"] = "Описание не должно быть пустым"
    elif len(description) > 2000:
        errors["description"] = "Описание не должно превышать 2000 символов"

    data["title"] = title
    data["title_ru"] = title_ru
    data["description"] = description
    if year is not None:
        data["year"] = year

    if not data["title"] and data["title_ru"]:
        data["title"] = data["title_ru"]

    return errors, data



@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    cur.execute("SELECT id, title, title_ru, year, description FROM films ORDER BY id;")
    rows = cur.fetchall()
    db_close(conn, cur)

    films = [dict(row) for row in rows]
    return jsonify(films)


@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id=%s;", (id,))
    else:
        cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id=?;", (id,))
    row = cur.fetchone()
    db_close(conn, cur)

    if row is None:
        abort(404)

    return jsonify(dict(row))


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("DELETE FROM films WHERE id=%s;", (id,))
    else:
        cur.execute("DELETE FROM films WHERE id=?;", (id,))
    deleted = cur.rowcount
    db_close(conn, cur)

    if deleted == 0:
        abort(404)

    return '', 204
 

def validate_film(data):
    errors = {}
    if not data.get("description"):
        errors["description"] = "Описание не должно быть пустым"
    return errors

def normalize_film(data: dict) -> dict:
    if (not data.get("title")) and data.get("title_ru"):
        data["title"] = data["title_ru"]
    return data



@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['PUT'])
def put_film(id):
    data = request.get_json()
    errors, film = validate_and_normalize_film(data)

    if errors:
        return jsonify(errors), 400

    conn, cur = db_connect()
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute(
            "UPDATE films SET title=%s, title_ru=%s, year=%s, description=%s WHERE id=%s;",
            (film["title"], film["title_ru"], film["year"], film["description"], id)
        )
    else:
        cur.execute(
            "UPDATE films SET title=?, title_ru=?, year=?, description=? WHERE id=?;",
            (film["title"], film["title_ru"], film["year"], film["description"], id)
        )
    updated = cur.rowcount
    db_close(conn, cur)

    if updated == 0:
        abort(404)

    film["id"] = id
    return jsonify(film)




@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    data = request.get_json()
    errors, film = validate_and_normalize_film(data)

    if errors:
        return jsonify(errors), 400

    conn, cur = db_connect()
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute(
            "INSERT INTO films (title, title_ru, year, description) "
            "VALUES (%s, %s, %s, %s) RETURNING id;",
            (film["title"], film["title_ru"], film["year"], film["description"])
        )
        new_id = cur.fetchone()["id"]
    else:
        cur.execute(
            "INSERT INTO films (title, title_ru, year, description) "
            "VALUES (?, ?, ?, ?);",
            (film["title"], film["title_ru"], film["year"], film["description"])
        )
        new_id = cur.lastrowid

    db_close(conn, cur)

    return str(new_id)



<<<<<<< HEAD

=======
>>>>>>> 112ea30 (merge after pull)
