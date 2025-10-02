from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404

@app.route("/")
@app.route("/index")
def index():
    name = "Филатова Виктория Михайловна"
    group = "ФБИ-34"
    course = "3 курс"
    year = "2025"

    return """<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        <nav>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
            </ul>
        </nav>
        <footer>
            <p>""" + name + """, """ + group + """, """ + course + """, """ + year + """</p>
        </footer>
    </body>
</html>"""

@app.route("/lab1")
def lab1():
    return """<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, 
        использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. 
        Относится к категории так называемых микрофреймворков — минималистичных 
        каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
        <p><a href="/">На главную</a></p>

        <h2>Список роутов</h2>
        <ul>
            <li><a href="/lab1/web">/lab1/web</a></li>
            <li><a href="/lab1/author">/lab1/author</a></li>
            <li><a href="/lab1/image">/lab1/image</a></li>
            <li><a href="/lab1/counter">/lab1/counter</a></li>
            <li><a href="/lab1/reset_counter">/lab1/reset_counter</a></li>
            <li><a href="/lab1/info">/lab1/info</a></li>
            <li><a href="/bad_request">/bad_request (400)</a></li>
            <li><a href="/unauthorized">/unauthorized (401)</a></li>
            <li><a href="/payment_required">/payment_required (402)</a></li>
            <li><a href="/forbidden">/forbidden (403)</a></li>
            <li><a href="/method_not_allowed">/method_not_allowed (405)</a></li>
            <li><a href="/im_a_teapot">/im_a_teapot (418)</a></li>
            <li><a href="/not_found">/not_found (404)</a></li>
            <li><a href="/cause_error">/cause_error (500)</a></li>
        </ul>

    </body>
</html>"""


@app.route("/lab1/web")
def web ():
    return """<!doctype html>
        <html>
           <body>
                <h1>web-сервер на flask</h1> 
                <p><a href="/author">Информация об авторе</a></p>
           </body>
        </html>""", 200, {
            "X-Server": "sample",
            'Content-Type': 'text/html; charset=utf-8'
        }

@app.route("/lab1/author")
def author():
    name = "Филатова Виктория Михайловна"
    group = "ФБИ-34"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/web">web</a>
            </body>
        </html>"""

@app.route("/lab1/image")
def image():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename = "lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="''' + path + '''">
    </body>
</html>
'''

count=0 

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + str(time) + ''' <br>
        Запрошенный адрес:  ''' + url + ''' <br>
        Ваш IP-адрес: ''' + client_ip + ''' <br>
        <p><a href="/reset_counter">Обнулить счётчик</a></p>
    </body>
</html>
'''

@app.route('/lab1/reset_counter')
def reset_counter():
    global count 
    count = 0
    return '''
<!doctype html>
<html>
    <body>
        <p>Счётчик очищен</p>
        <a href="/counter">Назад к счётчику</a>
    </body>
</html>
'''

@app.route('/lab1/info')
def info():
    return redirect("/lab1/author")


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
        <img src='""" + url_for("static", filename="404.png") + """' alt="404">
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


@app.route ('/lab2/a')
def a():
    return 'без слэша'

@app.route ('/lab2/a/')
def a2():
    return 'со слэшем'


flower_list = ['роза','тюльпан','незабудка','ромашка']

@app.route('/lab2/add_flower/')
def add_flower_missing():
    return "вы не задали имя цветка", 400


@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    name = name.strip()
    if name == "":
        return "вы не задали имя цветка", 400
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
  <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name}</p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p><a href="/lab2/flowers">Перейти к списку всех цветов</a></p>
  </body>
</html>
'''

@app.route('/lab2/flowers')
def all_flowers():
    return '''
<!doctype html>
<html>
  <body>
    <h1>Все цветы</h1>
    <p>Количество: ''' + str(len(flower_list)) + '''</p>
    <p>Полный список: ''' + ', '.join(flower_list) + '''</p>
  </body>
</html>
'''


@app.route('/lab2/flowers/<int:flower_id>')
def flower_by_id(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    name = flower_list[flower_id]
    return '''
<!doctype html>
<html>
  <body>
    <h1>Цветок №''' + str(flower_id) + '''</h1>
    <p>Название цветка: ''' + name + '''</p>
    <p><a href="/lab2/flowers"> Вернуться к списку всех цветов</a></p>
  </body>
</html>
'''


@app.route('/lab2/flowers/clear')
def clear_flowers():
    flower_list.clear()
    return '''
<!doctype html>
<html>
  <body>
    <h1>Список очищен</h1>
    <p>Все цветы удалены.</p>
    <p><a href="/lab2/flowers">Перейти к списку всех цветов</a></p>
  </body>
</html>
'''



@app.route ('/lab2/example')
def example():
    name  = ''
    group = 'ФБИ-34'
    course = ''
    lab_number = 2
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html', name=name, group=group,course = course,lab_number = lab_number, fruits = fruits )

@app.route ('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)
