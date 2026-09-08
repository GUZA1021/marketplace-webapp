from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin

class Listing(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False) # seller
    bought_by= db.Column(db.Integer, nullable=True) # buyer
    status = db.Column(db.Text, nullable=False, default="AVAILABLE")
    url= db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    city = db.Column(db.String(50), nullable=False)
    picture = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(20), nullable=True)
    condition = db.Column(db.String(20), nullable=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    address_name = db.Column(db.String(100), nullable=False)
    address_num = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    zipcode = db.Column(db.String(30), nullable=False)
    picture = db.Column(db.String(255), nullable=True)

    listings = db.relationship("Listing", backref="seller")

    def __repr__(self):
        return f'<User {self.name} with id {self.id} >'
    

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    listing_id = db.Column(db.Integer, db.ForeignKey("listing.id"), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    messages = db.relationship("Message", backref="conversation")
    listing = db.relationship("Listing", backref="conversations")
    

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    conversation_id = db.Column(db.Integer, db.ForeignKey("conversation.id"), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey("listing.id"), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reviewer = db.relationship("User", foreign_keys=[reviewer_id])
    seller = db.relationship("User", foreign_keys=[seller_id])
    listing = db.relationship("Listing")

    
# Tells flask_login how to find a user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

