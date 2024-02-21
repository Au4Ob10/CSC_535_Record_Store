from flask import Flask, request, render_template, redirect, url_for
# from Website import createdb

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/button_press')
# def button_press():
#     return redirect(url_for('registration'))

# @app.route('/registration')
# def registration():
#     return render_template('reg.html')




if __name__=='__main__':
    app.run(debug=True)


# @app.route('/register', methods=["POST", "GET"])
# def regPage():
#     return render_template("reg.html")


    