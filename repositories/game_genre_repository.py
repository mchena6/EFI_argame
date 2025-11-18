from models import GameGenre

class GameGenreRepository:

    # Obtener juegos a partir de un id de genero
    def get_by_genre_id(self, genre_id):
        return GameGenre.query.filter_by(genre_id=genre_id).all()