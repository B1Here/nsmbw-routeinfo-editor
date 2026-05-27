from routeinfogen.csvgen.utilities import isLevelPoint, isFlagPoint
from .abstractcsvgen import AbstractCsvGen

class PointCsvGen(AbstractCsvGen):
    def _fetchNames(self) -> list[str]:
        pointNames: list[str] = []
        for bone in self._getBones():
            if isLevelPoint(bone.name) or isFlagPoint(bone.name):
                pointNames.append(bone.name)

        return pointNames

    def _createCsvText(self, names: list[str]) -> str:
        csv: str = ""
        id: int = 0
        bones = self._getBones()
        for bone in names:
            routeInfoSettings = bones[bone].route_info_point_settings

            csv += (f"{id},{bone},{self._csvArrayGuard(routeInfoSettings.flags)},{self._csvArrayGuard(routeInfoSettings.unlocked_levels)},{self._csvArrayGuard(routeInfoSettings.unlocked_bones)},"
                + f",{self._csvArrayGuard(routeInfoSettings.unlocked_levels_secret_exit)},{self._csvArrayGuard(routeInfoSettings.unlocked_bones_secret_exit)},\r\n")
            id += 1

        return csv

    def _getFileName(self, world: str) -> str:
        return f"pointW{world}.csv"

    def _csvArrayGuard(self, string: str) -> str:
        return f'"{string}"' if "," in string else string
