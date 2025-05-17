import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
import datetime

class PetCard(SqlAlchemyBase):
    __tablename__ = 'cards'


    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String)
    age_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("pet_age.id"), nullable=False)
    age_value = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    gender = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    vaccinations = sqlalchemy.Column(sqlalchemy.String, default='Данные отсутствуют')
    diseases = sqlalchemy.Column(sqlalchemy.String, default='Данные отсутствуют')
    about = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.datetime.now)
    user = orm.relationship('User')
    pet_age = orm.relationship("PetAge")