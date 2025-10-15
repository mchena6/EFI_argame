from flask import request
from marshmallow import ValidationError
from flask.views import MethodView
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
    get_jwt
)
from passlib.hash import bcrypt

class UserRegisterAPI(MethodView):
    def post():
        ...


class AuthLoginAPI():
    def post():
        ...

class UserAPI(MethodView):
    # Traer usuarios (admin)
    def get():
        ...


class UserDetailAPI(MethodView):
    # Traer usuario (user, admin)
    def get(self,id):
        ...
    # Modificar usuario (admin)
    def patch(self,id):
        ...
    # Desactivar usuario (admin)
    def delete(self,id):
        ...


class GameAPI(MethodView):
    # Traer juegos 
    def get(self):
        ...
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
