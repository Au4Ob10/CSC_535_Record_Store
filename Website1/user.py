from flask import Blueprint, request, session, redirect, render_template, url_for, flash
from app import store_db, cur

user = Blueprint('user',__name__,static_folder="Website1/static", template_folder='Website1/templates')