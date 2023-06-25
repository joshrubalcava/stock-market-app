from app import app
from models import User, Ticker, Post, db
from get_data import get_tickers


db.drop_all()
db.create_all()

User.query.delete()
Ticker.query.delete()
Post.query.delete()

jake = User(first_name='Jake', last_name='Smith', email='jakefromstatefarm@yahoo.com', username='jakefromstatefarm', password='password')
peter = User(first_name='Peter', last_name='Doe', email='peterdoe@yahoo.com', username='peterdoe', password='password')

db.session.add_all([jake, peter])
db.session.commit()

tickers = get_tickers()

for ticker in tickers:
  new_ticker = Ticker(ticker=ticker['ticker'], name=ticker['name'], exchange=ticker['exchange'])

  db.session.add(new_ticker)
  db.session.commit()

post1 = Post(content='First post for apple', user_id=1, ticker='AAPL')
post2 = Post(content='Second post for apple', user_id=2, ticker='AAPL')
post3 = Post(content='Third post for apple', user_id=1, ticker='AAPL')
post4 = Post(content='Lorem ipsum dolor sit amet consectetur adipisicing elit. Obcaecati perferendis excepturi qui quos nihil nobis sequi debitis pariatur, blanditiis labore aliquam, suscipit soluta incidunt neque ipsum, dolore iure repellendus quia. Lorem ipsum dolor sit amet consectetur adipisicing elit. Obcaecati perferendis excepturi qui quos nihil nobis sequi debitis pariatur, blanditiis labore aliquam, suscipit soluta incidunt neque ipsum, dolore iure repellendus quia.', user_id=2, ticker='AAPL')

db.session.add_all([post1, post2, post3, post4])
db.session.commit()
