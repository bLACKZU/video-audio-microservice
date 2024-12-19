import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PW"] = os.environ.get("MYSQL_PW")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

@server.route("/login", methods = ['POST'])
def login():
    auth = request.authorization
    if not auth:
        return "Missing credentials", 401
    
    #Check db for username and password
    cur = mysql.connection.cursor()
    result = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username)
    )
    
    #Result is a list of rows where each row corresponds to the user(trying to log in) in the auth db
    if result > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "invalid creds", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "Invalid credentials, user doesn't exists", 401


