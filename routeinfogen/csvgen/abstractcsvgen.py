import bpy
from abc import ABC, abstractmethod
import re

class AbstractCsvGen(ABC):
    __armatures: list[bpy.types.Armature]

    def __init__(self, armatures: list[bpy.types.Armature]):
        self.__armatures = armatures

    def run(self) -> list[str]:
        """Runs the CSV generation process for all armatures and returns a list of successfully generated file names."""
        successfulFiles: list[str] = []

        for armature in self.__armatures:
            world = self._getWorldFromArmature(armature)
            csvData = self._createCsvText(self._fetchNames(armature))
            fileName = f"//{self._getFileName(world)}"
            self._saveFile(csvData, fileName)
            successfulFiles.append(fileName)

        return successfulFiles

    def _saveFile(self, content: str, path: str):
        with open(bpy.path.abspath(path), 'wb') as file:
            file.write(content.encode('shift_jis'))

    def _getWorldFromArmature(self, armature: bpy.types.Armature) -> str:
        match = re.match(r"^CS_W(\d[ab]?)$", armature.name)
        if match:
            return match.group(1)
        return "0"

    @abstractmethod
    def _fetchNames(self, armature: bpy.types.Armature) -> list[str]:
        """Fetches the names to be included in the CSV file from the given armature.

        :param armature: The armature to fetch names from."""
        pass

    @abstractmethod
    def _createCsvText(self, names: list[str]) -> str:
        """Creates the CSV text content based on the given names.

        :param names: The list of names to include in the CSV."""
        pass

    @abstractmethod
    def _getFileName(self, world: str) -> str:
        """Gets the file name for the CSV based on the given world.

        :param world: The world identifier.
        :return: The file name for the CSV."""
        pass
