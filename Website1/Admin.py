from flask import Blueprint, request, session, redirect, render_template, url_for, flash, jsonify
from app import store_db, cur


admin = Blueprint('admin',__name__,static_folder="Website1/static", template_folder='Website1/templates')

#Only admin related functions within this route adding new staff members, accessing orders, order history, managing staff members, adding albums, 
#restocking, discounting items 


@admin.route('/portal', methods=['GET', 'POST'])
def portal():
    if 'username' not in session:
        flash('You need to login first.', 'error')
        return redirect(url_for('auth1.login'))
    
    return render_template("admin_index.html")
@admin.route('/staff',methods=['GET','POST'])
def get_staff():
    try:
        cur.execute("SELECT * FROM staff_credentials WHERE isadmin = 0")
        staff_list = cur.fetchall()
        return render_template("staff.html", staff_list=staff_list)
    except Exception as e:
        print(e)
        flash('An error occurred while retrieving staff list. Please try again.', 'error')
        return render_template("staff.html", staff_list=None)
    finally:
        cur.close

def Staff():
    return get_staff()
@admin.route('/remove_staff', methods=['GET','POST'])
def Remove():
    if request.method == 'POST':
        try:
            staff_id_to_remove = request.form.get('remove_staff_id')
            remove_cursor = store_db.cursor()  # Create a new cursor
            remove_cursor.execute("DELETE FROM staff_credentials WHERE staff_id = %s", (staff_id_to_remove,))
            store_db.commit()
            flash('Staff member removed from database!', 'success')
        except Exception as e:
            print(e)
            store_db.rollback()
            flash('An error occurred while removing staff member. Please try again.', 'error')
        finally:
            remove_cursor.close()  # Close the cursor
        return redirect(url_for('admin.get_staff'))
    return redirect(url_for('admin.get_staff'))
        
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

#Retrieve OrderID & Info from mysql


def getOrderData():
    cur.execute("SELECT * FROM orders")
    col_data = cur.fetchall()
    
    return col_data
    
    
@admin.route('/orderhistory')    
def History():
    
    order_data = getOrderData()
    
    
    return render_template('order_history.html',order_data=order_data)

@admin.route('/addrecord', methods=['GET','POST'])
def Addrecord():
    return render_template('addrecord.html')

@admin.route('/stock', methods=['GET','POST'])
def Showstock():
    return render_template('stock.html')