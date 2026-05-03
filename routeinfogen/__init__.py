import bpy
from .blender import routeinfocsvgen

bl_info = {
    "name": "RouteInfo CSV Generator",
    "author": "B1Here",
    "blender": (3, 3, 0),
    "version": (1, 0, 1),
    "category": "Import-Export",
    "description": "Generate boilerplate RouteInfo CSV files for NSMBW",
    "location": "3D Viewport > Object > Generate RouteInfo CSVs",
}

def register():
    bpy.utils.register_class(routeinfocsvgen.RouteInfoCsvGen)
    bpy.types.VIEW3D_MT_object.append(routeinfocsvgen.drawOp)

def unregister():
    bpy.types.VIEW3D_MT_object.remove(routeinfocsvgen.drawOp)
    bpy.utils.unregister_class(routeinfocsvgen.RouteInfoCsvGen)

if __name__ == "__main__":
    register()
