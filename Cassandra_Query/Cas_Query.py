import os
from cassandra.cluster import Cluster

try:
    leaves_api_cas_host = os.environ["LEAVES_API_CAS_HOST"]
except:
    leaves_api_cas_host = '206.189.143.212'

cluster = Cluster([leaves_api_cas_host])
session = cluster.connect('wallabag_cass')

def query(id):
    try:
        statement = session.prepare("SELECT JSON * FROM wallabag_by_id Where id=?;")
        rows = session.execute(statement, [id])
        return rows
    except Exception as e:
        print("error " + str(e))
        with open('error.log', 'a') as the_file:
            the_file.write('cas read error ' + str(e) +'\n')
        return
