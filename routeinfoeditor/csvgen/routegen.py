from routeinfoeditor.csvgen.abstractcsvgen import AbstractCsvGen
from routeinfoeditor.csvgen.utilities import __is_defined__


class RouteCsvGen(AbstractCsvGen):
    def _fetch_names(self) -> list[str]:
        return list()

    def _create_csv(self, names: list[str]) -> str:
        routes = self._context.armature.route_info_route_settings.routes

        csv = ""
        for route in routes:
            csv += f"{route.name},{route.animation},{self._csv_array_guard(route.flags)}\r\n"

        return csv

    def _get_file_name(self, world: str) -> str:
        return f"routeW{world}.csv"
