from flask import Flask, render_template
from flask_mysqldb import MySQL
import os
application = Flask(__name__)
# application.config["MYSQL_URI"] = 'mysql://' + os.environ['MYSQL_USER'] + ':' + os.environ['MYSQL_PASSWORD'] + '@' + os.environ['MYSQL_HOSTNAME'] + ':3306/' + os.environ['MYSQL_DB']
# mysql = MySQL(application)

@application.route('/')
def index():
    return "hello"

if __name__ == '__main__':
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)