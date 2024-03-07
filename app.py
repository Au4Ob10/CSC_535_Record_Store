from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from os import environ

# Load environment variables
load_dotenv('.flaskenv')

print("MySQL Host:", environ.get("MYSQL_HOST"))
print("MySQL User:", environ.get("MYSQL_USER"))
print("MySQL Password:", environ.get("MYSQL_PASSWORD"))
print("MySQL Database:", environ.get("MYSQL_DB"))
print("MySQL Port:", int(environ.get('MYSQL_PORT')))

app = Flask(__name__, template_folder='Website1/templates')

app.secret_key = "csc-535-record-store-app"


# Configure MySQL
app.config['MYSQL_HOST'] = environ.get("MYSQL_HOST")
app.config['MYSQL_USER'] = environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = environ.get("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = environ.get("MYSQL_DB")
app.config['MYSQL_PORT'] = int(environ.get('MYSQL_PORT'))

mysql = MySQL(app)

try:
    mysql.connection.ping(reconnect=True)
    print("Successfully connected to MySQL database!")
except Exception as e:
    print("Failed to connect to MySQL database:", e)

from Website1.auth import auth1
app.register_blueprint(auth1, url_prefix="")


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



if __name__=='__main__':
    app.run(debug=True)
    


