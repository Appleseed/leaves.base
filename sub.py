# coding: utf-8
import redis
import threading
import time
import json
import aiohttp
import asyncio
from wallabag_api.wallabag import Wallabag

param = json

my_host = ""
username = ""
password = ""
client_id = ""
client_secret = ""
extension = ""

async def wallabagAPI(p_title, p_url, p_tags):
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
        data = await pr_post_entries(title, url, tags)

    async with aiohttp.ClientSession() as session:
        wall = Wallabag(host=my_host,
                        client_secret=params.get('client_secret'),
                        client_id=params.get('client_id'),
                        token=token,
                        extension=params['extension'],
                        aio_sess=session)

        await create_entry(p_title, p_url, p_tags)

def callback():
        r = redis.client.StrictRedis(host='redis')
        sub = r.pubsub()
        sub.subscribe('clock')
        while True:
                for m in sub.listen():
                        print ('received: {0}'.format(m['data']))

def main():
        global title
        global url
        global tags

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

        t = threading.Thread(target=callback)
        t.setDaemon(True)
        t.start()
        while True:
                print ('Waiting')
                time.sleep(30)

if __name__ == '__main__':
        main()
