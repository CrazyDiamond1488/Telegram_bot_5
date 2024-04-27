from sqlalchemy import create_engine, Column, Integer, String, Numeric # type: ignore
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import update
from BD.config import user, password, db_name
# Создание объекта Engine для PostgreSQL базы данных
engine = create_engine(f'postgresql+psycopg2://{user}:{password}@localhost:5432/{db_name}', echo=True)

# Определение базового класса моделей
Base = declarative_base()

# Определение модели данных для таблицы "currencies"
class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True)
    currency_name = Column(String)
    rate = Column(Numeric)

# Определение модели данных для таблицы "admins"
class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    chat_id = Column(String)

# Создание таблиц в базе данных
Base.metadata.create_all(engine)

# Создание объекта сессии для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Пример добавления данных в таблицу "admins"
admin1 = Admin(chat_id='939831823')
admin2 = Admin(chat_id='579595508')
session.add(admin1)
session.add(admin2)
# Фиксация изменений в базе данных
session.commit()

# Закрытие сессии
session.close()