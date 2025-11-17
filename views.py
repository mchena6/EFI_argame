from flask import request, jsonify
from marshmallow import ValidationError
from flask.views import MethodView
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from models import (
    db,
    User,
    Developer,
    Editor,
    Game,
    Genre,
    GameGenre,
    Review,
    Role
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
    RegisterSchema,
    LoginSchema,
    RoleSchema
)

from services.auth_service import AuthService
from services.game_service import GameService
from services.user_game_service import UserGameService

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

# API de registro (¡Refactorizada!)
class UserRegisterAPI(MethodView):
    
    def __init__(self):
        # Servicio de autenticacion
        self.service = AuthService()

    def post(self):
        try:
            # Validar datos de entrada
            data = RegisterSchema().load(request.json)
        except ValidationError as err:
            return jsonify({"Error": err.messages}), 400
        
        try:
            # Llamar al servicio para validar datos
            new_user = self.service.register_user(data)
            return UserSchema().dump(new_user), 201
        
        # Manejar errores
        except ValueError as e:
            # Deshacer cambios si hubo error
            db.session.rollback() 
            return {"message": str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {"message": "Error interno del servidor"}, 500


# API de login
class AuthLoginAPI(MethodView):

    def __init__(self):
        self.service = AuthService()

    def post(self):
        try:
            # Validar datos 
            data = LoginSchema().load(request.json)
        except ValidationError as err:
            return{"Error": err.messages}, 400

        try:
            # Llamar al servicio para loguearse
            token = self.service.login_user(data['email'], data['password'])
            
            # Mostrar token de acceso
            return {"access_token": token}, 200
        
        # Manejar errores
        except ValueError as e:
            return {"message": str(e)}, 401

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

    def __init__(self):
        self.service = GameService()

    # Traer juegos 
    def get(self):
        # Llamar al servicio para traer los juegos publicados
        games = self.service.get_published_games()
        return GameSchema(many=True).dump(games), 200

    # Agregar juego (admin)
    @jwt_required()
    @roles_required('admin')
    def post(self):
        try:
            # Validar datos
            data = GameSchema().load(request.json)
        except ValidationError as err:
            return jsonify({"Error": err.messages}), 400
        
        try:
            # Llamar al servicio para postear un juego
            new_game = self.service.create_game(data)
            return GameSchema().dump(new_game), 201
        
        # Manejar errores
        except Exception as e:
            db.session.rollback()
            return jsonify({"Error": f"Error interno: {str(e)}"}), 500

# API de detalle de juego
class GameDetailAPI(MethodView):
    
    def __init__(self):
        self.service = GameService()

    # Traer juego
    def get(self,id):
        try:
            # Llamar al servicio para traer juegos por id
            game = self.service.get_game_by_id(id)
            return GameSchema().dump(game), 200
        # Manejar error
        except ValueError as e:
            return jsonify({"Error": str(e)}), 404
    
    # Modificar juego (admin)
    @jwt_required()
    @roles_required('admin')
    def patch(self,id):
        
        if not request.json:
            return jsonify({"error": "No JSON data provided"}), 400

        try:
            # Validar datos
            data = GameSchema(partial=True).load(request.json)
        except ValidationError as err:
            return jsonify({"Error": err.messages}), 400
            
        try:
            # Llamar al servicio para modificar datos de un juego
            updated_game = self.service.update_game(id, data)
            return GameSchema().dump(updated_game), 200
        
        # Manejar errores
        except ValueError as e:
            db.session.rollback()
            return jsonify({"Error": str(e)}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({"Error": f"Error interno: {str(e)}"}), 500
        
    # Desactivar juego (admin)
    @jwt_required()
    @roles_required('admin')
    def delete(self,id):
        try:
            # Llamar al servicio para desactivar un juego
            message = self.service.disable_game(id)
            return jsonify(message), 200
        
        # Manejar error
        except ValueError as e:
            db.session.rollback()
            return jsonify({"Error": str(e)}), 404

# ----- Biblioteca de juegos -----

# API de biblioteca de juegos de usuario
class UserGameAPI(MethodView):    
    decorators = [jwt_required()]
    
    def __init__(self):
        self.service = UserGameService()

    # Traer juegos de usuario (user, admin)
    @roles_required('admin','user')
    def get(self,id):
        # Llamar al servicio para traer juegos por id de usuario
        user_games = self.service.get_games_for_user(user_id=id)
        return UserGameSchema(many=True).dump(user_games), 200
    
    # Agregar juego a usuario (user)
    @roles_required('user')
    def post(self,id):
        try:
            # Validar datos
            data = UserGameSchema().load(request.json)
        except ValidationError as err:
            return jsonify({"Error": err.messages}), 400
        
        # Obtener id del usuario logueado
        current_user_id = get_jwt_identity()
        # Verificar ownership
        if not check_ownership(current_user_id, id):
            return {'error':'No tienes permiso para agregar juegos a este usuario'}, 403
        
        # Obtener datos de la solicitud
        game_id = data['game_id']
        user_id = id
                
        try:
            # Llamar al servicio para agregar un juego a la biblioteca de un usuario
            new_user_game = self.service.add_game_to_user(
                user_id=user_id, 
                game_id=game_id, 
                current_user_id=current_user_id
            )
            return UserGameSchema().dump(new_user_game), 201
            
        # Manejar errores de duplicados
        except ValueError as e:
            db.session.rollback()
            return {'error': str(e)}, 400
        #  Manejar errores inesperados
        except Exception as e:
            db.session.rollback()
            return {'error': f'Error interno del servidor: {str(e)}'}, 500

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
        genre = Genre.query.filter_by(is_active=True).all()
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
            

# ----- Roles -----

# API de roles
class RoleAPI(MethodView):
    def get(self):
        roles = Role.query.all()
        return RoleSchema(many=True).dump(roles), 200