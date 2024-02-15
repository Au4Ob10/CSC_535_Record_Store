from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash, current_app
from flask_login import login_required

def getuserid():
    return session.get('userid', None)

