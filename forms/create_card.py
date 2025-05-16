from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired


class CreatePetCard(FlaskForm):

    name = StringField('Имя', validators=[DataRequired()])
    age1 = IntegerField('Возраст', validators=[DataRequired()])
    age2 = SelectField('Возраст', validators=[DataRequired()])
    gender = RadioField('Пол', validators=[DataRequired()])
    vaccinations = StringField('Прививки', validators=[DataRequired()])
    diseases = StringField('Болезни', validators=[DataRequired()])
    about = StringField('Описание', validators=[DataRequired()])
    submit = SubmitField('Создать объявление')

