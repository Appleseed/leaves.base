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
#       def __repr__(self):
#               return '%s %d' % (self.id, self.url)

        def get_data(self):
                return {
                        'id' : str(self.id),
                        'url' : self.url
                }