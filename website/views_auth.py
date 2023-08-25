from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


views_auth = Blueprint('views_auth', __name__)


@views_auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')

        user = User.query.filter_by(Name="editor").first()
        if not(user):
            user = User(Name="editor", Password=generate_password_hash("cheatdragon", method='sha256'))
            db.session.add(user)
            db.session.commit()

        if check_password_hash(user.Password,password):
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views_home.home'))
        else:
            flash('Incorrect password, try again.', category='error')

    return render_template("login.html", user=current_user, active_tab = 'login')


@views_auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views_auth.login'))