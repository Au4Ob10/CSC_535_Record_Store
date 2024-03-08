from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from os import environ
import mysql.connector

# Load environment variables
load_dotenv('.flaskenv')

print("MySQL Host:", environ.get('MYSQL_HOST'))
print("MySQL User:", environ.get('MYSQL_USER'))
print("MySQL Password:", environ.get('MYSQL_PASSWORD'))
print("MySQL Database:", environ.get('MYSQL_DB'))
print("MySQL Port:", int(environ.get('MYSQL_PORT')))

app = Flask(__name__, template_folder='Website1/templates')

app.secret_key = "csc-535-record-store-app"

store_db = mysql.connector.connect(
host= environ.get('MYSQL_HOST'),
user= environ.get('MYSQL_USER'),
passwd= environ.get('MYSQL_PASSWORD'),
database= environ.get('MYSQL_DB'),
port= int(environ.get('MYSQL_PORT')),
auth_plugin="mysql_native_password"
)
cur = store_db.cursor(buffered=True)
# app.config['MYSQL_HOST'] = environ.get('MYSQL_HOST')
# app.config['MYSQL_USER'] = environ.get('MYSQL_USER')
# app.config['MYSQL_PASSWORD'] = environ.get('MYSQL_PASSWORD')
# app.config['MYSQL_DB'] = environ.get('MYSQL_DB')
# app.config['MYSQL_PORT'] = int(environ.get('MYSQL_PORT'))
# app.config['MYSQL_AUTH_PLUGIN'] = 'mysql_native_password'

# mysql = MySQL(app)

def test_mysql_connection():
    try:
        # Execute a simple query to test the connection
        cur.execute("SELECT VERSION()")

        # Fetch and print the result
        db_version = cur.fetchone()[0]
        print("MySQL Database Version:", db_version)

        # Close cursor and database connection
        cur.close()
        store_db.close()

        return True  # Return True if connection and query execution were successful

    except mysql.connector.Error as err:
        # Print error message if connection or query execution fails
        print("Failed to connect to MySQL database:", err)
        return False  # Return False if there was an error


# Call the function to test the connection
test_result = test_mysql_connection()

if test_result:
    print("Connection test successful!")
else:
    print("Connection test failed!")

# try:
#     mysql.connection.ping(reconnect=True)
#     print("Successfully connected to MySQL database!")
# except Exception as e:
#     print("Failed to connect to MySQL database:", e)

from Website1.auth import auth1
app.register_blueprint(auth1, url_prefix="")


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



if __name__=='__main__':
    app.run(debug=True)
    


