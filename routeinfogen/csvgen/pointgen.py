import bpy
import re
from .abstractcsvgen import AbstractCsvGen

class PointCsvGen(AbstractCsvGen):
    def _fetchNames(self, armature: bpy.types.Armature) -> list[str]:
        pointNames: list[str] = []
        for bone in armature.bones:
            if re.compile(r"(?:[FW][a-zA-Z0-9]{3})").match(bone.name):
                pointNames.append(bone.name)

        return pointNames

    def _createCsvText(self, names: list[str]) -> str:
        csv: str = ""
        index: int = 0
        for bone in names:
            csv += f"{index},{bone},,,,,,,\r\n"
            index += 1

        return csv

    def _getFileName(self, world: str) -> str:
        return f"pointW{world}.csv"
