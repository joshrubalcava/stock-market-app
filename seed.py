from app import app
from models import User, Ticker, Post, Watchlist, UserWatchlist, db
from get_data import get_tickers


db.drop_all()
db.create_all()

User.query.delete()
Ticker.query.delete()
Post.query.delete()

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

watchlist1 = Watchlist(name='Watchlist1', user_id=1)
watchlist2 = Watchlist(name='Watchlist2', user_id=2)

db.session.add_all([watchlist1, watchlist2])
db.session.commit()

update_watchlist_1 = UserWatchlist(watchlist_id=1, ticker='AAPL')
update_watchlist_2 = UserWatchlist(watchlist_id=1, ticker='INTC')
update_watchlist_3 = UserWatchlist(watchlist_id=1, ticker='TSLA')
update_watchlist_4 = UserWatchlist(watchlist_id=2, ticker='AAPL')
update_watchlist_5 = UserWatchlist(watchlist_id=2, ticker='INTC')
update_watchlist_6 = UserWatchlist(watchlist_id=2, ticker='TSLA')

db.session.add_all([update_watchlist_1, update_watchlist_2, update_watchlist_3, update_watchlist_4, update_watchlist_5, update_watchlist_6])
db.session.commit()
