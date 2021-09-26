from flask import Flask, render_template
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

# @app.route('/properties')
# def users():
#     cur = mysql.connection.cursor()
#     cur.execute('''SELECT user, host FROM mysql.user''')
#     rv = cur.fetchall()
#     return str(rv)

@app.route('/properties')
def showproperties():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM property')
    data = cur.fetchall()
    cur.close()
    return str(data)
    #return render_template('index.html', contacts = data)

@app.route('/status')
def showstatus():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM status')
    data = cur.fetchall()
    cur.close()
    return str(data)
    #return render_template('index.html', contacts = data)

@app.route('/status_history')
def showstatushistory():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM status_history')
    data = cur.fetchall()
    cur.close()
    return str(data)

@app.route('/fulljoin')
def showfulljoin():
    cur = mysql.connection.cursor()
    cur.execute(
        '''SELECT * 
        FROM status_history
        INNER JOIN status
        ON status_history.status_id = status.id ''')
    data = cur.fetchall()
    cur.close()
    return str(data)




if __name__ == '__main__':
    app.run(port= 3000, debug= True)
