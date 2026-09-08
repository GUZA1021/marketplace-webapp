from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from .models import Listing, Conversation, Message
from . import db

conversations_bp = Blueprint("conversations", __name__)

@conversations_bp.route("/conversation/<int:listing_id>", methods=["GET", "POST"])
def view_conversation(listing_id):
    listing = Listing.query.get_or_404(listing_id)

    is_seller = (listing.user_id == current_user.id)

    if is_seller:
        conversation = Conversation.query.filter_by(listing_id=listing.id).first()

    else:
        conversation = Conversation.query.filter_by(
            listing_id=listing.id, 
            buyer_id=current_user.id
        ).first()

        if not conversation:
            conversation = Conversation(
                listing_id=listing.id, 
                buyer_id=current_user.id
            )
            db.session.add(conversation)
            db.session.commit()

    if request.method == "POST":
        text = request.form.get("text")
        if text:
            msg = Message(conversation_id=conversation.id, sender_id=current_user.id, text=text)
            db.session.add(msg)
            db.session.commit()

            return redirect(url_for("conversations.view_conversation", listing_id=listing.id))

    messages = Message.query.filter_by(conversation_id=conversation.id).order_by(Message.created_at.asc()).all()
    
    return render_template("conversation.html", item=listing, messages=messages, convo=conversation)


@conversations_bp.route("/inbox")
def inbox():
    is_buy = Conversation.buyer_id == current_user.id
    is_sell = Conversation.listing.has(user_id=current_user.id)
    conversations = Conversation.query.filter(is_buy | is_sell).all()
    

    return render_template("inbox.html", conversations=conversations)