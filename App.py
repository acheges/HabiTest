from flask import Flask, request, jsonify
import json
from flask_mysqldb import MySQL

# Initiate the connection
app = Flask(__name__)

# Mysql Connection
app.config["MYSQL_HOST"] = "3.130.126.210"
app.config["MYSQL_PORT"] = 3309
app.config["MYSQL_USER"] = "pruebas"
app.config["MYSQL_PASSWORD"] = "VGbt3Day5R"
app.config["MYSQL_DB"] = "habi_db"
mysql = MySQL(app)

# settings for memory app
app.secret_key = "example"


@app.route("/")
def index():
    return "Hello Humberto"


@app.route("/properties")
def showproperties():
    """Showing all the properties"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM property")
    # Getting the headers
    row_headers = [x[0] for x in cur.description]
    data = cur.fetchall()
    json_data = []
    for result in data:
        json_data.append(dict(zip(row_headers, result)))

    return jsonify(json_data)


@app.route("/status")
def showstatus():
    """Showing all the Status"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM status")
    # Getting the headers
    row_headers = [x[0] for x in cur.description]
    data = cur.fetchall()
    json_data = []
    for result in data:
        json_data.append(dict(zip(row_headers, result)))
    cur.close()
    return jsonify(json_data)


@app.route("/status_history")
def showstatushistory():
    """Showing Status History"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM status_history")
    # Getting the headers
    row_headers = [x[0] for x in cur.description]
    data = cur.fetchall()
    json_data = []
    for result in data:
        json_data.append(dict(zip(row_headers, result)))
    cur.close()
    return jsonify(json_data)


@app.route("/fulljoin")
def showfulljoin():
    """Testing a Full Inner Join"""
    cur = mysql.connection.cursor()
    cur.execute(
        """SELECT * 
        FROM status_history
        INNER JOIN status
        ON status_history.status_id = status.id
        INNER JOIN property
        ON property.id = status_history.property_id """
    )
    # Getting the headers
    row_headers = [x[0] for x in cur.description]
    data = cur.fetchall()
    json_data = []
    for result in data:
        json_data.append(dict(zip(row_headers, result)))
    cur.close()
    return jsonify(json_data)


@app.route("/last_status")
def last_status():
    """Displaying only the Last Status from the Status_History"""
    cur = mysql.connection.cursor()
    cur.execute(
        """
        SELECT
        last_status_table.property_id, 
        status_history.id, 
        last_status_table.last_update
        FROM status_history 
        INNER JOIN
        (SELECT property_id, MAX(update_date) AS last_update
        FROM status_history
        GROUP BY property_id) AS last_status_table
        ON last_status_table.property_id = status_history.property_id
        AND last_status_table.last_update = status_history.update_date
        """
    )
    # Getting the headers
    row_headers = [x[0] for x in cur.description]
    data = cur.fetchall()
    json_data = []
    for result in data:
        json_data.append(dict(zip(row_headers, result)))
    cur.close()
    return jsonify(json_data)


@app.route("/api/v1/updatedproperties", methods=['GET'])
def last_status_fulljoin():
    """Displaying only the Last Status from the Status_History with more information"""
    cur = mysql.connection.cursor()
    query = """
        SELECT * FROM 
        property 
        INNER JOIN

        (
        SELECT
        last_status_table.property_id, 
        status_history.id, 
        status_history.status_id,
        last_status_table.last_update
        FROM status_history 
        INNER JOIN
        (SELECT property_id, MAX(update_date) AS last_update
        FROM status_history
        GROUP BY property_id) AS last_status_table
        ON last_status_table.property_id = status_history.property_id
        AND last_status_table.last_update = status_history.update_date
        ) 

        AS stat 
        ON property.id = stat.property_id
        INNER JOIN
        status
        ON status.id = stat.status_id
        """
    query_parameters = request.args
    #------------------------------------------------
    status_id = query_parameters.get('status_id')
    property_id = query_parameters.get('property_id')
    city = query_parameters.get('city')
    #------------------------------------------------
    filters = []
    if status_id:
        #query += ' id=? AND'
        filters.append(status_id)
    if property_id:
        #query += ' published=? AND'
        filters.append(property_id)
    if city:
        #query += ' author=? AND'
        filters.append(city)

    print(filters)


    
    print(id)
    # We get the filters
    
    cur.execute(query)
    # Getting the headers
    row_headers = [x[0] for x in cur.description]
    data = cur.fetchall()
    json_data = []
    for result in data:
        json_data.append(dict(zip(row_headers, result)))
    cur.close()
    return jsonify(json_data)


if __name__ == "__main__":
    app.run(port=3000, debug=True)
