import bpy
import re
from .abstractcsvgen import AbstractCsvGen

class PointCsvGen(AbstractCsvGen):
    def _fetchNames(self, index: int) -> list[str]:
        pointNames: list[str] = []
        for bone in self._armatures[index].bones:
            if re.compile(r"(?:[FW][a-zA-Z0-9]{3})").match(bone.name):
                pointNames.append(bone.name)

        return pointNames

    def _createCsvText(self, names: list[str], index: int) -> str:
        csv: str = ""
        id: int = 0
        for bone in names:
            flags: list[str] = []
            if (bone.startswith('F') and (any(b.name.startswith(f"R{bone}") for b in self._armatures[index].bones)
                    or any((b.name.startswith("R") and b.name.endswith(bone)) for b in self._armatures[index].bones))):
                flags.append('stop')

            flagsStr = ''
            if len(flags) > 1:
                flagsStr = f'"{",".join(flags)}"'
            else:
                flagsStr = ",".join(flags)


            csv += f"{id},{bone},{flagsStr},,,,,,\r\n"
            id += 1

        return csv

    def _getFileName(self, world: str) -> str:
        return f"pointW{world}.csv"
