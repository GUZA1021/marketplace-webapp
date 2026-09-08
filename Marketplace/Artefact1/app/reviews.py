from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from .models import Listing, Review
from . import db

reviews_bp = Blueprint("reviews", __name__)

@reviews_bp.route("/reviews/<int:listing_id>", methods=["GET", "POST"])
@login_required
def new_review(listing_id):
    listing = Listing.query.get(listing_id)

    if request.method == "POST":
        rating = request.form.get("rating")
        comment = request.form.get("comment", "")

        review = Review(rating=rating, comment=comment, reviewer_id=current_user.id, seller_id=listing.user_id, listing_id=listing.id)
        
        db.session.add(review)
        db.session.commit()
        
        return redirect(url_for("Listings.view_listings"))
    
    return render_template("review.html", item=listing)