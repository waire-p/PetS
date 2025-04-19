from flask import Flask
from flask import render_template
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = '0yKJg9B62haFjq7K2gh1'


@app.route('/')
@app.route('/main_page')
def main_page():
    return render_template('base.html')


@app.route('/pets')
def pet_catalog():
    return render_template('pet_catalog.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
    db_session.global_init("db/PetSearch.db")
    db_sess = db_session.create_session()
