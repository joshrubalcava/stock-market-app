# Stock Market Application

The Beginner Stock Market App was built to help beginners gather basic information about stocks as well as relevent news. Most stock market applications that are available are hard for beginners to navigate due to the complexity of the information that is available. I wanted to incorporate just the basic information that would be relevant on a day to day basis in order for beginners to do minimal research to start.

To build this application, I used Jinja & Bootstrap for the front-end and used Python & Flask for the back-end. PostgreSQL & SQLAlchemy were also used to store user and stock data.

## How to use the Beginner Stock Market Application

### User Authentication

To use the basic functionality of this application, you do not need to be logged in to a user account, but you will be missing out on the ability to create posts for stocks and create a personal watchlist to return to whenever you log back in to the application.

### Home Page

The home page will be openly available with the daily prices for the S&P 500, NASDAQ, and Dow Jones Industrial Average. If you are logged in to your account and have a watchlist created, your watchlist will show on this page as well with the ability to transition to the pages for each individual stock. The most recent news articles will also be shown on this page with the functionality to take you to each of the articles main page. 

### Tickers

In the navbar, you will have the option to search for ticker symbols or you can click the "Tickers" button on the navbar which will direct you to the full listing of ticker symbols that are available. When you visit the full list of tickers, you can also search for tickers. The list of tickers also allows you to add tickers to your watchlist.

### User Login

If you have never signed up for an account, you simply need to click on the "Sign Up" button on the navbar. You will be navigated to a sign up page where you will need to enter your first name, last name, email, a username, and a password. An optional field to fill out will be to provide a URL for your own profile picture. Once you are signed up, you will be redirected to the home page.

### User Profile Page

If you are logged in to your acccount, you will have access to update your username, email and/or profile picture URL by pressing on the "Edit User Details Page. You will also be able to delete your account by Selecting the "Delete User" button. On your profile page, you will have access to your watchlist as well as any posts that you have created for stocks.

### Ticker Posts

To share you own opinion on a stock, simply search for a ticker symbol and select the ticker symbol from the list to be directed to the ticker details page. On the ticker details page, you just need to click on the "Add Post" button to be directed to a page where you can enter your post and select "Add Post!".

You are also able to edit you post by selecting the "Edit Post" button on the bottom of your post or you can delete the post entirely by selecting "Delete Post".

### Watchlist

Once you are logged in, you can create your own personal watchlist! If you currently do not have a watchlist created, it is as simple as going to the tickers list and clicking on the "Add to Watchlist" button. You will then be directed to a page to enter the name of your watchlist. You may elect to leave this field blank and you watchlist will be "Watchlist" by default.

### Database Schema

![Database Schema](/schema/db_schema.png "Database Schema")!

#### Users Table

The users table stores the first name, last name, email, username, hashed password, and image url for a user. The primary key (user ID) is used to link the Users table to the Posts table as well as linking the Users table to the Watchlists table.

#### Posts Table

The posts table stores the post content, timestamp of the post, the user ID (Foreign Key from Users Table), & the ticker symbol (Foreign Key from the Tickers Table).

#### Watchlists Table

The watchlists table stores the name of the watchlist, the ticker symbol (Foreign Key from Tickers Table), the open price, the close price, the high price, and the low price of the stock. The user ID (Foreign Key from Users Table) is also stored to link the Users table to the Watchlist table.

#### Tickers Table

The tickers table stores the ticker symbol, the name of the company, and the exchange it is traded on. The ticker symbol is used as the primary key to link the tickers table to the posts table as well as linking the tickers table to the watchlists table.
