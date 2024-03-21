from flask import Blueprint, request, session, redirect, render_template, url_for, flash, jsonify
from app import store_db, cur

user = Blueprint('user',__name__,static_folder="Website1/static", template_folder='Website1/templates')

#All user related routes so adding to cart removing from cart checking out and inserting payment info.
#Index functionality related to records should be kept here 

@user.route("/add_to_cart", methods=['GET', 'POST'])
def add_to_cart():
    try:
      current_user = session.get('email')
      record_id = request.form.get('record_id')
      cur.execute("SELECT customer_id FROM customer WHERE email = %s", (current_user))
      customer_id = cur.fetchone()
      
      cur.execute(
         "INSERT INTO `{email}_cart` (record_id, customer_id) VALUES (%s, %s)"
         , (record_id, customer_id))
      store_db.commit()  
      print('Item added to cart successfully')
      return jsonify({'message': 'Item added to cart successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500