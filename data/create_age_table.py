from data.pet_age import PetAge
from data import db_session


def create_table():
    db_sess = db_session.create_session()
    age_check = db_sess.query(PetAge).first()
    if age_check == None:
        age1 = PetAge()
        age2 = PetAge()
        age3 = PetAge()
        age4 = PetAge()
        age1.id = 1
        age1.age = 'день'
        age2.id = 2
        age2.age = 'неделя'
        age3.id = 3
        age3.age = 'месяц'
        age4.id = 4
        age4.age = 'год'
        db_sess.add(age1)
        db_sess.add(age2)
        db_sess.add(age3)
        db_sess.add(age4)
        db_sess.commit()


if __name__ == "__main__":
    create_table()
