from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Налаштування PostgreSQL
DATABASE_URL = "postgresql://<username>:<password>@localhost:5432/contacts_db"

# Створення об'єкта для підключення
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Функція для отримання сесії
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
