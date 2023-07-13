import requests, os
from keys import ALPHA_VANTAGE_KEY, TWELVE_DATA_KEY

AV_KEY = os.environ.get("ALPHA_VANTAGE_KEY", ALPHA_VANTAGE_KEY)
TD_KEY = os.environ.get("TWELVE_DATA_KEY", TWELVE_DATA_KEY)


def get_main_indices(main_indices):
  """ Gets the open, close, high, and low values for SPY, QQQ, & DIA """

  indices = []

  for index in main_indices:
    INDICES_URL = f'https://api.twelvedata.com/time_series?symbol={index}&interval=1day&apikey={TD_KEY}&source=docs'

    resp = requests.get(INDICES_URL)

    data = resp.json()
    
    open = str(round(float(data['values'][0]['open']), 2))
    high = str(round(float(data['values'][0]['high']), 2))
    low = str(round(float(data['values'][0]['low']), 2))
    close = str(round(float(data['values'][0]['close']), 2))
    
    if index == 'SPX':
      indices.append({
        'name': 'S&P 500', 
        'open': open,
        'high': high,
        'low': low,
        'close': close,
      })
    elif index == 'NDAQ':
      indices.append({
        'name': 'Nasdaq', 
        'open': open,
        'high': high,
        'low': low,
        'close': close,
      })
    else:
      indices.append({
        'name': 'Dow Jones', 
        'open': open,
        'high': high,
        'low': low,
        'close': close,
      })

  return indices

def get_news_articles():
  """ Gets news articles to post for main page """

  news = []

  try:
    NEWS_URL = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&limit=5&apikey={AV_KEY}'

    resp = requests.get(NEWS_URL)

    data = resp.json()

    feed = data['feed']

    for article in feed:
      title = article['title']
      url = article['url']
      authors = article['authors']
      summary = article['summary']
      banner_img = article['banner_image']
      source = article['source']
      topics = article['topics']
      overall_sentiment = article['overall_sentiment_label']

      news.append({
        'title': title,
        'url': url,
        'authors': authors,
        'summary': summary,
        'banner_img': banner_img,
        'source': source,
        'topics': topics,
        'overall_sentiment': overall_sentiment
      })

    return news
  except KeyError:
    return None

def get_news_for_ticker(ticker):
  """ Gets news articles that include the ticker symbol """

  url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&sort=RELEVANCE&limit=20&apikey={AV_KEY}'

  news = []

  resp = requests.get(url)

  data = resp.json()

  feed = data['feed']

  for article in feed:
    title = article['title']
    url = article['url']
    authors = article['authors']
    summary = article['summary']
    banner_img = article['banner_image']
    source = article['source']
    topics = article['topics']
    overall_sentiment = article['overall_sentiment_label']

    news.append({
      'title': title,
      'url': url,
      'authors': authors,
      'summary': summary,
      'banner_img': banner_img,
      'source': source,
      'topics': topics,
      'overall_sentiment': overall_sentiment
    })

  return news

def get_tickers():
  """ Get ticker symbols in the US """

  ticker_url = 'https://api.twelvedata.com/stocks?&country=US&source=docs'

  tickers = []

  resp = requests.get(ticker_url)

  data = resp.json()

  for symbol in data['data']:
    ticker = symbol['symbol']
    name = symbol['name']
    exchange = symbol['exchange']

    tickers.append({
      'ticker': ticker,
      'name': name,
      'exchange': exchange
    })

  return tickers

def get_ticker_details(ticker):
  """ Get data on individual tickers for ticker details page """

  ticker_url = f'https://api.twelvedata.com/time_series?symbol={ticker}&interval=1day&apikey={TD_KEY}'

  resp = requests.get(ticker_url)

  data = resp.json()

  return data['values'][:5]

def get_watchlist_ticker_data(ticker):
  """ Gets the open, close, high, and low values for watchlists """

  ticker_url = f'https://api.twelvedata.com/time_series?symbol={ticker}&interval=1day&apikey={TD_KEY}'

  resp = requests.get(ticker_url)

  data = resp.json()
  print(data)

  open = str(round(float(data["values"][0]['open']), 2))
  high = str(round(float(data["values"][0]['high']), 2))
  low = str(round(float(data["values"][0]['low']), 2))
  close = str(round(float(data["values"][0]['close']), 2))

  return {
    'open': open,
    'close': close,
    'high': high,
    'low': low
  }
