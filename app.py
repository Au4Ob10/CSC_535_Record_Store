from flask import Flask, request, render_template, redirect, url_for
# from Website import createdb

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')


if __name__=='__main__':
    app.run(debug=True)

    