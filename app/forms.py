from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, PasswordField, FloatField, BooleanField
from wtforms.widgets import CheckboxInput
from wtforms.validators import DataRequired, Email, EqualTo


class AddToBasket(FlaskForm):
    submit = SubmitField('Add to basket')


class RemoveFromBasket(FlaskForm):
    submit = SubmitField('Remove from Basket')


class PlaceOrder(FlaskForm):
    submit = SubmitField('Click to place order')


class GoToOrders(FlaskForm):
    submit = SubmitField('Go to my orders')


class ChangePassword(FlaskForm):
    oldpassword = PasswordField("Current Password", validators=[DataRequired()])
    password = PasswordField("New Password", validators=[DataRequired(), EqualTo('passwordCheck', message='Passwords must be the same')])
    passwordCheck = PasswordField("Re-Enter Password", validators=[DataRequired()])
    submit = SubmitField('Change Password')


class ChangeName(FlaskForm):
    oldname = StringField("Current Name", validators=[DataRequired()])
    newname = StringField("New Name", validators=[DataRequired(), EqualTo('namecheck', message='Names must be the same')])
    namecheck = StringField("Re-Enter Name", validators=[DataRequired()])
    submit = SubmitField('Change Name')


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    cookie_consent = BooleanField("Click here to consent to essential cookies", validators=[DataRequired()])
    submit = SubmitField("Login")


class SingupForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(),
                                                     EqualTo('passwordCheck', message='Passwords must be the same')])
    passwordCheck = PasswordField("Re-Enter Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")
