from models import db, UserGame

class UserGameRepository:
    
    # Obtener todos los juegos de la biblioteca de un usuario por su id
    def get_by_user_id(self, user_id):
        return UserGame.query.filter_by(user_id=user_id).all()

    # Verificar que no se agregue un mismo juego 2 veces
    def find_by_user_and_game(self, user_id, game_id):
        return UserGame.query.filter_by(user_id=user_id, game_id=game_id).first()

    # Agregar juego a la biblioteca del usuario
    def add(self, user_game):
        db.session.add(user_game)