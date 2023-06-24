# Name TBD

## Goal To Achieve

This web app will be designed to achieve a place where users are able to check news related to the US stock market, check for information on selected ticker symbols, and add ticker symbols to their own lists in order for quicker access when the user is signed in. It will show a list of suggested ticker symbols based on the biggest gainers/losers (maybe random tickers selected to display instead) so that if the user does not have symbols in mind, they will be able to start there. Also, there will be a sort of community posts for individual symbols so users can interact with each other.

## Technology Used

Will be using HTML, CSS/Bootstrap, JavaScript for the front-end and python/flask for the back-end. PostgreSQL/SQLAlchemy will be used to store user, stock, and other essential data.

## What kind of users will visit this site

1. Anybody interested in stock market data, news, and posting/reading opinions on the market
2. Gender: Male and Female
3. Age: 16 - 50
4. Device Preference: Desktop & Mobile Browsers

## What data will be used

- Alpha Vantage

  - News and Sentiments

  - Ticker Symbol Information
    - Daily Prices (Open, High, Low, Close)

- twelvedata
  - Used to all stocks to the data
  - Will use the list with polygon.io to get individual stock data

- Polygon.io
  - Get information for individual stocks

## Database Schema Notes

- User
  - user_id, int, primary_key, serialized
  - first_name, text
  - last_name, text
  - profile_image_url, text OR default
  - username, text, unique
  - password, text

- Post
  - post_id, primary_key, serialized
  - sentiment, select
  - content, text
  - created_at, date
  - user_id, foreign_key(User.id)

- UserStockList
  - user_id, int, primary_key, foreign_key(User.id)
  - ticker_symbol, text, primary_key
  - company_name, text

## Potential API Issues

- Limited API calls
- May need to find alternatives for additional information due to premium endpoints

## Sensitive information to store

- API keys

## App Functionality

- User login/logout
- Add stocks to a private list
- Add posts to individual stocks or the overall market (only when logged in)

## User Flow

## Features that make it more than just a CRUD app

What are features that would make it more than just a CRUD app?
