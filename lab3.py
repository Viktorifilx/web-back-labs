from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint ('lab3', __name__)

@lab3.route ('/lab3/')
def lab():
    name = request.cookies.get('name') or 'аноним'
    age = request.cookies.get('age') or 'не указан'
    name_color = request.cookies.get('name_color') or 'inherit'
    return render_template('lab3/lab3.html', name=name, name_color = name_color, age=age)


@lab3.route ('/lab3/cookie')
def cookie():
    resp = make_response (redirect ('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route ('/lab3/del_cookie')
def del_cookie():
    resp = make_response (redirect ('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors ['user'] = 'Заполните поле'
 
    age = request.args.get('age') 
    if age == '':
        errors ['age'] = 'Заполните поле'

    sex = request.args.get('sex') 
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template ('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')

    # Пусть кофе стоит 120 рублей, чёрный чай — 80 рублей, зелёный — 70 рублей.
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    # Добавка молока удорожает напиток на 30 рублей, а сахара — на 10.
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template ('lab3/pay.html', price=price)

@lab3.route('/lab3/thanks')
def thanks():
    price = request.args.get('price', default='—')
    return render_template('lab3/thanks.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')  
    bold = request.args.get('bold')

    if color or bg_color:
        resp = make_response(redirect('/lab3/settings'))

        if color:
            resp.delete_cookie('color', path='/lab3/settings')
            resp.delete_cookie('color', path='/lab3')
            resp.set_cookie('color', color, path='/', max_age=31536000)

        if bg_color:
            resp.delete_cookie('bg_color', path='/lab3/settings')
            resp.delete_cookie('bg_color', path='/lab3')
            resp.set_cookie('bg_color', bg_color, path='/', max_age=31536000)

        if font_size:
            resp.delete_cookie('font_size', path='/lab3/settings')
            resp.delete_cookie('font_size', path='/lab3')
            resp.set_cookie('font_size', font_size, path='/', max_age=31536000)

        if bold == 'on':
            resp.delete_cookie('bold', path='/lab3/settings')
            resp.delete_cookie('bold', path='/lab3')
            resp.set_cookie('bold', '1', path='/', max_age=31536000)

        return resp 

    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    bold = request.cookies.get('bold')
    return render_template('lab3/settings.html', color=color, bg_color=bg_color)


@lab3.route('/lab3/ticket')
def ticket():

    if not request.args:
        return render_template('lab3/ticket.html', errors={}, data={})

    errors = {}

    fio       = (request.args.get('fio') or '').strip()
    polka     = request.args.get('polka')  
    linen     = request.args.get('linen') == 'on'
    baggage   = request.args.get('baggage') == 'on'
    insurance = request.args.get('insurance') == 'on'
    age_raw   = (request.args.get('age') or '').strip()
    from_city = (request.args.get('from_city') or '').strip()
    to_city   = (request.args.get('to_city') or '').strip()
    date      = request.args.get('date') or ''

    if not fio:
        errors['fio'] = 'Укажите ФИО'
    if not polka:
        errors['polka'] = 'Выберите полку'
    try:
        age = int(age_raw)
        if age < 1 or age > 120:
            errors['age'] = 'Возраст от 1 до 120'
    except ValueError:
        errors['age'] = 'Возраст задайте числом'
        age = 0

    if not from_city:
        errors['from_city'] = 'Укажите пункт выезда'
    if not to_city:
        errors['to_city'] = 'Укажите пункт назначения'
    if not date:
        errors['date'] = 'Укажите дату поездки'

    data = {
        'fio': fio, 'polka': polka, 'linen': linen, 'baggage': baggage,
        'insurance': insurance, 'age': age_raw, 'from_city': from_city,
        'to_city': to_city, 'date': date
    }

    if errors:
        return render_template('lab3/ticket.html', errors=errors, data=data)

    is_child = age < 18
    price = 700 if is_child else 1000
    if polka in ('нижняя', 'нижняя боковая'):
        price += 100
    if linen:
        price += 75
    if baggage:
        price += 250
    if insurance:
        price += 150

    return render_template(
        'lab3/ticket_result.html',
        fio=fio, polka=polka, linen=linen, baggage=baggage, insurance=insurance,
        age=age, from_city=from_city, to_city=to_city, date=date,
        is_child=is_child, price=price
    )


    # --- каталог айфонов (простая структура) ---
PRODUCTS = [
    {"name": "iPhone SE (2022) 64GB",      "price": 39990,  "brand": "Apple", "color": "midnight"},
    {"name": "iPhone SE (2022) 128GB",     "price": 44990,  "brand": "Apple", "color": "starlight"},
    {"name": "iPhone 11 64GB",             "price": 49990,  "brand": "Apple", "color": "чёрный"},
    {"name": "iPhone 12 mini 128GB",       "price": 59990,  "brand": "Apple", "color": "синий"},
    {"name": "iPhone 12 64GB",             "price": 57990,  "brand": "Apple", "color": "фиолетовый"},
    {"name": "iPhone 12 128GB",            "price": 64990,  "brand": "Apple", "color": "зелёный"},
    {"name": "iPhone 13 mini 128GB",       "price": 69990,  "brand": "Apple", "color": "(PRODUCT)RED"},
    {"name": "iPhone 13 128GB",            "price": 74990,  "brand": "Apple", "color": "синий"},
    {"name": "iPhone 13 256GB",            "price": 84990,  "brand": "Apple", "color": "розовый"},
    {"name": "iPhone 13 Pro 128GB",        "price": 89990,  "brand": "Apple", "color": "graphite"},
    {"name": "iPhone 13 Pro Max 128GB",    "price": 99990,  "brand": "Apple", "color": "silver"},
    {"name": "iPhone 14 128GB",            "price": 79990,  "brand": "Apple", "color": "фиолетовый"},
    {"name": "iPhone 14 256GB",            "price": 92990,  "brand": "Apple", "color": "синий"},
    {"name": "iPhone 14 Plus 128GB",       "price": 89990,  "brand": "Apple", "color": "midnight"},
    {"name": "iPhone 14 Pro 128GB",        "price": 109990, "brand": "Apple", "color": "space black"},
    {"name": "iPhone 14 Pro Max 256GB",    "price": 129990, "brand": "Apple", "color": "deep purple"},
    {"name": "iPhone 15 128GB",            "price": 94990,  "brand": "Apple", "color": "розовый"},
    {"name": "iPhone 15 256GB",            "price": 104990, "brand": "Apple", "color": "жёлтый"},
    {"name": "iPhone 15 Plus 128GB",       "price": 104990, "brand": "Apple", "color": "голубой"},
    {"name": "iPhone 15 Pro 256GB",        "price": 129990, "brand": "Apple", "color": "natural titanium"},
    {"name": "iPhone 15 Pro 512GB",        "price": 159990, "brand": "Apple", "color": "blue titanium"},
    {"name": "iPhone 15 Pro Max 256GB",    "price": 149990, "brand": "Apple", "color": "black titanium"},
]


@lab3.route('/lab3/shop')
def shop():
    min_all = min(p['price'] for p in PRODUCTS)
    max_all = max(p['price'] for p in PRODUCTS)

    if 'reset' in request.args:
        resp = make_response(redirect('/lab3/shop'))
        resp.delete_cookie('shop_min_price', path='/')
        resp.delete_cookie('shop_max_price', path='/')
        return resp

    qmin = request.args.get('min')
    qmax = request.args.get('max')
    qmin = None if qmin is None or qmin == '' else qmin
    qmax = None if qmax is None or qmax == '' else qmax

    if qmin is None:
        qmin = request.cookies.get('shop_min_price')
    if qmax is None:
        qmax = request.cookies.get('shop_max_price')

    try:
        qmin = int(qmin) if qmin is not None else None
    except:
        qmin = None
    try:
        qmax = int(qmax) if qmax is not None else None
    except:
        qmax = None

    if qmin is not None and qmax is not None and qmin > qmax:
        qmin, qmax = qmax, qmin

    result = []
    for p in PRODUCTS:
        price = p['price']
        if qmin is not None and price < qmin:
            continue
        if qmax is not None and price > qmax:
            continue
        result.append(p)

    if 'min' in request.args or 'max' in request.args:
        resp = make_response(render_template(
            'lab3/shop.html',
            min_all=min_all, max_all=max_all,
            min_value=qmin, max_value=qmax,
            items=result
        ))
        if qmin is not None:
            resp.set_cookie('shop_min_price', str(qmin), max_age=31536000, path='/')
        else:
            resp.delete_cookie('shop_min_price', path='/')
        if qmax is not None:
            resp.set_cookie('shop_max_price', str(qmax), max_age=31536000, path='/')
        else:
            resp.delete_cookie('shop_max_price', path='/')
        return resp

    return render_template(
        'lab3/shop.html',
        min_all=min_all, max_all=max_all,
        min_value=qmin, max_value=qmax,
        items=result
    )

