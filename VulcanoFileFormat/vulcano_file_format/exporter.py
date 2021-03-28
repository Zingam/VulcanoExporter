FFM_MESSAGE = "Vulcano File Format Exporter:\n    "

# This is required to support reloading of modules in Blender with F8
if "bpy" in locals():
    import importlib
    importlib.reload(utils)
else:
    from .blender import utils

import bmesh
import bpy
import os

def printCollectionObjects(collection, tabSpace):
    for collection in collection.children:
        collectionMessage = "    > Collection:  {}".format(collection.name)
        # Add white space to the front of the string
        collectionMessageLength = len(collectionMessage) + tabSpace
        outputMessage = collectionMessage.rjust(collectionMessageLength)
        print(outputMessage)
        
        for object in collection.objects:
            collectionMessage = "      - {:10}: {}".format(object.type, object.name)
            # Add white space to the front of the string
            collectionMessageLength = len(collectionMessage) + tabSpace
            outputMessage = collectionMessage.rjust(collectionMessageLength)
            print(outputMessage)
            
        printCollectionObjects(collection, tabSpace + 2)

def print_object_info(object: bpy.types.Object):
    print("  > Found object \"{0}\" of type {1}"
        .format(object.name, object.type))
    location= object.location
    print("    at location: {0:10f}, {1:10f}, {2:10f}"
            .format(location.x, location.y, location.z))

    if object.data is not None:
        print("    of type: {0}".format(type(object.data)))

def export_VulcanoFileFormatMesh(operator, context):       
    if True == operator.clear_system_console:
        # Clear System Console
        os.system("cls")

        import sys
        print("Python version: {}".format(sys.version))
        print("       info:    {}".format(sys.version_info))
    
    # Begin export
    print("\n")
    print("====================================================================")
    
    export_utils = utils.get_utils()
    if None == export_utils:
        errorMessage = "Export failed: " + utils.get_last_error()
        operator.report({'ERROR'}, errorMessage)
        print(FFM_MESSAGE, errorMessage)
        print("====================================================================")
        return
    modifierManager = export_utils.ModifierManager()

    print(FFM_MESSAGE, "Exporting mesh...")
    print("\n") 
    
    
    # print("operator.exported_file_type", 
        # operator.exported_file_type, 
        # type(operator.exported_file_type))
    # print("operator.path_mode", 
        # operator.path_mode, 
        # type(operator.path_mode))
    # print("operator.use_selection", 
        # operator.use_selection, 
        # type(operator.use_selection))
    # print("operator.apply_modifiers", 
        # operator.apply_modifiers, 
        # type(operator.apply_modifiers))


    # Enumerate the collections in the scene's master collection
    print("  Collections:")
    print("    > Collection:  ", context.scene.collection.name) 
    printCollectionObjects(context.scene.collection, 2)
    
    # Enumerate the objects in the scene
    print("\n")
    for object in context.scene.objects:
        if "MESH" == object.type:           
            if True == operator.apply_modifiers:
                # Create a temporary mesh with applied modifiers
                mesh = modifierManager.apply_modifiers(object, context, operator)
            else:
                mesh = object.data
            
            # Print mesh data
            print("  ----------------------------------------------------------")

            print_object_info(object)
            
            print("\n    Vertex coordinates:\n")
            for vertex in mesh.vertices:
                print("    {0:10f}, {1:10f}, {2:10f}"
                    .format(vertex.co.x, vertex.co.y, vertex.co.z))
            
            print("\n  Faces (indices):\n")
            for polygon in mesh.polygons:
                indices = "    "
                vertices = polygon.vertices
                for index in polygon.vertices:
                    indices += ("{0:4d},".format(index))
                print(indices[:-1])
                    
            # Create a bmesh object from the mesh object
            bmesh_object = bmesh.new()
            bmesh_object.from_mesh(mesh)
            
            # Remove the temporary mesh with applied modifiers
            if True == operator.apply_modifiers:
                modifierManager.clear_mesh()
            
            # Convert the bmesh object's faces to triangles
            bmesh.ops.triangulate(bmesh_object, faces=bmesh_object.faces)
            
            print("\n  > Converting to:", type(bmesh_object))
            print("\n    Vertex coordinates:\n")
            mesh = object.data
            for vertex in bmesh_object.verts:
                print("    {0:10f}, {1:10f}, {2:10f}"
                    .format(vertex.co.x, vertex.co.y, vertex.co.z))
            
            print("\n    Faces (indices):\n")
            for face in bmesh_object.faces:
                indices = "    "
                for vertex in face.verts:
                    indices += ("{0:4d},".format(vertex.index))
                print(indices[:-1])
                        
            bmesh_object.free()
            
            print("  ----------------------------------------------------------")

        if "EMPTY" == object.type:
            print("  ----------------------------------------------------------")

            print_object_info(object)

            print("  ----------------------------------------------------------")
    
    print("\n")
    print("Mesh successfully exported to file:\n    ", operator.filepath)
    print("====================================================================")
