from datetime import datetime

import pymorphy3
from flask import Flask, abort
from flask import render_template
from flask import request, redirect
from pymorphy3 import MorphAnalyzer

from data import db_session
from data.animal_cards import PetCard
from data.create_age_table import create_table
from data.pet_age import PetAge
from data.user import User
from form.register import Register

app = Flask(__name__)
app.config['SECRET_KEY'] = '0yKJg9B62haFjq7K2gh1'
db_session.global_init("db/PetSearch.db")
USER_ID = None


def get_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    db_sess.close()
    return user

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html')


@app.route('/')
def main_page():
    user_now = get_user(USER_ID)
    create_table()
    return (render_template('base.html', user_now=user_now)
            and render_template('main.html', user_now=user_now))


@app.route('/pets')
def pet_catalog():
    user_now = get_user(USER_ID)
    morph = MorphAnalyzer()
    db_sess = db_session.create_session()
    cards = []
    page = request.args.get('page', 1, type=int)
    per_page = 12
    total_items = len(db_sess.query(PetCard).all())
    total_pages = (total_items + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    for card in db_sess.query(PetCard).order_by(PetCard.created_date.desc()).all()[start:end]:
        about = card.about
        age_value, age_id = card.age_value, card.age_id
        age_units_name = ''
        for name in db_sess.query(PetAge).all():
            if name.id == age_id:
                age_units_name = name.age
                break
        res = morph.parse(str(age_units_name))[0]
        age = str(age_value) + ' ' + res.make_agree_with_number(age_value).word
        if len(about) >= 65:
            about = card.about[:63] + '...'
        cards.append({'id':card.id, 'name': card.name, 'age': age, 'about': about, 'gender': card.gender})
    return render_template('pet_catalog.html', user_now=user_now, cards=cards, page=page, total_pages=total_pages)


@app.route('/about')
def about():
    user_now = get_user(USER_ID)
    with open('data/about.txt', encoding='utf-8') as file:
        about_text = file.read()
    return render_template('about.html', about_text=about_text, user_now=user_now)


@app.route('/articles')
def articles():
    user_now = get_user(USER_ID)
    articles = [
        {
            "title": "Как подготовить дом к появлению питомца",
            "summary": "Полезные советы перед тем, как взять щенка.",
            "url": "https://ru.wikihow.com/%D0%BF%D0%BE%D0%B4%D0%B3%D0%BE%D1%82%D0%BE%D0%B2%D0%B8%D1%82%D1%8C%D1%81%D1%8F-%D0%BA-%D0%BF%D0%BE%D1%8F%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8E-%D1%89%D0%B5%D0%BD%D0%BA%D0%B0-%D1%83-%D0%B2%D0%B0%D1%81-%D0%B4%D0%BE%D0%BC%D0%B0"
        },
        {
            "title": "Почему важно забирать животных из приюта",
            "summary": "Аргументы в пользу усыновления, а не покупки.",
            "url": "https://harpersbazaar.kz/10-prichin-zabrat-zhivotnoe-iz-prijuta/"
        },
        {
            "title": "Как завести котёнка",
            "summary": "Полезные советы перед тем, как взять щенка.",
            "url": "https://www.hillspet.ru/cat-care/new-pet-parent/bringing-home-and-raising-your-new-kitten/"
        },
        {
            "title": "Что нужно знать, перед тем как завести кошку",
            "summary": "Дополнительные советы.",
            "url": "https://www.royalcanin.com/ua/ru-ua/cats/thinking-of-getting-a-cat/things-to-consider-before-getting-a-cat/"
        },
        {
            "title": "Как завести попугая",
            "summary": "Советы для тех кто решился взять попугая.",
            "url": "https://magizoo.ru/stati/popugai/chto-nuzhno-znat-prezhde-chem-zavesti-popugaya/"
        },
        {
            "title": "Что нужно знать прежде, чем завести экзотическое животное?",
            "summary": "Советы перед тем как брать какое-либо живтное.",
            "url": "https://zoo-galereya.ru/articles/chto-nuzhno-znat-prezhde-chem-zavesti-ekzoticheskoe-zhivotnoe_art.html/"
        }
    ]
    return render_template("articles.html", articles=articles, user_now=user_now)


@app.route('/pets/<int:card_id>', methods=['GET'])
def pet_card(card_id):
    if request.method == 'GET':
        user_now = get_user(USER_ID)
        morph = pymorphy3.MorphAnalyzer()
        db_sess = db_session.create_session()
        for card in db_sess.query(PetCard).all():
            if card_id == card.id:
                id = card.user_id
                user = db_sess.query(User).filter(User.id == id).first()
                age_value, age_id = card.age_value, card.age_id
                age_units_name = ''
                for name in db_sess.query(PetAge).all():
                    if name.id == age_id:
                        age_units_name = name.age
                        break
                res = morph.parse(str(age_units_name))[0]
                age = str(age_value) + ' ' + res.make_agree_with_number(age_value).word
                if user.phone == 'not phone':
                    phone = 'Данные отсутствуют'
                d = {'name': card.name, 'age': age, 'gender': card.gender,
                     'vaccinations': card.vaccinations, 'diseases': card.diseases, 'about': card.about,
                     'phone': phone, 'email': user.email}
                creator_id = str(user).split()[2]
                return render_template('pet_card.html', **d, user_id = creator_id, user_now=user_now)
        return render_template('pet_error.html', user_now=user_now)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global USER_ID
    if request.method == "POST":
        email = request.form.get("email")  # Получаем email из формы
        password = request.form.get("password")  # Получаем пароль
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == email).first()
        if not user:
            return render_template('login.html', message="Почта не зарегистрирована")
        if not user.check_password(password):
            return render_template('login.html', message="Неверный пароль")
        USER_ID = user.id
        return redirect("/")
    return render_template('login.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    global USER_ID
    form = Register()
    user_now = get_user(USER_ID)
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("register.html", user_now=user_now, form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form, message="Пользователь уже зарегистрирован")
        if not form.phone.data:
            user = User(login=form.name.data, email=form.email.data, phone="not phone")
        else:
            user = User(login=form.name.data, email=form.email.data, phone=form.phone.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        user_in_bd = db_sess.query(User).filter(User.email == user.email).first()
        USER_ID = user_in_bd.id
        db_sess.commit()
        return redirect("/")
    return render_template("register.html", user_now=user_now, form=form)


@app.route("/profile")
def profile():
    morph = MorphAnalyzer()
    user_now = get_user(USER_ID)
    db_sess = db_session.create_session()

    cards = []
    page = request.args.get('page', 1, type=int)
    per_page = 12
    total_items = len(db_sess.query(PetCard).filter(PetCard.user_id == USER_ID).all())
    total_pages = (total_items + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    for card in db_sess.query(PetCard).order_by(PetCard.created_date.desc()).filter(PetCard.user_id == USER_ID).all()[start:end]:
        about = card.about
        age_value, age_id = card.age_value, card.age_id
        age_units_name = ''
        for name in db_sess.query(PetAge).all():
            if name.id == age_id:
                age_units_name = name.age
                break
        res = morph.parse(str(age_units_name))[0]
        age = str(age_value) + ' ' + res.make_agree_with_number(age_value).word
        if len(about) >= 65:
            about = card.about[:63] + '...'
        cards.append({'id': card.id, 'name': card.name, 'age': age, 'about': about, 'gender': card.gender})
    return render_template('profile.html', user_now=user_now, cards=cards, page=page,
                           total_pages=total_pages, user=user_now)


@app.route("/exit")
def exit():
    global USER_ID
    USER_ID = None
    return redirect("/")

@app.route('/pets/<int:card_id>/edit_card', methods=['GET', 'POST'])
def edit_card(card_id):
    user_now = get_user(USER_ID)
    db_sess = db_session.create_session()
    card =  db_sess.query(PetCard).filter(PetCard.id == card_id).first()
    user = db_sess.query(User).filter(User.id == USER_ID).first()

    if request.method == "POST" and user.id == card.user_id:
        if request.form.get("name") != '':
            card.name = request.form.get("name") # Получаем имя питомца
        if request.form.get('age2') != '':
            card.age_id = int(request.form.get('age2'))
        if request.form.get("age1") != '':
            card.age_value = int(request.form.get("age1"))  # Получаем возраст
        if request.form.get("gender"):
            card.gender = request.form.get("gender")  # Получаем пол животного
        vac = request.form.get("vaccinations")  # Получаем информацию о прививках
        dis = request.form.get("diseases")  # Получаем инфу о болезнях
        if vac.strip() != '':
            card.vaccinations = vac
        if dis.strip() != '':
            card.diseases = dis
        if request.form.get("about") != '':
            card.about = request.form.get("about")  # Получаем доп. инфу о животном
        db_sess.merge(card)
        db_sess.commit()
        return redirect("/")
    elif request.method == 'GET' and user.id == card.user_id:
        if card:
            return render_template('edit_card.html', user_now=user_now, card_id=card_id)
        else:
            abort(404)
    elif user.id != card.user_id:
        return render_template('perm_error.html')


@app.route('/pets/create_card', methods=['GET', 'POST'])
def create_card():
    user_now = get_user(USER_ID)
    print(user_now)
    if request.method == "POST":
        db_sess = db_session.create_session()
        card = PetCard()
        card.user_id = USER_ID
        card.name = request.form.get("name")  # Получаем имя питомца
        card.age_id = int(request.form.get('age2'))
        card.age_value = int(request.form.get("age1"))# Получаем возраст
        card.gender = request.form.get("gender")  # Получаем пол животного
        vac = request.form.get("vaccinations")  # Получаем информацию о прививках
        dis = request.form.get("diseases")  # Получаем инфу о болезнях
        if vac.strip() != '':
            card.vaccinations = vac
        if dis.strip() != '':
            card.diseases = dis
        card.about = request.form.get("about")  # Получаем доп. инфу о животном
        date = datetime.today()
        card.created_date = date
        db_sess.add(card)
        db_sess.commit()
        return redirect("/")
    elif request.method == 'GET':
        return render_template('create_card.html', user_now=user_now)


@app.route('/privacy')
def privacy():
    user_now = get_user(USER_ID)
    return render_template('privacy.html', user_now=user_now)


@app.route('/rules')
def rules():
    user_now = get_user(USER_ID)
    return render_template('rules.html', user_now=user_now)



@app.route('/pets/<int:card_id>/delete_card', methods=['GET', 'POST'])
def delete_card(card_id):
    user_now = get_user(USER_ID)
    db_sess = db_session.create_session()
    obj = db_sess.query(PetCard).filter(PetCard.id == card_id).first()
    user = db_sess.query(User).filter(User.id ==  USER_ID).first()

    if request.method == 'GET' and user.id == obj.user_id:
        return render_template('delete_card.html', user_now=user_now)
    elif 'yes' in request.form and user.id == obj.user_id:
        if obj:
            db_sess.delete(obj)
            db_sess.commit()
            return redirect("/")
        else:
            return abort(404)
    elif 'no'in request.form and user.id == obj.user_id:
        return  redirect('/profile')
    elif user.id != obj.user_id:
        return render_template('perm_error.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
    db_session.global_init("db/PetSearch.db")
    create_table()
    db_sess = db_session.create_session()