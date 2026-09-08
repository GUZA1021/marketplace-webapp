from flask import Blueprint, render_template
from flask import render_template
from .models import Listing
from . import db

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    query = Listing.query.filter_by(status="AVAILABLE")
    listings = query.order_by(Listing.id.desc()).all()
    return render_template("listing.html", items=listings)

@main_bp.route("/sell", methods=["GET", "POST"])
def sell():
    return render_template("sell.html")
