from api.auth import bp
from flask import jsonify, request, redirect, url_for, flash, render_template
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from api import db
from api.models import User, Baba, Apprentice

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_data = request.form.get('email_or_username')
        password = request.form.get('password')

        user = User.query.filter(
            or_(
                User.email == user_data,
                User.username == user_data
            )
        ).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('main.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email or username does not exist.', category='error')
    return render_template('login.html')

@bp.route('/sign-up')
def register():
    return '<h1>Testing the Register Page</h1>'

@bp.route('/logout')
def logout():
    return '<h1>Testing the Logout Page</h1>'