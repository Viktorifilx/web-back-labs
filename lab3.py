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
