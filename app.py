from flask import Flask, request, render_template, redirect, url_for
from Website import app as website_app
from Website.routes import*


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



if __name__=='__main__':
    website_app.run(debug=True)

