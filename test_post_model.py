"""Post model tests."""

import os
from unittest import TestCase

from sqlalchemy import exc

from models import db, User, Post

os.environ['DATABASE_URL'] = "postgresql:///stock_market_app_test_db"

from app import app

db.create_all()


class PostModelTestCase(TestCase):
  """Test views for messages."""

  def setUp(self):
    """Create test client, add sample data."""

    User.query.delete()
    Post.query.delete()

    u1 = User.signup("John", "Doe", "email1@email.com", "test1", "password", "/static/images/default-pic.png")
    uid1 = 1111
    u1.id = uid1

    u2 = User.signup("Jane", "Doe", "email2@email.com", "test2", "password", "/static/images/default-pic.png")
    uid2 = 2222
    u2.id = uid2

    # p1 = Post("test content 1", u1.id, 'AAPL')
    p1 = Post(content="Test content for post 1", user_id=1111, ticker="AAPL")
    pid1 = 1234
    p1.id = pid1

    p2 = Post(content="test content for post 2", user_id=1111, ticker="AAPL")
    pid2 = 4321
    p2.id = pid2

    db.session.commit()

    u1 = User.query.get(uid1)
    u2 = User.query.get(uid2)
    p1 = Post.query.get(pid1)
    p2 = Post.query.get(pid2)

    self.u1 = u1
    self.uid1 = uid1

    self.u2 = u2
    self.uid2 = uid2

    self.p1 = p1
    self.pid1 = pid1

    self.p2 = p2
    self.pid2 = pid2

    self.client = app.test_client()

  def tearDown(self):
    res = super().tearDown()
    db.session.rollback()
    return res

  def test_post_model(self):
    """Does basic model work?"""

    u = User.signup("test", "user", "test@gmail.com", "testuser", "password", "/static/images/default-pic.png")
    uid = 1234
    u.id = uid

    p = Post(
      content="test content for unittest",
      user_id=1234,
      ticker="AAPL",
    )

    db.session.add_all([u, p])
    db.session.commit()

  def test_valid_post(self):
    u = User.signup("test", "user", "test@gmail.com", "testuser", "password", "/static/images/default-pic.png")
    uid = 1234
    u.id = uid

    p = Post(content="test post for test valid post", user_id=1234, ticker="AAPL")
    pid = 5678
    p.id = pid

    db.session.add_all([u, p])
    db.session.commit()

    p_test = Post.query.get_or_404(pid)
    self.assertIsNotNone(p_test)
    self.assertEqual(p.content, 'test post for test valid post')
    self.assertEqual(p.user_id, 1234)
    self.assertEqual(p.ticker, 'AAPL')
