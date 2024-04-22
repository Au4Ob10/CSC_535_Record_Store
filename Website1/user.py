from flask import Blueprint, request, session, redirect, render_template, url_for, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email
import datetime


from app import store_db, cur


user = Blueprint('user',__name__,static_folder="Website1/static", template_folder='Website1/templates')

#All user related routes so adding to cart removing from cart checking out and inserting payment info.
#Index functionality related to records should be kept here 


class PaymentForm(FlaskForm):
    cardholder_name = StringField('Name on Card', validators=[DataRequired(), Length(min=2, max=100)])
    card_number = StringField('Card Number', validators=[DataRequired(), Length(min=16, max=16)])
    expiry_date = StringField('Expiration Date (MM/YY)', validators=[DataRequired(), Length(min=5, max=5)])
    cvv = StringField('CVV', validators=[DataRequired(), Length(min=3, max=3)])
    submit = SubmitField()
    
@user.route("/add_to_cart", methods=['POST'])
def add_to_cart():
    try:
        if request.method == 'POST':
            
           
            name = session.get('name')
            id = session.get('customer_id')
            record_id = request.form.get('record_id')
            price = request.form.get('price')
            
            # Constructing the table name using current_user's email
            table_name = f"{name}{id}_cart"
            
            with store_db.cursor() as cur2:
                cur2.execute(f"SELECT * FROM {table_name}")
                myresults = cur2.fetchall()
                
                print(myresults)
                print(record_id)
                # Create table if not exists
        
             
                # Commit the table creation
                store_db.commit()
                
                rec_id_check = f"SELECT record_id FROM {table_name} WHERE record_id = %s;"
                cur2.execute(rec_id_check, (record_id,))
                id_result = cur2.fetchall()
                
                # Check if the record_id already exists in the table
            
                if not id_result:
                    # If the record_id doesn't exist, insert the new record
                    sql = f"INSERT INTO {table_name} (record_id, customer_id, price, quantity) VALUES (%s, %s, %s, %s);"
                    cur2.execute(sql, (record_id, id, price, 1))
                    print("this is true")
                    store_db.commit()

                else:
                    # If the record_id exists, update the quantity
                    update_query = f"""UPDATE {table_name} 
                                    SET quantity = quantity + 1
                                    WHERE record_id = %s;"""
                    cur2.execute(update_query, (record_id,))
                    store_db.commit()
                
            
               
                print('Item added to cart successfully')
                return redirect(url_for('user.home'))


    except Exception as e:
        store_db.rollback()
        return redirect(url_for('user.home'))

