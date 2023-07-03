from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, URL, Email, Optional, Length

class UserAddForm(FlaskForm):
  """ Form for adding new users """

  first_name = StringField('First Name', validators=[DataRequired()])
  last_name = StringField('Last Name', validators=[DataRequired()])
  email = StringField('Email', validators=[Email()])
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[Length(min=6)])
  image_url = StringField('Profile Image URL', validators=[Optional(), URL()])

class UserLoginForm(FlaskForm):
  """ Form for logging in users """

  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[Length(min=6)])

class EditUserForm(FlaskForm):
  """ Form for editing the user information """

  username = StringField(label='Username', validators=[DataRequired()])
  email = StringField(label='Email', validators=[Email()])
  image_url = StringField('Profile Image URL', validators=[Optional(), URL()])

class AddPost(FlaskForm):
  """ Form for adding new posts for tickers """

  content = TextAreaField('Content', validators=[Length(min=10)])

class EditPost(FlaskForm):
  """ Edit Post """

  content = TextAreaField('Enter new post', validators=[Length(min=10)])

class CreateWatchlist(FlaskForm):
  """ Create new user watchlist """
  
  name = StringField('Watchlist Name', validators=[Optional()])
