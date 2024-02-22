from flask import request, session, redirect, render_template, url_for, flash
from app import app



@app.route("/")
def index():
    user_id = session.get("usr_id", None)
    if not user_id:
        return redirect("/login")
    return redirect(f"/home/{user_id}")


