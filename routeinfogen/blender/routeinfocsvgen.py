import bpy
import re
from ..csvgen.abstractcsvgen import AbstractCsvGen
from ..csvgen.routegen import RouteCsvGen
from ..csvgen.pointgen import PointCsvGen
from ..csvgen.utilities import isDefined

class RouteInfoCsvGen(bpy.types.Operator):
    """Generate boilerplate RouteInfo CSV files for NSMBW"""

    bl_idname = "routeinfo.generate"
    bl_label = "Generate boilerplate RouteInfo CSV files for NSMBW"

    type: bpy.props.EnumProperty(
        name="Type",
        description="The type to generate CSV for",
        items=(
            ('ALL', "All", ""),
            ('ROUTE', "Route", ""),
            ('POINT', "Point", ""),
        ),
        default='ALL'
    ) # pyright: ignore[reportInvalidTypeForm]

    filePath: bpy.props.StringProperty(
        name="File Path",
        description="The path to save the generated CSV file",
        default="//",
    ) # pyright: ignore[reportInvalidTypeForm]

    def execute(self, context: bpy.types.Context): # pyright: ignore[reportIncompatibleMethodOverride]
        armatureData = self.__getCsArmatures(context)
        if not armatureData:
            self.report({'WARNING'}, "No CS_Wx armatures found in the scene.")
            return {'CANCELLED'}

        classes: list[type[AbstractCsvGen]] = [RouteCsvGen, PointCsvGen]

        # Remove classes that don't match the selected type
        if self.type != 'ALL':
            if self.type != 'ROUTE':
                classes.remove(RouteCsvGen)
            if self.type != 'POINT':
                classes.remove(PointCsvGen)

        # Run each generator for each armature
        for cls in classes:
            op = cls(armatureData)
            successfulFiles = op.run()
            if len(successfulFiles) < len(armatureData):
                self.report({'WARNING'}, f"Generated {len(successfulFiles)} out of {len(armatureData)} files for {cls.__name__}.")
                continue
            for fileName in successfulFiles:
                self.report({'INFO'}, f"Successfully generated CSV file {fileName}")
        self.report({'INFO'}, "Finished generating CSV files.")

        return {'FINISHED'}

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        if not layout:
            return
        layout.use_property_split = True
        layout.prop(self, "type")
        layout.prop(self, "filePath")

    def __getCsArmatures(self, context: bpy.types.Context) -> list[bpy.types.Armature]:
        """Helper function to get all armature objects in the scene that match the naming pattern for `CS_Wxy`."""
        csArmatures: list[bpy.types.Object] = []
        csPattern = re.compile(r"^CS_W\d[ab]?$")

        for obj in context.scene.objects:
            if obj.type == 'ARMATURE' and csPattern.match(obj.name):
                csArmatures.append(obj)
        if not csArmatures:
            return []

        armatureData: list[bpy.types.Armature] = []
        for obj in csArmatures:
            if obj.data and isinstance(obj.data, bpy.types.Armature) and csPattern.match(obj.data.name):
                armatureData.append(obj.data)

        return armatureData

def drawOp(cls: bpy.types.Operator, context: bpy.types.Context):
    if not isDefined(cls.layout):
        return
    layout: bpy.types.UILayout = cls.layout
    layout.separator()
    layout.operator(RouteInfoCsvGen.bl_idname, text="Generate RouteInfo CSVs", icon="CURRENT_FILE")
