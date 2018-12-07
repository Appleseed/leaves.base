# Written by Jagannath Bilgi <jsbilgi@yahoo.com>
"""
Creates web service on localhost port 6500 for retrieving data from cassandra
Expects id to be retrived

example


"""
import os
from flask import Flask, request, jsonify
import Cas_Query
import json

try:
    leaves_api_cas_port = os.environ["LEAVES_API_CAS_PORT"]
except:
    leaves_api_cas_port = 6500

app = Flask(__name__)

@app.route('/params')
def params():
    try:
        id = request.args['id'];
        id = int(id)
    except Exception as e:
        with open('error.log', 'a') as the_file:
            the_file.write(str(e) +'\n')
        print("Error")
        id = 1;
    res_set = (Cas_Query.query(id))
    if res_set:
        for rs in res_set:
            r1 = rs
        if r1:
            for rs in r1:
                r2 = rs
                r3 = r2.replace('\\"',"~~").replace("'","^^").replace(', "',', ""')

                list = r3.split(', "')
                doc = {}
                for i in list[1:-1]:
                    ii = i.replace('": ', '":$$ ')
                    keyvalue = ii.split(':$$ ')
                    m = keyvalue[0].replace('"','')
                    v = keyvalue[1].replace('"','').replace('~~','"').replace('^^',"'")
                    if m in ("headers,published_by"):
                        v = v.replace('N;','null')
                    if m in ("is_archived,is_starred,reading_time"):
                        v = int(v)
                    if m in ("label"):
                        m = "tags"
                    doc[m] = v
            return jsonify(doc)
        else:
            return jsonify({"Status": "No data found"})
    else:
        return jsonify({"Status":"No data found"})
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=leaves_api_cas_port)
