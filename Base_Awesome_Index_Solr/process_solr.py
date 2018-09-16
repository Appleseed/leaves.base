# Written by Jagannath Bilgi <jsbilgi@yahoo.com>
import os
import configparser
import datetime
import requests

import redis

import bs4_extract_body
import metadata_Api

config = configparser.ConfigParser()
config.read('config.ini')

# Track starting time of script, needed to delete items removed from drupal
dt_started = datetime.datetime.now()

# Solr endpoints for each collection
POST_EP = os.environ["LEAVES_SOLR_URL"]

if not POST_EP:
    POST_EP = config['DEFAULT']['post_ep']

"""
ingest_solr process is created index document retrived from wallabag api. 
new column content_text is created to hold only readable text from sites.

"""
def ingest_solr(doc):
    post_docs = {}
    for key, value in doc.items():
        with open("d_temp", "a+") as f:
            f.write("Hi2\n")
        if key == 'content':
            try:
                content_text = bs4_extract_body.text_from_html(value)
            except:
                content_text = None
            if value != None:
                post_docs[key] = value
            if content_text != None:
                post_docs['content_text'] = content_text
        elif key == 'tags':
            tags = []
            slugs = []
            for i in value:
                for key1, value1 in i.items():
                    if key1 == "label":
                        tags.append(value1)
                    elif key1 == "slug":
                        slugs.append(value1)
            if tags != None :
               post_docs[key] = tags
            if slugs != "None" :
              post_docs["slugs"] = slugs
        elif key == "_links":
            for key1, value1 in value.items():
                for key2, value2 in value1.items():
                   if value2 != None :
                      post_docs[key] = value2
        else:
            if value != None:
                post_docs[key] = value
            if key == "id":
                id_val = value

    content_full = metadata_Api.content_full(post_docs['url'])
    post_docs['content_metadata_full']=content_full

    content_raw = metadata_Api.content_raw(post_docs['url'])
    post_docs['content_metadata_raw']=content_raw

    content_read = metadata_Api.content_read(post_docs['url'])
    post_docs['content_metadata_read']=content_read

    content_text = metadata_Api.content_text(post_docs['url'])
    post_docs['content_metadata_text']=content_text

    meta_card = metadata_Api.meta_card(post_docs['url'])
    post_docs['meta_card']=meta_card

    meta_pagerank = metadata_Api.meta_pagerank(post_docs['url'])
    post_docs['meta_pagerank']=meta_pagerank

    print('Url ', post_docs['url'], ' Title ', post_docs['title'])
    try:
        requests.post(POST_EP + '/update/json/docs?commit=true', json=post_docs)
    except Exception as e:
        print("Error ", str(e))

"""
Ingesting to solr
"""
def main():
    try:
        """
        Reading messages from redis queue with "decode_responses=True ensures" ensures messages are read properly in ascii.
        Noticed that redis always sending first message as 1 and need to be ignored.
        """
        r = redis.client.StrictRedis(host='redis', decode_responses=True)
        sub = r.pubsub()
        sub.subscribe('awesome_solr')
        while True:
            for m in sub.listen():
                if m['data'] != 1:
                    with open("d_temp", "a+") as f:
                        f.write("Hi1\n")
                    ingest_solr(eval("dict({})".format(m['data'])))
    except Exception as e:
        print("Error ", str(e))
if __name__ == '__main__':
    main()
