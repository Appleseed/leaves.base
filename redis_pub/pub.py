import redis
import time
import csv

def pubToRedis(file_name):
        r = redis.client.StrictRedis(host='redis')
        with open(file_name, "r") as awesome_tag_list:
             csv_file = csv.reader(awesome_tag_list)
             for row in csv_file:
                if len(row) != 0:
                    print ('Sending ',row)
                    r.publish('clock', row)
                    time.sleep(1)

