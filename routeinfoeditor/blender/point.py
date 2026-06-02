import bpy

from routeinfoeditor.blender.armatureutils import __get_bone__
from routeinfoeditor.blender.common import __is_defined__
from routeinfoeditor.nsmbw.routeinfoutils import (
    __is_flag_point__,
    __is_level_point__,
)


class RouteInfoPointSettings(bpy.types.PropertyGroup):
    flags: bpy.props.StringProperty(
        name="Flags",
        description="Flags this point should have (comma-separated)",
        default="",
        options=set(),
    )

    unlocked_levels: bpy.props.StringProperty(
        name="Unlocked Levels",
        description="Levels this level unlocks (comma-separated)",
        default="",
        options=set(),
    )

    unlocked_bones: bpy.props.StringProperty(
        name="Unlocked Bones",
        description="Bones this level unlocks (comma-separated)",
        default="",
        options=set(),
    )

    unlocked_levels_secret_exit: bpy.props.StringProperty(
        name="Unlocked Levels",
        description="Secret levels this level unlocks (comma-separated)",
        default="",
        options=set(),
    )

    unlocked_bones_secret_exit: bpy.props.StringProperty(
        name="Unlocked Bones",
        description="Secret bones this level unlocks (comma-separated)",
        default="",
        options=set(),
    )


class RouteInfoPointPanel(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "ROUTEINFO_POINT_PT_bone_attrs"
    bl_label = "RouteInfo Point Data"
    bl_context = "bone"

    @classmethod
    def poll(cls, context) -> bool:
        bone = __get_bone__(context)
        if not __is_defined__(bone):
            return False

        return __is_level_point__(bone.name) or __is_flag_point__(bone.name)

    def draw(self, context) -> None:
        layout = self.layout
        if not __is_defined__(layout):
            return

        bone = __get_bone__(context)
        if not __is_defined__(bone):
            return

        layout.use_property_split = True
        layout.use_property_decorate = False

        point_settings = bone.route_info_point_settings
        layout.prop(bone, "name")
        layout.prop(point_settings, "flags")
        if __is_level_point__(bone.name):
            layout.prop(point_settings, "unlocked_levels")
            layout.prop(point_settings, "unlocked_bones")


class RouteInfoPointSecretPanel(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "ROUTEINFO_POINT_PT_bone_secret_attrs"
    bl_label = "Secret Exit"
    bl_parent_id = "ROUTEINFO_POINT_PT_bone_attrs"
    bl_context = "bone"

    @classmethod
    def poll(cls, context) -> bool:
        bone = __get_bone__(context)
        if not __is_defined__(bone):
            return False

        return __is_level_point__(bone.name)

    def draw(self, context) -> None:
        layout = self.layout
        if not __is_defined__(layout):
            return

        bone = __get_bone__(context)
        if not __is_defined__(bone):
            return

        layout.use_property_split = True
        layout.use_property_decorate = False

        point_settings = bone.route_info_point_settings
        layout.prop(point_settings, "unlocked_levels_secret_exit")
        layout.prop(point_settings, "unlocked_bones_secret_exit")
