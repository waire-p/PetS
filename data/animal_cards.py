import sqlalchemy
from .db_session import SqlAlchemyBase
import datetime

class PetCard(SqlAlchemyBase):
    __tablename__ = 'cards'


    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(""), nullable=False, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    age =  sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    gender = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    vaccinations = sqlalchemy.Column(sqlalchemy.String)
    diseases = sqlalchemy.Column(sqlalchemy.String)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.datetime.now )