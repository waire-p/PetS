import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class PetAge(SqlAlchemyBase):
    __tablename__ = 'pet_age'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    pet_card = orm.relationship('PetCard', back_populates='pet_age')
