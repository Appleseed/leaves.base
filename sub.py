import redis
import threading
import time
import aiohttp
import asyncio
import json
import csv
from wallabag_api.wallabag import Wallabag

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


    async with aiohttp.ClientSession(loop=loop) as session:
        wall = Wallabag(host=my_host,
                        client_secret=params.get('client_secret'),
                        client_id=params.get('client_id'),
                        token=token,
                        extension=params['extension'],
                        aio_sess=session)

        await create_entry(title, url, tags)

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
#    wallabagAPI()

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
     callback()

if __name__ == '__main__':
    main()
