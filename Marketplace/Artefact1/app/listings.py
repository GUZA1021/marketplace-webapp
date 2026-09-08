from flask import Blueprint, render_template, redirect, url_for, current_app, request, flash
from .forms import ListingForm
from .models import Listing
from . import db
from flask_login import current_user, login_required
import os
from werkzeug.utils import secure_filename

listings_bp = Blueprint("Listings", __name__)

@listings_bp.route("/listings/new", methods=["GET","POST"])
@login_required
def create_listing():
    form = ListingForm()

    if form.validate_on_submit():
        file_name = "default.png"
        #Pic
        if form.picture.data:
            file = form.picture.data
            file_name = secure_filename(file.filename)
            file.save(os.path.join(current_app.root_path, "static/uploads/Item", file_name))

        listing = Listing(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            city=form.city.data.strip(),
            seller = current_user,
            picture = file_name,
            category=request.form.get("category"),
            condition=request.form.get("condition")
        )

        db.session.add(listing)
        db.session.commit()

        return redirect(url_for("Listings.view_listings"))
    
    return render_template("sell.html", form=form)

@listings_bp.route("/listings")
def view_listings():
    search = request.args.get("search", "")
    category = request.args.get("category", "")

    query = Listing.query.filter_by(status="AVAILABLE")

    if search:
        query = query.filter(Listing.title.contains(search))

    if category:
        query = query.filter_by(category=category)

    listings = query.order_by(Listing.id.desc()).all()

    return render_template("listing.html", items=listings)

@listings_bp.route("/listings/<int:listing_id>")
def listing_page(listing_id):
    listing = Listing.query.get(listing_id)
    return render_template("item_page.html", item=listing)

@listings_bp.route("/listings/<int:listing_id>/review", methods=["GET", "POST"])
def review_user(listing_id):
    listing = Listing.query.get_or_404(listing_id)

    if listing.user_id == current_user.id:
        return "Can't review yourself"

    if listing.status == "AVAILABLE":
        return redirect(url_for("Listings.listing_page", listing_id=listing.id))

    return redirect(url_for("reviews.new_review", listing_id=listing.id))

@listings_bp.route("/item/<int:listing_id>/delete", methods=["GET", "POST"])
def delete_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)

    if listing.user_id != current_user.id:
        return 403
    
    db.session.delete(listing)
    db.session.commit()

    flash("Listing deleted")
    return redirect(url_for("users.user_profile", username=current_user.name))

@listings_bp.route("/my_listings", methods=["GET", "POST"])
def my_listings():
    listings = current_user.listings
    return render_template("listing.html", items=listings)

@listings_bp.route("/mark_as_sold/<int:listing_id>", methods=["POST"])
def mark_as_sold(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    buyer = request.form.get("buyer_id")

    if listing.user_id != current_user.id:
        return 403
    
    listing.status ="SOLD"
    listing.bought_by = buyer

    db.session.commit()

    return redirect(url_for("Listings.listing_page", listing_id=listing.id))