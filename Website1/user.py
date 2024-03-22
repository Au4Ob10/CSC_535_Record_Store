from flask import Blueprint, request, session, redirect, render_template, url_for, flash
from app import store_db, cur

user = Blueprint('user',__name__,static_folder="Website1/static", template_folder='Website1/templates')

#All user related routes so adding to cart removing from cart checking out and inserting payment info.
#Index functionality related to records should be kept here 
@user.route('/home')
def home():
    current_user = session.get('email')
    #cart_item_count is a test variable 
    cart_item_count=5
    return render_template('userhome.html', current_user=current_user, cart_item_count=cart_item_count)

@user.route('/cart')
def cart():
    return render_template('cart.html')