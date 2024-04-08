from flask import Blueprint, request, session, redirect, render_template, url_for, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email


from app import store_db, cur

user = Blueprint('user',__name__,static_folder="Website1/static", template_folder='Website1/templates')

#All user related routes so adding to cart removing from cart checking out and inserting payment info.
#Index functionality related to records should be kept here 


class PaymentForm(FlaskForm):
    cardholder_name = StringField('Cardholder Name', validators=[DataRequired(), Length(min=2, max=100)])
    card_number = StringField('Card Number', validators=[DataRequired(), Length(min=16, max=16)])
    expiry_date = StringField('Expiry Date (MM/YY)', validators=[DataRequired(), Length(min=5, max=5)])
    cvv = IntegerField('CVV', validators=[DataRequired()])
    submit = SubmitField('Submit Payment')
@user.route("/add_to_cart", methods=['POST'])
def add_to_cart():
    try:
        cur2 = store_db.cursor()
        current_user = session.get('email')
        record_id = request.form.get('record_id')
        
        # Fetching customer_id based on email
        cur2.execute("SELECT customer_id FROM customer WHERE email = %s", (current_user,))
        customer_id = cur2.fetchone()[0]
        
        # Constructing the table name using current_user's email
        table_name = f"{current_user}_cart"
        
        # Constructing and executing the SQL query
        sql = f"INSERT INTO `{table_name}` (record_id, customer_id) VALUES (%s, %s)"
        cur2.execute(sql, (record_id, customer_id))
        
        store_db.commit()  

        print('Item added to cart successfully')
        return jsonify({'message': 'Item added to cart successfully'}), 200

    except Exception as e:
        store_db.rollback()
        return jsonify({'error': str(e)}), 500

@user.route('/home')
def home():
    current_user = session.get('email')
    #cart_item_count is a test variable 
    cart_item_count=5
    return render_template('userhome.html', current_user=current_user, cart_item_count=cart_item_count)

@user.route('/cart')
def cart():
    return render_template('cart.html')


@user.route('/payment', methods=['GET', 'POST'])
def payment():
    form = PaymentForm()
    if form.validate_on_submit():
        print("Form data:")
        print("Cardholder Name:", form.cardholder_name.data)
        print("Card Number:", form.card_number.data)
        print("Expiry Date:", form.expiry_date.data)
        print("CVV:", form.cvv.data)
        # process the form data
        # process the form data
        return render_template('orderprocessed.html', title='Payment', form=form)
    else: return render_template('payment.html', title='Payment', form=form)