from repositories.role_repository import RoleRepository

class RoleService:
    def __init__(self):
        self.repo = RoleRepository()

    # Obtener todos los roles
    def get_all_roles(self):
        return self.repo.get_all()