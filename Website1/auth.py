from flask import Blueprint, request, session, redirect, render_template, url_for, flash
from app import store_db, cur
auth1 = Blueprint('auth1',__name__,static_folder="Website1/static", template_folder='Website1/templates')


@auth1.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_or_username = request.form.get('email_or_username')
        password = request.form.get('password')

        try:
            # Check if the login credentials match an email in the customer table
            cur.execute("SELECT email FROM customer WHERE email = %s AND passw = %s", (email_or_username, password))
            user_email = cur.fetchone()
            if user_email:
                session['email'] = user_email[0]  # Store the user's email in the session
                flash('Login successful!', 'success')
                return redirect(url_for('auth1.portal'))

            # Check if the login credentials match a username in the staff_credentials table
            cur.execute("SELECT username, isadmin FROM staff_credentials WHERE username = %s AND password = %s", (email_or_username, password))
            staff_data = cur.fetchone()
            if staff_data:
                username, isadmin = staff_data
                if isadmin == 1:
                    session['username'] = username  # Store the username in the session
                    flash('Admin Login!', 'success')
                    return redirect(url_for('admin.portal'))
                else:
                    session['username'] = username  # Store the username in the session
                    flash('Staff Login!', 'success')
                    return redirect(url_for('staff.portal'))

            flash('Invalid email/username or password. Please try again.', 'error')

        except Exception as e:
            flash(f'Error occurred: {e}', 'error')

    return render_template("index.html")

@auth1.route('/portal', methods=['GET', 'POST'])
def portal():
    if 'email' not in session:
        flash('You need to login first.', 'error')
        return redirect(url_for('auth1.login'))
    
    return render_template("index.html")

@auth1.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@auth1.route('/create_account_form', methods=['GET'])
def create_account_form():
    return render_template('create_account.html')

@auth1.route('/create_account', methods=['POST'])
def create_account():
    if request.method == 'POST':
        try:

            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            passw = request.form['pass1']
            passw2 = request.form['pass2']
            phone_num = request.form['phone_num']
            address = request.form['address']
            address2 = request.form.get('address2', '') 
            city = request.form['city']
            state = request.form['state']
            postal_code = request.form['postal_code']

            if passw == passw2:

                # Insert data into the database
                cur.execute("INSERT INTO customer (first_name, last_name, email, passw, phone_num, if_register) VALUES (%s, %s, %s, %s, %s, 1)",
                            (first_name, last_name, email, passw, phone_num))
                store_db.commit()

                # Get the customer ID of the newly inserted record
                customer_id = cur.lastrowid

                # Insert address into the database
                cur.execute("INSERT INTO address (customer_id, address, address2, city, state, postal_code) VALUES (%s, %s, %s, %s, %s, %s)",
                            (customer_id, address, address2, city, state, postal_code))
                store_db.commit()

                flash('Account created successfully!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Passwords do not match. Please try again.', 'error')
                return redirect(url_for('create_account_form'))

        except Exception as e:
            # Handle database errors
            print(e)
            store_db.rollback()
            flash('An error occurred while creating the account. Please try again.', 'error')
            return redirect(url_for('create_account_form'))

        finally:
            cur.close()