from models import db, User
from repositories.user_repository import UserRepository

class UserService:
    
    def __init__(self):
        self.user_repo = UserRepository()

    # Obtener lista de todos los usuarios activos.
    def get_active_users(self):
        return self.user_repo.get_all_active()

    # Obtener usuario por id
    def get_user_by_id(self, id):
        user = self.user_repo.get_by_id(id)
        # Mandar error si no lo encuentra
        if not user:
            raise ValueError(f"Usuario con id {id} no encontrado")
        return user

    # Actualizar usuario
    def update_user(self, id, data):
        # Obtener el usuario 
        user = self.get_user_by_id(id)

        # Validar email nuevo
        if 'email' in data and data['email'] != user.email:
            # Verificar si el email ya existe en la base de datos
            if self.user_repo.get_by_email(data['email']):
                # Mandar error si ya existe
                raise ValueError(f"El email '{data['email']}' ya está en uso")
            user.email = data['email']
        
        # Actualizar nombre de usuario
        if 'username' in data:
            user.username = data['username']
            
        # Actualizar fecha y guardar cambios
        user.updated_at = db.func.now()
        db.session.commit()
        return user

    # Desactivar usuario 
    def disable_user(self, id):
        # Obtener usuario 
        user = self.get_user_by_id(id)
        
        # Desactivar y mostrar mensaje
        user.is_active = False
        db.session.commit()
        return {"message": "Usuario desactivado"}