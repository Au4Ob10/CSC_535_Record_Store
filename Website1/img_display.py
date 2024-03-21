from flask import Blueprint, request, session, redirect, render_template, url_for, flash, jsonify
from app import store_db, cur, app



img_display = Blueprint('img_display',__name__,static_folder="Website1/static", template_folder='Website1/templates')

@img_display.route('/img_display')
def display_records():
    cursor = store_db.cursor()
    cursor.execute("SELECT record_name, artist, img_link FROM records_detail")
    records = cursor.fetchall()
    return render_template('record_cart_page.html', records=records)

# if __name__ == '__main__':
#     app.run(debug=True)
