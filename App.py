import json

from flask_mysqldb import MySQL

from flask import Flask, jsonify, request

# Initiate the connection
app = Flask(__name__)

# ------------

# --------------


# Mysql Connection
app.config["MYSQL_HOST"] = "3.130.126.210"
app.config["MYSQL_PORT"] = 3309
app.config["MYSQL_USER"] = "pruebas"
app.config["MYSQL_PASSWORD"] = "VGbt3Day5R"
app.config["MYSQL_DB"] = "habi_db"
mysql = MySQL(app)

# Settings for memory app
app.secret_key = "example"

# This is not the most elegant solution.
# But the mysql IFNULL sometimes fail when pulling data from database
def del_none(d):
    """
    Delete keys with the value "None" or "Empty"
    """
    if isinstance(d, dict):
        for key, value in list(d.items()):
            if value is None or value == "" or value == "Empty":
                del d[key]
            elif isinstance(value, dict):
                del_none(value)
    elif isinstance(d, list):
        for ele in d:
            del_none(ele)
    return d


@app.route("/")
def index():
    """Basic definition of the project"""
    return jsonify(project="Habi Test", name="Humberto Gasperin ", test="Api Example")


### Exploring the tables
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


@app.route("/api/v1/updatedproperties", methods=["GET"])
def last_status_fulljoin():
    """Displaying only the Last Status from the Status_History with the full information"""
    # We try to avoid unnecessary redundancy
    query = """
        SELECT
        property.address,
        property.city,
        property.price,
        property.description,
        stat.property_id,
        stat.status_id,
        stat.last_update,
        status.name,
        status.label,
        property.year
        
        FROM 
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
        ) AS stat

        ON property.id = stat.property_id
        INNER JOIN
        status
        ON status.id = stat.status_id
        """
    query_parameters = request.args
    # ------------------------------------------------
    status_id = query_parameters.get("status_id")
    property_id = query_parameters.get("property_id")
    city = query_parameters.get("city")
    year = query_parameters.get("year")
    ymin = query_parameters.get("ymin")
    ymax = query_parameters.get("ymax")
    pmin = query_parameters.get("pmin")
    pmax = query_parameters.get("pmax")
    # ------------------------------------------------
    # We add optional filters
    # -------------------------------------------------
    cur = mysql.connection.cursor()

    filters = []
    if status_id:

        filters.append(f"status_id = {status_id}")
    if property_id:
        filters.append(f"property_id = {property_id}")
    if city:
        filters.append(f"property.city = '{city}'")
    if year:
        filters.append(f"year = {year}")
    if ymin:
        filters.append(f"year >= {ymin}")
    if ymax:
        filters.append(f"year <= {ymax}")
    if pmin:
        filters.append(f"price >= {pmin}")
    if pmax:
        filters.append(f"price <= {pmax}")

    if filters:
        add_filters = f""" WHERE {" AND ".join(filters)}"""
        print(add_filters)

        cur.execute(query + add_filters)
    else:
        cur.execute(query)

    # Getting the headers
    row_headers = [x[0] for x in cur.description]
    data = cur.fetchall()
    json_data = []
    for result in data:
        json_data.append(dict(zip(row_headers, result)))
    cur.close()
    if json_data:
        null = None
        alternative = del_none(json_data)

        return jsonify(alternative)
    else:
        return jsonify(message="no results for this query")


if __name__ == "__main__":
    app.run(port=3000, debug=True)
