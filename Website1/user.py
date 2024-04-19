from flask import Blueprint, request, session, redirect, render_template, url_for, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email


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
        cur2 = store_db.cursor()
        name = session.get('name')
        id = session.get('customer_id')
        record_id = request.form.get('record_id')
        price = request.form.get('price')
        quantity = 1
        
        
        # Constructing the table name using current_user's email
        table_name = f"{name}{id}_cart"
        
        # Constructing and executing the SQL query
        sql = f"INSERT INTO `{table_name}` (record_id, customer_id, price, quantity) VALUES (%s, %s, %s, %s)"
        cur2.execute(sql, (record_id, id, price, quantity))
        
        cur2.execute(f"Update customer set cart = cart + 1 where customer_id = {id}")
        
        store_db.commit()  

        print('Item added to cart successfully')
        return redirect(url_for('user.home'))

    except Exception as e:
        store_db.rollback()
        return redirect(url_for('user.home'))

@user.route('/home')
def home():
    current_user = session.get('email')
    print(current_user)
    cur.execute("SELECT record_id, record_name, artist, img_link, price FROM records_detail")
    records = cur.fetchall()
    cur.execute("Select cart from customer where email = %s", (current_user,)) 
    cart_item_count = cur.fetchone()[0]
    print(cart_item_count)
    return render_template('userhome.html', current_user=current_user, cart_item_count=cart_item_count, records=records)

@user.route('/cart', methods=['GET', 'POST'])
def cart():
    current_user = session.get('email')
    name = session.get('name')
    id = session.get('customer_id')
    current_user_cart = f"`{name}{id}_cart`"

    cur.execute(f"""SELECT 
                           records_detail.record_name, 
                           records_detail.artist, 
                           records_detail.genre, 
                           records_detail.img_link,
                           {current_user_cart}.price * {current_user_cart}.quantity,
                           {current_user_cart}.quantity,
                           {current_user_cart}.itemID
                    FROM {current_user_cart}
                    INNER JOIN records_detail 
                    ON {current_user_cart}.record_id = records_detail.record_id;""")

    cart_details = cur.fetchall()

    cur.execute(f"""SELECT SUM({current_user_cart}.price * 
                              {current_user_cart}.quantity)
                              FROM {current_user_cart}""")

    item_total = cur.fetchone()
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
        item_id = request.form.get('item_id')
        
        # Constructing the table name using current_user's email
        table_name = f"{name}{id}_cart"
        
        # Constructing and executing the SQL query
        sql = f"DELETE FROM `{table_name}` WHERE itemID = %s"
        cur2.execute(sql, (item_id,))
        cur2.execute("Select cart from customer where customer_id = %s", (id,))
        cart_item_count = cur2.fetchone()[0]
        if cart_item_count > 0:
            cur2.execute(f"Update customer set cart = cart - 1 where customer_id = {id}")
        
        store_db.commit()  

        print('Item removed from cart successfully')
        return redirect(url_for('user.cart'))
    except Exception as e:
        store_db.rollback()
        return redirect(url_for('user.cart'))
    
@user.route('/record_details', methods=['GET','POST'])
def record_detail():
    try:
        name = session.get('name')
        id = session.get('customer_id')
        record_id=request.form.get('record_id')
        cur.execute('Select * from records_detail where record_id = %s',(record_id,))
        record_data = cur.fetchall()
        return render_template('record_detail.html', record_data=record_data, name=name, id=id)

    except Exception as e:
        flash('Unable to grab record_id','error')
        return redirect(url_for('user.home'))
    
@user.route('/review_record',methods=['GET','POST'])
def review_record():
    try:
        name = session.get('name')
        id = session.get('customer_id')
        record_id=request.form.get('record_id')
        review=request.form.get('review')
        cur.execute("INSERT INTO review_table (name,customer_id,record_id,review) Values(%s,%s,%s,%s)",(name,id,record_id,review,))
        store_db.commit()
        flash('Review has been posted thank you!','info')
        return redirect(url_for('user.home'))
    except Exception as e:
        flash('Unable to upload review','error')
        return redirect(url_for('user.home'))
    