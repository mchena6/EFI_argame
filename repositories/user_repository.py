from models import db, User

class UserRepository:
    
    # Buscar usuario por su email
    def get_by_email(self, email):
        return User.query.filter_by(email=email).first()

    # Agrega un nuevo usuario a la base de datos
    def add(self, user):
        db.session.add(user)
    
    # Obtener todos los usuarios que están activos
    def get_all_active(self):
        return User.query.filter_by(is_active=True).all()
    
    # Obtener usuario por id
    def get_by_id(self, id):
        return User.query.get(id)
    
    # Obtener cantidad de usuarios
    def count_all(self):
        return User.query.count()
