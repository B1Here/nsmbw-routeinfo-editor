from routeinfoeditor.blender.armatureutils import __get_bones__
from routeinfoeditor.csvgen.abstractcsvgen import AbstractCsvGen
from routeinfoeditor.nsmbw.routeinfoutils import (
    __is_level_point__,
    __is_flag_point__,
)


class PointCsvGen(AbstractCsvGen):
    def _create_csv(self) -> str:
        csv: str = ""
        id: int = 0
        bones = list(
            filter(
                lambda b: __is_level_point__(b.name) or __is_flag_point__(b.name),
                __get_bones__(self._context),
            )
        )

        for bone in bones:
            point_settings = bone.route_info_point_settings

            csv += (
                f"{id},{bone.name},{self._csv_array_guard(point_settings.flags)},{self._csv_array_guard(point_settings.unlocked_levels)},{self._csv_array_guard(point_settings.unlocked_bones)},"
                + f",{self._csv_array_guard(point_settings.unlocked_levels_secret_exit)},{self._csv_array_guard(point_settings.unlocked_bones_secret_exit)},\r\n"
            )
            id += 1

        return csv

    def _get_file_name(self, world: str) -> str:
        return f"pointW{world}.csv"
