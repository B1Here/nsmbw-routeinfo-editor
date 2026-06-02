from routeinfoeditor.csvgen.abstractcsvgen import AbstractCsvGen
from routeinfoeditor.csvgen.utilities import (
    __get_bones__,
    __is_level_point__,
    __is_flag_point__,
)


class PointCsvGen(AbstractCsvGen):
    def _fetch_names(self) -> list[str]:
        point_names: list[str] = []
        for bone in __get_bones__(self._context):
            if __is_level_point__(bone.name) or __is_flag_point__(bone.name):
                point_names.append(bone.name)

        return point_names

    def _create_csv(self, names: list[str]) -> str:
        csv: str = ""
        id: int = 0
        bones = __get_bones__(self._context)
        for bone in names:
            point_settings = bones[bone].route_info_point_settings

            csv += (
                f"{id},{bone},{self._csv_array_guard(point_settings.flags)},{self._csv_array_guard(point_settings.unlocked_levels)},{self._csv_array_guard(point_settings.unlocked_bones)},"
                + f",{self._csv_array_guard(point_settings.unlocked_levels_secret_exit)},{self._csv_array_guard(point_settings.unlocked_bones_secret_exit)},\r\n"
            )
            id += 1

        return csv

    def _get_file_name(self, world: str) -> str:
        return f"pointW{world}.csv"

    def _csv_array_guard(self, string: str) -> str:
        return f'"{string}"' if "," in string else string
