from app import db
from app.model import Document
from sqlalchemy.orm import Session

import createDb
# Create a db session
sess = Session(db)

def pr_insert_document(docId, url):
    # Store processing state in sql
    sqldoc = Document(docId, url)
    if documentProcessed(url) == 0:
        sess.add(sqldoc)
        sess.commit()
    else:
        sqldoc.tick()

def documentProcessed(url):
    try:
        sqldoc = sess.query(Document).filter(Document.url == url).first()
        if sqldoc == None:
            return 0
        else:
            return 1
    except Exception as e:
        print("Error while retrieving document from db ", str(e))
        return 0

def initialiseDB():
    try:
        sqldoc = sess.query(Document).first()
        print("Db already present")
    except Exception as e:
        createDb.initialiseDB()
        print("Error while retrieving document from db ", str(e))