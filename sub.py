import asyncio
import json
import csv

import aiohttp
import redis
from wallabag_api.wallabag import Wallabag

from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from Testcass.testcass import Entry
from datetime import datetime

param = json

my_host = ""
username = ""
password = ""
client_id = ""
client_secret = ""
extension = ""

title = ""
url = ""
tags = ""

async def wallabagAPI(loop):
    params = {'username': username,
              'password': password,
              'client_id': client_id,
              'client_secret': client_secret,
              'extension': extension}

    token = await Wallabag.get_token(host=my_host, **params)

    def pr_post_entries(title, url, tags):
        starred = 0
        archive = 0
        data = wall.post_entries(url, title, tags, starred, archive)
        return data

    async def create_entry(title, url, tags):
        print('Title ', title, ' url ', url, ' tags ', tags)
        data = await pr_post_entries(title, url, tags)
        try:
           crt_at = datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%S+%f")
           upd_at = datetime.strptime(data["updated_at"], "%Y-%m-%dT%H:%M:%S+%f")
           published_by = ','.join(data["published_by"])

           entry = Entry.create(id=data["id"], user_name = data["user_name"], title=data["title"], url=data["url"],is_archived=data["is_archived"],
                                is_starred = data["is_starred"], content = data["content"], create_at = crt_at,
                                update_at = upd_at, mimetype = data["mimetype"], language = data["language"],
                                reading_time = data["reading_time"], domain_name = data["domain_name"],
                                preview_picture = data["preview_picture"], uid = data["uid"],
                                http_status = data["http_status"], published_at = data["published_at"],
                                published_by = published_by, headers = data["headers"],
                                starred_at = data["starred_at"], origin_url = data["origin_url"] )
           entry.save()
        except Exception as e:
            print("Failed while creating entry in Cassandra " + str(e))

    async with aiohttp.ClientSession(loop=loop) as session:
        wall = Wallabag(host=my_host,
                        client_secret=params.get('client_secret'),
                        client_id=params.get('client_id'),
                        token=token,
                        extension=params['extension'],
                        aio_sess=session)

        try:
            await create_entry(title, url, tags)
        except:
            print("Failed for ", url)


def callWallabag(p_title, p_url, p_tags):
    param = json.load(open('wallabag_param'))

    global my_host
    global username
    global password
    global client_id
    global client_secret
    global extension

    my_host = param["host"]
    username = param["username"]
    password = param["password"]
    client_id = param["client_id"]
    client_secret = param["client_secret"]
    extension = param["extension"]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(wallabagAPI(loop))

def callback():
    global title
    global url
    global tags
    r = redis.client.StrictRedis(host='redis', decode_responses=True)
    sub = r.pubsub()
    sub.subscribe('clock')
    while True:
        for m in sub.listen():
            title = ''
            url = ''
            tags = ''
            if m['data'] != 1:
                csv_str = csv.reader(m['data'][1:-1], quotechar="'", delimiter=",")
                for val in csv_str:
                   if val[0].strip():
                    if not title.strip():
                       title = val[0]
                    elif not url.strip():
                       url = val[0]
                    elif not tags.strip():
                       tags = val[0]
                callWallabag(title, url, tags)

def main():
    cluster = Cluster(['cassandra'],port=9042)
    session = cluster.connect()
    session.execute(
            """CREATE KEYSPACE IF NOT EXISTS test WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };"""
        )
    session = cluster.connect(keyspace="test")
    connection.setup(['cassandra'], "cqlengine", protocol_version=3)
    sync_table(Entry)

    callback()

if __name__ == '__main__':
    main()