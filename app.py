from flask import Flask, request, render_template
from Website import __init__

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


if __name__=='__main__':
    app.run(debug=True)

    