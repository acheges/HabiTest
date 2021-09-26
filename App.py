from flask import Flask, render_template,jsonify
import json
from flask_mysqldb import MySQL

# Initiate the connection
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = '3.130.126.210' 
app.config['MYSQL_PORT'] = 3309
app.config['MYSQL_USER'] = 'pruebas'
app.config['MYSQL_PASSWORD'] = 'VGbt3Day5R'
app.config['MYSQL_DB'] = 'habi_db'
mysql = MySQL(app)

# settings for memory app
app.secret_key = "example"



@app.route('/')
def index():
    return 'Hello Humberto'

@app.route('/queryall')
def addcontact():
    return 'Aca aparecerán todos'

@app.route('/properties')
def showproperties():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM property')
    # Getting the headers
    row_headers=[x[0] for x in cur.description]
    data = cur.fetchall()
    json_data = []
    for result in data:
        json_data.append(dict(zip(row_headers,result)))
    
    return jsonify(json_data)
    


@app.route('/status')
def showstatus():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM status')
    # Getting the headers
    row_headers=[x[0] for x in cur.description]
    data = cur.fetchall()
    json_data = []
    for result in data:
        json_data.append(dict(zip(row_headers,result)))
    cur.close()
    return jsonify(json_data)


@app.route('/status_history')
def showstatushistory():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM status_history')
    # Getting the headers
    row_headers=[x[0] for x in cur.description]
    data = cur.fetchall()
    json_data = []
    for result in data:
        json_data.append(dict(zip(row_headers,result)))
    cur.close()
    return jsonify(json_data)

@app.route('/fulljoin')
def showfulljoin():
    cur = mysql.connection.cursor()
    cur.execute(
        '''SELECT * 
        FROM status_history
        INNER JOIN status
        ON status_history.status_id = status.id
        INNER JOIN property
        ON property.id = status_history.property_id ''')
    # Getting the headers
    row_headers=[x[0] for x in cur.description]
    data = cur.fetchall()
    json_data = []
    for result in data:
        json_data.append(dict(zip(row_headers,result)))
    cur.close()
    return jsonify(json_data)

@app.route('/last_status')
def last_status():
    cur = mysql.connection.cursor()
    cur.execute(
        '''SELECT property_id, MAX(update_date)
        FROM status_history
        GROUP BY property_id ''')

    # Getting the headers
    row_headers=[x[0] for x in cur.description]
    data = cur.fetchall()
    json_data = []
    for result in data:
        json_data.append(dict(zip(row_headers,result)))
    cur.close()
    return jsonify(json_data)

if __name__ == '__main__':
    app.run(port= 3000, debug= True)
