from flask import request, jsonify
from marshmallow import ValidationError
from flask.views import MethodView
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
    get_jwt
)
from passlib.hash import bcrypt
from datetime import timedelta

from models import (
    db,
    User,
    UserCredentials,
    Developer,
    Editor,
    Game,
    Genre,
    GameGenre,
    Review,
    UserGame
)

from schemas import(
    UserSchema,
    UserGameSchema,
    DeveloperSchema,
    EditorSchema,
    GameSchema,
    GenreSchema,
    GameGenreSchema,
    ReviewSchema,
    RoleSchema,
    RegisterSchema,
    LoginSchema
)

from functools import wraps

# Función para verificar si un usuario es propietario de un recurso o es admin
def check_ownership(user_id, resource_owner_id):
    # Verificar si el usuario es el propietario
    if str(user_id) != str(resource_owner_id):
        return False
    claims = get_jwt()
    # Verificar si el usuario es admin
    if claims.get("role") == "admin":
        return True
    return True

# Decorador para roles
def roles_required(*allowed_roles: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            role = claims.get("role")
            if not role or role not in allowed_roles:
                return {"Error": "acceso denegado"}, 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


# ----- Autenticacion -----


# API de registro
class UserRegisterAPI(MethodView):
    def post(self):
        try:
            # Traer y validar datos
            data = RegisterSchema().load(request.json)
        except ValidationError as err:
            return jsonify({"Error": err.messages}), 400
        
        # Verificar si el email ya existe
        if User.query.filter_by(email=data['email']).first():
            return {"message": "Email en uso"}, 400
        
        # Crear usuario
        new_user = User(
            username=data['username'],
            name=data['name'],
            email=data['email']
        )
        # Guardar en la base de datos
        db.session.add(new_user)
        db.session.flush()

        # Hashear la contraseña
        password_hash = bcrypt.hash(data['password'])

        # Crear credenciales
        credentials = UserCredentials(
            user_id=new_user.id,
            password_hash=password_hash,
            role_id=data['role_id']
        )
        # Guardar credenciales en la base de datos
        db.session.add(credentials)
        db.session.commit()
        return UserSchema().dump(new_user), 201


# API de login
class AuthLoginAPI(MethodView):
    def post(self):
        # Traer y validar datos
        try:
            data = LoginSchema().load(request.json)
        except ValidationError as err:
            return{"Error": err.messages}, 400

        # Buscar usuario por email
        user = User.query.filter_by(email=data['email']).first()

        # Verificar si el usuario existe
        if not user or not user.credentials:
            return {"message": "Email no valido"}, 401
        
        # Verificar contraseña
        if not bcrypt.verify(data['password'], user.credentials.password_hash):
            return {"message": "Contraseña incorrecta"}, 401
        
        # Crear elementos para el token de acceso
        identity = str(user.id)
        additional_claims = {
            'id' : user.id,
            'email' : user.email,
            'username' : user.username,
            'role' : user.credentials.role.name,
        }
        expiration = timedelta(hours=24)
        
        # Generar el token de acceso
        token = create_access_token(
            identity=identity,
            additional_claims=additional_claims,
            expires_delta=expiration
        )
        return {"access_token": token}, 200
        


# ----- Usuarios -----


# API de usuarios
class UserAPI(MethodView):
    # Traer usuarios activos (admin)
    @jwt_required()
    @roles_required('admin')
    def get(self):
        users = User.query.filter_by(is_active=True).all()
        return UserSchema(many=True).dump(users), 200


# API de detalle de usuario
class UserDetailAPI(MethodView):
    decorators = [jwt_required()]
    # Traer usuario (user, admin)
    @roles_required('admin','user')
    def get(self,id):
        user = User.query.get_or_404(id)
        return UserSchema().dump(user), 200
    
    # Modificar usuario (admin)
    @roles_required('admin')
    def patch(self,id):
        # Traer usuario
        user = User.query.get_or_404(id)
        try:
            # Validar datos
            data = UserSchema(partial=True).load(request.json)
            # Actualizar campos
            if 'username' in data:
                user.username = data['username']
            if 'email' in data:
                user.email = data['email']
            # Actualizar fecha de actualizacion y guardar   
            user.updated_at = db.func.now()
            db.session.commit()
        except ValidationError as err:
            return jsonify({"Error": err.messages}), 400
        return UserSchema().dump(user), 200
    
    # Desactivar usuario (admin)
    @roles_required('admin')
    def delete(self,id):
        # Traer usuario y desactivar
        user = User.query.get_or_404(id)
        user.is_active = False
        db.session.commit()
        return {"message": "Usuario desactivado"}, 200


# ------ Juegos -----


# API de juegos
class GameAPI(MethodView):
    # Traer juegos 
    def get(self):
        games = Game.query.filter_by(is_published=True).all()
        return GameSchema(many=True).dump(games), 200

    # Agregar juego (admin)
    @jwt_required()
    @roles_required('admin')
    def post(self):
        try:
            # Traer y validar datos
            data = GameSchema().load(request.json)
        except ValidationError as err:
            return jsonify({"Error": err.messages}), 400
        
        # Crear juego nuevo
        new_game = Game(
            name=data['name'],
            price=data['price'],
            release_date=data['release_date'],
            thumbnail=data['thumbnail'],
            description=data['description'],
            uploaded_at=db.func.now(),
            developer_id=data['developer_id'],
            editor_id=data['editor_id'])
        # Guardar en la base de datos
        db.session.add(new_game)
        db.session.commit()
        return GameSchema().dump(new_game), 201


# API de detalle de juego
class GameDetailAPI(MethodView):
    # Traer juego
    def get(self,id):
        game = Game.query.get_or_404(id)
        return GameSchema().dump(game), 200
    
    # Modificar juego (admin)
    @jwt_required()
    @roles_required('admin')
    def patch(self,id):
        # Traer juego por id
        game = Game.query.get_or_404(id)
        try:
            # Validar datos
            data = GameSchema(partial=True).load(request.json)
            # Actualizar campos
            if 'name' in data:
                game.name = data['name']
            if 'price' in data:
                game.price = data['price']
            if 'release_date' in data:
                game.release_date = data['release_date']
            if 'thumbnail' in data:
                game.thumbnail = data['thumbnail']
            if 'description' in data:
                game.description = data['description']
            if "is_free" in data:
                game.is_free = data['is_free']
            if "created_at" in data:
                game.created_at = data['created_at']
            if "uploaded_at" in data:
                game.uploaded_at = data['uploaded_at']
            if 'developer_id' in data:
                game.developer_id = data['developer_id']
            if 'editor_id' in data:
                game.editor_id = data['editor_id']
            db.session.commit()
        except ValidationError as err:
            return jsonify({"Error": err.messages}), 400
        return GameSchema().dump(game), 200
    
    # Desactivar juego (admin)
    @jwt_required()
    @roles_required('admin')
    def delete(self,id):
        # Traer juego por id y desactivar
        game = Game.query.get_or_404(id)
        game.is_published = False
        db.session.commit()
        return {"message": "Juego desactivado"}, 200


# ----- Biblioteca de juegos -----


# API de biblioteca de juegos de usuario
class UserGameAPI(MethodView):    
    decorators = [jwt_required()]
    # Traer juegos de usuario (user, admin)
    @roles_required('admin','user')
    def get(self,id):
        # Traer juegos por id de usuario
        user_games = UserGame.query.filter_by(user_id=id).all()
        return UserGameSchema(many=True).dump(user_games), 200
    
    # Agregar juego a usuario (user)
    @roles_required('user')
    def post(self,id):
        try:
            # Validar datos
            data = UserGameSchema().load(request.json)
        except ValidationError as err:
            return jsonify({"Error": err.messages}), 400
        
        # Verificar ownership
        current_user_id = get_jwt_identity()
        if not check_ownership(current_user_id, id):
            return {'error':'No tienes permiso para agregar juegos a este usuario'}, 403

        # Agregar juego a la biblioteca
        new_user_game = UserGame(
            user_id=id,
            game_id=data['game_id'],
            claimed_at=db.func.now()
        )
        # Guardar en la base de datos
        db.session.add(new_user_game)
        db.session.commit()
        return UserGameSchema().dump(new_user_game), 201


# ----- Reviews -----


# API de reviews
class ReviewAPI(MethodView):
    # Traer review 
    def get(self,id):
        # Traer reviews por id de juego
        reviews = Review.query.filter_by(game_id=id).all()
        return ReviewSchema(many=True).dump(reviews), 200
    
    # Agregar review (user)
    @jwt_required()
    @roles_required('user')
    def post(self,id):
        try:
            # Validar datos
            data = ReviewSchema().load(request.json)
        except ValidationError as err:
            return jsonify({"Error": err.messages}), 400
        
        # Obtener usuario logueado
        current_user_id = get_jwt_identity()
        
        # Crear nueva review
        new_review = Review(
            user_id=current_user_id,
            game_id=id,
            rating=data['rating'],
            text_review=data['text_review']
        )
        # Guardar en la base de datos
        db.session.add(new_review)
        db.session.commit()
        return ReviewSchema().dump(new_review), 201


# API de detalle de review
class ReviewDetailAPI(MethodView):
    # Desactivar review (moderator, user, admin)
    @jwt_required()
    @roles_required('admin','moderator','user')
    def delete(self,id):
        # Traer review por id
        review = Review.query.get_or_404(id)
        # Obtener rol y usuario actual
        claims = get_jwt()
        user_role = claims.get('role')
        current_user_id = get_jwt_identity()

        # Verificar ownership
        if user_role == 'user' and not check_ownership(current_user_id, review.user_id):
            return {'error':'No tienes permiso para borrar esta review'}, 403

        # Desactivar review
        review.is_visible = False
        db.session.commit()
        return {"message": "Review desactivada"}, 200
    
    #Traer reseña
    def get(self,id):
        # Traer review por id
        review = Review.query.get_or_404(id)
        return ReviewSchema().dump(review), 200


# ----- Generos -----


# Api de generos
class GenreAPI(MethodView):
    # Traer generos 
    def get(self):
        genre = Genre.query.all()
        return GenreSchema(many=True).dump(genre), 200
    
    # Agregar genero (moderator, admin)
    @jwt_required()
    @roles_required('admin','moderator')
    def post(self):
        try:
            # Validar datos
            data = GenreSchema().load(request.json)
        except ValidationError as err:
            return jsonify({"Error": err.messages}), 400
        
        # Crear nuevo genero
        new_genre = Genre(
            name=data['name']
        )
        # Guardar en la base de datos
        db.session.add(new_genre)
        db.session.commit()
        return GenreSchema().dump(new_genre), 201


# API de detalle de genero
class GenreDetailAPI(MethodView):
    # Modificar genero (Moderator, admin)
    decorators = [jwt_required()]
    @roles_required('admin','moderator')
    def put(self,id):
        try:
            # Validar datos
            data = GenreSchema(partial=True).load(request.json)
        except ValidationError as err:
            return jsonify({"Error": err.messages}), 400
        
        # Traer genero por id
        genre = Genre.query.get_or_404(id)
        # Actualizar campos
        if 'name' in data:
            genre.name = data['name']
        if 'is_active' in data:
            genre.is_active = data['is_active']
        db.session.commit()
        return GenreSchema().dump(genre), 200
    
    # Eliminar genero (admin)
    @roles_required('admin')
    def delete(self,id):
        # Traer genero por id y desactivar
        genre = Genre.query.get_or_404(id)
        genre.is_active = False
        db.session.commit()
        return {"message": "Genero desactivado"}, 200


# API de juegos por genero
class GenreGamesAPI(MethodView):
    @jwt_required()
    @roles_required('admin','moderator','user')
    # Traer juegos por genero
    def get(self,id):
        # Traer juegos por id de genero
        game_genres = GameGenre.query.filter_by(genre_id=id).all()
        return GameGenreSchema(many=True).dump(game_genres), 200


# ----- Developers y Editors -----


# API de developers
class DeveloperAPI(MethodView):
    @jwt_required()
    @roles_required('admin','moderator','user')
    # Traer developers
    def get(self):
        developers = Developer.query.all()
        return DeveloperSchema(many=True).dump(developers), 200
    


# API de detalle de developer
class DeveloperDetailAPI(MethodView):
    @jwt_required()
    @roles_required('admin','moderator','user')
    # Traer developer por id
    def get(self,id):
        developer = Developer.query.get_or_404(id)
        return DeveloperSchema().dump(developer), 200


# API de editors
class EditorAPI(MethodView):
    @jwt_required()
    @roles_required('admin','moderator','user')
    # Traer editores
    def get(self):
        editors = Editor.query.all()
        return EditorSchema(many=True).dump(editors), 200


# API de detalle de editor
class EditorDetailAPI(MethodView):
    @jwt_required()
    @roles_required('admin','moderator','user')
    # Traer editor por id
    def get(self,id):
        editor = Editor.query.get_or_404(id)
        return EditorSchema().dump(editor), 200


# ------ Estadisticas -----


# API de estadisticas
class StatsAPI(MethodView):
    # Traer estadisticas (admin, moderator)
    @jwt_required()
    @roles_required('admin','moderator')
    def get(self):
        # Total de usuarios
        total_users = User.query.count()
        # Total de juegos
        total_games = Game.query.count()
        # Total de reviews
        total_reviews = Review.query.count()
        # Total de juegos subidos en la ultima semana
        posts_last_week = Game.query.filter(
            Game.uploaded_at >= db.func.now() - db.text('INTERVAL 7 DAY')
        ).count()
        return {
            "total_users": total_users,
            "total_games": total_games,
            "total_reviews": total_reviews,
            "posts_last_week": posts_last_week
        }, 200
            
