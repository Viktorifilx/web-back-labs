from flask import Blueprint, redirect, url_for, request   # добавь request
import datetime                                           # добавь datetime

lab1 = Blueprint('lab1', __name__)



@lab1.route("/lab1")
def lab():
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


@lab1.route("/lab1/web")
def web ():
    return """<!doctype html>
        <html>
           <body>
                <h1>web-сервер на flask</h1> 
                <p><a href="/lab1/author">Информация об авторе</a></p>
           </body>
        </html>""", 200, {
            "X-Server": "sample",
            'Content-Type': 'text/html; charset=utf-8'
        }


@lab1.route("/lab1/author")
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
                <a href="/lab1/web">web</a>
            </body>
        </html>"""


@lab1.route("/lab1/image")
def image():
    path = url_for("static", filename="lab1/oak.jpg")
    css_path = url_for("static", filename="lab1/lab1.css")
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


@lab1.route('/lab1/counter')
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


@lab1.route('/lab1/reset_counter')
def reset_counter():
    global count 
    count = 0
    return '''
<!doctype html>
<html>
    <body>
        <p>Счётчик очищен</p>
        <a href="/lab1/counter">Назад к счётчику</a>
    </body>
</html>
'''


@lab1.route('/lab1/info')
def info():
    return redirect("/lab1/author")