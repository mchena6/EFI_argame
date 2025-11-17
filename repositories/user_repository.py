from models import db, User

class UserRepository:
    
    # Buscar usuario por su email
    def get_by_email(self, email):
        return User.query.filter_by(email=email).first()

    # Agrega un nuevo usuario a la base de datos
    def add(self, user):
        db.session.add(user)
