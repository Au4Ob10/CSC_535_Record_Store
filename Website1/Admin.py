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

@admin.route('/addstaff', methods=['GET','POST'])
def Add():
    if request.method == 'POST':
        try:
            usern = request.form['username']
            email = request.form['email']
            pass1 = request.form['pass1']
            pass2 = request.form['pass2']
            if pass1 == pass2:
                cur.execute("Insert Into staff_credentials(username,password,email,isadmin) VALUES (%s,%s,%s,0)",
                            (usern,pass1,email))
                store_db.commit()
                flash('Staff member added to database!','success')
                return render_template("add_staff.html")
        except Exception as e:
            print(e)
            store_db.rollback()
            flash('An error occurred while creating staff member. Please try again.', 'error')
            return render_template("add_staff.html")
        finally:
            cur.close
    return render_template("add_staff.html")

@admin.route('/orderhistory')    
def History():
    return render_template('order_history.html')

