from models import db, Genre

class GenreRepository:
    
    # Obtener genero por id
    def get_by_id(self, id):
        return Genre.query.get(id)
    
    # Buscar genero por nombre
    def get_by_name(self, name):
        return Genre.query.filter_by(name=name).first()

    def get_all_active(self):
    # Obtener una lista de todos los generos activos
        return Genre.query.filter_by(is_active=True).all()
    
    # Agrega un nuevo género a la sesión.
    def add(self, genre):
        db.session.add(genre)