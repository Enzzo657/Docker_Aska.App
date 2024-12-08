from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import secrets
import os
import bcrypt
# Загружаем переменные из .env файла
load_dotenv()

# Создание приложения Flask
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Ключ для работы с сессиями
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://enzzo:123456@192.168.0.106/mybase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация SQLAlchemy
db = SQLAlchemy(app)

# Модель таблицы пользователей
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    hash_fact = db.Column(db.String(200), nullable=False)  # Хэш двухфакторной аутентификации
    backup_codes = db.Column(db.Text, nullable=True)  # Резервные коды (хранятся как текст)

# Предустановленный логин и пароль администратора
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = os.getenv('ADMIN_PASSWORD_HASH')

# Проверка пароля администратора
def check_admin_password(password):
    return bcrypt.checkpw(password.encode('utf-8'), ADMIN_PASSWORD_HASH.encode('utf-8'))

# Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Проверяем имя пользователя и хэш пароля
        if username == ADMIN_USERNAME and check_admin_password(password):
            session['logged_in'] = True  # Устанавливаем флаг аутентификации в сессии
            flash('Успешный вход!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверный логин или пароль.', 'danger')
    return render_template('login.html')

# Главная страница (поиск пользователей и добавление новых)
@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect('/login')  # Перенаправляем на страницу входа, если не авторизован

    users = None

    if request.method == 'POST':
        # Обработка формы поиска
        search_term = request.form.get('search')
        if search_term.isdigit():
            # Поиск по ID
            users = Client.query.filter_by(id=int(search_term)).all()
        else:
            # Поиск по имени
            users = Client.query.filter(Client.name.ilike(f'%{search_term}%')).all()
    return render_template('index.html', users=users)

# Добавление нового пользователя
@app.route('/add', methods=['POST'])
def add_user():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Извлекаем значения из формы
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        hash_fact = request.form.get('hash_fact')
        backup_codes = request.form.get('backup_codes')

        if name and email and password and hash_fact and backup_codes:
            # Создаем нового пользователя
            new_user = Client(
                name=name,
                email=email,
                password=password,
                hash_fact=hash_fact,
                backup_codes=backup_codes
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Пользователь успешно добавлен!', 'success')

            return redirect(url_for('index'))

        flash('Не удалось добавить пользователя. Проверьте данные.', 'danger')

# Выход из системы
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)  # Удаляем информацию о входе из сессии
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('login'))

# Запуск приложения
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создаем все таблицы (если их нет)
    app.run(host='0.0.0.0', port=8000, debug=True)
