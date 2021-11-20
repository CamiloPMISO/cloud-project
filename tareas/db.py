import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

postgres_host = os.getenv('POSTGRES_HOST')
postgres_pass = os.getenv('POSTGRES_PASS')

engine = create_engine(f"postgresql://postgres:{postgres_pass}@{postgres_host}:5432/postgres")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()