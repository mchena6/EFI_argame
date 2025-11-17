from models import db, Review
from repositories.review_repository import ReviewRepository

class ReviewService:
    
    def __init__(self):
        self.review_repo = ReviewRepository()

    # Obtener la lista de reviews para un juego
    def get_reviews_for_game(self, game_id):
        return self.review_repo.get_by_game_id(game_id)

    # Obtener una review por id
    def get_review_by_id(self, review_id):
        review = self.review_repo.get_by_id(review_id)
        # Mandar error si no se encuentra
        if not review:
            raise ValueError(f"Review no encontrada")
        return review

    # Agregar nueva review
    def add_review(self, game_id, user_id, data):
        
        # Verificar si el usuario ya hizo una review en un juego especifico
        existing = self.review_repo.find_by_user_and_game(user_id, game_id)
        # Mandar error 
        if existing:
            raise ValueError("Ya has enviado una review para este juego")

        # Crear review
        new_review = Review(
            user_id=user_id,
            game_id=game_id,
            rating=data['rating'],
            text_review=data.get('text_review') 
        )
        
        # LLamar repositorio para guardar en la base de datos
        self.review_repo.add(new_review)
        db.session.commit()
        return new_review

    # Desactiva una review
    def disable_review(self, review_id):
        # Obtener review
        review = self.get_review_by_id(review_id)
        # Desactivar review y guardar cambios
        review.is_visible = False
        db.session.commit()
        
        return {"message": "Review desactivada"}