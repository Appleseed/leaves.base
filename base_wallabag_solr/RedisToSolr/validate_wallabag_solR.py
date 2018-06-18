#Jagannath Bilgi <jsbilgi@yahoo.com>

import json
import configparser
import requests

import redis

config = configparser.ConfigParser()
config.read('config.ini')

# Solr endpoints for each collection
POST_EP = config['DEFAULT']['post_ep']

"""
query_solr process is created to retrieve id's from solr to validate all id's in the list are ingested.

"""
def query_solr(id_str):
   try:
        source_id_list = id_str.rstrip().split(",")
        qry_str = '("' + '","'.join(source_id_list) + '")'
        target_id_list = []
        res = requests.get(POST_EP + '/select?fl=id&rows=30&q=id:' + qry_str)
        for i in list(res.json().values())[1]['docs']:
            for k, v in i.items():
                target_id_list.append(v)

        source_set = set(source_id_list)
        target_set = set(target_id_list)
        missing_id_set = source_set - target_set
        if not bool(missing_id_set):
           print("no id is missing")
        else:
           missing_ids = ','.join(str(s) for s in missing_id_set)
           print("missing ids ", missing_ids)
           with open("missing_ids", "a") as f:
                f.write("," + missing_ids)
   except Exception as e:
       print("Error ", str(e))

def main():
    try:
        """
        Reading messages from redis queue with "decode_responses=True ensures" ensures messages are read properly in ascii.
        Noticed that redis always sending first message as 1 and need to be ignored.
        """
        r = redis.client.StrictRedis(host='redis', decode_responses=True)
        sub = r.pubsub()
        sub.subscribe('awesome_solr_missing_id')
        while True:
            for m in sub.listen():
                if m['data'] != 1:
                    query_solr(m['data'])

    except Exception as e:
        print("Error ", str(e))

if __name__ == '__main__':
    main()
