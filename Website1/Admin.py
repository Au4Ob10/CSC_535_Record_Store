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
                cur.execute("Select * from staff_credentials where username = %s", (usern,))
                is_exist = cur.fetchall()
                if is_exist:
                    flash('Username already exists!','error')
                    return render_template("add_staff.html")
                else:
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

# @admin.route('/addstaff', methods=['GET','POST'])
# def Add():

@admin.route('/addRecord', methods=['GET', 'POST'])
def addRecord():
    if request.method == 'POST':
        record_name = request.form['record_name']
        artist = request.form['artist']
        genre = request.form['genre']
        img_link = request.form['img_link']
        price = request.form['price']
        quantity = request.form['quantity']

        # Insert record into the database
        insert_query = "INSERT INTO records_detail (record_name, artist, genre, img_link, price, quantity) VALUES (%s, %s,%s, %s, %s, %s)"
        record_data = (record_name, artist, genre, img_link,price,quantity)
        cur.execute(insert_query, record_data)
        store_db.commit()
        flash('Record added to database','info')
        return redirect(url_for('admin.addRecord'))
    return render_template('add_record.html')

@admin.route('/deleteRecord', methods=['GET','POST'])
def deleteRecord():
    if request.method == 'POST':
        record_id = request.form['record_id']
        cur.execute("DELETE FROM records_detail WHERE record_id = %s", (record_id,))
        store_db.commit()
        flash('Record deleted successfully!', 'success')
        return redirect(url_for('admin.Showstock'))
    return render_template('stock.html')
    
    

@admin.route('/stock', methods=['GET','POST'])
def Showstock():
    if request.method == 'GET':
        cur.execute("SELECT * FROM records_detail")
        stock_data = cur.fetchall()
        return render_template('stock.html', stock_data=stock_data)
    

@admin.route('/addstock', methods=['POST'])
def addstock():
    if request.method == 'POST':
        record_id = request.form['record_id']
        quantity = request.form['quantity']
        cur.execute("UPDATE records_detail SET quantity = quantity + %s WHERE record_id = %s", (quantity, record_id))
        store_db.commit()
        flash('Stock updated successfully!', 'success')
        return redirect(url_for('admin.Showstock'))
    
@admin.route('/removestock', methods=['POST'])
def removestock():
    if request.method == 'POST':
        record_id = request.form['record_id']
        quantity = request.form['quantity']
        cur.execute("UPDATE records_detail SET quantity = quantity - %s WHERE record_id = %s", (quantity, record_id))
        store_db.commit()
        flash('Stock updated successfully!', 'success')
        return redirect(url_for('admin.Showstock'))
    return render_template('stock.html')

@admin.route('/displaycart', methods=['GET','POST'])
def displaycart():
    try:
        cur.execute("Select * from customer")
        customer_data = cur.fetchall()
        return render_template('admin_cart_index.html', customer_data=customer_data)
    except Exception as e:
        print(e)
        flash('an error occurred while retrieving customer data please try again.', 'error')
        return render_template('admin_cart_index.html', customer_data=None)
    
@admin.route('/editcart', methods=['GET','POST'])
def editcart():
    try:
            customerid = request.form['userid']
            username = request.form['username']
            print(username)
            print(customerid)
            current_user_cart = f"`{username}{customerid}_cart`"

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
            return render_template('admin_edit.html',cart_details=cart_details, item_total=item_total)
        
    except Exception as e:
        print(e)
        flash('An error occurred while retrieving cart data. Please try again.', 'error')
        return redirect(url_for('admin.displaycart'))
    

@admin.route('/updatecart', methods=['POST'])
def discount():
    customerid = request.form['userid']
    item_id = request.form['item_id']
    new_price = request.form['new_price']
    cur.execute("SELECT first_name FROM customer WHERE customer_id = %s", (customerid,))
    username = cur.fetchone()[0]
    current_user_cart = f"`{username}{customerid}_cart`"
    try:
        cur.execute(f"UPDATE {current_user_cart} SET price = %s WHERE itemID = %s", (new_price, item_id))
        store_db.commit()
        flash('Cart updated successfully!', 'success')
        return redirect(url_for('admin.editcart'))
    except Exception as e:
        print(e)
        flash('An error occurred while updating cart. Please try again.', 'error')
        return redirect(url_for('admin.editcart'))