from models import db, Developer

class DeveloperRepository:

    # Obtener todos los desarrolladores
    def get_all_developers(self):
        return Developer.query.all()
    
    # Obtener desarrollador por id
    def get_developer_by_id(self, id):
        return Developer.query.get_or_404(id)
