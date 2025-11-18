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

    # Obtener cantidad de juegos
    def count_all(self):
        return Game.query.count()

    # Obtener cantidad de juegos posteados en la ultima semana
    def count_recent(self, days=7):
        return Game.query.filter(
            Game.uploaded_at >= db.func.now() - db.text(f'INTERVAL {days} DAY')
        ).count()