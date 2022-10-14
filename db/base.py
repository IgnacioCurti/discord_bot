from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("sqlite:///db.db")
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
session = SessionLocal()
Base = declarative_base()
