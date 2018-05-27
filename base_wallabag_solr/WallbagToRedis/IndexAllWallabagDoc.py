import asyncio
import json

import aiohttp
from wallabag_api.wallabag import Wallabag
import PublishToSolr

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

    #get wallabag token
    token = await Wallabag.get_token(host=my_host, **params)

    def pr_get_entry():
        data = wall.get_entries()
        # data = wall.get_entry(entry=1)
        return data

    async def get_entry():
        data = await pr_get_entry()
        #try:
        #    PublishToSolr.publishToSolr(data)
        #except Exception as e:
        #    print('Error while queing ', str(e))
        for k, v in data.items():
             if k == '_embedded':
                 for k1, v1 in (v.items()):
                     for x in range(len(v1)):
                         """
                         move to redis queue for solr ingestion
                         """
                         try:
                             PublishToSolr.publishToSolr(v1[x])
                         except Exception as e:
                             print('Error while queing ', str(e))

    async with aiohttp.ClientSession(loop=loop) as session:
        wall = Wallabag(host=my_host,
                        client_secret=params.get('client_secret'),
                        client_id=params.get('client_id'),
                        token=token,
                        extension=params['extension'],
                        aio_sess=session)
        await get_entry()

def main():
    """
    Creates event loop that is required for wallabag api. Wallabag token is generated using login parameter saved in walla_param json file
    Save wallabag response in cassandra tables
    """
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

    # Create event loop required for wallabag api
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wallabagAPI(loop))

if __name__ == '__main__':
    main()