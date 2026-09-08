from flask import Flask,  request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import Review, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] ="sqlite:///reviews.db"

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/reviews", methods=["POST"])
def create_review():
    data = request.get_json()

    review = Review(
        listing_id=data["listing_id"],
        receiver_id=data["receiver_id"],
        author_id=data["author_id"],
        rating=data["rating"],
        comment=data.get("comment")
    )

    db.session.add(review)
    db.session.commit()


    return jsonify({"id": review.id}), 201


@app.route("/reviews/user/<int:user_id>")
def get_review(user_id):
    reviews = Review.query.filter_by(receiver_id=user_id).all()
    return jsonify([{"rating": r.rating, "comment": r.comment} for r in reviews])

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5003, debug=True)