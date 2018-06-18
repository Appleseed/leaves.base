import RedisQueue

awesome_solr_missing_id = 'awesome_solr_missing_id'
def find_missing_ids():
    with open("wallabag_id_list", "r") as f:
         for line in f:
             RedisQueue.pushToQueue(awesome_solr_missing_id, line)

def main():
    find_missing_ids()

if __name__ == '__main__':
    main()