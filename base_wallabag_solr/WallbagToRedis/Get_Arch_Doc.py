import requests
import math
resp = requests.get('http://192.168.99.100:5001/')
if (resp.status_code != 200) :
   raise ApiError('GET /tasks/ {}'.format(resp.status_code))

page_size = 30
with open("Wallabag_Arch_id_list", 'w') as f:
     for page in range(int(int(resp.text) / page_size)):
         resp = requests.get('http://192.168.99.100:5001/query?page=' + str(page+1))
         if (resp.status_code != 200) :
            raise ApiError('GET /tasks/ {}'.format(resp.status_code))
         f.write(','+ resp.text[1:-1] + '\n')
         print(resp.text[1:-1])