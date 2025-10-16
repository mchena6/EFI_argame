from flask import Flask
from flask_jwt_extended import JWTManager
from models import (
    db
)

from views import (
    GameAPI,
    UserRegisterAPI,
    AuthLoginAPI,
    UserAPI,
    UserDetailAPI,
    ReviewAPI,
    ReviewDetailAPI,
    GenreAPI,
    GenreDetailAPI,
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://BD2021:BD2021itec@143.198.156.171:3306/argame_db'
)
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'SECRET_KEY'

jwt = JWTManager(app)
db.init(app)

app.add_url_rule(
    '/games',
    view_func=GameAPI.as_view('games_api'),
    methods=['GET', 'POST']
)
