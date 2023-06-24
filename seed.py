from app import app
from models import User, Ticker, db
from get_data import get_tickers


db.drop_all()
db.create_all()

User.query.delete()

jake = User(first_name='Jake', last_name='Smith', email='jakefromstatefarm@yahoo.com', username='jakefromstatefarm', password='password')
peter = User(first_name='Peter', last_name='Doe', email='peterdoe@yahoo.com', username='peterdoe', password='password')

db.session.add_all([jake, peter])
db.session.commit()

Ticker.query.delete()

tickers = get_tickers()

for ticker in tickers:
  new_ticker = Ticker(ticker=ticker['ticker'], name=ticker['name'], exchange=ticker['exchange'])

  db.session.add(new_ticker)
  db.session.commit()
