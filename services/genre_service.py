from models import db, Genre
from repositories.genre_repository import GenreRepository

class GenreService:
    
    def __init__(self):
        self.genre_repo = GenreRepository()

    # Obtener todos los generos activos
    def get_active_genres(self):
        return self.genre_repo.get_all_active()

    # Obtener genero por id
    def get_genre_by_id(self, id):
        genre = self.genre_repo.get_by_id(id)
        # Manejar error si no se encuentra
        if not genre:
            raise ValueError("Género no encontrado")
        return genre

    # Agregar nuevo genero
    def create_genre(self, data):
        # Crear nuevo genero.
        # Verificar duplicados (por nombre)
        if self.genre_repo.get_by_name(data['name']):
            raise ValueError(f"El género '{data['name']}' ya existe")

        # Crear genero
        new_genre = Genre(
            name=data['name']
        )
        
        # Agregar a la base de datos y guardar cambios
        self.genre_repo.add(new_genre)
        db.session.commit()
        return new_genre

    # Actualizar un genero
    def update_genre(self, id, data):
        
        # Obtener genero
        genre = self.get_genre_by_id(id)
        
        # Verificar que no se intente agregar un nombre duplicado
        if 'name' in data and data['name'] != genre.name:
            if self.genre_repo.get_by_name(data['name']):
                raise ValueError(f"El género '{data['name']}' ya existe")
            genre.name = data['name']
            
        # Guardar cambios
        db.session.commit()
        return genre

    # Desactivar genero 
    def disable_genre(self, id):
        # Obtener el genero
        genre = self.get_genre_by_id(id)
        
        # Desactivar genero
        genre.is_active = False
        db.session.commit()
        return {"message": "Genero desactivado"}