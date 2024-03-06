from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from os import environ

app = Flask(__name__)
app.secret_key = "csc-535-record-store-app"

load_dotenv('.flaskenv')
app.config['MYSQL_HOST'] = environ.get("MYSQL_IP")
app.config['MYSQL_USER'] = environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = environ.get("MYSQL_PASS")
app.config['MYSQL_DB'] = environ.get("MYSQL_DB")
app.config['MYSQL_PORT'] = environ.get('MYSQL_PORT')

mysql = MySQL(app)




def init_cursor():
    return mysql.connection.cursor(cursors.DictCursor)




with app.app_context():
    print("App is running")

    from app.routes import *
    from app.database import *

#read_sql("create_tables")