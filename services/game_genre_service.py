from repositories.game_genre_repository import GameGenreRepository
from repositories.genre_repository import GenreRepository

class GameGenreService:
    def __init__(self):
        self.game_genre_repo = GameGenreRepository()
        self.genre_repo = GenreRepository() 

    # Obtener juegos por genero
    def get_games_for_genre(self, genre_id):
        # Verificar que existe el genero
        genre = self.genre_repo.get_by_id(genre_id)
        # Mandar error si no lo encuentra
        if not genre:
            raise ValueError(f"Género con id {genre_id} no encontrado")
        
        return self.game_genre_repo.get_by_genre_id(genre_id)