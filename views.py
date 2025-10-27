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
    UserCredentialsSchema,
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

# API de registro
class UserRegisterAPI(MethodView):
    def post(self):
        try:
            data = RegisterSchema().load(request.json)
        except ValidationError as err:
            return jsonify({"Error": err.messages}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return {"message": "Email en uso"}, 400
        
        new_user = User(
            username=data['username'],
            name=data['name'],
            email=data['email']
        )
        db.session.add(new_user)
        db.session.flush()

        password_hash = bcrypt.hash(data['password'])

        credentials = UserCredentials(
            user_id=new_user.id,
            password_hash=password_hash,
            role_id=data['role_id']
        )
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
        # Generar el token de acceso
        token = create_access_token(
            identity=identity,
            additional_claims=additional_claims
        )
        return {"access_token": token}, 200
        

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
        user = User.query.get_or_404(id)
        try:
            data = UserSchema(partial=True).load(request.json)
            if 'username' in data:
                user.username = data['username']
            if 'email' in data:
                user.email = data['email']
            user.updated_at = db.func.now()
            db.session.commit()
        except ValidationError as err:
            return jsonify({"Error": err.messages}), 400
        return UserSchema().dump(user), 200
    # Desactivar usuario (admin)
    @roles_required('admin')
    def delete(self,id):
        user = User.query.get_or_404(id)
        user.is_active = False
        db.session.commit()
        return {"message": "Usuario desactivado"}, 200


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
            data = GameSchema().load(request.json)
        except ValidationError as err:
            return jsonify({"Error": err.messages}), 400
        
        new_game = Game(
            name=data['name'],
            price=data['price'],
            release_date=data['release_date'],
            thumbnail=data['thumbnail'],
            description=data['description'],
            uploaded_at=db.func.now(),
            developer_id=data['developer_id'],
            editor_id=data['editor_id'])
        db.session.add(new_game)
        db.session.commit()
        return GameSchema().dump(new_game), 201

class GameDetailAPI(MethodView):
    # Traer juego
    def get(self,id):
        game = Game.query.get_or_404(id)
        return GameSchema().dump(game), 200
    # Modificar juego (admin)
    @jwt_required()
    @roles_required('admin')
    def patch(self,id):
        game = Game.query.get_or_404(id)
        try:
            data = GameSchema(partial=True).load(request.json)
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
        game = Game.query.get_or_404(id)
        game.is_published = False
        db.session.commit()
        return {"message": "Juego desactivado"}, 200


class UserGameAPI(MethodView):    
    decorators = [jwt_required()]
    # Traer juegos de usuario (user, admin)
    @roles_required('admin','user')
    def get(self,id):
        user_games = UserGame.query.filter_by(user_id=id).all()
        return UserGameSchema(many=True).dump(user_games), 200
    # Agregar juego a usuario (user)
    @roles_required('user')
    def post(self,id):
        try:
            data = UserGameSchema().load(request.json)
        except ValidationError as err:
            return jsonify({"Error": err.messages}), 400
        
        current_user_id = get_jwt_identity()
        if str(id) != current_user_id:
            return {'error':'No tienes permiso para agregar juegos a este usuario'}, 403

        new_user_game = UserGame(
            user_id=id,
            game_id=data['game_id'],
            claimed_at=db.func.now()
        )
        db.session.add(new_user_game)
        db.session.commit()
        return UserGameSchema().dump(new_user_game), 201


class ReviewAPI(MethodView):
    # Traer review 
    def get(self,id):
        reviews = Review.query.filter_by(game_id=id).all()
        return ReviewSchema(many=True).dump(reviews), 200
    # Agregar review (user)
    @jwt_required()
    @roles_required('user')
    def post(self,id):
        try:
            data = ReviewSchema().load(request.json)
        except ValidationError as err:
            return jsonify({"Error": err.messages}), 400
        
        current_user_id = get_jwt_identity()
        
        new_review = Review(
            user_id=current_user_id,
            game_id=id,
            rating=data['rating'],
            text_review=data['text_review']
        )
        db.session.add(new_review)
        db.session.commit()
        return ReviewSchema().dump(new_review), 201


class ReviewDetailAPI(MethodView):
    # Desactivar review (moderator, user, admin)
    @jwt_required()
    @roles_required('admin','moderator','user')
    def delete(self,id):
        review = Review.query.get_or_404(id)
        claims = get_jwt()
        user_role = claims.get('role')
        current_user_id = get_jwt_identity()

        if user_role == 'user' and str(review.user_id) != current_user_id:
            return {'error':'No tienes permiso para borrar esta review'}, 403

        review.is_visible = False
        db.session.commit()
        return {"message": "Review desactivada"}, 200
    #Traer reseña
    def get(self,id):
        review = Review.query.get_or_404(id)
        return ReviewSchema().dump(review), 200

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
            data = GenreSchema().load(request.json)
        except ValidationError as err:
            return jsonify({"Error": err.messages}), 400
        
        new_genre = Genre(
            name=data['name']
        )
        db.session.add(new_genre)
        db.session.commit()
        return GenreSchema().dump(new_genre), 201

class GenreDetailAPI(MethodView):
    # Modificar genero (Moderador, admin)
    decorators = [jwt_required()]
    @roles_required('admin','moderator')
    def put(self,id):
        try:
            data = GenreSchema(partial=True).load(request.json)
        except ValidationError as err:
            return jsonify({"Error": err.messages}), 400
        genre = Genre.query.get_or_404(id)
        if 'name' in data:
            genre.name = data['name']
        if 'is_active' in data:
            genre.is_active = data['is_active']
        db.session.commit()
        return GenreSchema().dump(genre), 200
    # Eliminar genero (admin)
    @roles_required('admin')
    def delete(self,id):
        genre = Genre.query.get_or_404(id)
        genre.is_active = False
        db.session.commit()
        return {"message": "Genero desactivado"}, 200
    

