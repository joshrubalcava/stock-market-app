from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """ Connect to database """

    db.app = app
    db.init_app(app)


class User(db.Model):
    """ Table for users """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.Text, nullable=False)

    last_name = db.Column(db.Text, nullable=False)

    email = db.Column(db.Text, nullable=False, unique=True)

    username = db.Column(db.Text, nullable=False, unique=True)

    password = db.Column(db.Text, nullable=False)

    image_url = db.Column(db.Text, default='/static/images/default-pic.png')

    def __repr__(self):
        u = self
        return f'<User id={u.id} first_name={u.first_name} last_name={u.last_name} username={u.username} image_url={u.image_url}'

    @classmethod
    def signup(cls, first_name, last_name, email, username, password, image_url):
        """
        Sign up user

        Hashes password and adds user to the database
        """

        hashed_password = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=hashed_password,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """
        Find user with `username` and `password`.

        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If you can't find matching user (or if password is wrong), returns False.
        """

        user = User.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False


class Watchlist(db.Model):
    """ Table for user watchlists """

    __tablename__ = 'watchlists'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    ticker_symbol = db.Column(db.Text, db.ForeignKey('tickers.ticker'))

    def __repr__(self):
        u = self
        return f'<WatchList user_id={u.user_id} ticker_symbol={u.ticker_symbol}'


class Ticker(db.Model):
    """ Table for US Ticker Symbols """

    __tablename__ = 'tickers'

    ticker = db.Column(db.Text, primary_key=True, nullable=False)

    name = db.Column(db.Text, nullable=False)

    exchange = db.Column(db.Text, nullable=False)

    watchlist = db.relationship('User', secondary='watchlists', backref='tickers')

    def __repr__(self):
        u = self
        return f'<Ticker ticker={u.ticker} name={u.name}, primary_exchange={u.primary_exchange}'
