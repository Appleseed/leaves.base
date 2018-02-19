# coding: utf-8
import redis
import datetime
import time

def main():
        r = redis.client.StrictRedis(host='redis')
        while True:
                now = datetime.datetime.now()
                print ('Sending {0}'.format(now))
                r.publish('clock',now)
                time.sleep(1)

if __name__ == '__main__':
        main()