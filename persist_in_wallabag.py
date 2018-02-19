# coding: utf-8
import aiohttp
import asyncio
import json
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

    def pr_post_entry_tags(tags):
        entry = 1
        data = wall.post_entry_tags(entry, tags)
        return data

    async def create_entry(title, url, tags):
        data = await pr_post_entries(title, url, tags)

    async def entry_tags(tags):
        data = await pr_post_entry_tags(tags)

    async with aiohttp.ClientSession(loop=loop) as session:
        wall = Wallabag(host=my_host,
                        client_secret=params.get('client_secret'),
                        client_id=params.get('client_id'),
                        token=token,
                        extension=params['extension'],
                        aio_sess=session)

        await create_entry(title, url, tags)

def callWallabag(p_title, p_url, p_tags):
    global title
    global url
    global tags

    title = p_title
    url = p_url
    tags = p_tags

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
