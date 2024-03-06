from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
import pymysql
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os



app = Flask(__name__)
app.secret_key = "csc-535-record-store-app"







app.config['MYSQL_HOST'] = os.environ.get("MYSQL_IP")
app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASS")
app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB")
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT'))

mysql = mydb.cursor()
def init_cursor():
return mysql._connection.cursor(dictionary=True)



#read_sql("create_tables")