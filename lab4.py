from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint ('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods = ['POST'])
def div ():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error = 'Оба поля должны быть заполнены!')

    x1 = int (x1)
    x2 = int (x2)

    if x2 == 0:
        return render_template('lab4/div.html', error='Деление на ноль невозможно!')
        
    result = x1/x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)
    

@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods = ['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error = 'Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2

    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)



@lab4.route('/lab4/add-form')
def add_form():
    return render_template('lab4/add-form.html')

@lab4.route('/lab4/add', methods=['POST'])
def add():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    # Если поле пустое — считаю как 0
    if x1 == '':
        x1 = 0
    if x2 == '':
        x2 = 0

    x1 = int(x1)
    x2 = int(x2)
    result = x1 + x2

    return render_template('lab4/add.html', x1=x1, x2=x2, result=result)



@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    # Если пустое поле — подставляю 1
    if x1 == '':
        x1 = 1
    if x2 == '':
        x2 = 1

    x1 = int(x1)
    x2 = int(x2)
    result = x1 * x2

    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def pow_func():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)

    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='0 в степени 0 не имеет смысла!')

    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)

tree_count = 0

@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count

    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')

    if operation == 'cut':
        tree_count -= 1
    elif operation == 'plant':
        tree_count += 1

    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < 10:
        tree_count += 1

    return redirect('/lab4/tree')

users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр Филатов', 'gender': 'мужской'},
    {'login': 'bob',  'password': '555', 'name': 'Борис Котов',        'gender': 'мужской'},
    {'login': 'kate', 'password': '999', 'name': 'Екатерина Смирнова', 'gender': 'женский'},
    {'login': 'anna', 'password': '777', 'name': 'Анна Иванова',       'gender': 'женский'}
]


@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'name' in session:
            return render_template('lab4/login.html', authorized=True, name=session['name'], gender=session['gender'])
        return render_template('lab4/login.html', authorized=False, login_value='', error=None)

    login = request.form.get('login')
    password = request.form.get('password')

    if login == '' or login is None:
        return render_template('lab4/login.html', authorized=False, login_value='', error='не введён логин')
    if password == '' or password is None:
        return render_template('lab4/login.html', authorized=False, login_value=login, error='не введён пароль')

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = user['login']; session['name'] = user['name']; session['gender'] = user['gender']
            return redirect('/lab4/login')

    return render_template('lab4/login.html', authorized=False, login_value=login, error='Неверные логин и/или пароль')


@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None); session.pop('name', None); session.pop('gender', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'GET':
        return render_template('lab4/fridge.html')

    temp = request.form.get('temperature')

    if temp == '':
        return render_template('lab4/fridge.html', error='ошибка: не задана температура')

    temp = int(temp)

    if temp < -12:
        return render_template('lab4/fridge.html', error='не удалось установить температуру — слишком низкое значение')

    if temp > -1:
        return render_template('lab4/fridge.html', error='не удалось установить температуру — слишком высокое значение')

    if temp >= -12 and temp <= -9:
        return render_template('lab4/fridge.html', message=f'Установлена температура: {temp}°C', snowflakes=3)

    if temp >= -8 and temp <= -5:
        return render_template('lab4/fridge.html', message=f'Установлена температура: {temp}°C', snowflakes=2)

    if temp >= -4 and temp <= -1:
        return render_template('lab4/fridge.html', message=f'Установлена температура: {temp}°C', snowflakes=1)


@lab4.route('/lab4/grain', methods=['GET', 'POST'])
def grain():
    if request.method == 'GET':
        return render_template('lab4/grain.html')

    grain_type = request.form.get('grain')
    weight = request.form.get('weight')

    if weight == '':
        return render_template('lab4/grain.html', error='ошибка: не указан вес')

    weight = float(weight)

    if weight <= 0:
        return render_template('lab4/grain.html', error='ошибка: вес должен быть больше 0')

    if weight > 100:
        return render_template('lab4/grain.html', error='такого объёма сейчас нет в наличии')

    if grain_type == 'ячмень':
        price = 12000
    elif grain_type == 'овёс':
        price = 8500
    elif grain_type == 'пшеница':
        price = 9000
    elif grain_type == 'рожь':
        price = 15000
    else:
        return render_template('lab4/grain.html', error='ошибка: не выбран вид зерна')

    total = price * weight
    discount_text = ''
    if weight > 10:
        discount = total * 0.1
        total = total - discount
        discount_text = f'применена скидка за большой объём: 10% ({int(discount)} руб.)'

    return render_template('lab4/grain.html', message='Заказ успешно сформирован.', grain=grain_type, weight=weight, total=int(total), discount_text=discount_text)


@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab4/register.html')

    name = request.form.get('name')
    login = request.form.get('login')
    password = request.form.get('password')
    confirm = request.form.get('confirm')
    gender = request.form.get('gender')

    if name == '' or login == '' or password == '' or confirm == '' or gender == '':
        return render_template('lab4/register.html', error='все поля должны быть заполнены')

    if password != confirm:
        return render_template('lab4/register.html', error='пароли не совпадают')

    for u in users:
        if u['login'] == login:
            return render_template('lab4/register.html', error='пользователь с таким логином уже существует')

    users.append({'login': login, 'password': password, 'name': name, 'gender': gender})
    return render_template('lab4/register.html', message='Регистрация прошла успешно')


@lab4.route('/lab4/users')
def users_list():
    if 'login' not in session:
        return redirect('/lab4/login')
    return render_template('lab4/users.html', users=users, current=session['login'])


@lab4.route('/lab4/users/delete', methods=['POST'])
def delete_me():
    if 'login' not in session:
        return redirect('/lab4/login')

    login = session['login']

    for i in range(len(users)):
        if users[i]['login'] == login:
            users.pop(i)
            break

    session.pop('login', None); session.pop('name', None); session.pop('gender', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/users/edit', methods=['GET', 'POST'])
def edit_me():
    if 'login' not in session:
        return redirect('/lab4/login')

    current_login = session['login']

    for u in users:
        if u['login'] == current_login:
            current_user = u
            break

    if request.method == 'GET':
        return render_template('lab4/edit_user.html', user=current_user)

    new_login = request.form.get('login')
    new_password = request.form.get('password')
    new_confirm = request.form.get('confirm')

    if new_name == '' or new_login == '':
        return render_template('lab4/edit_user.html', user=current_user, error='имя и логин не могут быть пустыми')

    if new_password == '' and new_confirm == '':
        current_user['name'] = new_name
        current_user['login'] = new_login
        session['name'] = new_name
        session['login'] = new_login
        return redirect('/lab4/users')

    if new_password != new_confirm:
        return render_template('lab4/edit_user.html', user=current_user, error='пароль и подтверждение не совпадают')

    current_user['name'] = new_name
    current_user['login'] = new_login
    current_user['password'] = new_password
    session['name'] = new_name
    session['login'] = new_login

    return redirect('/lab4/users')
