import sqlalchemy
from flask import Flask
from flask import render_template
from sqlalchemy.orm import query
from data import db_session
from data.animal_cards import PetCard

app = Flask(__name__)
app.config['SECRET_KEY'] = '0yKJg9B62haFjq7K2gh1'


@app.route('/')
def main_page():
    return render_template('base.html') and render_template('main.html')


@app.route('/pets')
def pet_catalog():

    #posts = sqlalchemy.paginate(query, page=1, per_page=20, error_out=False).items
    return render_template('pet_catalog.html')


@app.route('/about')
def about():
    with open('data/about.txt', encoding='utf-8') as file:
        about_text = file.read()
    return render_template('about.html', about_text=about_text)


@app.route('/articles')
def articles():
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
        }
    ]
    return render_template("articles.html", articles=articles)


@app.route('/pets/<card_id>')
def pet_card(card_id):
    card = db_sess.query(PetCard).filter(PetCard.id == int(card_id)).first()
    return render_template('pet_card.html', id=card.id)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
    db_session.global_init("db/PetSearch.db")
    db_sess = db_session.create_session()