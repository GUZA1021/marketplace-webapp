from flask import render_template, Blueprint, flash, current_app, request
from werkzeug.utils import secure_filename
from . import db
from .models import User, Listing, Review
from flask_login import login_required, current_user
from .forms import SettingsForm
import os

# Define the blueprint
users_bp = Blueprint("users", __name__, url_prefix="/users")

"""
Settings page where users can change their info
"""
@users_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = SettingsForm()

    #prefil form
    if request.method == "GET":
        form.username.data = current_user.name
        form.email.data = current_user.email
        form.address_name.data = current_user.address_name
        form.address_num.data = current_user.address_num
        form.city.data = current_user.city
        form.zipcode.data = current_user.zipcode

    if form.validate_on_submit():
        current_user.name = form.username.data
        current_user.email=form.email.data
        current_user.address_name=form.address_name.data
        current_user.address_num=form.address_num.data
        current_user.city=form.city.data
        current_user.zipcode=form.zipcode.data

        #Pic
        if form.picture.data:
            file = form.picture.data
            secure_file_name = secure_filename(file.filename)
            file.save(os.path.join(current_app.root_path, "static/uploads", secure_file_name))
            current_user.picture = secure_file_name

        db.session.commit()

    if form.is_submitted() and not form.validate_on_submit():
        flash("Please try again")

    return render_template("settings.html", form=form)

"""
Profile page where users can view their listings and reviews.
"""
@users_bp.route("/<username>", methods=["GET"])
@login_required
def user_profile(username):
    profile = User.query.filter_by(name=username).first_or_404()

    items = Listing.query.filter_by(user_id=profile.id).order_by(Listing.id.desc()).all()
    reviews = Review.query.filter_by(seller_id=profile.id).order_by(Review.created_at.desc()).all()
    is_own_user = current_user.id == profile.id

    return render_template("user_profile.html", profile=profile, reviews=reviews, items=items, is_own_user=is_own_user)