from models import db, Game, GameGenre
from repositories.game_repository import GameRepository
from repositories.genre_repository import GenreRepository

class GameService:
    
    # Repositorios
    def __init__(self):
        self.game_repo = GameRepository()
        self.genre_repo = GenreRepository()

    # Llamar al repositorio de juegos publicados
    def get_published_games(self):
        return self.game_repo.get_all_published()
    
    # Traer juegos por id
    def get_game_by_id(self, id):
        game = self.game_repo.get_by_id(id)
        # Devolver error si no se encuentra
        if not game:
            raise ValueError(f"Juego con id {id} no encontrado")
        return game

    # Postear un juego nuevo
    def create_game(self, data):
        # Crear juego
        new_game = Game(
            name=data['name'],
            price=data['price'],
            release_date=data['release_date'],
            thumbnail=data['thumbnail'],
            description=data['description'],
            developer_id=data['developer_id'],
            editor_id=data['editor_id'],
        )
        # Llamar repositorio para agregarlo a la base de datos
        self.game_repo.add(new_game)
        
        # Verificar si hay una lista de generos en los datos
        if 'genre_ids' in data:
            # Llamar repositorio para agregar los generos nuevos
            self._associate_genres(new_game, data['genre_ids'])
        
        # Guardar cambios
        db.session.commit()
        return new_game

    # Actualizar un juego
    def update_game(self, id, data):
        # Llamar repositorio para obtener juego
        game = self.get_game_by_id(id)

        # Actualizar campos simples
        if 'name' in data:
            game.name = data['name']
        if 'price' in data:
            game.price = data['price']
        if 'release_date' in data:
            game.release_date = data['release_date']
        if 'thumbnail' in data:
            game.thumbnail = data['thumbnail']
        if 'description' in data:
            game.description = data['description']
        if "is_free" in data:
            game.is_free = data['is_free']
        if 'developer_id' in data:
            game.developer_id = data['developer_id']
        if 'editor_id' in data:
            game.editor_id = data['editor_id']
        if 'is_published' in data:
            game.is_published = data['is_published']

        # Actualizar géneros
        if 'genre_ids' in data:
            # Llamar repositorio para borrar generos del juego
            self.game_repo.clear_genre_associations(id)
            # Llamar repositorio para agregar los generos nuevos
            self._associate_genres(game, data['genre_ids'])
        
        # Actualizar fecha y guardar cambios
        game.uploaded_at = db.func.now()
        db.session.commit()
        return game

    # Desactivar un juego
    def disable_game(self, id):
        # Llamar repositorio para verificar si existe el juego
        game = self.get_game_by_id(id) 
        game.is_published = False
        db.session.commit()
        # Mostrar mensaje
        return {"message": "Juego desactivado"}

    # Manejo de generos al postear o modificar un juego
    def _associate_genres(self, game, genre_ids):
        for genre_id in genre_ids:
            # Usamos el repo de generos
            genre = self.genre_repo.get_by_id(genre_id)
            
            # Solo asociar si el genero existe y está activo
            if genre and genre.is_active:
                new_association = GameGenre(genre=genre)
                game.genres.append(new_association)