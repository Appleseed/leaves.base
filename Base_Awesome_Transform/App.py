# Written by Jagannath Bilgi <jsbilgi@yahoo.com>
"""
Creates web service on localhost port 5000 for loading wallabag
Expects awesome site url and file name without any extensions

End point of awesomesite url should be readme.md

example

http://192.168.99.100:5000/params?arg1=%22https://raw.githubusercontent.com/sindresorhus/awesome/master/readme.md%22&arg2=sindresorhus

"""

from flask import Flask, request
import Process_Combine

app = Flask(__name__)

@app.route('/params')
def params():
    arg1 = request.args['arg1']
    arg2 = request.args['arg2']

    Process_Combine.md_to_csv(arg1, arg2)
    return "Done"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')