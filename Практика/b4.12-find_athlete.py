"""
Author: Vladimir Scherbinin
Модуль получает id пользователя и ищет
ближайшего к пользователю атлета по возрасту и росту
"""

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class User(Base):
	__tablename__ = "user"
	id = sa.Column(sa.Integer, primary_key=True)
	first_name = sa.Column(sa.Text)
	last_name = sa.Column(sa.Text)
	height = sa.Column(sa.Float)
	birthdate = sa.Column(sa.Text)

class Athelete(Base):
	__tablename__ = "athelete"
	id = sa.Column(sa.Integer, primary_key=True)
	birthdate = sa.Column(sa.Text)
	height = sa.Column(sa.Float)
	name = sa.Column(sa.Text)

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def get_user(id, session):
	query = session.query(User).filter(User.id == id)
	return query.first()

def nearest_by_birthday_athelete(user_birthdate, session):
	"""
	Нахождение ближайшего атлета осуществляется средствами СУБД
	выбирается запись с минимальной по модулю разницей между днем рождения 
	атлета и днем рождения пользователя
	"""
	query = session.query(
		Athelete.name, 
		Athelete.birthdate, 
		func.min(func.abs(func.julianday(Athelete.birthdate)-func.julianday(user_birthdate)))
		).first()
	return query

def nearest_by_height_athelete(user_height, session):
	"""
	Нахождение ближайшего атлета осуществляется средствами СУБД
	выбирается запись с минимальной по модулю разницей между днем рождения 
	атлета и днем рождения пользователя
	"""
	query = session.query(
		Athelete.name, 
		Athelete.height, 
		func.min(func.abs(Athelete.height - user_height))
		).first()
	return query

def get_ids(session):
	query = session.query(User.id).all()
	return [user.id for user in query]

def main():
    user_id = input("\nВведите идентификатор пользователя: ")
    session = connect_db()
    user = get_user(user_id, session)
    if user is None:
    	print("\nПользователя с таким идентификатором нет в базе данных.")
    	ids = get_ids(session)
    	print("Выберите один и существующих: {}\n".format(ids))
    else:
    	print("\nНайден пользователь с идентификатором: {}\n{} {}.\nДата рождения: {}\nРост: {}\n".format(
    		user_id, 
    		user.first_name, 
    		user.last_name,
    		user.birthdate,
    		user.height
    		)
    	)
    	athelet = nearest_by_birthday_athelete(user.birthdate, session)
    	print("Ближайший к пользователю по возрасту атлет: {}\nДата рождения: {}".format(
    		athelet.name, athelet.birthdate)
    	)
    	athelet = nearest_by_height_athelete(user.height, session)
    	print("Ближайший к пользователю по росту атлет: {}\nРост: {}".format(
    		athelet.name, athelet.height)
    	)

if __name__ == "__main__":
	main()