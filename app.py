from flask import Flask
# Libreria para manejar JWT
from flask_jwt_extended import JWTManager
from models import (
    db
)

# Vistas
from views import (
    GameAPI,
    GameDetailAPI,
    UserRegisterAPI,
    AuthLoginAPI,
    UserAPI,
    UserDetailAPI,
    UserGameAPI,
    ReviewAPI,
    ReviewDetailAPI,
    GenreAPI,
    GenreDetailAPI,
    UserRegisterAPI,
    AuthLoginAPI,
    DeveloperAPI,
    DeveloperDetailAPI,
    EditorAPI,
    EditorDetailAPI,
    GenreGamesAPI,
    StatsAPI,
    RoleAPI
)

# Libreria para cargar variables de entorno
import os 
from dotenv import load_dotenv

# Variables de entorno
load_dotenv()

# Cargar variables de entorno para la BD
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Libreria para manejar CORS
from flask_cors import CORS

# Configuracion de la aplicacion
app = Flask(__name__)
CORS(app)
# Conexion a base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

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

# Biblioteca de juegos de usuario
app.add_url_rule(
    '/users/<int:id>/games',
    view_func=UserGameAPI.as_view('user_game_api'),
    methods=['GET', 'POST']
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

# Informacion de developers
app.add_url_rule(
    '/developers',
    view_func=DeveloperAPI.as_view('developer_api'),
    methods=['GET']
)

# Informacion detallada de developer
app.add_url_rule(
    '/developers/<int:id>',
    view_func=DeveloperDetailAPI.as_view('developer_detail_api'),
    methods=['GET']
)

# Informacion de editores
app.add_url_rule(
    '/editors',
    view_func=EditorAPI.as_view('editor_api'),
    methods=['GET']
)

# Informacion detallada de editor
app.add_url_rule(
    '/editors/<int:id>',
    view_func=EditorDetailAPI.as_view('editor_detail_api'),
    methods=['GET']
)

# Informacion de juegos por genero
app.add_url_rule(
    '/genres/<int:id>/games',
    view_func=GenreGamesAPI.as_view('genre_games_api'),
    methods=['GET']
)


# Estadisticas
app.add_url_rule(
    '/stats',
    view_func=StatsAPI.as_view('stats_api'),
    methods=['GET']
)

# Roles de usuario
app.add_url_rule(
    '/roles',
    view_func=RoleAPI.as_view('roles_api'),
    methods=['GET']
)

if __name__ == '__main__':
    app.run(debug=True)
