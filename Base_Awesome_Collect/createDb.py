from app import Base
from app import db
from app import model

def initialiseDB() :
    Base.metadata.drop_all(db)
    Base.metadata.create_all(db)