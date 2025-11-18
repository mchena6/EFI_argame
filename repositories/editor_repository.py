from models import Editor

class EditorRepository:

    # Obtener todos los editores
    def get_all(self):
        return Editor.query.all()
    
    # Obtener editor por id
    def get_by_id(self, id):
        return Editor.query.get(id)