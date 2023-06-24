from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
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
