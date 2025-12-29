from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, logout_user, login_required, current_user

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def main():
    if current_user.is_authenticated:
        return render_template('lab8/lab8.html', username=current_user.login)
    return render_template('lab8/lab8.html', username='Anonymous')

@lab8.route('/lab8/public')
def public_articles():
    public_articles_list = articles.query.filter_by(is_public=True).all()
    return render_template('lab8/public_articles.html', articles=public_articles_list)


@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember = request.form.get('remember') == 'on'  # Получаем значение чекбокса
    
    if not login_form or not password_form:
        return render_template('lab8/login.html', 
                              error='Логин и пароль должны быть заполнены')
    
    user = users.query.filter_by(login=login_form).first()
    
    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=remember)  # Используем значение чекбокса
            return redirect('/lab8/')
    
    return render_template('lab8/login.html', 
                          error='Ошибка входа: логин и/или пароль неверны')


@lab8.route('/lab8/search', methods=['GET', 'POST'])
def search_articles():
    if request.method == 'GET':
        return render_template('lab8/search.html')

    search_query = request.form.get('query', '').strip()

    if not search_query:
        return render_template('lab8/search.html', error='Введите поисковый запрос')

    # ищем по title ИЛИ по text (скобки важны)
    pattern = f'%{search_query}%'
    cond = (articles.title.ilike(pattern)) | (articles.article_text.ilike(pattern))

    if current_user.is_authenticated:
        # ВАЖНО: убрали login_id != current_user.id
        # Теперь ищем по публичным + по своим (и публичные свои тоже попадут)
        all_articles = articles.query.filter(
            cond,
            (articles.is_public == True) | (articles.login_id == current_user.id)
        ).all()
    else:
        all_articles = articles.query.filter(
            articles.is_public == True,
            cond
        ).all()

    return render_template(
        'lab8/search_results.html',
        articles=all_articles,
        query=search_query,
        count=len(all_articles)
    )


@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('lab8/register.html', error='Имя пользователя не должно быть пустым')
    if not password_form:
        return render_template('lab8/register.html', error='Пароль не должен быть пустым')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)

    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    login_user(new_user, remember=False)
    
    return redirect('/lab8/')


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')


@lab8.route('/lab8/articles')
@login_required
def articles_list():
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=user_articles)


@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    
    if not title or not article_text:
        return render_template('lab8/create_article.html', 
                              error='Название и текст статьи обязательны')
    
    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=article_text,
        is_favorite=False,
        is_public=True,
        likes=0
    )
    
    db.session.add(new_article)
    db.session.commit()
    
    return redirect('/lab8/articles')

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)
    
    if article.login_id != current_user.id:
        return "У вас нет прав на редактирование этой статьи", 403
    
    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = request.form.get('is_favorite') == 'on'
    is_public = request.form.get('is_public') == 'on'
    
    if not title or not article_text:
        return render_template('lab8/edit_article.html', 
                              article=article,
                              error='Название и текст статьи обязательны')
    
    article.title = title
    article.article_text = article_text
    article.is_favorite = is_favorite
    article.is_public = is_public
    
    db.session.commit()
    
    return redirect('/lab8/articles')


@lab8.route('/lab8/delete/<int:article_id>')
@login_required
def delete_article(article_id):
    article = articles.query.get_or_404(article_id)
    
    if article.login_id != current_user.id:
        return "У вас нет прав на удаление этой статьи", 403
    
    db.session.delete(article)
    db.session.commit()
    
    return redirect('/lab8/articles')