from flask import Blueprint, render_template, request, session
from lab5 import db_connect   # берем нашу функцию подключения

lab6 = Blueprint('lab6', __name__)


@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')


# на всякий случай вешаем ОДНУ и ту же функцию на два URL,
# чтобы работало и старое /lab6/json-rpc-api/, и новое /lab6/offices-api/
@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
@lab6.route('/lab6/offices-api/', methods=['POST'])
def api():
    data = request.get_json() or {}
    rpc_id = data.get('id')
    method = data.get('method')

    # ---------- 1. Получение списка кабинетов ----------
    if method == 'info':
        conn, cur = db_connect()

        cur.execute("""
            SELECT number, tenant, price
            FROM offices
            ORDER BY number
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # rows — это список СЛОВАРЕЙ (RealDictRow),
        # поэтому берём значения по именам колонок
        offices = []
        for row in rows:
            offices.append({
                "number": row["number"],
                "tenant": row["tenant"],
                "price": row["price"],
            })

        return {
            "jsonrpc": "2.0",
            "result": offices,
            "id": rpc_id
        }

    # ---------- 2. Проверка авторизации ----------
    login = session.get('login')
    if not login:
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": 1,
                "message": "Unauthorized"
            },
            "id": rpc_id
        }

    # ---------- 3. Бронирование ----------
    if method == 'booking':
        office_number = data.get('params')

        conn, cur = db_connect()
        cur.execute(
            "SELECT tenant FROM offices WHERE number = %s",
            (office_number,)
        )
        row = cur.fetchone()

        if row is None:
            cur.close()
            conn.close()
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32601,
                    "message": "Office not found"
                },
                "id": rpc_id
            }

        # row — тоже словарь
        tenant = row["tenant"]

        if tenant != '':
            cur.close()
            conn.close()
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": 2,
                    "message": "Already booked"
                },
                "id": rpc_id
            }

        cur.execute(
            "UPDATE offices SET tenant = %s WHERE number = %s",
            (login, office_number)
        )
        conn.commit()
        cur.close()
        conn.close()

        return {
            "jsonrpc": "2.0",
            "result": "success",
            "id": rpc_id
        }

    # ---------- 4. Снятие аренды ----------
    if method == 'cancellation':
        office_number = data.get('params')

        conn, cur = db_connect()
        cur.execute(
            "SELECT tenant FROM offices WHERE number = %s",
            (office_number,)
        )
        row = cur.fetchone()

        if row is None:
            cur.close()
            conn.close()
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32601,
                    "message": "Office not found"
                },
                "id": rpc_id
            }

        tenant = row["tenant"]

        if tenant == '':
            cur.close()
            conn.close()
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": 3,
                    "message": "Not booked"
                },
                "id": rpc_id
            }

        if tenant != login:
            cur.close()
            conn.close()
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": 4,
                    "message": "Forbidden"
                },
                "id": rpc_id
            }

        cur.execute(
            "UPDATE offices SET tenant = '' WHERE number = %s",
            (office_number,)
        )
        conn.commit()
        cur.close()
        conn.close()

        return {
            "jsonrpc": "2.0",
            "result": "success",
            "id": rpc_id
        }

    return {
        "jsonrpc": "2.0",
        "error": {
            "code": -32601,
            "message": "Method not found"
        },
        "id": rpc_id
    }
 