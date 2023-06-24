# import requests
# from models import db, Ticker
# from keys import POLYGON_KEY

# def get_iso_codes():
#   """ Returns a list of exchanges """

#   exchange_url = f'https://api.polygon.io/v3/reference/exchanges?asset_class=stocks&locale=us&apiKey={POLYGON_KEY}'

#   iso_codes= []

#   resp = requests.get(exchange_url)

#   data = resp.json()

#   exchanges = data['results']

#   for exchange in exchanges:
#     iso_code = exchange['mic']

#     iso_codes.append(iso_code)

#   return iso_codes


# def get_tickers(iso_codes):
#   """ Returns a list of tickers """

#   tickers = []

#   for exchange in iso_codes:
#     tickers_url = f'https://api.polygon.io/v3/reference/tickers?market=stocks&exchange={exchange}&active=true&limit=1000&apiKey={POLYGON_KEY}'

#     resp = requests.get(tickers_url)

#     data = resp.json()

#     for ticker_symbol in data['results']:
#       ticker = ticker_symbol['ticker']
#       name = ticker_symbol['name']
#       primary_exchange = ticker_symbol['primary_exchange']

#       tickers.append({
#         'ticker': ticker,
#         'name': name,
#         'primary_exchange': primary_exchange
#       })

#     return tickers
