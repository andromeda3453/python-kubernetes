import jwt
import datetime
import os
from flask import Flask, request
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app)

# config - os.environ.get gets an environment variable. environment var is set with the "export <var_name>=<var_val>" command
app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
app.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))


@app.route("/login", methods=["POST"])
def login():
    # pulls the authentication Bearer from the header of the request
    auth = request.authorization
    if not auth:
        return "credentials missing", 401

    # check if user exists in db
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username,)
    )

    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if str.lower(auth.username) != str.lower(email) or auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)


@app.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "missing credentials", 401

    # Value of Auth header will be in the form Bearer <token>. We need to split the string and get the token part
    encoded_jwt = encoded_jwt.split(" ")[1]

    # decode jwt and check validity
    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )

    except:
        return "not authorized", 403

    # return decoded token with user claims (data)
    return decoded, 200


def createJWT(username, secret, role):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1),
            "iat": datetime.datetime.now(datetime.UTC),
            "admin": role,
        },
        secret,
        algorithm="HS256",
    )


if __name__ == "__main__":
    #need to set host to 0.0.0.0 to make the server accessible from all public IPs. omitting this would make it run on localhost and only be accessible on the local machine
    app.run(host='0.0.0.0', port=5000)
