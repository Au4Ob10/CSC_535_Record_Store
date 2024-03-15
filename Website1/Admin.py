from flask import Blueprint, request, session, redirect, render_template, url_for, flash
from app import store_db, cur

admin = Blueprint('admin',__name__,static_folder="Website1/static", template_folder='Website1/templates')


@admin.route('/portal', methods=['GET', 'POST'])
def portal():
    if 'username' not in session:
        flash('You need to login first.', 'error')
        return redirect(url_for('auth1.login'))
    
    return render_template("admin_index.html")
@admin.route('/staff',methods=['GET','POST'])
def Staff():
    return render_template("staff.html")
def Remove():
    return render_template("staff.html")

@admin.route('/addstaff')
def Add():
    return render_template("add_staff.html")

@admin.route('/orderhistory')    
def History():
    return render_template('order_history.html')
