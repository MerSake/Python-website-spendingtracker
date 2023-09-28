from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from passlib.hash import sha256_crypt as hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['Get', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if hash.verify(password, user.password):
                flash('You are logged in', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('incorrect password', category='error')
        else:
            flash('User does not exist', category='error')

    return render_template("/login.html", user=current_user)


@auth.route('/sign_up', methods=['Get', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email is already used', category='error')
        elif len(email) < 4:
            flash('Email must be greater the 3 characters.', category='error')
        elif len(firstName) < 2:
            flash('Name must be longer then 1 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 7:
            flash('Password must be longer then 6 characters', category='error')
        else:
            new_user = User(email=email, first_name=firstName,
                            password=hash.encrypt(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created', category='success')
            return redirect(url_for('views.home'))

    return render_template("/sign_up.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
