import bpy

from routeinfoeditor.blender.common import __is_defined__


def __get_bone__(
    context: bpy.types.Context,
) -> bpy.types.EditBone | bpy.types.Bone | bpy.types.PoseBone | None:
    if not __is_defined__(context.object):
        return context.bone

    if context.object.mode == "EDIT":
        return context.active_bone
    if context.object.mode == "POSE":
        return context.active_pose_bone
    return context.active_bone


def __get_bones__(
    context: bpy.types.Context,
) -> (
    bpy.types.ArmatureBones
    | bpy.types.ArmatureEditBones
    # | bpy.types.ArmaturePoseBones if that would exist. "bpy.types.bpy_prop_collection[bpy.types.PoseBone]" does not work even though that's what Blender itself uses.
    | list
):
    if not __is_defined__(context.object) or not __is_defined__(context.armature):
        return list()

    if context.object.mode == "EDIT":
        return context.armature.edit_bones
    if context.object.mode == "POSE":
        return context.armature.pose.bones
    return context.armature.bones
