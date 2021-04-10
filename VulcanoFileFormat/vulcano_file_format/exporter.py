FFM_MESSAGE = "Vulcano File Format Exporter:\n    "

# This is required to support reloading of modules in Blender with F8
if "bpy" in locals():
    import importlib
    importlib.reload(utils)
else:
    from .blender import utils

import os  # noqa
import bpy  # noqa
import bmesh  # noqa


def print_bl_collection_objects(bl_collection: bpy.types.Collection, tab_space: int):
    for bl_collection in bl_collection.children:
        collection_message = "    > Collection:  {}".format(bl_collection.name)
        # Add white space to the front of the string
        collection_message_length = len(collection_message) + tab_space
        output_message = collection_message.rjust(collection_message_length)
        print(output_message)

        for bl_object in bl_collection.objects:
            collection_message = "      - {:10}: {}".format(
                bl_object.type, bl_object.name)
            # Add white space to the front of the string
            collection_message_length = len(collection_message) + tab_space
            output_message = collection_message.rjust(
                collection_message_length)
            print(output_message)

        print_bl_collection_objects(bl_collection, tab_space + 2)


def print_object_info(bl_object: bpy.types.Object):
    print("  > Found object \"{0}\" of type {1}"
          .format(bl_object.name, bl_object.type))
    location = bl_object.location
    print("    at location: {0:10f}, {1:10f}, {2:10f}"
          .format(location.x, location.y, location.z))

    if bl_object.data is not None:
        print("    of type: {0}".format(type(bl_object.data)))


def export_vffmsh(operator, context):
    if operator.clear_system_console:
        # Clear System Console
        os.system("cls")

        print("Blender version: {}\n".format(bpy.app.version_string))

        import sys  # noqa
        print("Python version:  {}".format(sys.version))
        print("       info:     {}".format(sys.version_info))

    # Begin export
    print("\n")
    print("====================================================================")

    export_utils = utils.get_utils()
    if export_utils is None:
        error_message = "Export failed: " + utils.get_last_error()
        operator.report({'ERROR'}, error_message)
        print(FFM_MESSAGE, error_message)
        print("====================================================================")

        return

    modifier_manager = export_utils.ModifierManager()

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
    print_bl_collection_objects(context.scene.collection, 2)

    # Enumerate the objects in the scene
    print("\n")
    for bl_object in context.scene.objects:
        if bl_object.type == "MESH":
            if operator.apply_modifiers:
                # Create a temporary mesh with applied modifiers
                mesh = modifier_manager.apply_modifiers(
                    bl_object, context, operator)
            else:
                mesh = bl_object.data

            # Print mesh data
            print("  ----------------------------------------------------------")

            print_object_info(bl_object)

            print("\n    Vertex coordinates:\n")
            for vertex in mesh.vertices:
                print("    {0:10f}, {1:10f}, {2:10f}"
                      .format(vertex.co.x, vertex.co.y, vertex.co.z))

            print("\n  Faces (indices):\n")
            for polygon in mesh.polygons:
                indices = "    "
                for index in polygon.vertices:
                    indices += ("{0:4d},".format(index))
                print(indices[:-1])

            # Create a bmesh object from the mesh object
            bmesh_object = bmesh.new()
            bmesh_object.from_mesh(mesh)

            # Remove the temporary mesh with applied modifiers
            if operator.apply_modifiers:
                modifier_manager.clear_mesh()

            # Convert the bmesh object's faces to triangles
            bmesh.ops.triangulate(bmesh_object, faces=bmesh_object.faces)

            print("\n  > Converting to:", type(bmesh_object))
            print("\n    Vertex coordinates:\n")
            mesh = bl_object.data
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

        if bl_object.type == "EMPTY":
            print("  ----------------------------------------------------------")

            print_object_info(bl_object)

            print("  ----------------------------------------------------------")

    print("\n")
    print("Mesh successfully exported to file:\n    ", operator.filepath)
    print("====================================================================")
