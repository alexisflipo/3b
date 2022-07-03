from flask import Flask, render_template
from flask_mysqldb import MySQL
import os
app = Flask(__name__)
app.config["MYSQL_URI"] = 'mysql://' + os.environ['MYSQL_USER'] + ':' + os.environ['MYSQL_PASSWORD'] + '@' + os.environ['MYSQL_HOSTNAME'] + ':3306/' + os.environ['MYSQL_DB']
mysql = MySQL(app)

@app.route('/')
def index():
    return (render_template('index.html'))

if __name__ == '__main__':
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    app.run(host='178.62.29.157', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)