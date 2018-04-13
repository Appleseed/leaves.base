from urllib.parse import urlparse

import configparser
import datetime
import re
import requests
import time

import sys
import json

config = configparser.ConfigParser()
config.read('config.ini')

# Track starting time of script, needed to delete items removed from drupal
dt_started = datetime.datetime.now()

# Solr endpoints for each collection
POST_EP = config['DEFAULT']['post_ep']

# Return value in doc or None if key doesn't exist
def getValue(doc, field):
  if field in doc:
    return doc[field]
  else:
    return None

# Utility function to remove html tags, expects a multivalued field
def stripTags(data):
  if data == None:
    return

  for idx, val in enumerate(data):
    exp = re.compile('<.*?>')
    data[idx] = re.sub(exp, '', val)

def titleize(chars):
  result = []
  prev_letter = ' '

  for ch in chars:
      if not prev_letter.isalpha() and prev_letter != "'":
          result.append(ch.upper())
      else:
          result.append(ch.lower())

      prev_letter = ch

  return "".join(result) 
id_val = ""
post_docs = {}
def ingest_solr(doc):
   for key, value in doc.items():
       if key == 'tags':
           for i in value:
               for key1, value1 in i.items():
                   if key1 == "label":
                       post_docs[key] = value1
                   elif key1 == "slug":
                       post_docs["slug"] = value1
       elif key == "_links":
           for key1, value1 in value.items():
               for key2, value2 in value1.items():
                   post_docs[key] = value2
       else:
           post_docs[key] = value
           if key == "id":
               id_val = value
   try:
        requests.post(POST_EP + '/update/json/docs?commit=true', json=post_docs)
   except Exception as e:
       print("Error ", str(e))

   try:
        res = requests.get(POST_EP + '/select?q = id:' + str(id_val) + ' & wt = json & indent = true ')
        print(res)
   except Exception as e:
       print("Error ", str(e))
