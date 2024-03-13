from flask import Blueprint, request, session, redirect, render_template, url_for, flash
from app import cur
auth1 = Blueprint('auth1',__name__,static_folder="Website1/static", template_folder='Website1/templates')


def get_current_employee_id():
    return session.get('employeeID', None)

@auth1.route('/login', methods=['GET', 'POST'])
def login():
    entered_pin = request.form.get('pin')

    if request.method == 'POST':
        try:
            # Check manager PIN
            cur.execute("SELECT employeeID, is_manager FROM Employees WHERE pin = %s", (entered_pin,))
            result = cur.fetchone()

            if result:
                    employeeID, is_manager = result
                    session['employeeID'] = employeeID  # Store employeeID in the session

                    if is_manager:
                        flash('Login successful as Manager!', category='success')
                        return render_template("Manager.html")
                    else:
                        flash('Login successful as Employee!', category='success')
                        return redirect(url_for('auth.create_order'))
            else:
                flash('Invalid pin please try again', category='error')
                        
        except Exception as e:
            flash(f'Error fetching orders: {e}', category='error')

    return render_template("login.html", boolean=True)

@auth1.route('/portal', methods=['GET','POST'])
def portal():
    return render_template("orders.html")
# @auth1.route("/")
# def index():
#     user_id = session.get("usr_id", None)
#     if not user_id:
#         return redirect("/login")
#     return redirect(f"/home/{user_id}")

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
            phone_num = request.form['phone_num']
            address = request.form['address']
            address2 = request.form.get('address2', '') 
            city = request.form['city']
            state = request.form['state']
            postal_code = request.form['postal_code']

            # Insert data into the database
            cur.execute("INSERT INTO customer (first_name, last_name, email, phone_num, if_register) VALUES (%s, %s, %s, %s, 1)",
                           (first_name, last_name, email, phone_num))
            store_db.commit()

            # Get the customer ID of the newly inserted record
            customer_id = cur.lastrowid

            # Insert address into the database
            cur.execute("INSERT INTO address (customer_id, address, address2, city, state, postal_code) VALUES (%s, %s, %s, %s, %s, %s)",
                           (customer_id, address, address2, city, state, postal_code))
            store_db.commit()

            flash('Account created successfully!', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            # Handle database errors
            print(e)
            store_db.rollback()
            flash('An error occurred while creating the account. Please try again.', 'error')
            return redirect(url_for('index'))

        finally:
            cur.close()