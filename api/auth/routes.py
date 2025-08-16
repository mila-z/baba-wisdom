from api.auth import bp
from flask import jsonify, request, redirect, url_for, flash, render_template
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from datetime import datetime
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
                return redirect(url_for('home.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email or username does not exist.', category='error')
    return render_template('login.html', user=current_user)

@bp.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        role = request.form.get('role').lower()
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter(
            or_(
                User.email == email,
                User.username == username
            )
        ).first()
        if user:
            # maybe separate the messages for whether the problem is the email or the username
            flash('Email or username already exists', category='error')
        if len(email) < 4:
            flash('Email must be at least 4 characters.', category='error')
        elif len(username) < 4:
            flash('Username must be at least 4 characters.', category='error')
        elif role not in ['baba', 'apprentice']:
            flash('Role must be either \'baba\' or \'apprentice\'.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(
                email=email, 
                username=username,
                role=role, 
                password=generate_password_hash(password1, method='pbkdf2:sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True) 
            flash('Account created!', category='success')
            if role =='baba':
                return redirect(url_for('auth.setup_baba_profile'))
            else:
                return redirect(url_for('auth.setup_apprentice_profile'))
    return render_template('sign_up.html', user=current_user)

@bp.route('/sign-up/setup-baba', methods=['GET', 'POST'])
@login_required
def setup_baba_profile():
    if request.method == 'POST':
        village = request.form.get('village')
        bio = request.form.get('bio')

        if len(village) < 4:
            flash('Village must be at least 4 characters.', category='error')
        if len(bio) < 4:
            flash('Bio must be at least 4 characters.', category='error')
        else:
            baba = Baba(user_id=current_user.id, village=village, bio=bio)
            db.session.add(baba)
            db.session.commit()
            return redirect(url_for('home.home'))
    return render_template('setup_baba.html', user=current_user)

@bp.route('/sign-up/setup-apprentice', methods=['GET', 'POST'])
@login_required
def setup_apprentice_profile():
    if request.method == 'POST':
        birth_date_str = request.form.get('birth_date')
        
        try:
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', category='error')
            return redirect(url_for('auth.setup_apprentice_profile'))

        apprentice = Apprentice(user_id=current_user.id, birth_date=birth_date)
        db.session.add(apprentice)
        db.session.commit()

        return redirect(url_for('home.home'))
    return render_template('setup_apprentice.html', user=current_user)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))