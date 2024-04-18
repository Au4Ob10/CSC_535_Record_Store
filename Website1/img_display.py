from flask import Blueprint, request, session, redirect, render_template, url_for, flash, jsonify
from app import store_db, cur, app



img_display = Blueprint('img_display',__name__,static_folder="Website1/static", template_folder='Website1/templates')


cur.execute("SELECT record_name, artist, img_link FROM records_detail")
records = cur.fetchall()

@img_display.route('/img_display')
def display_records():
 
    return render_template('record_store_homepage.html', records=records)

# if __name__ == '__main__':
#     app.run(debug=True)