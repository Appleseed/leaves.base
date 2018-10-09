# Written by Jagannath Bilgi <jsbilgi@yahoo.com>
import os
import asyncio
import csv
import json

import aiohttp
import redis
from wallabag_api.wallabag import Wallabag

import RedisQueue
import awesome_nlp
import save_local

"""
    Needs to meet all prerequisite of wallabag program
    
    Update wallabag_param file with Wallagabag host and login parameters
    
    This module reads redis message queue and loads entries to wallagbag through wallabag_api.
    Below lines in wallaba_api is commented and replaced line 3 
            # if len(tags) > 0 and ',' in tags:          #Line 1
            #     params['tags'] = tags.split(',')       #Line 2
            params['tags'] = tags                        #Line 3
    Wallagbag stores information within and responsed with complete web content as document. This document is further queued for indexing(solR) 
    Process exists if host is not available
"""

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
nlp_username= ""
nlp_password = ""

async def wallabagAPI(loop):
    params = {'username': username,
              'password': password,
              'client_id': client_id,
              'client_secret': client_secret,
              'extension': extension}

    awesome_solr_queue = 'awesome_solr'
    # get wallabag token
    token=""
    try:
        token = os.environ["LEAVES_API_ACCESSTOKEN"]
    except :
        pass
    if not token:
        try:
            token = await Wallabag.get_token(host=my_host, **params)
        except:
            pass

    def pr_post_entries(title, url, tags):
        starred = 0
        archive = 0
        if title.strip() != "" :
            data = wall.post_entries(url=url, title=title, tags=tags, archive=archive, starred=starred)
        else:
            if tags:
                data = wall.post_entries(url=url, tags=tags, archive=archive, starred=starred);
            else:
                data = wall.post_entries(url=url, archive=archive, starred=starred);
        return data

    async def create_entry(title, url, tags):
        print('Title ', title, ' url ', url, ' tags ', tags)
        data = await pr_post_entries(title, url, tags)
        if save_local.documentProcessed(url) == 0:
            try:
                keywords = awesome_nlp.getTags(nlp_username, nlp_password, url)
                data.update({"keywords":keywords})
                try:
                    with open("data_dump", "r") as f:
                        pass
                except:
                    with open("data_dump", "w") as f:
                        f.write(json.dumps(data))
            except Exception as e:
                print("Error while getting keywords ", str(e))
            """
            queue document to redis 
            """
            try:
                RedisQueue.pushToQueue(awesome_solr_queue, data)
                save_local.pr_insert_document(data["id"],url)
            except Exception as e:
                print('Error while moving to queue for indexing ', str(e))

    async with aiohttp.ClientSession(loop=loop) as session:
        wall = Wallabag(host=my_host,
                        client_secret=params.get('client_secret'),
                        client_id=params.get('client_id'),
                        token=token,
                        extension=params['extension'],
                        aio_sess=session)

        try:
            if url.strip():
                await create_entry(title, url, tags)
        except Exception as e:
            print("Failed for ", url, str(e))

def callWallabag(p_title, p_url, p_tags):
    param = json.load(open('wallabag_param'))
    nlp_param = json.load(open('nlp_param'))

    global my_host
    global username
    global password
    global client_id
    global client_secret
    global extension

    global nlp_username
    global nlp_password

    username = param["username"]
    password = param["password"]
    client_id = param["client_id"]
    client_secret = param["client_secret"]
    extension = param["extension"]
    try:
        my_host = os.environ["LEAVES_API_URL"]
    except:
        print("Error parameter LEAVES_API_URL not defined")

    if not my_host:
        my_host = param["host"]

    try:
        nlp_username = os.environ["LEAVES_WATSON_USER"]
        nlp_password = os.environ["LEAVES_WATSON_KEY"]
    except:
        print("Error Watson parameters not defined")
    if not nlp_username:
        nlp_username = nlp_param["NLPusername"]
        nlp_password = nlp_param["NLPpassword"]

    # Create event loop required for wallabag api
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wallabagAPI(loop))

def callback():
    global title
    global url
    global tags
    """
    Reading messages from redis queue with "decode_responses=True ensures" ensures messages are read properly in ascii.
    Noticed that redis always sending first message as 1 and need to be ignored. Parsed message is stored in below variables
        title
        url
        tags
    """
    r = redis.client.StrictRedis(host='redis', decode_responses=True)
    sub = r.pubsub()
    sub.subscribe('awesome')
    while True:
        for m in sub.listen():
            title = ''
            url = ''
            tags = ''
            if m['data'] != 1:
                if type(m['data']) == str and m['data'].strip() != None:
                    arg_list = m['data'].split(", ")
                    i = 0
                    for val in arg_list:
                        if (i == 0) :
                            if val != 'dummy':
                                title = val
                        if (i == 1) :
                            if val != 'dummy':
                                url = val
                        if (i == 2) :
                            if val != 'dummy':
                                tags = val
                        i = i + 1
                else:
                    csv_str = csv.reader(m['data'][1:-1], quotechar="'", delimiter=",")
                    for val in csv_str:
                        if val[0].strip():
                            if not title.strip():
                                if val[0] != 'dummy':
                                    title = val[0]
                            elif not url.strip():
                                if val[0] != 'dummy':
                                    url = val[0]
                            elif not tags.strip():
                                if val[0] != 'dummy':
                                    tags = val[0]
                callWallabag(title, url, tags)

def main():
    """
    Creates event loop that is required for wallabag api. Wallabag token is generated using login parameter saved in walla_param json file
    Save wallabag response in cassandra tables
    """
    save_local.initialiseDB()
    callback()

if __name__ == '__main__':
    main()