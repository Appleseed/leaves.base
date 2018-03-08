from flask import Flask, request
import collect_awesome_md_csvpy

app = Flask(__name__)

@app.route('/params')
def params():
    arg1 = request.args['arg1']
    arg2 = request.args['arg2']

    collect_awesome_md_csvpy.md_csv(arg1, arg2)
    return "Done"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')