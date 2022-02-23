from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from decouple import config


#when passing the data directly
#check in .env file
DATABASE_USERNAME_Val = config('SQLALCHEMY_DATABASE_URL')

engine = create_engine(DATABASE_USERNAME_Val)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()