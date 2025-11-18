from models import db, Review

class ReviewRepository:
    
    # Obtener todas las reviews de un juego por su id
    def get_by_game_id(self, game_id):    
        return Review.query.filter_by(game_id=game_id).all()

    # Obtiene una review por su id
    def get_by_id(self, review_id):
        return Review.query.get(review_id)

    # Verificar si ya existe una review del usuario para ese juego.
    def find_by_user_and_game(self, user_id, game_id):
        return Review.query.filter_by(user_id=user_id, game_id=game_id).first()

    # Agrega una nueva review a la base de datos
    def add(self, review):
        db.session.add(review)

    # Obtener cantidad de reviews
    def count_all(self):
        return Review.query.count()