import sys
from flask import Flask, jsonify, request
import mysql.connector as mariadb

app = Flask(__name__)
page_size = 30

@app.route('/')
def get_Archieve_Count():
    mariadb_connection = mariadb.connect(user=mysqluser, password=mysqlpassword, database=mysqldatabase,host=mysqlhost_db)
    cursor = mariadb_connection.cursor()
    cursor.execute("SELECT count(1) from wallabag_entry WHERE is_archived = 1")
    rv = cursor.fetchall()
    t_list = [x[0] for x in rv]
    return str(t_list[0])


@app.route('/query')
def get_Archieve_ids():
    try:
        page_no = request.args['page']
    except Exception as e:
        page_no = '1'

    starting_row = (int(page_no) - 1) * page_size
    sql_stmt = "SELECT id FROM wallabag_entry WHERE is_archived = 1 LIMIT " + str(starting_row) + "," + str(page_size)
    mariadb_connection = mariadb.connect(user='wallabag', password='wallapass', database='wallabag',host='db')
    cursor = mariadb_connection.cursor()
    cursor.execute(sql_stmt)
    try:
        rv = cursor.fetchall()
    except:
        rv = None
    t_list = [x[0] for x in rv]
    print(t_list)
    return str(t_list)

if __name__ == '__main__':
    mysqluser = sys.argv[1]
    mysqlpassword = sys.argv[2]
	mysqldatabase = sys.argv[3]
	mysqlhost_db = sys.argv[4]
    app.run(debug=True,host='0.0.0.0',port=5001)