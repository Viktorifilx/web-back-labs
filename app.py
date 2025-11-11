from flask import Flask, render_template, request, url_for
import os
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')


app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)

@app.route("/")
@app.route("/index")
def index():
    # теперь можно снова отдавать шаблон
    return render_template(
        "index.html",
        name="Филатова Виктория Михайловна",
        group="ФБИ-34",
        course="3 курс",
        year="2025"
    )




@app.route("/bad_request")
def bad_request():
    return "400 Bad Request — Неверный запрос", 400

@app.route("/unauthorized")
def unauthorized():
    return "401 Unauthorized — Требуется авторизация", 401

@app.route("/payment_required")
def payment_required():
    return "402 Payment Required — Необходима оплата", 402

@app.route("/forbidden")
def forbidden():
    return "403 Forbidden — Доступ запрещён", 403

@app.route("/method_not_allowed")
def method_not_allowed():
    return "405 Method Not Allowed — Метод не разрешён", 405

@app.route("/im_a_teapot")
def im_a_teapot():
    return "418 I'm a teapot — Я чайник", 418


log_404 = []  

@app.errorhandler(404)
def not_found(err):
    import datetime
    client_ip = request.remote_addr
    url = request.url
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_404.append((time, client_ip, url))

    log_html = """
    <table border="1" cellpadding="5" cellspacing="0" style="margin:20px auto; border-collapse:collapse;">
        <tr>
            <th>Дата и время</th>
            <th>IP-адрес</th>
            <th>Запрошенный адрес</th>
        </tr>
    """
    for entry in log_404:
        log_html += "<tr><td>" + entry[0] + "</td><td>" + entry[1] + "</td><td>" + entry[2] + "</td></tr>"
    log_html += "</table>"

    return """<!doctype html>
<html>
    <head>
        <title>404 Not Found — Страница не найдена</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                text-align: center; 
                background-color: #f8f8f8; 
                color: #333;
            }
            h1 { 
                color: #e74c3c; 
                margin-top: 30px;
            }
            p { 
                font-size: 18px; 
            }
            img { 
                width: 300px; 
                margin: 20px 0;
            }
            a {
                display: inline-block;
                margin-top: 20px;
                text-decoration: none;
                color: #2980b9;
                font-weight: bold;
            }
            a:hover {
                text-decoration: underline;
            }
            table {
                width: 80%;
                border: 1px solid #ccc;
            }
            th {
                background-color: #eee;
            }
        </style>
    </head>
    <body>
        <h1>404 — Ой! Такой страницы нет</h1>
        <p>IP-адрес: """ + client_ip + """</p>
        <p>Дата и время: """ + time + """</p>
        <p>Вы пытались открыть: """ + url + """</p>
        <p><a href="/">Вернуться на главную</a></p>

        <h2>Журнал обращений</h2>
        """ + log_html + """
        <img src='""" + url_for("static", filename="lab1/404.png") + """' alt="404">
    </body>
</html>""", 404



@app.route("/cause_error")
def cause_error():
    x = 1 / 0
    return "Это никогда не выполнится"

@app.errorhandler(500)
def internal_error(err):
    return """<!doctype html>
<html>
    <head>
        <title>500 Внутренняя ошибка сервера</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                text-align: center; 
                background-color: #ffe6e6; 
                color: #333;
            }
            h1 { 
                color: #e74c3c; 
                margin-top: 50px;
            }
            p { 
                font-size: 18px; 
            }
            a {
                display: inline-block;
                margin-top: 20px;
                text-decoration: none;
                color: #2980b9;
                font-weight: bold;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>500 — Внутренняя ошибка сервера</h1>
        <p>Произошла ошибка на сервере. Попробуйте снова позднее.</p>
        <p><a href="/">Вернуться на главную</a></p>
    </body>
</html>""", 500

if __name__ == "__main__":
    app.run(debug=True)
