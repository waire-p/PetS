from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TelField
from wtforms.validators import DataRequired, Regexp, Optional


class Register(FlaskForm):
    name = StringField("Имя пользователя", validators=[DataRequired()])
    email = EmailField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_again = PasswordField("Повторите пароль", validators=[DataRequired()])
    phone = StringField('Номер телефона',
                        validators=[Optional(), Regexp(r'^\+7\d{10}$', message="Формат: +79991234567")])
    submit = SubmitField("Зарегистрироваться")