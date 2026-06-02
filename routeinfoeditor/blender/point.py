import bpy

from routeinfoeditor.csvgen.utilities import __is_defined__, __is_flag_point__, __is_level_point__


class RouteInfoPointSettings(bpy.types.PropertyGroup):
    flags: bpy.props.StringProperty(
        name="Flags",
        description="Flags this point should have (comma-separated)",
        default="",
        options=set(),
    )  # pyright: ignore[reportInvalidTypeForm]

    unlocked_levels: bpy.props.StringProperty(
        name="Unlocked Levels",
        description="Levels this level unlocks (comma-separated)",
        default="",
        options=set(),
    )  # pyright: ignore[reportInvalidTypeForm]

    unlocked_bones: bpy.props.StringProperty(
        name="Unlocked Bones",
        description="Bones this level unlocks (comma-separated)",
        default="",
        options=set(),
    )  # pyright: ignore[reportInvalidTypeForm]

    unlocked_levels_secret_exit: bpy.props.StringProperty(
        name="Unlocked Levels",
        description="Secret levels this level unlocks (comma-separated)",
        default="",
        options=set(),
    )  # pyright: ignore[reportInvalidTypeForm]

    unlocked_bones_secret_exit: bpy.props.StringProperty(
        name="Unlocked Bones",
        description="Secret bones this level unlocks (comma-separated)",
        default="",
        options=set(),
    )  # pyright: ignore[reportInvalidTypeForm]


class RouteInfoPointPanel(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "ROUTEINFO_POINT_PT_bone_attrs"
    bl_label = "RouteInfo Point Data"
    bl_context = "bone"

    @classmethod
    def poll(cls, context) -> bool:
        bone = context.bone if context.bone else context.edit_bone
        if bone:
            return __is_level_point__(bone.name) or __is_flag_point__(bone.name)
        return False

    def draw(self, context):
        layout = self.layout
        if not __is_defined__(layout):
            return
        layout.use_property_split = True
        layout.use_property_decorate = False
        bones = (
            context.armature.edit_bones
            if context.object.mode == "EDIT"
            else context.armature.bones
        )

        bone = (
            bones[context.edit_bone.name]
            if context.object.mode == "EDIT"
            else bones[context.bone.name]
        )
        if not __is_defined__(bone):
            return
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
        bone = context.bone if context.bone else context.edit_bone
        if bone:
            return __is_level_point__(bone.name)
        return False

    def draw(self, context):
        layout = self.layout
        if not __is_defined__(layout):
            return
        layout.use_property_split = True
        layout.use_property_decorate = False
        bones = (
            context.armature.edit_bones
            if context.object.mode == "EDIT"
            else context.armature.bones
        )

        bone = (
            bones[context.edit_bone.name]
            if context.object.mode == "EDIT"
            else bones[context.bone.name]
        )
        if not __is_defined__(bone):
            return
        layout.use_property_split = True
        layout.use_property_decorate = False
        point_settings = bone.route_info_point_settings
        layout.prop(point_settings, "unlocked_levels_secret_exit")
        layout.prop(point_settings, "unlocked_bones_secret_exit")
