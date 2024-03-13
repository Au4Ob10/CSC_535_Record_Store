from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from os import environ
import mysql.connector
load_dotenv('.flaskenv')
app = Flask(__name__, template_folder='Website1/templates')

######START -Initialize Database Function
def initialize_database(): 
    try:
        # Connect to MySQL without specifying the database
        store_db = mysql.connector.connect(
            host=environ.get('MYSQL_HOST'),
            user=environ.get('MYSQL_USER'),
            passwd=environ.get('MYSQL_PASSWORD'),
            port=int(environ.get('MYSQL_PORT')),
            auth_plugin="mysql_native_password"
        )

        # Create a cursor object
        cur = store_db.cursor(buffered=True)

        # Execute SQL commands to create the database
        cur.execute("CREATE DATABASE IF NOT EXISTS record_store")
        cur.execute("USE record_store")

        # Execute the provided MySQL code
        with open('Recordstore.sql', 'r') as file:
            sql_script = file.read()
            cur.execute(sql_script)

        # Close the cursor
        cur.close()

        print("Database initialized successfully.")

    except mysql.connector.Error as err:
        print("Error:", err)


initialize_database()
######END



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

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)
    


