import bpy

class ModifierManager:
    def __init__(self):
        self.mesh = None

    def apply_modifiers(self, object, context, operator):
        self.mesh = object.to_mesh(context.scene,
                operator.apply_modifiers, "PREVIEW")
        return self.mesh

    def clear_mesh(self)
        bpy.data.meshes.remove(self.mesh)