@user.route('/home')
def home():
    current_user = session.get('email')
    name = session.get('name')
    id = session.get('customer_id')
    table_name = f"{name}{id}_cart"
    
    with store_db.cursor() as cur:
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
                                    record_id int NOT NULL,
                                    customer_id int NOT NULL,
                                    price int NOT NULL,
                                    quantity int NOT NULL,
                                    PRIMARY KEY(record_id)
                                    ) ENGINE = InnoDB;""")
        
        # print(current_user)

        cur.execute("SELECT record_id, record_name, artist, img_link, price FROM records_detail")
        records = cur.fetchall()
        cur.execute("Select cart from customer where email = %s", (current_user,)) 
        cart_item_count = cur.fetchone()[0]
        cur.execute(f"SELECT SUM(quantity) FROM {table_name}")
        total_qty = cur.fetchone()[0]
        
        if not total_qty:
            total_qty = 0
        # print(cart_item_count)
    return render_template('userhome.html', total_qty=total_qty, current_user=current_user, cart_item_count=cart_item_count, records=records)

@user.route('/cart', methods=['GET', 'POST'])
def cart():
    current_user = session.get('email')
    name = session.get('name')
    id = session.get('customer_id')
    current_user_cart = f"{name}{id}_cart"

    cur.execute(f"""SELECT 
                           records_detail.record_name, 
                           records_detail.artist, 
                           records_detail.genre, 
                           records_detail.img_link,
                           {current_user_cart}.price * {current_user_cart}.quantity,
                           {current_user_cart}.quantity,
                           {current_user_cart}.record_id
                    FROM {current_user_cart}
                    INNER JOIN records_detail 
                    ON {current_user_cart}.record_id = records_detail.record_id;""")

    cart_details = cur.fetchall()

    cur.execute(f"""SELECT SUM({current_user_cart}.price * 
                              {current_user_cart}.quantity)
                              FROM {current_user_cart}""")

    item_total = cur.fetchone()[0]
    
    if not item_total:
        item_total = 0
    return render_template('cart.html',cart_details=cart_details, item_total=item_total)



@user.route('/payment', methods=['GET', 'POST'])
def payment():
    form = PaymentForm()
    labels_and_inputs = [(item.label, item) for item in form]
    if form.validate_on_submit():
        print("Form data:")
        print("Cardholder Name:", form.cardholder_name.data)
        print("Card Number:", form.card_number.data)
        print("Expiry Date:", form.expiry_date.data)
        print("CVV:", form.cvv.data)
       
        # process the form data
        # process the form data
        return render_template('orderprocessed.html', title='Payment', form=form)
    else: 
        return render_template('payment.html', title='Payment', labels_and_inputs=labels_and_inputs[0:4], submit_btn=labels_and_inputs[4], form=form)
    
    
@user.route('/remove_from_cart', methods=['GET', 'POST'])
def remove_from_cart():
    try:
        cur2 = store_db.cursor()
        name = session.get('name')
        id = session.get('customer_id')
        item_id = request.form.get('record_id')
        
        # Constructing the table name using current_user's email
        table_name = f"{name}{id}_cart"
        
        # Constructing and executing the SQL query
        sql = f"DELETE FROM `{table_name}` WHERE record_id = %s"
        cur2.execute(sql, (item_id,))
        cur2.execute("Select cart from customer where customer_id = %s", (id,))
        cart_item_count = cur2.fetchone()[0]
        if cart_item_count > 0:
            cur2.execute(f"Update customer set cart = cart - 1 where customer_id = {id}")
        
        store_db.commit()  

        print('Item removed from cart successfully')
        print(item_id)
        return redirect(url_for('user.cart'))
    except Exception as e:
        store_db.rollback()
        return redirect(url_for('user.cart'))
    
@user.route('/record_details', methods=['GET','POST'])
def record_details():
    try:
        current_user = session.get('email')
        record_id = request.form.get('record_id')
        cur.execute("Select cart from customer where email = %s", (current_user,)) 
        cart_item_count = cur.fetchone()[0]
        cur.execute('Select * from records_detail where record_id = %s',(record_id,))
        record_data = cur.fetchall()
        cur.execute('Select * from review_table where record_id = %s',(record_id,))
        review_data = cur.fetchall()
        return render_template('deets.html',record_data=record_data, current_user=current_user, cart_item_count=cart_item_count,review_data=review_data)
    except Exception as e:
        print(e)
        flash('Unable to grab record_id','error')
        return redirect(url_for('user.home'))
    
@user.route('/review_record',methods=['GET','POST'])
def review_record():
    try:
        name = session.get('name')
        id = session.get('customer_id')
        record_id = request.form.get('id')
        review=request.form.get('review')
        print(request.form)
        print(record_id)
        cur.execute("INSERT INTO review_table (customer_name,customer_id,record_id,review) Values(%s,%s,%s,%s)",(name,id,record_id,review,))
        cur.execute("Update records_detail set review_count = review_count + 1 where record_id = %s",(record_id,))
        store_db.commit()
        flash('Review has been posted thank you!','info')
        return redirect(url_for('user.home'))
    except Exception as e:
        print(e)
        flash('Unable to upload review','error')
        return redirect(url_for('user.home'))
    
@user.route('/search_logged', methods=['GET'])
def search_records():
    current_user = session.get('email')
    print(current_user)
    search_query = request.args.get('query')
    cursor = store_db.cursor(dictionary=True)
    cur.execute("Select cart from customer where email = %s", (current_user,)) 
    cart_item_count = cur.fetchone()[0]
    sql = "SELECT * FROM records_detail WHERE record_name LIKE %s OR artist LIKE %s OR genre LIKE %s"
    cursor.execute(sql, ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
    records = cursor.fetchall()
    print (records)
    cursor.close()
    return render_template('search_results_logged.html', current_user=current_user, cart_item_count=cart_item_count, records=records)

@user.route('/profile', methods=['GET'])
def profile():
    try:
        current_user = session.get('email')
        cur.execute("Select * from customer where email = %s", (current_user,))
        user_data = cur.fetchall()
        return render_template('profile.html', user_data=user_data)
        
    except Exception as e:
        flash('Unable to grab user data', 'error')
        return redirect(url_for('user.home'))
    
@user.route('/change_password', methods=['GET','POST'])
def change_password():
    try:
        current_user = session.get('email')
        old_pass = request.form.get('old_pass')
        new_pass1 = request.form.get('new_pass1')
        new_pass2 = request.form.get('new_pass2')
        cur.execute("Select passw from customer where email = %s", (current_user,))
        if old_pass != cur.fetchone()[0]:
            flash('Old password is incorrect', 'error')
            return redirect(url_for('user.profile'))
        else:
            if new_pass1 != new_pass2:
                flash('New passwords do not match', 'error')
                return redirect(url_for('user.profile'))
            else:
                cur.execute("Update customer set passw = %s where email = %s", (new_pass1, current_user))
                store_db.commit()
                flash('Password has been changed successfully', 'info')
                return redirect(url_for('user.profile'))
    except Exception as e:
        flash('Unable to grab user data', 'error')
        return redirect(url_for('user.profile'))
@user.route('/change_email', methods=['GET','POST'])
def change_email():
    try:
        current_email = session.get('email')
        old_email = request.form.get('old_email')
        email1 = request.form.get('email1')
        email2 = request.form.get('email2')
        if current_email == old_email:
            if email1 != email2:
                flash('New emails do not match', 'error')
                return redirect(url_for('user.profile'))
            else:
                cur.execute("Select email from customer where email = %s", (email1,))
                if cur.fetchone():
                    flash('Email already exists', 'error')
                    return redirect(url_for('user.profile'))
                else:
                    cur.execute("Update customer set email = %s where email = %s", (email1, current_email))
                    store_db.commit()
                    session['email'] = email1
                    flash('Email has been changed successfully', 'info')
                    return redirect(url_for('user.profile'))
        
    except Exception as e:
        flash('Unable to grab user data', 'error')
        return redirect(url_for('user.profile'))
    
        
    