# Written by Jagannath Bilgi <jsbilgi@yahoo.com>

import asyncio
import csv
import json
from datetime import datetime

import aiohttp
import redis
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from wallabag_api.wallabag import Wallabag
from CassStruct.cassStruct import Entry, Tags, Published_by

import PublishToSolr

"""
Needs to meet all prerequisite of wallabag program
 
Update wallabag_param file with Wallagabag host and login parameters
 
This module reads redis message queue and loads entries to wallagbag through wallabag_api.

Below lines in wallaba_api is commented and replaced line 3 
        # if len(tags) > 0 and ',' in tags:          #Line 1
        #     params['tags'] = tags.split(',')       #Line 2
        params['tags'] = tags                        #Line 3

Wallagbag's returned information is stored in Entry, Tags and Published_by cassandra tables under awesome_transform key space.

Process waits for "cassandra" host with 9042 port to be available for 180 sec. Process exists if host is not available
 
"""

import time
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

    def pr_post_entries(title, url, tags):
        starred = 0
        archive = 0
        data = wall.post_entries(url, title, tags, starred, archive)
        return data

    async def create_entry(title, url, tags):
        print('Title ', title, ' url ', url, ' tags ', tags)
        data = await pr_post_entries(title, url, tags)

        """
        queue document to redis 
        
        """
        try:
            PublishToSolr.publishtoSolr(data)
        except Exception as e:
            print('Error while queing ', str(e))

        """
        Wallabag returns date fileds including fractions. Hence convert 
        it to cassndra timestamp format 
        """
        try:
           crt_at = datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%S+%f")
           upd_at = datetime.strptime(data["updated_at"], "%Y-%m-%dT%H:%M:%S+%f")
           if data["published_at"]:
               upd_at = datetime.strptime(data["published_at"], "%Y-%m-%dT%H:%M:%S+%f")
           else:
               upd_at = None

           if data["starred_at"]:
               strd_at = datetime.strptime(data["starred_at"], "%Y-%m-%dT%H:%M:%S+%f")
           else:
               strd_at = None

           """
           Wallabag provides Published_by as a list of values. Convert it to comma separated for  display purpose
           """

           if type(data["published_by"]) == list :
               published_by = ''.join(data["published_by"])
           else:
               published_by = data["published_by"]

           tag_flag = 0
           publishers_flag = 0
           entry = Entry.create(id=data["id"], user_name = data["user_name"], title=data["title"], url=data["url"], is_archived=data["is_archived"],
                                                                is_starred = data["is_starred"], content = data["content"], create_at = crt_at,
                                                                update_at = upd_at, mimetype = data["mimetype"], language = data["language"],
                                                                reading_time = data["reading_time"], domain_name = data["domain_name"],
                                                                preview_picture = data["preview_picture"], uid = data["uid"],
                                                                http_status = data["http_status"], published_at = upd_at,
                                                                published_by = published_by, headers = data["headers"],
                                                                starred_at = strd_at, origin_url = data["origin_url"])
           if data["tags"]:
                for row in data["tags"]:
                    if len(row["label"]) != 0:
                        tag_flag = 1
                        tags = Tags.create(tag= row["label"], slug = row["slug"], id= data["id"], url=data["url"])
           if data["published_by"]:
                for row in data["published_by"]:
                    if len(row) != 0 :
                        publishers_flag = 1
                        publishers = Published_by.create(publisher = row, title=data["title"], id = data["id"], url=data["url"])

           if tag_flag == 1:
                tags.save()
           if publishers_flag == 1:
                publishers.save()
           entry.save()
        except Exception as e:
            print("Failed while creating entry in Cassandra ", url, str(e))
            print("id", type(data["id"]), data["id"])
            print("created_at", type(data["created_at"]), data["created_at"])
            print("update_at", type(data["updated_at"]), data["updated_at"])
            print("published_at", type(data["published_at"]), data["published_at"])
            print("is_archived", type(data["is_archived"]),data["is_archived"])
            print("is_starred",type(data["is_starred"]), data["is_starred"])
            print("reading_time", type( data["reading_time"]),  data["reading_time"])
            print("starred_at", type(data["starred_at"]), data["starred_at"])

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
    print("Waiting for cassandra to to be available")
    retires = 0
    conn = False
    while retires < 6 and conn == False:
        try:
            time.sleep(30)
            cluster = Cluster(['cassandra'], port=9042)
            session = cluster.connect()
            conn = True
        except:
            retires = retires + 1
            continue

    if not conn:
        print("Unable to connect to Cassandra")
    else:
        print("Connected to cassandra")
        session.execute(
                """CREATE KEYSPACE IF NOT EXISTS awesome_transform WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };"""
            )
        session = cluster.connect(keyspace="awesome_transform")

        # Establish cqlsh connection with cassnadra

        connection.setup(['cassandra'], "cqlengine", protocol_version=3)

        # Sync application class definition with casandra table structure

        sync_table(Entry)
        sync_table(Tags)
        sync_table(Published_by)

        """
        Creates event loop that is required for wallabag api. Wallabag token is generated using login parameter saved in walla_param json file
        Save wallabag response in cassandra tables
        """
        callback()

if __name__ == '__main__':
    main()