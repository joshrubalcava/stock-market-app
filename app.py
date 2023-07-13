import os
from flask import Flask, session, render_template, redirect, g, flash, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Ticker, Post, Watchlist
from forms import UserAddForm, UserLoginForm, EditUserForm, AddPost, EditPost, CreateWatchlist
from sqlalchemy.exc import IntegrityError
from get_data import get_main_indices, get_news_articles, get_ticker_details, get_news_for_ticker, get_watchlist_ticker_data, get_tickers

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.app_context().push()

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///stock_market_db'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgresql:///stock_market_db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.debug = False
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'secret_key')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.before_first_request
def update_main_indices_data():

    main_indices = ['SPX', 'IXIC', 'DJI']

    global main_indices_data 
    main_indices_data = get_main_indices(main_indices)


# @app.before_first_request
# def add_tickers_to_db():


#     Ticker.query.delete()

#     tickers = get_tickers()

#     for ticker in tickers:
#         new_ticker = Ticker(ticker=ticker['ticker'], name=ticker['name'], exchange=ticker['exchange'])

#         db.session.add(new_ticker)
#         db.session.commit()


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/')
def show_home_page():
    """ shows home page """

    indices_data = main_indices_data

    news = get_news_articles()

    if g.user:
        if Watchlist.query.filter_by(user_id=g.user.id).first() == None:
            watchlist = None
        else:
            watchlist = Watchlist.query.filter_by(user_id=g.user.id)

        return render_template('home.html', indices=indices_data, news=news, watchlist=watchlist)
    else: 
        return render_template('home.html', indices=indices_data, news=news)


