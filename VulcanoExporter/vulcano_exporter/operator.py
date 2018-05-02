import bpy
import bpy_extras

class VulcanoExporter(
    bpy.types.Operator,
    bpy_extras.io_utils.ExportHelper):
    """Exports current scene to Vulcano File Format (.vmsh)"""
    
    bl_idname = "vulcano_exporter.vmsh"
    bl_label = "Vulcano File (.vmsh)"
    
    ############################################################################
    # Operator properties
    ############################################################################
    
    filename = bpy.props.StringProperty(subtype="FILE_NAME")
    filename_ext = ".vmsh"
    filepath = bpy.props.StringProperty(subtype="FILE_PATH")
    
    # File filter
    filter_glob = bpy.props.StringProperty(
        default="*.vmsh",
        options={"HIDDEN"})
    
    # Export options
    exported_file_type = bpy.props.EnumProperty(
        items=(("EXPORT_FORMAT_BINARY", "Binary",
                "Exports Vulcano File (.vmsh) in binary format"),
               ("EXPORT_FORMAT_ASCII", "ASCII",
                "Exports Vulcano File (.vmsh) in ASCII text format")),
        name="Format type",
        description="Select the exported file format type")
    
    use_selection = bpy.props.BoolProperty(
        name="Selection Only",
        description="Export selected objects only",
        default=True)
    
    ############################################################################
    # Methods
    ############################################################################
    
    def draw(self, context):
        """
        Draw the layout manually. Without this method the UI methods will be
        placed in the layout automatically.
        """ 
        # Draw a box and put the UI elements inside
        box = self.layout.box()
        box.prop(self, "exported_file_type")
        box.prop(self, "use_selection")
    
    def execute(self, context):
        from . import exporter
        exporter.export_VulcanoFileFormatMesh(context)
        
        return {"FINISHED"}
    
    def invoke(self, context, event):
        """
        Initialize the operator from the context at the moment the operator
        is called. invoke() is typically used to assign properties which are then 
        used by execute().
        """
        # Open the File Selection dialog
        context.window_manager.fileselect_add(self)
        
        return {"RUNNING_MODAL"}

    ############################################################################
    # Class methods
    ############################################################################
        
    @classmethod
    def poll(cls, context):
        
        return context.active_object is not None
    