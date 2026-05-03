import bpy
from abc import ABC, abstractmethod
import re

class AbstractCsvGen(ABC):
    _armatures: list[bpy.types.Armature]

    def __init__(self, armatures: list[bpy.types.Armature]):
        self._armatures = armatures

    def run(self) -> list[str]:
        successfulFiles: list[str] = []

        for index in range(len(self._armatures)):
            world = self._getWorldFromArmature(index)
            csvData = self._createCsvText(self._fetchNames(index), index)
            fileName = f"//{self._getFileName(world)}"
            self._saveFile(csvData, fileName)
            successfulFiles.append(fileName)

        return successfulFiles

    def _saveFile(self, content: str, path: str):
        with open(bpy.path.abspath(path), 'wb') as file:
            file.write(content.encode('shift_jis'))

    def _getWorldFromArmature(self, index: int) -> str:
        match = re.match(r"^CS_W(\d[ab]?)$", self._armatures[index].name)
        if match:
            return match.group(1)
        return "0"

    @abstractmethod
    def _fetchNames(self, index: int) -> list[str]:
        pass

    @abstractmethod
    def _createCsvText(self, names: list[str], index: int) -> str:
        pass

    @abstractmethod
    def _getFileName(self, world: str) -> str:
        pass
