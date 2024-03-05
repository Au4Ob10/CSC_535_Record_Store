from flask import request, session, redirect, render_template, url_for, flash
from Website import app, mysql

def init_cursor():
    return mysql.connection.cursor(dictionary=True)



@app.route("/")
def index():
    user_id = session.get("usr_id", None)
    if not user_id:
        return redirect("/login")
    return redirect(f"/home/{user_id}")

@app.route('/create_account_form', methods=['GET'])
def create_account_form():
    return render_template('create_account.html')

@app.route('/create_account', methods=['POST'])
def create_account():
    if request.method == 'POST':
        try:
            cursor = init_cursor()
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone_num = request.form['phone_num']
            address = request.form['address']
            address2 = request.form.get('address2', '')  # Optional field
            city = request.form['city']
            state = request.form['state']
            postal_code = request.form['postal_code']

            # Insert data into the database
            cursor.execute("INSERT INTO customer (first_name, last_name, email, phone_num, if_register) VALUES (%s, %s, %s, %s, 1)",
                           (first_name, last_name, email, phone_num))
            mysql.connection.commit()

            # Get the customer ID of the newly inserted record
            customer_id = cursor.lastrowid

            # Insert address into the database
            cursor.execute("INSERT INTO address (customer_id, address, address2, city, state, postal_code) VALUES (%s, %s, %s, %s, %s, %s)",
                           (customer_id, address, address2, city, state, postal_code))
            mysql.connection.commit()

            flash('Account created successfully!', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            # Handle database errors
            print(e)
            mysql.connection.rollback()
            flash('An error occurred while creating the account. Please try again.', 'error')
            return redirect(url_for('index'))

        finally:
            cursor.close()