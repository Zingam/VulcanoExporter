import bpy

from . import exporter


class VulcanoExporter(bpy.types.Operator):
    """Exports current scene to Vulcano File Format (.vmsh)"""
    bl_idname = "object.vulcano_exporter"
    bl_label = "Exports Vulcano File (.vmsh)"
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        exporter.export_VulcanoFileFormatMesh(context)
        return {"FINISHED"}
    