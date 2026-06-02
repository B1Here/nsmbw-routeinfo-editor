import bpy
import re
from typing import TypeGuard, TypeVar

T = TypeVar("T")


def __is_defined__(obj: T | None) -> TypeGuard[T]:
    return obj is not None


def __is_level_point__(name: str) -> bool:
    return re.match(r"^W[1-9](?:S[0-1]|K[0-3]|[ACGTWX]0|0[1-9])$", name) is not None


def __is_flag_point__(name: str) -> bool:
    return re.match(r"^F[0-9abcdkls][0-9C]{2}$", name) is not None


def __is_key_point__(name: str) -> bool:
    return re.match(r"^K[a0-9][0-9][0-9a-f]$", name) is not None


def __is_point__(name: str) -> bool:
    return __is_level_point__(name) or __is_flag_point__(name) or __is_key_point__(name)


def __get_bones__(context: bpy.types.Context):
    if context.object.mode == "EDIT":
        return context.armature.edit_bones
    if context.object.mode == "POSE":
        return context.armature.pose.bones
    return context.armature.bones
