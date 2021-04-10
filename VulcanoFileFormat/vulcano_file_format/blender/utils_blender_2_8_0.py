class ModifierManager:
    def __init__(self):
        self.mesh_owner = None

    def apply_modifiers(self, object, context, operator):
        depsgraph = context.evaluated_depsgraph_get()
        self.mesh_owner = object.evaluated_get(depsgraph)
        return self.mesh_owner.to_mesh()

    def clear_mesh(self):
        self.mesh_owner.to_mesh_clear()
