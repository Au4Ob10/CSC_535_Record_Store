from flask import Blueprint, request, session, redirect, render_template, url_for, flash, jsonify
from app import store_db, cur, app

img_display = Blueprint('img_display',__name__,static_folder="Website1/static", template_folder='Website1/templates')

@app.route("/shopping_page")
def shopping_page():
    return render_template('shopping_page.html')