from flask import Flask
from flask import render_template


app = Flask(__name__)

@app.route('/')
@app.route('/main_page')
def main_page():
    return render_template('base.html')


@app.route('/pets')
def pet_catalog():
    return render_template('pet_catalog.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')