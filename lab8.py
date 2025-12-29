from flask import Blueprint, render_template

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def main():
    return render_template('lab8/lab8.html', username='Anonymous')


@lab8.route('/lab8/login')
def login():
    return "<h1>Lab8: Вход</h1>"


@lab8.route('/lab8/register')
def register():
    return "<h1>Lab8: Регистрация</h1>"


@lab8.route('/lab8/articles')
def articles():
    return "<h1>Lab8: Список статей</h1>"


@lab8.route('/lab8/create')
def create():
    return "<h1>Lab8: Создать статью</h1>"