@app.route('/signup', methods=['GET', 'POST'])
def user_sign_up():
    """
    Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                username=form.username.data,
                password=form.password.data,
                image_url=form.image_url.data or User.image_url.default.arg
            )
            db.session.commit()
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('/users/signup.html', form=form)

        do_login(user)
        flash(f'Hello {user.first_name}!')

        return redirect('/')
    else:
        return render_template('/users/signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Handles logging in user """

    form = UserLoginForm()

    if form.validate_on_submit():
        user = User.authenticate(username=form.username.data, password=form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect('/')

        flash("Invalid credentials.", 'danger')

    return render_template('/users/login.html', form=form)


@app.route('/logout')
def logout():
    """ Handles logging out the user """

    do_logout()

    flash('You have been logged out!', 'success')
    return redirect('/')


##############################################################################
# General user routes:

@app.route('/users/<int:user_id>')
def user_show(user_id):
    """ Show User Profile """

    if not g.user.id:
        flash('Unauthorized Access')
        return redirect('/')

    user = User.query.get_or_404(user_id)

    if Watchlist.query.filter_by(user_id=user_id).first() == None:
        watchlist = None
    else:
        watchlist = Watchlist.query.filter_by(user_id=g.user.id)

    if Post.query.filter_by(user_id=user_id).first() == None:
        posts = None
    else: 
        posts = Post.query.filter_by(user_id=user_id)

    return render_template('users/show.html', user=user, posts=posts, watchlist=watchlist)



@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """ Edit user information """

    if not g.user:
        flash('Unauthorized Access', 'danger')
        return redirect('/')

    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.image_url = form.image_url.data or User.image_url.default.arg

        db.session.commit()
        flash(f'User details updated!', 'success')
        return redirect(f'/users/{user.id}')

    else:
        return render_template('users/edit.html', form=form, user=user)


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """ Delete user account from database """

    if not g.user:
        flash('Unauthorized Access')
        return redirect('/')


    user = User.query.get_or_404(user_id)

    db.session.query(Post).filter(Post.user_id==user_id).delete()
    db.session.commit()

    db.session.delete(user)
    db.session.commit()

    return redirect('/signup')


##############################################################################
# General ticker routes:

@app.route('/tickers')
def show_all_tickers():
    """ Shows all tickers and allows a user to search the list """
    
    tickers = Ticker.query.all()

    return render_template('tickers/list.html', tickers=tickers)


@app.route('/tickers/search')
def show_stock_list():
    """ Show a list of stocks based on input search """

    search = request.args['ticker']

    tickers = Ticker.query.filter(Ticker.ticker.ilike(f'%{search}%') | Ticker.name.ilike(f'%{search}%')).all()

    return render_template('tickers/list.html', tickers=tickers)



@app.route('/tickers/<ticker_name>')
def ticker_details(ticker_name):
    """ Shows information about a selected ticker symbol """

    ticker = Ticker.query.get_or_404(ticker_name)
    
    if Post.query.filter_by(ticker=ticker.ticker).first() == None:
        posts = None
    else:
        posts = Post.query.filter_by(ticker=ticker.ticker).order_by(Post.timestamp.desc())

    ticker_details = get_ticker_details(ticker_name)

    ticker_news = get_news_for_ticker(ticker.ticker)

    return render_template('tickers/ticker_details.html', ticker=ticker, ticker_details=ticker_details, news=ticker_news, posts=posts)



@app.route('/tickers/<ticker_name>/post/add', methods=['GET', 'POST'])
def add_post(ticker_name):
    """ Form to submit a new post for a ticker """

    form = AddPost()
    ticker = Ticker.query.get_or_404(ticker_name)

    if form.validate_on_submit():
        try:
            new_post = Post(
                content = form.content.data,
                user_id = g.user.id,
                ticker = ticker_name
            )
            db.session.add(new_post)
            db.session.commit()

            return redirect(f'/tickers/{ticker_name}')
        except AttributeError:
            flash('Please login to add a new post', 'warning')
            return redirect('/login')
    else:
        return render_template('/tickers/new_post.html', form=form, ticker=ticker)


@app.route('/tickers/<ticker_name>/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(ticker_name, post_id):
    """ Handles the user editing a post """

    ticker = Ticker.query.get_or_404(ticker_name)
    post = Post.query.get_or_404(post_id)

    form = EditPost(obj=post)

    if not g.user:
        flash('Unauthorized Access', 'danger')
        return redirect(f'/tickers/{ticker_name}')

    if form.validate_on_submit():
        try:
            post.content = form.content.data
            db.session.commit()

            return redirect(f'/tickers/{ticker_name}')
        except AttributeError:
            flash('Please login to add a new post', 'warning')
            return redirect('/login')
    else:
        return render_template('/tickers/edit_post.html', form=form, ticker=ticker)


@app.route('/tickers/<ticker_name>/post/<int:post_id>/delete', methods=['DELETE'])
def delete_post(ticker_name, post_id):
    """ Handles deleting a user post """

    if not g.user:
        flash('Please login or sign up to create a post', 'danger')
        return redirect(f'/tickers/{ticker_name}')

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    user_posts = Post.query.filter_by(user_id=g.user.id)

    if user_posts.first():
        return jsonify(posts=True)
    else:
        return jsonify(posts=None)


##############################################################################
# General watchlist routes:

@app.route('/watchlists/<ticker_id>/add', methods=['GET', 'POST'])
def create_or_update_watchlist(ticker_id):
    """ 
    Creates a new watchlist if no watchlist is already created and adds stocks to watchlist if the user already has a watchlist 
    """

    if not g.user:
        flash(f'Please login or sign up to add {ticker_id} to watchlist', 'danger')
        return redirect('/tickers')

    form = CreateWatchlist()
    ticker = Ticker.query.get_or_404(ticker_id)
    ticker_details = get_watchlist_ticker_data(ticker_id)

    if Watchlist.query.filter_by(user_id=g.user.id).first() == None:
        if form.validate_on_submit():
            new_watchlist = Watchlist(name=form.name.data or Watchlist.name.default.arg, ticker=ticker.ticker, open=ticker_details['open'], close=ticker_details['close'], high=ticker_details['high'], low=ticker_details['low'], user_id=g.user.id)

            db.session.add(new_watchlist)
            db.session.commit()
            flash(f'Watchlist created!', 'success')
            return redirect(f'/users/{g.user.id}')

        else:
            return render_template('watchlists/new.html', form=form)
    else: 
        watchlist = Watchlist.query.filter_by(user_id=g.user.id).first()
        add_ticker_to_watchlist = Watchlist(name=watchlist.name, ticker=ticker.ticker, open=ticker_details['open'], close=ticker_details['close'], high=ticker_details['high'], low=ticker_details['low'], user_id=g.user.id)   

        db.session.add(add_ticker_to_watchlist)
        db.session.commit()
        flash(f'{ticker.ticker} added to {watchlist.name}!', 'success')
        return redirect('/tickers')



@app.route('/watchlists/<ticker_id>/delete', methods=['DELETE'])
def delete_watchlist_ticker(ticker_id):
    """ Delete a ticker from the watchlist """

    if not g.user.id:
        flash('Unauthorized Access', 'danger')
        return redirect('/')

    watchlist_item = Watchlist.query.get_or_404(ticker_id)

    db.session.delete(watchlist_item)
    db.session.commit()

    user_watchlist = Watchlist.query.filter_by(user_id=g.user.id)

    if user_watchlist.first():
        return jsonify(watchlist=user_watchlist.all())
    else:
        return jsonify(watchlist=None)


@app.route('/watchlists/delete', methods=['DELETE'])
def delete_watchlist():
    """ Delete user watchlist """

    if not g.user.id:
        flash('Unauthorized Access', 'danger')
        return redirect('/')

    Watchlist.query.filter_by(user_id=g.user.id).delete()

    db.session.commit()

    return jsonify(watchlist=None)
