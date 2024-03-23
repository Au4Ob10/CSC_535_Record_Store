from flask import Blueprint, request, session, redirect, render_template, url_for, flash, jsonify
from app import store_db, cur

user = Blueprint('user',__name__,static_folder="Website1/static", template_folder='Website1/templates')

#All user related routes so adding to cart removing from cart checking out and inserting payment info.
#Index functionality related to records should be kept here 

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