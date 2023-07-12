from app import app
from models import User, Ticker, Post, Watchlist, db
from get_data import get_tickers, get_watchlist_ticker_data


db.drop_all()
db.create_all()

User.query.delete()
Ticker.query.delete()
Post.query.delete()
Watchlist.query.delete()

jake = User.signup(first_name='Jake', last_name='Smith', email='jakefromstatefarm@yahoo.com', username='jakefromstatefarm', password='password', image_url='/static/images/default-pic.png')
peter = User.signup(first_name='Peter', last_name='Doe', email='peterdoe@yahoo.com', username='peterdoe', password='password', image_url='/static/images/default-pic.png')

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

apple = get_watchlist_ticker_data('AAPL')
intel = get_watchlist_ticker_data('INTC')
tesla = get_watchlist_ticker_data('TSLA')

watchlist_1 = Watchlist(ticker='AAPL', open=apple['open'], close=apple['low'], high=apple['high'], low=apple['low'], user_id=1)
watchlist_2 = Watchlist(ticker='INTC', open=intel['open'], close=intel['low'], high=intel['high'], low=intel['low'], user_id=1)
watchlist_3 = Watchlist(ticker='TSLA', open=tesla['open'], close=tesla['low'], high=tesla['high'], low=tesla['low'], user_id=1)
watchlist_4 = Watchlist(ticker='AAPL', open=apple['open'], close=apple['low'], high=apple['high'], low=apple['low'], user_id=2)
watchlist_5 = Watchlist(ticker='INTC', open=intel['open'], close=intel['low'], high=intel['high'], low=intel['low'], user_id=2)
watchlist_6 = Watchlist(ticker='TSLA', open=tesla['open'], close=tesla['low'], high=tesla['high'], low=tesla['low'], user_id=2)

db.session.add_all([watchlist_1, watchlist_2, watchlist_3, watchlist_4, watchlist_5, watchlist_6])
db.session.commit()
