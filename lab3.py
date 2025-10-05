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

