from app import Base

from sqlalchemy import Column, DateTime, Integer, String

import datetime

# Document processing record
class Document(Base):
    __tablename__ = 'docs'

    id = Column(Integer, primary_key=True)
    walla_id = Column(String(64), unique=True)
    url = Column(String(500), unique=True)
    dt_processed = Column(DateTime())

    def __init__(self, walla_id, url):
      self.walla_id = walla_id
      self.url = url
      self.dt_processed = datetime.datetime.now()

    def __repr__(self):
      return 'Document {}'.format(self.walla_id)

    def tick(self):
      self.dt_processed = datetime.datetime.now()
