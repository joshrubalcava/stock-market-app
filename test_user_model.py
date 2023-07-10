"""User model tests."""

import os
from unittest import TestCase

from sqlalchemy import exc

from models import db, User

os.environ['DATABASE_URL'] = "postgresql:///stock_market_app_test_db"

from app import app

db.create_all()


class UserModelTestCase(TestCase):
  """Test views for messages."""

  def setUp(self):
    """Create test client, add sample data."""

    User.query.delete()

    u1 = User.signup("John", "Doe", "email1@email.com", "test1", "password", "/static/images/default-pic.png")
    uid1 = 1111
    u1.id = uid1

    u2 = User.signup("Jane", "Doe", "email2@email.com", "test2", "password", "/static/images/default-pic.png")
    uid2 = 2222
    u2.id = uid2

    db.session.commit()

    u1 = User.query.get(uid1)
    u2 = User.query.get(uid2)

    self.u1 = u1
    self.uid1 = uid1

    self.u2 = u2
    self.uid2 = uid2

    self.client = app.test_client()

  def tearDown(self):
    res = super().tearDown()
    db.session.rollback()
    return res

  def test_user_model(self):
    """Does basic model work?"""

    u = User(
      first_name="Tom",
      last_name="Smith",
      email="test@test.com",
      username="testuser",
      password="HASHED_PASSWORD",
      image_url="/static/images/default-pic.png"
    )

    db.session.add(u)
    db.session.commit()

  def test_valid_signup(self):
    u = User.signup("New", "User", "test@gpython3 -m unittest test_user_model.pymail.com", "newtestuser", "password", image_url="/static/images/default-pic.png")
    uid = 99999
    u.id = uid
    db.session.commit()

    u_test = User.query.get_or_404(uid)
    self.assertIsNotNone(u_test)
    self.assertEqual(u.username, 'newtestuser')
    self.assertEqual(u.email, 'test@gmail.com')
    self.assertNotEqual(u.password, 'test')
    self.assertTrue(u.password.startswith("$2b$"))

  def test_invalid_username_signup(self):
    invalid = User.signup("test", "user", "test@test.com", None, "password", "/static/images/default-pic.png")
    uid = 123456789
    invalid.id = uid
    with self.assertRaises(exc.IntegrityError) as context:
        db.session.commit()

  def test_invalid_email_signup(self):
    invalid = User.signup("test", "test", None, "testuser", "password", "/static/images/default-pic.png")
    uid = 123789
    invalid.id = uid
    with self.assertRaises(exc.IntegrityError) as context:
        db.session.commit()

  def test_invalid_password_signup(self):
    with self.assertRaises(ValueError) as context:
        User.signup("test", "test", "email@email.com", "testuser", None, "/static/images/default-pic.png")

  def test_valid_authentication(self):
    u = User.authenticate(self.u1.username, "password")
    self.assertIsNotNone(u)
    self.assertEqual(u.id, self.uid1)

  def test_invalid_username(self):
    self.assertFalse(User.authenticate("badusername", "password"))

  def test_wrong_password(self):
    self.assertFalse(User.authenticate(self.u1.username, "badpassword"))
