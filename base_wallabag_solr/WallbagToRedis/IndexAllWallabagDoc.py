import sys
import time
import os
import asyncio
import json

import aiohttp
from wallabag_api.wallabag import Wallabag
import RedisQueue

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
option = sys.argv[1]

async def wallabagAPI(loop):
    params = {'username': username,
              'password': password,
              'client_id': client_id,
              'client_secret': client_secret,
              'extension': extension}

    awesome_solr_queue = 'awesome_solr'
    awesome_solr_missing_id = 'awesome_solr_missing_id'

    #get wallabag token
    try:
       walla_key = os.environ['WALLA_KEY']
    except Exception as e:
       print("Using credentials from param file")
       walla_key = None

    if not walla_key:
       token = await Wallabag.get_token(host=my_host, **params)
    else:
       print("Environment key ", walla_key)
       token = walla_key

    def pr_get_entries(page=None):
       data = wall.get_entries(page=page)
       return data

    def pr_get_entry(id):
       data = wall.get_entry(entry=id)
       return data

    def check_missing_id():
        time.sleep(120)
        with open("wallabag_id_list", "r") as f:
             for line in f:
                 RedisQueue.pushToQueue(awesome_solr_missing_id, line)

    async def get_entry(id):
        data = await pr_get_entry(id)
        RedisQueue.pushToQueue(awesome_solr_queue,data)
    async def get_entry(id):
        data = await pr_get_entry(id)
        RedisQueue.pushToQueue(awesome_solr_queue,data)

    async def get_entries():
        data = await pr_get_entries()
        for k, v in data.items():
             if k == 'pages':
                total_pages = v
             if k == '_embedded':
                 for k1, v1 in (v.items()):
                     id_str = None
                     for x in range(len(v1)):
                         """
                         queue document to redis
                         """
                         try:
                             print("Sending message " + str(v1[x]["id"]))
                             for k2, v2 in v1[x].items():
                                 if k2 == 'tags':
                                    print("tags ", v2)
                             if not id_str:
                                id_str = str(v1[x]["id"])
                             else:
                                id_str = id_str + ',' + str(v1[x]["id"])
                                RedisQueue.pushToQueue(awesome_solr_queue, v1[x])
                         except Exception as e:
                             print('Error while queing ', str(e))
                 with open("wallabag_id_list","a") as f:
                      f.write(id_str + '\n')
                 for x in range(2,total_pages):
                     await get_page(x)
                     print("Ingected entries from page ", x)
                 check_missing_id()
    async def get_page(page):
        data = await pr_get_entries(page)
        for k, v in data.items():
             if k == '_embedded':
                 for k1, v1 in (v.items()):
                     id_str = None
                     for x in range(len(v1)):
                         """
                         queue document to redis
                         """
                         try:
                             print("Sending message " + str(v1[x]["id"]))
                             if not id_str:
                                id_str = str(v1[x]["id"])
                             else:
                                id_str = id_str + ',' + str(v1[x]["id"])
                                RedisQueue.pushToQueue(awesome_solr_queue, v1[x])
                         except Exception as e:
                             print('Error while queing ', str(e))
                 with open("wallabag_id_list","a") as f:
                      f.write(id_str + '\n')
    async with aiohttp.ClientSession(loop=loop) as session:
        wall = Wallabag(host=my_host,
                        client_secret=params.get('client_secret'),
                        client_id=params.get('client_id'),
                        token=token,
                        extension=params['extension'],
                        aio_sess=session)
        if option == '1':
           await get_entries()
        else:
           if option == '2':
              file_name = "missing_ids"
           else:
              file_name = "Wallabag_Arch_id_list"

           with open(file_name, "r") as f:
                for line in f:
                    id_list = line[1:].rstrip().split(",")
                    for id in (range(len(id_list))):
                        print("id ", id_list[id])
                        await get_entry(id_list[id])
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
    print("option selected ", option)
    main()