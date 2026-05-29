import bpy
import re
from routeinfogen.csvgen.utilities import isDefined

class RouteInfoRoutesList(bpy.types.UIList):
    bl_idname = "ROUTEINFO_ROUTE_UL_routes_list"

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index, flt_flag):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.name, icon='CON_TRACKTO')
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="")

class RouteInfoRouteDetailProperties(bpy.types.PropertyGroup):
    animation: bpy.props.EnumProperty(
        name="Animation",
        description="The animation this route should use",
        items=(
            ('ジャンプ', 'Jump', ''),
            ('道', 'Walk Grass', ''),
            ('砂', 'Walk Sand', ''),
            ('流砂', 'Walk Quicksand', ''),
            ('雪', 'Walk Snow', ''),
            ('氷', 'Walk Ice', ''),
            ('木', 'Walk Wood', ''),
            ('土', 'Walk Dirt', ''),
            ('坂', 'Snowy Slope', ''),
            ('氷坂', 'Icy Slope', ''),
            ('はしご', 'Metal Ladder', ''),
            ('はしご岩', 'Rock Ladder', ''),
            ('はしご縄', 'Rope Ladder', ''),
            ('はしご左', 'Metal Ladder (Left)', ''),
            ('はしご右', 'Metal Ladder (Right)', ''),
            ('ツタ', 'Vine', ''),
            ('スイッチブロック', '(UNUSED) Switch Block', ''),
            ('雲', '(UNUSED) Walk Cloud', ''),
            ('水', '(UNUSED) Walk Water', '')
        ),
        default="道",
        options=set()
    ) # pyright: ignore[reportInvalidTypeForm]
    flags: bpy.props.StringProperty(
        name="Flags",
        description="The flags for this route (comma-separated)",
        options=set()
    ) # pyright: ignore[reportInvalidTypeForm]

class RouteInfoRouteSettings(bpy.types.PropertyGroup):
    routes: bpy.props.CollectionProperty(type=RouteInfoRouteDetailProperties) # pyright: ignore[reportInvalidTypeForm]
    active_route_index: bpy.props.IntProperty() # pyright: ignore[reportInvalidTypeForm]

class RouteInfoRoutePanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_options = {'DEFAULT_CLOSED'}
    bl_idname = "ROUTEINFO_ROUTE_PT_armature_attrs"
    bl_label = "RouteInfo Route Data"
    bl_context = "data"

    @classmethod
    def poll(cls, context) -> bool:
        pattern = re.compile(r"^CS_W\d[ab]?$")
        if isDefined(context.object) and context.object.type == 'ARMATURE' and isDefined(context.armature):
            return (pattern.match(context.object.name) is not None
                and pattern.match(context.armature.name) is not None
                and context.armature.name == context.object.name)
        return False

    def draw(self, context):
        layout = self.layout
        if not isDefined(layout):
            return
        layout.use_property_split = True
        layout.use_property_decorate = False
        armature = context.armature
        if not isDefined(armature):
            return
        armatureSettings = armature.route_info_route_settings
        row = layout.row()
        row.template_list(RouteInfoRoutesList.bl_idname, "", armatureSettings, "routes", armatureSettings, "active_route_index")
        column = row.column(align=True)
        column.operator("routeinfo.move_route_up", icon='TRIA_UP', text="")
        column.operator("routeinfo.move_route_down", icon='TRIA_DOWN', text="")
        row = layout.row()
        row.operator("routeinfo.refresh_routes", icon='FILE_REFRESH')

        column = row.column()
        column.enabled = ['EDIT', 'POSE'].__contains__(context.active_object.mode)
        column.operator("routeinfo.route_select_bones", icon='GROUP_BONE')
        routeSettings = armature.route_info_route_settings
        index = routeSettings.active_route_index
        if index < 0 or index >= len(routeSettings.routes):
            return
        routeDetails = routeSettings.routes[index]
        layout.prop(routeDetails, "animation")
        layout.prop(routeDetails, "flags")
