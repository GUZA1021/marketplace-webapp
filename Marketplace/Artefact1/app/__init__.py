from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
def create_app():
    app = Flask(__name__, template_folder="Templates",static_folder="static")

    app.config["SECRET_KEY"] = "dev"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///marketplace.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["WTF_CSRF_ENABLED"] = False
    #app.config["SESSION_PERMANENT"] = False #reset 

    #@app.before_request
    #def make_session_permanent():
    #    session.permanent = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    #Redirect users who are not logged in
    login_manager.login_view = 'auth.login'
    # Enable session protection to guard against session hijacking
    # 'strong' mode ensures that the session is invalidated if the user's IP or browser changes
    login_manager.session_protection = 'strong'

    # IMPORT MODELS
    from . import models

    # REGISTER BLUEPRINTS
    from .auth import auth_bp
    from .main import main_bp
    from .listings import listings_bp
    from .users import users_bp
    from .conversations import conversations_bp
    from .reviews import reviews_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(listings_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(conversations_bp)
    app.register_blueprint(reviews_bp)

    with app.app_context():
        db.create_all()

    return app

