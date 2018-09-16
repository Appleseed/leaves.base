from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

db = create_engine('sqlite:///docs.db')
Base = declarative_base()
