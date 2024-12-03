from flask import Blueprint, request, session, redirect, render_template, url_for, flash, jsonify
from app import store_db, cur
auth1 = Blueprint('auth1',__name__,static_folder="Website1/static", template_folder='Website1/templates')


@auth1.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_or_username = request.form.get('email_or_username')
        password = request.form.get('password')

        try:
            # Check if the login credentials match an email in the customer table
            cur.execute("SELECT customer_id, first_name, email  FROM customer WHERE email = %s AND passw = %s", (email_or_username, password))
            result = cur.fetchone()
            if result:
                customer_id, first_name, user_email = result
                session['email'] = user_email  # Store the user's email in the session
                session['name'] = first_name  # Store the user's name in the session
                session['customer_id'] = customer_id  # Store the user's ID in the session
                flash('Login successful!', 'info')
                return redirect(url_for('auth1.portal'))

            # Check if the login credentials match a username in the staff_credentials table
            cur.execute("SELECT username, isadmin FROM staff_credentials WHERE username = %s AND password = %s", (email_or_username, password))
            staff_data = cur.fetchone()
            if staff_data:
                username, isadmin = staff_data
                if isadmin == 1:
                    session['username'] = username  # Store the username in the session
                    flash('Admin Login!', 'info')
                    return redirect(url_for('admin.portal'))
                else:
                    session['username'] = username  # Store the username in the session
                    flash('Staff Login!', 'info')
                    return redirect(url_for('staff.portal'))

            flash('Invalid email/username or password. Please try again.', 'error')

        except Exception as e:
            flash(f'Error occurred: {e}', 'error')

    return redirect(url_for("auth1.index"))

@auth1.route('/portal', methods=['GET', 'POST'])
def portal():
    if 'email' not in session:
        flash('You need to login first.', 'error')
        return redirect(url_for('auth1.login'))    
    return redirect(url_for("user.home"))


@auth1.route('/', methods=['GET', 'POST'])
def index():
    cur.execute("SELECT record_name, artist, img_link FROM records_detail")
    records = cur.fetchall()
    return render_template('record_store_homepage.html',records=records)


@auth1.route('/search', methods=['GET'])
def search_records():
    search_query = request.args.get('query')
    cursor = store_db.cursor(dictionary=True)
    sql = "SELECT * FROM records_detail WHERE record_name LIKE %s OR artist LIKE %s OR genre LIKE %s"
    cursor.execute(sql, ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
    records = cursor.fetchall()
    cursor.close()
    return render_template('search_results.html', records=records)


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
            # Check password 1 and 2 see if they match
            if passw == passw2:
                # Check if Email is in Database
                cur.execute("Select email from customer where email =%s",(email,))
                result=cur.fetchone()
                print(result)
                if result:
                    flash('User already exists in the database try again', 'error')
                    return redirect(url_for('auth1.create_account_form'))
                else:
                    cur.execute("INSERT INTO customer (first_name, last_name, email, passw, phone_num, if_register) VALUES (%s, %s, %s, %s, %s, 1)",
                                (first_name, last_name, email, passw, phone_num))
                    # logging.debug('Created customer entry')
                    print('Created customer entry')
                    store_db.commit()

                    # Get the customer ID of the newly inserted record
                    customer_id = cur.lastrowid

                    # Insert address into the database
                    cur.execute("INSERT INTO address (customer_id, address, address2, city, state, postal_code) VALUES (%s, %s, %s, %s, %s, %s)",
                                (customer_id, address, address2, city, state, postal_code))
                    # logging.debug('Created address entry')
                    print('Created address entry')
                    store_db.commit()

                    cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS `{first_name}{customer_id}_cart` (
                        `itemID` INT NOT NULL AUTO_INCREMENT,
                        `record_id` INT,
                        `customer_id` INT,
                        `price` DECIMAL(10, 2),
                        `quantity` INT,
                        PRIMARY KEY (`itemID`)
                    )
                    """)
                    # logging.debug('Created cart table')
                    print('Created cart table')
                    store_db.commit()



                    flash('Account created successfully!', 'info')
                    session['email'] = email
                    session['name'] = first_name
                    session['customer_id'] = customer_id
                    return redirect(url_for('user.home'))
            else:
                flash('Passwords do not match. Please try again.', 'error')
                return redirect(url_for('auth1.create_account_form'))
                


        except Exception as e:
            # Handle database errors
            print(e)
            store_db.rollback()
            flash('An error occurred while creating the account. Please try again.', 'error')
            return redirect(url_for('auth1.create_account_form'))


        finally:
            # cur.close()
            pass


@auth1.route("/logout", methods=['GET','POST'])
def logout():
    cur.execute("SELECT record_name, artist, img_link FROM records_detail")
    records = cur.fetchall()
    session['username'] = ''
    session['email'] = ''
    flash('Logged Out!', 'success')
    return render_template('record_store_homepage.html',records=records)

def orderList():
   my_cur = store_db.cursor()
   my_cur.execute("SELECT * FROM orders", multi=True)
   order_data = my_cur.fetchall()
   
   my_cur.close()
   return order_data
    
@auth1.route('/orderdata')
def fetch_data():
    order_data = orderList()
    return jsonify(order_data)