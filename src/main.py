import mysql.connector
from flask import jsonify
from flask import Flask, request
from flask_cors import CORS

import config

app = Flask(__name__)
CORS(app)
cors = CORS(app,resources={
		r"/*": {
			"origins": "*"
		}
})

@app.route("/Hello")
def hello():
	print("Hi")
	return "Hello World!"		

		
@app.route('/users',methods=['GET'])
def users():
	
	db_connection = mysql.connector.connect(
	host=config.mysql_host,
	user=config.mysql_user,
	passwd=config.mysql_pass,
	database=config.mysql_db
	)
	my_database = db_connection.cursor()
	sql_statement = "SELECT * FROM UID"
	my_database.execute(sql_statement)
	output = my_database.fetchall()
	resp = jsonify(output)
	return resp
		
@app.route('/users', methods=['POST'])
def add_user():
	_json = request.json
	_firstname = _json['FirstName']
	_lastname = _json['LastName']
	_uid = _json['UID']
	sql = "INSERT INTO UID(UID, FirstName, LastName) VALUES(%s, %s, %s)"
	data = (_uid, _firstname, _lastname)
	db_connection = mysql.connector.connect(
	host=config.mysql_host,
	user=config.mysql_user,
	passwd=config.mysql_pass,
	database=config.mysql_db
	)
	conn = db_connection.cursor()
	conn.execute(sql, data)
	db_connection.commit()
	return "Record Inserted"
	
@app.route('/validate', methods=['POST'])
def validate_user():
	_json = request.json
	_firstname = _json['FirstName']
	_lastname = _json['LastName']
	_uid = _json['UID']
	db_connection = mysql.connector.connect(
	host=config.mysql_host,
	user=config.mysql_user,
	passwd=config.mysql_pass,
	database=config.mysql_db
	)
	conn = db_connection.cursor()
	sql = "SELECT * FROM UID WHERE UID=%s And FirstName=%s And LastName=%s"
	data = (_uid,_firstname,_lastname)
	conn.execute(sql,data)
	row = conn.fetchone()
	if row is None:
		return jsonify("UID not found. Please try again !")
	else: 
		return jsonify("Validation Successful")
	
		
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.port, debug=config.debug_mode)
