from models import db, UserGame
from repositories.user_game_repository import UserGameRepository

class UserGameService:
    
    def __init__(self):
        self.user_game_repo = UserGameRepository()

    # Obtener biblioteca de usuario
    def get_games_for_user(self, user_id):
        # Llamar repositorio para traer los juegos del usuario
        return self.user_game_repo.get_by_user_id(user_id)

    # Agregar juego a la biblioteca del usuario
    def add_game_to_user(self, user_id, game_id, current_user_id):

        # Llamar repositorio para verificar si el juego ya está en la biblioteca
        existing_entry = self.user_game_repo.find_by_user_and_game(user_id, game_id)
        if existing_entry:
            raise ValueError("El usuario ya tiene este juego en su biblioteca")
            
        # Crear registro de juego en biblioteca 
        new_user_game = UserGame(
            user_id=user_id,
            game_id=game_id,
            claimed_at=db.func.now()         )
        
        # Llamar repositorio para agregar el juego a la biblioteca 
        self.user_game_repo.add(new_user_game)
        # Guardar cambios
        db.session.commit()
        
        return new_user_game