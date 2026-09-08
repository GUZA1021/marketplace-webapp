from flask import Flask, render_template, request, redirect, session
import requests

app = Flask(__name__)
app.secret_key = "frontend-dev"

AUTH_URL = "http://auth:5000"
LISTING_URL = "http://listings:5001"
REVIEW_URL = "http://reviews:5003"


@app.route("/")
def index():
    res = requests.get(f"{LISTING_URL}/listings")
    listings = res.json()
    return render_template("listings.html", listings=listings)


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        res = requests.post(f"{AUTH_URL}/sessions", json={"email": email, "password": password})

        if res.status_code == 200:
            session["user_id"] = res.json()["user_id"]
            session["email"] = res.json()["email"]
            return redirect("/")
        

        return "Login failed", 401
    

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        res = requests.post(
            f"{AUTH_URL}/users",
            json={"email": email, "password": password}
        )

        if res.status_code == 201:
            return redirect("/login")

        return "Registration failed", 400

    return render_template("register.html")

@app.route("/profile")
def profile():
    user_id = session.get("user_id")

    if not user_id:
        return redirect("/login")
    
    user_id = int(user_id)
    
    user = session.get("email")

    #fetch listings
    listings_res = requests.get(f"{LISTING_URL}/listings")
    all_listings = listings_res.json()

    items = [l for l in all_listings if l["seller_id"] == user_id]

    #fetch reviews received
    reviews_res = requests.get(f"{REVIEW_URL}/reviews/user/{user_id}")
    reviews = reviews_res.json()

    return render_template("profile.html",email=user,items=items,reviews=reviews, is_own_user = True)



@app.route("/buy/<int:listing_id>", methods=["POST"])
def buy(listing_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    
    res = requests.post(
        f"{LISTING_URL}/listings/{listing_id}/buy",
        json={"buyer_id": user_id}
    )

    #check if purchase was sucessfull
    if res.status_code == 200:
        return redirect(f"/review/{listing_id}")
    else:
        return redirect ("/")
    
@app.route("/sell", methods=["GET","POST"])
def sell():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    
    if request.method == "POST":
        res = requests.post(f"{LISTING_URL}/listings", json={
                "title": request.form["title"],
                "description":request.form["description"],
                "price": request.form["price"],
                "seller_id": session["user_id"]
            }
        )
        if res.status_code == 201:
            return redirect("/")
    
    
    return render_template("sell.html")


@app.route("/delete/<int:listing_id>", methods=["POST"])
def delete_listing(listing_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    requests.delete(
        f"{LISTING_URL}/listings/{listing_id}",
        json={"user_id": user_id}
    )

    return redirect("/profile")



@app.route("/review/<int:listing_id>", methods=["GET", "POST"])
def review(listing_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    # submuit review
    if request.method == "POST":
        rating = request.form.get("rating")
        
        if not rating:
            return render_template("review.html", listing_id=listing_id)
        
        #fetch seller ID
        listing_response = requests.get(f"{LISTING_URL}/listings/{listing_id}")
        listing = listing_response.json()
        seller = listing["seller_id"]

        res = requests.post(
            f"{REVIEW_URL}/reviews",
            json={
                "listing_id": listing_id,
                "receiver_id": seller,
                "author_id": user_id,
                "rating": int(rating),
                "comment": request.form.get("comment")
            }
        )
        
        if res.status_code == 201:
            return redirect("/")
            
    return render_template("review.html", listing_id=listing_id)






@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5002, debug=True)