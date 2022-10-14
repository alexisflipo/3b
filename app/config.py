from dotenv import load_dotenv
import os
 
load_dotenv()
FLASK_ADMIN_SWATCH = "cerulean"
user = os.environ.get("MYSQL_USER")
user_pwd = os.environ.get("MYSQL_PASSWORD")
db = os.environ.get("MYSQL_DATABASE")
flask_secret = os.environ.get("FLASK_SECRET_KEY")
SQLALCHEMY_DATABASE_URI = f"mysql://{user}:{user_pwd}@mysql_db/{db}?use_unicode=1&charset=utf8"
SQLALCHEMY_TRACK_MODIFICATIONS = False
MAIL_USE_TLS = True
MAIL_DEBUG = True
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = os.environ.get('MAIL_PORT')
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')
# TESTING=True
TESTING=False
SECRET_KEY=flask_secret
SECRET_KEY='flask'