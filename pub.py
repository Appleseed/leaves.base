import redis
import datetime
import time
import csv

#file_name = sys.argv[1]
file_name = "sindresorhus.csv"
def main():
        r = redis.client.StrictRedis(host='192.168.99.100')
        with open(file_name, "r") as awesome_tag_list:
             csv_file = csv.reader(awesome_tag_list)
             for row in csv_file:
#        while True:
#                now = datetime.datetime.now()
                print ('Sending ',row)
                r.publish('clock',row)
                time.sleep(1)

if __name__ == '__main__':
        main()