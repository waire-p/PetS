from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField, DateField
from wtforms.validators import DataRequired


class EditPetCard(FlaskForm):
    name = StringField('*Заголовок', validators=[DataRequired()])
    text = StringField('*Текст новости', validators=[DataRequired()])
    private = BooleanField('Сделать новость приватной')

