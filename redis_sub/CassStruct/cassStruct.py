from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns

class Base(Model):
    __abstract__ = True
    __keyspace__ = "test"

class Entry(Base):
        user_name = columns.Text()
        title = columns.Text()
        url = columns.Text()
        is_archived = columns.Integer()
        is_starred = columns.Integer()
        content = columns.Text()
        create_at = columns.DateTime()
        update_at = columns.DateTime()
        mimetype = columns.Text()
        language = columns.Text()
        reading_time = columns.Integer()
        domain_name = columns.Text()
        preview_picture = columns.Text()
        uid = columns.Text()
        http_status = columns.Text()
        published_at = columns.DateTime()
        published_by = columns.Text()
        headers = columns.Text()
        starred_at = columns.DateTime()
        origin_url = columns.Text()
        id = columns.Integer(primary_key=True)
        def get_data(self):
                return {
                        'id' : str(self.id),
                        'url' : self.url
                }

class Tags(Base):
        tag = columns.Text(primary_key=True)
        id = columns.Integer(primary_key=True)
        slug = columns.Text()
        url = columns.Text()

        def get_data(self):
                return {
                        'tag': self.tag,
                        'id': self.id,
                        'slug': self.slug,
                        'url': self.url
                }

class Published_by(Base):
        publisher = columns.Text(primary_key=True)
        id = columns.Integer(primary_key=True)
        title = columns.Text()
        url = columns.Text()

        def get_data(self):
                return {
                        'publisher': self.publisher,
                        'id': self.id,
                        'title': self.title,
                        'url': self.url
                }
