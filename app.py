from flask import Flask
from flask_jwt_extended import JWTManager
from models import (
    db
)

from views import (
    GameAPI,
    GameDetailAPI,
    UserRegisterAPI,
    AuthLoginAPI,
    UserAPI,
    UserDetailAPI,
    ReviewAPI,
    ReviewDetailAPI,
    GenreAPI,
    GenreDetailAPI,
    UserRegisterAPI,
    AuthLoginAPI
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://BD2021:BD2021itec@143.198.156.171:3306/argame_db'
)
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'SECRET_KEY'

jwt = JWTManager(app)
db.init_app(app)

# Rutas de los endpoints

# Juegos
app.add_url_rule(
    '/games',
    view_func=GameAPI.as_view('games_api'),
    methods=['GET', 'POST']
)

# Informacion detallada de juego
app.add_url_rule(
    '/games/<int:id>',
    view_func=GameDetailAPI.as_view('game_detail_api'),
    methods=['GET', 'PATCH', 'DELETE']
)


# Registro de usuario
app.add_url_rule(
    '/register',
    view_func=UserRegisterAPI.as_view('user_register_api'),
    methods=['POST']
)

# Login de usuario
app.add_url_rule(
    '/login',
    view_func=AuthLoginAPI.as_view('auth_login_api'),
    methods=['POST']    
)

# Informacion de usuarios
app.add_url_rule(
    '/users',
    view_func=UserAPI.as_view('users_api'),
    methods=['GET']
)

# Informacion detallada de usuario
app.add_url_rule(
    '/users/<int:id>',
    view_func=UserDetailAPI.as_view('user_detail_api'),
    methods=['GET', 'PATCH', 'DELETE']
)

# Informacion de reviews
app.add_url_rule(
    '/games/<int:id>/reviews',
    view_func=ReviewAPI.as_view('review_api'),
    methods=['GET', 'POST']
)

# Informacion detallada de review
app.add_url_rule(
    '/reviews/<int:id>',
    view_func=ReviewDetailAPI.as_view('review_detail_api'),
    methods=['DELETE']
)

# Informacion de generos
app.add_url_rule(
    '/genres',
    view_func=GenreAPI.as_view('genre_api'),
    methods=['GET', 'POST']
)

# Informacion detallada de genero
app.add_url_rule(
    '/genres/<int:id>',
    view_func=GenreDetailAPI.as_view('genre_detail_api'),
    methods=['PUT', 'DELETE']
)

if __name__ == '__main__':
    app.run(debug=True)