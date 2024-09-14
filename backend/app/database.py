from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


engine = create_engine(os.environ.get("SQLALCHAMY_DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
