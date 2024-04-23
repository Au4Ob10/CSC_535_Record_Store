from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from os import environ
import mysql.connector

# Load environment variables
load_dotenv('.flaskenv')
# Debug for DB info
# print("MySQL Host:", environ.get('MYSQL_HOST'))
# print("MySQL User:", environ.get('MYSQL_USER'))
# print("MySQL Password:", environ.get('MYSQL_PASSWORD'))
# print("MySQL Database:", environ.get('MYSQL_DB'))
# print("MySQL Port:", int(environ.get('MYSQL_PORT')))

app = Flask(__name__, template_folder='Website1/templates',static_folder='Website1/templates/static')

app.secret_key = "csc-535-record-store-app"

#Populate database on flask run
def check_database():
    connection = mysql.connector.connect(
        host=environ.get('MYSQL_HOST'),
        user=environ.get('MYSQL_USER'),
        passwd=environ.get('MYSQL_PASSWORD'),
        port=int(environ.get('MYSQL_PORT')),
        auth_plugin="mysql_native_password"
    )

    # Check if the database exists
    cursor = connection.cursor()
    try:
        cursor.execute("USE record_store")
    except mysql.connector.Error as err:
        # If the database does not exist, create it
        if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database 'record_store' created successfully.")
        else:
            print(err)
            exit(1)
    finally:
        print("databased")
        cursor.close()
        connection.close()
#Populate database on flask run
def create_database(cursor):
    # Read SQL script from file
    with open("Recordstore.sql", "r") as sql_file:
        sql_script = sql_file.read()
    # Execute SQL script to create the database
    cursor.execute(sql_script, multi=True)

    # Close the cursor
    cursor.close()

check_database()

store_db = mysql.connector.connect(
host= environ.get('MYSQL_HOST'),
user= environ.get('MYSQL_USER'),
passwd= environ.get('MYSQL_PASSWORD'),
database= environ.get('MYSQL_DB'),
port= int(environ.get('MYSQL_PORT')),
auth_plugin="mysql_native_password"
)
cur = store_db.cursor(buffered=True)










from Website1.auth import auth1
app.register_blueprint(auth1, url_prefix="")

from Website1.user import user
app.register_blueprint(user, url_prefix="/user")

from Website1.staff import staff
app.register_blueprint(staff, url_prefix="/staff")

from Website1.Admin import admin
app.register_blueprint(admin, url_prefix="/admin")







if __name__=='__main__':
    app.run(debug=True)
    

