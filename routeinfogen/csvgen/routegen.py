import bpy
import re
from .abstractcsvgen import AbstractCsvGen

class RouteCsvGen(AbstractCsvGen):

    def _fetchNames(self, index: int) -> list[str]:
        routeBones: list[bpy.types.Bone] = []
        for bone in self._armatures[index].bones:
            if re.compile(r"R(?:[FKW][a-zA-Z0-9]{3}){2}").match(bone.name):
                routeBones.append(bone)

        result: list[str] = []
        for bone in routeBones:
            self.__addRouteForBone(bone, result)

        return result

    def _createCsvText(self, names: list[str], index: int) -> str:
        csv = ""
        routeAnimation = self._config.get("routeAnimation", "道") # Default to "Walk Grass"
        for name in names:
            csv += f"{name},{routeAnimation},\r\n"

        return csv

    def _getFileName(self, world: str) -> str:
        return f"routeW{world}.csv"

    def __addRouteForBone(self, bone: bpy.types.Bone, routeNames: list[str]):
        if bone.children and filter(lambda child: re.compile(r"[FKW][a-zA-Z0-9]{3}").match(child.name), bone.children):
            self.__addRouteViaChild(bone, routeNames)
            return
        routeNames.append(bone.name)

    def __addRouteViaChild(self, bone: bpy.types.Bone, routeNames: list[str]):
        if not bone.children:
            return
        boneName = bone.name
        if boneName.startswith("R"):
            boneName = boneName[1:5]
        routeNames.append(f"R{boneName}{bone.children[0].name}")
        self.__addRouteViaChild(bone.children[0], routeNames)

        if bone.name.startswith("R"):
            lastChild: bpy.types.Bone = self.__getLastPointChild(bone)
            if bone.name[1:5] != bone.children[0].name and bone.name[5:9] != lastChild.name:
                routeNames.append(f"R{lastChild.name}{bone.name[5:9]}")

    def __getLastPointChild(self, bone: bpy.types.Bone) -> bpy.types.Bone:
        if not bone.children:
            return bone
        return self.__getLastPointChild(bone.children[0])
