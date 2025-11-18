from models import Role

class RoleRepository:

    # Obtener todos los roles
    def get_all(self):
        return Role.query.all()