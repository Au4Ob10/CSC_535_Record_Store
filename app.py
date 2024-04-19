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

store_db = mysql.connector.connect(
host= environ.get('MYSQL_HOST', 'localhost'),
user= environ.get('MYSQL_USER'),
passwd= environ.get('MYSQL_PASSWORD', 'root'),
database= environ.get('MYSQL_DB'),
port= int(environ.get('MYSQL_PORT')),
auth_plugin="mysql_native_password"
)
cur = store_db.cursor(buffered=True)








# def test_mysql_connection():
#     try:
#         # Execute a simple query to test the connection
#         cur.execute("SELECT VERSION()")

#         # Fetch and print the result
#         db_version = cur.fetchone()[0]
#         print("MySQL Database Version:", db_version)

#         # Close cursor and database connection

#         return True  # Return True if connection and query execution were successful

#     except mysql.connector.Error as err:
#         # Print error message if connection or query execution fails
#         print("Failed to connect to MySQL database:", err)
#         return False  # Return False if there was an error


# test_result = test_mysql_connection()

# if test_result:
#     print("Connection test successful!")
# else:
#     print("Connection test failed!")


from Website1.auth import auth1
app.register_blueprint(auth1, url_prefix="")

from Website1.user import user
app.register_blueprint(user, url_prefix="/user")

from Website1.staff import staff
app.register_blueprint(staff, url_prefix="/staff")

from Website1.Admin import admin
app.register_blueprint(admin, url_prefix="/admin")

from Website1.img_display import img_display
app.register_blueprint(img_display, url_prefix="/img_display")


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/vines_record', methods=['GET'])
def vines_record_page():
    return render_template('record_page.html')

@app.route('/user_cart', methods=['GET','POST'])
def user_cart_page():
    return render_template('customer_cart.html')



if __name__=='__main__':
    app.run(debug=True)
    