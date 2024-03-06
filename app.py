from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from os import environ


app = Flask(__name__, template_folder='Website1/templates')

app.secret_key = "csc-535-record-store-app"

# Load environment variables
load_dotenv('.flaskenv')

# Configure MySQL
app.config['MYSQL_HOST'] = environ.get("MYSQL_IP")
app.config['MYSQL_USER'] = environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = environ.get("MYSQL_PASS")
app.config['MYSQL_DB'] = environ.get("MYSQL_DB")
app.config['MYSQL_PORT'] = int(environ.get('MYSQL_PORT'))

mysql = MySQL(app)

from Website1.auth import auth1
app.register_blueprint(auth1, url_prefix="")


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



if __name__=='__main__':
    app.run(debug=True)
    


