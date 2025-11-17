from passlib.hash import bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta

from models import db, User, UserCredentials
from repositories.user_repository import UserRepository
from repositories.user_credentials_repository import UserCredentialsRepository

class AuthService:
    
    def __init__(self):
        # Repositorios
        self.user_repo = UserRepository()
        self.credentials_repo = UserCredentialsRepository()

    # Registro de usuario 
    def register_user(self, data):
        # Verificar si el email ya existe
        if self.user_repo.get_by_email(data['email']):
            raise ValueError("Email en uso")
        
        # Crear usuario
        new_user = User(
            username=data['username'],
            name=data['name'],
            email=data['email']
        )
        # Llamar al repositorio para agregarlo a la base de datos
        self.user_repo.add(new_user)
        db.session.flush()

        # Hashear contraseña
        password_hash = bcrypt.hash(data['password'])

        # Crear credenciales
        credentials = UserCredentials(
            user_id=new_user.id,
            password_hash=password_hash,
            role_id=data['role_id']
        )
        # Usar el repositorio para agregarlas a la base de datos
        self.credentials_repo.add(credentials)

        # Guardar cambios        
        db.session.commit()
        
        return new_user

    # Login de usuario
    def login_user(self, email, password):

        # Verificar si el mail esta registrado como usuario
        user = self.user_repo.get_by_email(email)

        # Verificar que el usuario existe
        if not user or not user.credentials:
            raise ValueError("Email no valido")
        
        # Verificar contraseña
        if not bcrypt.verify(password, user.credentials.password_hash):
            raise ValueError("Contraseña incorrecta")
        
        # Crear claims
        identity = str(user.id)
        additional_claims = {
            'id' : user.id,
            'email' : user.email,
            'username' : user.username,
            'role' : user.credentials.role.name,
        }
        # Tiempo de expiracion: 24 horas 
        expiration = timedelta(hours=24)
        
        # Crear token de acceso
        token = create_access_token(
            identity=identity,
            additional_claims=additional_claims,
            expires_delta=expiration
        )
        return token