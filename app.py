from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404

@app.route("/")
@app.route("/web")
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

@app.route("/author")
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

@app.route("/image")
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

@app.route('/counter')
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

@app.route('/reset_counter')
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

@app.route('/info')
def info():
    return redirect("/author")


