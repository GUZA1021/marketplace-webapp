from flask import Flask,  request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import Listing, db


app= Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///listings.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/listings", methods=["POST"])
def create_listing():
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON body required"}), 400


    required = ["title","description","price","seller_id"]

    if not all(field in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    seller_id = data.get("seller_id")
    if not seller_id:
        return jsonify({"error": "seller_id required"}), 400
    
    listing = Listing(
        title=data["title"],
        description=data["description"],
        price=data["price"],
        seller_id=data["seller_id"],
        status="AVAILABLE"   
    )


    db.session.add(listing)
    db.session.commit()

    return jsonify({"id": listing.id}), 201

@app.route("/listings", methods=["GET"])
def get_listings():
    listings = Listing.query.all()
    return jsonify([{"id": l.id,"title": l.title,"description": l.description,"price": l.price,"status": l.status,"seller_id": l.seller_id} for l in listings]), 200

@app.route("/listings/<int:listing_id>", methods=["GET"])
def get_listing(listing_id):
    listing = Listing.query.get(listing_id)

    if not listing: 
        return jsonify({"error": "Listing not found"}), 404
    
    return jsonify({
        "id": listing.id, 
        "title": listing.title, 
        "description": listing.description,
        "price": listing.price,
        "seller_id": listing.seller_id,
        "buyer_id": listing.buyer_id,
        "status": listing.status
    }), 200


@app.route("/listings/<int:listing_id>/buy", methods=["POST"])
def buy_listing(listing_id):
    data = request.get_json()
    buyer_id = data.get("buyer_id")

    if not data:
        return jsonify({"error": "JSON body required"}), 400


    if not buyer_id:
        return jsonify({"error": "buyer_id rneeded"}), 400
    
    listing = Listing.query.get(listing_id)

    if listing.status != "AVAILABLE":
        return jsonify({"error": "Already sold"}), 409
    
    if listing.seller_id == buyer_id:
        return jsonify({"error": "Cannot buy own listing"}), 403
    
    listing.status = "SOLD"
    listing.buyer_id = buyer_id

    db.session.commit()

    return jsonify({"message": "Purhcase successful"}), 200

@app.route("/listings/<int:listing_id>", methods=["DELETE"])
def delete_listings(listing_id):
    data = request.get_json()
    user_id = data.get("user_id")
   
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    if not user_id:
        return jsonify({"error": "user_id required"}), 400
    
    
    listing = Listing.query.get(listing_id)

    if not listing:
        return jsonify({"error": "Listing not found"}), 404


    if listing.seller_id != user_id:
        return jsonify({"error": "Not your listing"}), 403
    
    if listing.status == "SOLD":
        return jsonify({"error": "Cannot delete sold listings"}), 409
    
    db.session.delete(listing)
    db.session.commit()

    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
