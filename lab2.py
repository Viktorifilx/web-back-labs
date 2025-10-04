from flask import Blueprint, redirect, url_for, render_template
lab2 = Blueprint ('lab2', __name__)

@app.route ('/lab2/a')
def a():
    return 'без слэша'

@app.route ('/lab2/a/')
def a2():
    return 'со слэшем'


flowers = [
    {"name": "роза",      "price": 300},
    {"name": "тюльпан",   "price": 310},
    {"name": "незабудка", "price": 320},
    {"name": "ромашка",   "price": 330},
    {"name": "георгин",   "price": 300},
    {"name": "гладиолус", "price": 310},
]


@app.route('/lab2/flowers')
def flowers_page():
    return render_template('flowers.html', flowers=flowers)

@app.route('/lab2/add_flower/<name>/<int:price>')
def add_flower(name, price):
    name = name.strip()
    if not name:
        return "вы не задали имя цветка", 400
    flowers.append({"name": name, "price": price})
    return redirect('/lab2/flowers')

@app.route('/lab2/del_flower/<int:flower_id>')
def del_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flowers):
        abort(404)
    del flowers[flower_id]
    return redirect('/lab2/flowers')

@app.route('/lab2/del_all_flowers')
def del_all_flowers():
    flowers.clear()
    return redirect('/lab2/flowers')



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


@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return '''
<!doctype html>
<html>
  <body>
    <h1>Расчёт с параметрами:</h1>
    <p>''' + str(a) + ' + ' + str(b) + ' = ' + str(a + b) + '''</p>
    <p>''' + str(a) + ' - ' + str(b) + ' = ' + str(a - b) + '''</p>
    <p>''' + str(a) + ' * ' + str(b) + ' = ' + str(a * b) + '''</p>
    <p>''' + str(a) + ' / ' + str(b) + ' = ' + str(round(a / b, 2)) + '''</p>
    <p>''' + str(a) + '^' + str(b) + ' = ' + str(a ** b) + '''</p>
  </body>
</html>
'''

@app.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_redirect_to_b1(a):
    return redirect('/lab2/calc/' + str(a) + '/1')


books = [
    {"author": "Достоевский Ф.М.", "title": "Преступление и наказание", "genre": "Роман", "pages": 672},
    {"author": "Толстой Л.Н.", "title": "Война и мир", "genre": "Исторический роман", "pages": 1225},
    {"author": "Булгаков М.А.", "title": "Мастер и Маргарита", "genre": "Фэнтези", "pages": 480},
    {"author": "Пушкин А.С.", "title": "Евгений Онегин", "genre": "Поэма", "pages": 224},
    {"author": "Лермонтов М.Ю.", "title": "Герой нашего времени", "genre": "Роман", "pages": 320},
    {"author": "Оруэлл Дж.", "title": "1984", "genre": "Антиутопия", "pages": 352},
    {"author": "Киз Д.", "title": "Цветы для Элджернона", "genre": "Научная фантастика", "pages": 352},
    {"author": "Толкин Дж.Р.Р.", "title": "Хоббит", "genre": "Фэнтези", "pages": 310},
    {"author": "Роулинг Дж.К.", "title": "Гарри Поттер и философский камень", "genre": "Фэнтези", "pages": 384},
    {"author": "Верн Ж.", "title": "20 000 лье под водой", "genre": "Приключения", "pages": 416}
]

@app.route('/lab2/books')
def books_view():
    return render_template('books.html', books=books)

objects = [
    {"name": "клубника",           "img": "клубника.jpg",           "desc": "Сладкая и ароматная ягода."},
    {"name": "малина",             "img": "малина.jpg",             "desc": "Нежная ягода с кисло‑сладким вкусом."},
    {"name": "ежевика",            "img": "ежевика.jpg",            "desc": "Сочная тёмная ягода."},
    {"name": "голубика",           "img": "голубика.jpg",           "desc": "Мелкая синяя ягода, богата антиоксидантами."},
    {"name": "черника",            "img": "черника.jpg",            "desc": "Лесная ягода с насыщенным цветом."},
    {"name": "чёрная смородина",   "img": "черная смородина.jpg",   "desc": "Кисло‑сладкая, очень витаминная."},
    {"name": "красная смородина",  "img": "красная смородина.jpg",  "desc": "Прозрачные ягодки‑бусины."},
    {"name": "крыжовник",          "img": "крыжовник.jpg",          "desc": "Зелёные или красные колючие ягоды."},
    {"name": "брусника",           "img": "брусника.jpg",           "desc": "Кисловатая северная ягода."},
    {"name": "клюква",             "img": "клюква.jpg",             "desc": "Очень кислая, хороша для морсов."},
    {"name": "облепиха",           "img": "облепиха.jpg",           "desc": "Ярко‑оранжевая, маслянистая."},
    {"name": "вишня",              "img": "вишня.jpg",              "desc": "Косточковая ягода с насыщенным вкусом."},
    {"name": "черешня",            "img": "черешня.jpg",            "desc": "Сладкая родственница вишни."},
    {"name": "земляника",          "img": "земляника.jpg",          "desc": "Лесная сестра клубники."},
    {"name": "ирга",               "img": "ирга.jpg",               "desc": "Сладкая синеватая ягода."},
    {"name": "морошка",            "img": "морошка.jpg",            "desc": "Северная янтарная ягода."},
    {"name": "жимолость",          "img": "жимолость.jpg",          "desc": "Раннеспелая синяя ягода."},
    {"name": "барбарис",           "img": "барбарис.jpg",           "desc": "Кислые продолговатые ягодки."},
    {"name": "рябина",             "img": "рябина.jpg",             "desc": "Оранжево‑красные грозди."},
    {"name": "калина",             "img": "калина.jpg",             "desc": "Яркая красная ягода с терпким вкусом."}
]

@app.route('/lab2/gallery')
def gallery():
    return render_template('gallery.html', objects=objects)
