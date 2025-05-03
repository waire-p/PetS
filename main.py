import sqlalchemy
from flask import Flask
from flask import render_template
from sqlalchemy.orm import query
from data import db_session
from data.animal_cards import PetCard
from data.user import User
from flask import request, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = '0yKJg9B62haFjq7K2gh1'
db_session.global_init("db/PetSearch.db")
user_now = None


@app.route('/')
def main_page():
    return render_template('base.html', user_now=user_now)


@app.route('/pets')
def pet_catalog():

    #posts = sqlalchemy.paginate(query, page=1, per_page=20, error_out=False).items
    return render_template('pet_catalog.html', user_now=user_now)


@app.route('/pets/<card_id>')
def pet_card(card_id):
    card = db_sess.query(PetCard).filter(PetCard.id == int(card_id)).first()
    return render_template('pet_card.html', id=card.id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global user_now
    if request.method == "POST":
        email = request.form.get("email")  # Получаем email из формы
        password = request.form.get("password")  # Получаем пароль
        print("Email:", email)
        print("Пароль:", password)
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == email).first()
        if not user:
            return render_template('login.html', message="Неверный пароль или email")
        user_now = user
        return redirect("/")
    return render_template('login.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
    db_session.global_init("db/PetSearch.db")
    db_sess = db_session.create_session()