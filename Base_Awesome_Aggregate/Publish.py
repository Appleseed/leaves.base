# Written by Jagannath Bilgi <jsbilgi@yahoo.com>

import redis
import time
import csv

"""

This module reads csv entries generated using "Base_awesome_transform" and queue's csv entries into redis message queue in format
Title, URL, Tags 

# tags can be null or comma separated value. Below is sample message

Frontend Development,https://github.com/dypsilon/frontend-dev-bookmarks,"sindresorhus,Platforms"

"""

def publishToRedis(file_name):
        r = redis.client.StrictRedis(host='redis')
        with open(file_name, "r") as awesome_tag_list:
             csv_file = csv.reader(awesome_tag_list)
             for row in csv_file:
                if len(row) != 0:
                    print ('Sending ',row)
                    r.publish('awesome', row)
                    time.sleep(1)

