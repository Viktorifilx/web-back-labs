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
