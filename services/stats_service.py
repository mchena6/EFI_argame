from repositories.user_repository import UserRepository
from repositories.game_repository import GameRepository
from repositories.review_repository import ReviewRepository

class StatsService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.game_repo = GameRepository()
        self.review_repo = ReviewRepository()

    def get_stats(self):
        # Totales 
        total_users = self.user_repo.count_all()
        total_games = self.game_repo.count_all()
        total_reviews = self.review_repo.count_all()
        posts_last_week = self.game_repo.count_recent(days=7)
        
        return {
            "total_users": total_users,
            "total_games": total_games,
            "total_reviews": total_reviews,
            "posts_last_week": posts_last_week
        }