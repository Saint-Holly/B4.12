"""
Author: Vladimir Scherbinin
Модуль попелнения БД пользователей
"""

from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Date)
    height = sa.Column(sa.Float)

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def request_data():
	first_name = input("Введи свое имя: ")
	last_name = input("Введи свою фамилию: ")
	birthdate = input("День рождения (Формат: ДД-ММ-ГГГГ): ")
	gender = input("Твой пол (Формат: м/ж): ")
	height = input("Рост в метрах: ")
	email = input("Email: ")
	user = User(
		# id = user_id,
		first_name = first_name,
		last_name = last_name,
		birthdate = datetime.strptime(birthdate, "%d-%m-%Y"),
		gender = gender,
		height = height,
		email = email
	)
	return user

def main():
	user = request_data()
	session = connect_db()
	session.add(user)
	session.commit()
	print("Данные сохранены.")

if __name__ == "__main__":
	main()