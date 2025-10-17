from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),unique=True,nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    credentials = db.relationship('UserCredentials',back_populates='user',uselist=False)
    reviews = db.relationship('Review',back_populates='user')
    user_games = db.relationship('UserGame', back_populates='user')
    

class Developer(db.Model):
    __tablename__ = 'developers'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    games = db.relationship('Game', backref='developer')


class Editor(db.Model):
    __tablename__ = 'editors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    games = db.relationship('Game', backref='editor')


class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Double(), nullable=False)
    release_date = db.Column(db.Date(), nullable=False)
    thumbnail = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(),nullable=False)
    is_free = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    uploaded_at = db.Column(db.DateTime, onupdate=db.func.now())
    developer_id = db.Column(db.ForeignKey('developers.id'))
    editor_id = db.Column(db.ForeignKey('editors.id'))
    is_published = db.Column(db.Boolean(), default=True)

    reviews = db.relationship('Review', back_populates='game')
    user_games = db.relationship('UserGame', back_populates='game')
    genres= db.relationship('GameGenre', back_populates='game')

class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    games = db.relationship('GameGenre', back_populates='genre')

class GameGenre(db.Model):
    __tablename__ = 'games_genres'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=False)

    game = db.relationship('Game', back_populates='genres')
    genre = db.relationship('Genre', back_populates='games')

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    text_review = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    user = db.relationship('User', back_populates='reviews')
    game = db.relationship('Game', back_populates='reviews')

class UserCredentials(db.Model):
    __tablename__ = 'user_credentials'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    user = db.relationship('User', back_populates='credentials')
    role = db.relationship('Role', back_populates='credentials')


class UserGame(db.Model):
    __tablename__ = 'user_games'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    claimed_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    user = db.relationship('User', back_populates='user_games')
    game = db.relationship('Game', back_populates='user_games')

class role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=True)