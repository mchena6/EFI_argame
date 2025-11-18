from repositories.developer_repository import DeveloperRepository

class DeveloperService:
    def __init__(self):
        self.repo = DeveloperRepository()

    # Obtener todos los desarrolladores
    def get_all_developers(self):
        return self.repo.get_all()
    
    # Obtener desarrollador por id
    def get_developer_by_id(self, id):
        developer = self.repo.get_by_id(id)
        # Manejar error si no lo encuentra
        if not developer:
            raise ValueError(f"Desarrollador no encontrado")
        return developer