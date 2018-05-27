# Written by Jagannath Bilgi <jsbilgi@yahoo.com>

import redis
import time

"""

This module receives document as input and queue it to awesome_solr message queue

"""

def publishToSolr(doc):
        r = redis.client.StrictRedis(host='redis')
        r.publish('awesome_solr', doc)
        time.sleep(1)

