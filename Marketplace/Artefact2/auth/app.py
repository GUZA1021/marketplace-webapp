from flask import Flask,  request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from models import db, User


app= Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///auth.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
bcrypt = Bcrypt(app)

with app.app_context():
    db.create_all()


# register 
@app.route("/users", methods=["POST"])
def register():
    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing data"}), 400
    
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error":"User already exists"}), 409
    
    password_hash = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    user = User(email=data["email"], password=password_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify({"id": user.id, "email": user.email}), 201



# login
@app.route("/sessions", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data.get("email")).first()

    if not user or not bcrypt.check_password_hash(user.password, data.get("password")):
        return jsonify({"error":"Invalid login"}), 401
    
    #assuming that the list id is the user id (Change later maybe)
    return jsonify({"user_id": user.id, "email" : user.email}), 200

# User lookup
@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)

    return jsonify({"id": user.id, "email": user.email}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
