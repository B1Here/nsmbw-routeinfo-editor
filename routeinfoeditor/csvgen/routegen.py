import bpy
from .utilities import isDefined
from .abstractcsvgen import AbstractCsvGen

class RouteCsvGen(AbstractCsvGen):
    def _fetchNames(self) -> list[str]:
        return list()

    def _createCsvText(self, names: list[str]) -> str:
        routes = self._context.armature.route_info_route_settings.routes

        csv = ""
        for route in routes:
            csv += f"{route.name},{route.animation},{route.flags}\r\n"

        return csv

    def _getFileName(self, world: str) -> str:
        return f"routeW{world}.csv"

    def __addRouteViaChild(self, bone: bpy.types.Bone, routeNames: list[str]):
        if not isDefined(bone.children) or len(bone.children) == 0:
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
        if not isDefined(bone.children) or len(bone.children) == 0:
            return bone
        return self.__getLastPointChild(bone.children[0])
