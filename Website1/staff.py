from flask import Blueprint, request, session, redirect, render_template, url_for, flash
from app import store_db, cur

staff = Blueprint('staff',__name__,static_folder="Website1/static", template_folder='Website1/templates')
#All staff related routes similar to admin but less privledges they can manage and discount orders but they can not manage staff or add new records/restock inventory

@staff.route('/portal', methods=['GET', 'POST'])
def portal():
    if 'username' not in session:
        flash('You need to login first.', 'error')
        return redirect(url_for('auth1.login'))
    
    return render_template("staff_index.html")

@staff.route('/orderhistory')    
def History():
    return render_template('staff_order_history.html')