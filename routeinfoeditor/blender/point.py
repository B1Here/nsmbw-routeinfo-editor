import bpy

from ..csvgen.utilities import isDefined, isFlagPoint, isLevelPoint


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
            return isLevelPoint(bone.name) or isFlagPoint(bone.name)
        return False

    def draw(self, context):
        layout = self.layout
        if not isDefined(layout):
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
        if not isDefined(bone):
            return
        boneSettings = bone.route_info_point_settings
        layout.prop(bone, "name")
        layout.prop(boneSettings, "flags")
        if isLevelPoint(bone.name):
            layout.prop(boneSettings, "unlocked_levels")
            layout.prop(boneSettings, "unlocked_bones")


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
            return isLevelPoint(bone.name)
        return False

    def draw(self, context):
        layout = self.layout
        if not isDefined(layout):
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
        if not isDefined(bone):
            return
        layout.use_property_split = True
        layout.use_property_decorate = False
        boneSettings = bone.route_info_point_settings
        layout.prop(boneSettings, "unlocked_levels_secret_exit")
        layout.prop(boneSettings, "unlocked_bones_secret_exit")
