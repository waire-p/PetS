from datetime import datetime

from flask import Flask
from flask import render_template
import pymorphy3
from data import db_session
from data.animal_cards import PetCard
from data.user import User
from flask import request, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = '0yKJg9B62haFjq7K2gh1'
db_session.global_init("db/PetSearch.db")
USER_NOW = None


@app.route('/')
def main_page():
    return render_template('base.html', user_now=USER_NOW)


@app.route('/pets')
def pet_catalog():
    # posts = sqlalchemy.paginate(query, page=1, per_page=20, error_out=False).items
    return render_template('pet_catalog.html', user_now=USER_NOW)


@app.route('/pets/<int:card_id>', methods=['GET'])
def pet_card(card_id):
    if request.method == 'GET':
        db_sess = db_session.create_session()
        for card in db_sess.query(PetCard).all():
            if card_id == card.id:
                d = {'name':card.name, 'age': card.age, 'gender': card.gender,
                        'vaccinations':card.vaccinations, 'diseases': card.diseases, 'about':card.about}
                return render_template('pet_card.html', **d)
        return render_template('pet_error.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global USER_NOW
    if request.method == "POST":
        email = request.form.get("email")  # Получаем email из формы
        password = request.form.get("password")  # Получаем пароль
        print("Email:", email)
        print("Пароль:", password)
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == email).first()
        if not user:
            return render_template('login.html', message="Неверный пароль или email")
        USER_NOW = user
        return redirect("/")
    return render_template('login.html')


@app.route('/create_card', methods=['GET', 'POST'])
def create_card():
    global USER_NOW
    morph = pymorphy3.MorphAnalyzer()
    if request.method == "POST":
        #photo = request.form.get("file")
        db_sess = db_session.create_session()
        card = PetCard()

        for user in db_sess.query(User).all():
            if user.login == str(USER_NOW).split()[2]:
                card.user_id = user.id
                card.contacts = user.phone
                break
        card.name = request.form.get("name")  # Получаем имя питомца
        age_time_units = morph.parse(request.form.get('age2'))[0]
        age_number = request.form.get("age1")
        card.age =  str(age_number) + ' ' + age_time_units.make_agree_with_number(int(age_number)).word  # Получаем возраст
        card.gender = request.form.get("gender")  # Получаем пол животного
        vac = request.form.get("vaccinations") # Получаем информацию о прививках
        dis = request.form.get("diseases")  # Получаем инфу о болезнях
        if vac.strip() != '':
            card.vaccinations =  vac
        if dis.strip() != '':
            card.diseases = dis
        card.about = request.form.get("about")  # Получаем доп. инфу о животном
        card.created_date = datetime.today()
        db_sess.add(card)
        db_sess.commit()
        return redirect("/")
    elif request.method == 'GET':
        return render_template('create_card.html', user_now=USER_NOW)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
    db_session.global_init("db/PetSearch.db")
