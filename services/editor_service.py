from repositories.editor_repository import EditorRepository

class EditorService:

    def __init__(self):
        self.repo = EditorRepository()

    # Obtener todos los editores
    def get_all_editors(self):
        return self.repo.get_all()
    
    # Obtener editor por id
    def get_editor_by_id(self, id):
        editor = self.repo.get_by_id(id)
        # Manejar error si no lo encuentra
        if not editor:
            raise ValueError(f"Editor no encontrado")
        return editor