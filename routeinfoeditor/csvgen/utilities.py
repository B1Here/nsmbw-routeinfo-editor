import bpy
import re
from typing import TypeGuard, TypeVar

T = TypeVar('T')

def isDefined(obj: T | None) -> TypeGuard[T]:
    return obj is not None

def isLevelPoint(name: str) -> bool:
    return re.match(r"^W[1-9](?:S[0-1]|K[0-3]|[ACGTWX]0|0[1-9])$", name) is not None

def isFlagPoint(name: str) -> bool:
    return re.match(r"^F[0-9abcdkls][0-9C]{2}$", name) is not None

def isKeyPoint(name: str) -> bool:
    return re.match(r"^K[a0-9][0-9][0-9a-f]$", name) is not None

def isPoint(name: str) -> bool:
    return isLevelPoint(name) or isFlagPoint(name) or isKeyPoint(name)

def getModeSpecificBones(context: bpy.types.Context):
    if (context.object.mode == 'EDIT'):
        return context.armature.edit_bones
    if (context.object.mode == 'POSE'):
        return context.armature.pose.bones
    return context.armature.bones
