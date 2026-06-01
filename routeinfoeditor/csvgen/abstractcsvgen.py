import bpy
from abc import ABC, abstractmethod
import re

class AbstractCsvGen(ABC):
    def __init__(self, context: bpy.types.Context, config: dict):
        self._context = context
        self._config = config

    def run(self) -> list[str]:
        successfulFiles: list[str] = []

        world = self._getWorldFromArmature(self._context.armature)
        csvData = self._createCsvText(self._fetchNames())
        path: str = self._config.get("filePath", "//")
        if not path.endswith("/"):
            path += "/"
        fileName = f"{path}{self._getFileName(world)}"
        self._saveFile(csvData, fileName)
        successfulFiles.append(fileName)

        return successfulFiles

    def _saveFile(self, content: str, path: str):
        with open(bpy.path.abspath(path), 'wb') as file:
            file.write(content.encode('shift_jis'))

    def _getWorldFromArmature(self, armature: bpy.types.Armature | None) -> str:
        if armature is None:
            return "0"
        match = re.match(r"^CS_W(\d[ab]?)$", armature.name)
        if match:
            return match.group(1)
        return "0"

    @abstractmethod
    def _fetchNames(self) -> list[str]:
        pass

    @abstractmethod
    def _createCsvText(self, names: list[str]) -> str:
        pass

    @abstractmethod
    def _getFileName(self, world: str) -> str:
        pass
