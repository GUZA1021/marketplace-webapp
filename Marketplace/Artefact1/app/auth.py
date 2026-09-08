from flask import Blueprint, render_template, url_for, redirect, flash
from . import db
from .models import User
from .forms import RegisterForm, LoginForm
from app import bcrypt
from flask_login import login_user, current_user, logout_user, login_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("users.index"))
    
    if form.validate_on_submit():
        user = User.query.filter(User.email==form.email.data.strip()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # If the user credentials are correct, start an authenticated session
            login_user(user)
            # Redirect to the user personal page
            flash("Login succesful")
            return redirect(url_for("users.index"))
        else: 
            flash("Please log in with a valid user or password")

    return render_template("login.html", form=form)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data)
        user = User(
            name=form.username.data.strip(), 
            email=form.email.data.strip(), 
            password=password_hash,
            address_name=form.address_name.data.strip(),
            address_num=form.address_num.data.strip(),
            city=form.city.data.strip(),
            zipcode=form.zipcode.data.strip(),
            picture="default.png"
        )

        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("users.index"))

    if current_user.is_authenticated:
        return redirect(url_for("users.index"))

    if form.is_submitted() and not form.validate_on_submit():
        flash("Please try again")

    return render_template('register.html', form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))