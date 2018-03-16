from app import Base

from sqlalchemy import Column, DateTime, Integer, String

import datetime


# Document processing record
class Document(Base):
    __tablename__ = 'docs'

    id = Column(Integer, primary_key=True)
    solr_id = Column(String(64), unique=True)
    dt_processed = Column(DateTime())

    def __init__(self, solr_id):
      self.solr_id = solr_id
      self.dt_processed = datetime.datetime.now()

    def __repr__(self):
      return 'Document {}'.format(self.solr_id)

    def tick(self):
      self.dt_processed = datetime.datetime.now()
