# Written by Jagannath Bilgi <jsbilgi@yahoo.com>

import redis
import time

"""

This module receives document as input and queue it to different queues

"""

def pushToQueue(queue_name, doc):
        r = redis.client.StrictRedis(host='redis')
        r.publish(queue_name, doc)
        print("message sent to ", queue_name)
        time.sleep(1)
