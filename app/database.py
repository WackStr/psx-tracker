import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings


db_user = settings.POSTGRES_USER
db_password = settings.POSTGRES_PASSWORD
db_name = settings.POSTGRES_DB

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@db/{db_name}"

# Create the engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)

# Create a configured "SessionLocal" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()