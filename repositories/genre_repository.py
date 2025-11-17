from models import db, Genre

class GenreRepository:
    # Obtener genero por id
    def get_by_id(self, id):
        return Genre.query.get(id)