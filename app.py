from flask import Flask, session, render_template, redirect, g, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Ticker, Post, Watchlist, UserWatchlist
from forms import UserAddForm, UserLoginForm, EditUserForm, AddPost, EditPost
from sqlalchemy.exc import IntegrityError
from get_data import get_main_indices, get_news_articles, get_ticker_details, get_news_for_ticker

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///stock_market_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.debug = True
app.config['SECRET_KEY'] = 'secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)


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

    main_indices = ['SPX', 'NDAQ', 'DIA']

    indices_data = get_main_indices(main_indices)

    news = get_news_articles()

    if not g.user:
        watchlists = None
    else:
        watchlists = Watchlist.query.filter_by(user_id=g.user.id).all()
        print(watchlists)

    return render_template('home.html', indices=indices_data, news=news, watchlists=watchlists)


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

    user = User.query.get_or_404(user_id)

    if Post.query.filter_by(user_id=user_id).first() == None:
        posts = None
    else: 
        posts = Post.query.filter_by(user_id=user_id)

    return render_template('users/show.html', user=user, posts=posts)



@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """ Edit user information """

    if g.user.id != user_id:
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

    user = User.query.get_or_404(user_id)

    db.session.query(Post).filter(Post.user_id==user_id).delete()
    db.session.commit()

    db.session.delete(user)
    db.session.commit()

    return redirect('/signup')


##############################################################################
# General ticker routes:

@app.route('/tickers/search')
def show_stock_list():
    """ Show a list of stocks based on input search """

    search = request.args['ticker']

    tickers = Ticker.query.filter(Ticker.ticker.like(f'%{search.upper()}%')).all()

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

    if g.user.id != post.user_id:
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


@app.route('/tickers/<ticker_name>/post/<int:post_id>/delete', methods=['POST'])
def delete_post(ticker_name, post_id):
    """ Handles deleting a user post """

    post = Post.query.get_or_404(post_id)

    if g.user.id != post.user_id:
        flash('Unauthorized Access')
        return redirect(f'/tickers/{ticker_name}')

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/tickers/{ticker_name}')


##############################################################################
# General watchlist routes:
