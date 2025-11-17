from models import db, Game, GameGenre

class GameRepository:
    
    # Obtener todos los juegos que están marcados como 'published'.
    def get_all_published(self):
        return Game.query.filter_by(is_published=True).all()

    # Obtener juego por id
    def get_by_id(self, id):
        return Game.query.get(id)
    
    # Agregar juego a la base de datos
    def add(self, game):
        db.session.add(game)
    
    # Eliminar generos de un juego en la tabla 'genre_game'
    def clear_genre_associations(self, game_id):
        db.session.execute(
            db.delete(GameGenre).where(GameGenre.game_id == game_id)
        )