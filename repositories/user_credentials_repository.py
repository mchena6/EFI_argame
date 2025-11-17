from models import db

class UserCredentialsRepository:
    
    # Agrega nuevas credenciales a la sesión de la base de datos
    def add(self, credentials):
        db.session.add(credentials)
