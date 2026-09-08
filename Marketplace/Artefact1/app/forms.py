from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired, Optional, InputRequired, Length, ValidationError, Email, EqualTo
from .models import User


class ListingForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[Optional()]
    )

    description = StringField(
        "Description",
        validators=[DataRequired()]
    )

    price = StringField(
        "Price",
        validators=[DataRequired()]
    )

    discount_price = StringField(
        "Discount price",
        validators=[Optional()]
    )

    city = StringField(
        "City",
        validators=[DataRequired()]
    )
    

    picture = FileField(
        "ProfilePic", 
        validators=[]
    )

    submit = SubmitField("Create listing")


class RegisterForm(FlaskForm):
    username = StringField(
        'Name',
        validators=[DataRequired(), Length(max=30)], 
        render_kw={"placeholder":"Enter your name"}
    )

    email = StringField (
        'Email',
        validators=[DataRequired(), Email(), Length(max=30)], 
        render_kw={"placeholder":"Enter your email"}
    )

    password = PasswordField(
        'Password', 
        validators=[DataRequired(), Length(min=4, max=30), EqualTo("password_confirm", message="Password must match")], 
        render_kw={"placeholder":"Enter your Password"}
    )
    
    password_confirm = PasswordField(
        'Confirm Password', 
        validators=[DataRequired()], 
        render_kw={"placeholder":"Confirm Password"}
    )

    address_name = StringField (
        'Address',
        validators=[DataRequired(), Length(max=30)], 
        render_kw={"placeholder":"Address"}
    )

    address_num = StringField (
        'Street number',
        validators=[DataRequired(), Length(max=30)], 
        render_kw={"placeholder":"Street number"}
    )

    city = StringField (
        'City',
        validators=[DataRequired(), Length(max=30)], 
        render_kw={"placeholder":"City"}
    )

    zipcode = StringField (
        'Email',
        validators=[DataRequired(), Length(max=30)], 
        render_kw={"placeholder":"Zipcode"}
    )
    
    submit = SubmitField("Register")

    def validate_username(self, username):
        #Query database for existing users
        existing_user = User.query.filter(User.name==username.data).first()

        if existing_user: 
            raise ValidationError("This user already exists")
        
    def validate_email(self, email):
        #Query database for existing emails
        existing_user = User.query.filter(User.email==email.data).first()

        if existing_user: 
            raise ValidationError("This user already exists")

class LoginForm(FlaskForm):
    email = StringField(
        'Email', 
        validators=[DataRequired(), Email()],
        render_kw={"placeholder":"Enter your email"}
    )

    password = PasswordField(
        'Password', 
        validators=[DataRequired()],
        render_kw={"placeholder":"Enter your password"}
    )
    
    submit = SubmitField('Sign in')

class SettingsForm(FlaskForm):
    username = StringField(
        'Name',
        validators=[DataRequired(), Length(max=30)], 
        render_kw={"placeholder":"Enter your name"}
    )

    email = StringField (
        'Email',
        validators=[DataRequired(), Email(), Length(max=30)], 
        render_kw={"placeholder":"Enter your email"}
    )

    password = PasswordField(
        'Password', 
        validators=[DataRequired(), Length(min=4, max=30), EqualTo("password_confirm", message="Password must match")], 
        render_kw={"placeholder":"Enter your Password"}
    )
    
    password_confirm = PasswordField(
        'Confirm Password', 
        validators=[DataRequired()], 
        render_kw={"placeholder":"Confirm Password"}
    )

    address_name = StringField (
        'Address',
        validators=[DataRequired(), Length(max=30)], 
        render_kw={"placeholder":"Address"}
    )

    address_num = StringField (
        'Street number',
        validators=[DataRequired(), Length(max=30)], 
        render_kw={"placeholder":"Street number"}
    )

    city = StringField (
        'City',
        validators=[DataRequired(), Length(max=30)], 
        render_kw={"placeholder":"City"}
    )

    zipcode = StringField (
        'Email',
        validators=[DataRequired(), Length(max=30)], 
        render_kw={"placeholder":"Zipcode"}
    )

    picture = FileField(
        "ProfilePic", 
        validators=[]
    )
    
    submit = SubmitField("Register")
