#Jagannath Bilgi <jsbilgi@yahoo.com>

import configparser
import datetime
import requests

import redis

import bs4_extract_body

config = configparser.ConfigParser()
config.read('config.ini')

# Track starting time of script, needed to delete items removed from drupal
dt_started = datetime.datetime.now()

# Solr endpoints for each collection
POST_EP = config['DEFAULT']['post_ep']

"""
ingest_solr process is created to index document retrived from wallabag api.
new column content_text is created to hold only readable text from sites.

"""
def ingest_solr(doc):
   post_docs = {}
   for key, value in doc.items():
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
   print('Url ', post_docs['url'], ' Title ', post_docs['title'])
   try:
        res = requests.post(POST_EP + '/update/json/docs?commit=true', json=post_docs)
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
                    ingest_solr(eval("dict({})".format(m['data'])))
    except Exception as e:
        print("Error ", str(e))
if __name__ == '__main__':
    main()
