FFM_MESSAGE = "Vulcano File Format Exporter: "

import bpy
import bmesh
import os

def export_VulcanoFileFormatMesh(context):
    # Clear System Console
    os.system("cls")
    
    # Begin export
    print("\n==========================================================")
    print(FFM_MESSAGE, "Exporting mesh...")
    
    for object in bpy.data.objects:
        if "MESH" == object.type:
            mesh = object.data
            
            print("\n> Found object \"%s\"" % (object.name), "of type:", type(mesh))
            
            print("\n  Vertex coordinates:\n")
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
            
            # Convert the bmesh object's faces to triangles
            bmesh.ops.triangulate(bmesh_object, faces=bmesh_object.faces)
            
            print("\n> Converting to:", type(bmesh_object))
            print("\n  Vertex coordinates:\n")
            mesh = object.data
            for vertex in bmesh_object.verts:
                print("    {0:10f}, {1:10f}, {2:10f}"
                    .format(vertex.co.x, vertex.co.y, vertex.co.z))
            
            print("\n  Faces (indices):\n")
            for face in bmesh_object.faces:
                indices = "    "
                for vertex in face.verts:
                    indices += ("{0:4d},".format(vertex.index))
                print(indices[:-1])
                        
            bmesh_object.free()
                        