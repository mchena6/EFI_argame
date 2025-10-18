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
            return {"message": "Credenciales invalidas"}, 401
        # Verificar contraseña
        if not bcrypt.verify(data['password'], user.credentials.password_hash):
            return {"message": "Credenciales invalidas"}, 401
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
    def get(self):
        users = User.query.filter_by(is_active=True).all()
        return UserSchema(many=True).dump(users), 200


# API de detalle de usuario
class UserDetailAPI(MethodView):
    # Traer usuario (user, admin)
    def get(self,id):
        user = User.query.get_or_404(id)
        return UserSchema().dump(user), 200
    # Modificar usuario (admin)
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
    def post(self):
        ...

class GameDetailAPI(MethodView):
    # Traer juego
    def get(self,id):
        ...
    # Modificar juego (admin)
    def put(self,id):
        ...
    # Desactivar juego (admin)
    def delete(self,id):
        ...
    

class ReviewAPI(MethodView):
    # Traer review
    def get(self,id):
        ...
    # Agregar review (requiere autorizacion)
    def post(self,id):
        ...

class ReviewDetailAPI(MethodView):
    # Desactivar review (moderator, user, admin)
    def delete(self,id):
        ...


class GenreAPI():
    # Traer generos
    def get():
        ...
    # Agregar genero
    def post():
        ...

class GenreDetailAPI(MethodView):
    def put(self,id):
        ...
    def delete(self,id):
        ...
