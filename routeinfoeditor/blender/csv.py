import bpy
import re
from typing import Literal

from bpy.types import Context
from ..csvgen.utilities import (
    getModeSpecificBones,
    isDefined,
    isFlagPoint,
    isLevelPoint,
)
from ..csvgen.abstractcsvgen import AbstractCsvGen
from ..csvgen.routegen import RouteCsvGen
from ..csvgen.pointgen import PointCsvGen

allFlags = [
    "stop",
    "crossroad",
    "dokan",
    "scrollY",
    "scrollA",
    "scroll",
    "focus",
    "camstop",
    "demo1",
    "demo2",
    "demo3",
    "demo4",
    "demo5",
    "demo6",
    "demo7",
    "sand",
    "ice",
    "noshift",
    "link1",
    "switch",
    "ura",
    "scale",
    "demostop",
    "tilt",
    "board",
    "link2",
    "link3",
    "link4",
    "link5",
    "anchor",
]


class RouteInfoCsvGenOperator(bpy.types.Operator):
    """Generate RouteInfo CSV files"""

    bl_idname = "routeinfo.generate"
    bl_label = "Generate RouteInfo CSV files"

    def execute(
        self, context: bpy.types.Context
    ) -> set[
        Literal["RUNNING_MODAL", "CANCELLED", "FINISHED", "PASS_THROUGH", "INTERFACE"]
    ]:
        armatureData = context.armature
        if not isDefined(armatureData):
            self.report({"ERROR"}, "No armature found.")
            return {"CANCELLED"}
        riSettings = armatureData.route_info_csv_settings

        classes: list[type[AbstractCsvGen]] = [RouteCsvGen, PointCsvGen]

        # Run each generator for each armature
        for cls in classes:
            op = cls(
                context, {"filePath": riSettings.filePath, "mode": context.object.mode}
            )
            fileName = op.run()
            if not fileName:
                self.report(
                    {"ERROR"},
                    f"Failed to generate CSV file for {cls.__name__}.",
                )
                continue
            self.report({"INFO"}, f"Successfully generated CSV file {fileName}")
        self.report({"INFO"}, "Finished generating CSV files.")

        return {"FINISHED"}


class RouteInfoDataCleanupOperator(bpy.types.Operator):
    """Clean up csv column data that is not supposed to be present on specific bones, points and routes"""

    bl_idname = "routeinfo.cleanup"
    bl_label = "Cleanup Non-Point Data"

    def execute(
        self, context: Context
    ) -> set[
        Literal["RUNNING_MODAL", "CANCELLED", "FINISHED", "PASS_THROUGH", "INTERFACE"]
    ]:
        armatureData = context.armature
        if not isDefined(armatureData):
            self.report({"ERROR"}, "No armature found.")
            return {"CANCELLED"}

        for bone in getModeSpecificBones(context):
            pointSettings = bone.route_info_point_settings
            if not isFlagPoint(bone.name) and not isLevelPoint(bone.name):
                pointSettings.flags = ""

            if not isLevelPoint(bone.name):
                pointSettings.unlocked_levels = ""
                pointSettings.unlocked_bones = ""
                pointSettings.unlocked_levels_secret_exit = ""
                pointSettings.unlocked_bones_secret_exit = ""

        self.report({"INFO"}, "Finished cleaning up RouteInfo data.")

        return {"FINISHED"}


class RouteInfoValidateOperator(bpy.types.Operator):
    """Validate RouteInfo data and report any issues"""

    bl_idname = "routeinfo.validate"
    bl_label = "Validate RouteInfo Data"

    def execute(
        self, context: Context
    ) -> set[
        Literal["RUNNING_MODAL", "CANCELLED", "FINISHED", "PASS_THROUGH", "INTERFACE"]
    ]:
        armatureData = context.armature
        if not isDefined(armatureData):
            self.report({"ERROR"}, "No armature found.")
            return {"CANCELLED"}

        allBoneNames = list(map(lambda b: b.name, getModeSpecificBones(context)))

        warningCount = 0
        # Check that all flags on flag points and level points are valid point flags
        for bone in filter(
            lambda b: isFlagPoint(b.name) or isLevelPoint(b.name),
            getModeSpecificBones(context),
        ):
            pointSettings = bone.route_info_point_settings
            for flag in filter(lambda f: f.strip(), pointSettings.flags.split(",")):
                if flag and flag not in allFlags:
                    self.report(
                        {"WARNING"},
                        f'Bone {bone.name} has a flag "{flag}" that is not a valid point flag.',
                    )
                    warningCount += 1

        # Check that all unlocked levels and bones on level points reference existing bones
        for bone in filter(
            lambda b: isLevelPoint(b.name), getModeSpecificBones(context)
        ):
            pointSettings = bone.route_info_point_settings
            for level in filter(
                lambda l: l.strip() != "", pointSettings.unlocked_levels.split(",")
            ):
                if level and level not in allBoneNames:
                    self.report(
                        {"WARNING"},
                        f"Bone {bone.name} has an unlocked level {level} that does not exist.",
                    )
                    warningCount += 1

            for boneName in filter(
                lambda b: b.strip() != "", pointSettings.unlocked_bones.split(",")
            ):
                if boneName and boneName not in allBoneNames:
                    self.report(
                        {"WARNING"},
                        f"Bone {bone.name} has an unlocked bone {boneName} that does not exist.",
                    )
                    warningCount += 1

            for level in filter(
                lambda l: l.strip() != "",
                pointSettings.unlocked_levels_secret_exit.split(","),
            ):
                if level and level not in allBoneNames:
                    self.report(
                        {"WARNING"},
                        f"Bone {bone.name} has an unlocked secret exit level {level} that does not exist.",
                    )
                    warningCount += 1

            for boneName in filter(
                lambda b: b.strip() != "",
                pointSettings.unlocked_bones_secret_exit.split(","),
            ):
                if boneName and boneName not in allBoneNames:
                    self.report(
                        {"WARNING"},
                        f"Bone {bone.name} has an unlocked secret exit bone {boneName} that does not exist.",
                    )
                    warningCount += 1

        if warningCount > 0:
            self.report(
                {"WARNING"},
                f"Finished validating RouteInfo data with {warningCount} warning(s).",
            )
        else:
            self.report(
                {"INFO"}, "Finished validating RouteInfo data with no issues found."
            )
        return {"FINISHED"}


class RouteInfoCsvSettings(bpy.types.PropertyGroup):
    filePath: bpy.props.StringProperty(
        name="File Path",
        description="The directory to save generated CSV files in",
        default="//",
        subtype="DIR_PATH",
        options=set(),
    )  # pyright: ignore[reportInvalidTypeForm]


class RouteInfoCsvPanel(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "ROUTEINFO_PT_armature_attrs"
    bl_label = "RouteInfo CSV Configuration"
    bl_context = "data"

    @classmethod
    def poll(cls, context) -> bool:
        pattern = re.compile(r"^CS_W\d[ab]?$")
        if context.object and context.object.type == "ARMATURE" and context.armature:
            return (
                pattern.match(context.object.name) is not None
                and pattern.match(context.armature.name) is not None
                and context.armature.name == context.object.name
            )
        return False

    def draw(self, context):
        layout = self.layout
        if not isDefined(layout):
            return
        layout.use_property_split = True
        layout.use_property_decorate = False
        layout.prop(context.armature.route_info_csv_settings, "filePath")
        layout.operator(
            RouteInfoCsvGenOperator.bl_idname,
            text="Generate RouteInfo CSVs",
            icon="TEXT",
        )
        layout.separator()
        layout.operator(
            RouteInfoDataCleanupOperator.bl_idname,
            text="Cleanup Non-Point Data",
            icon="BRUSH_DATA",
        )
        layout.operator(
            RouteInfoValidateOperator.bl_idname,
            text="Validate RouteInfo Data",
            icon="CHECKMARK",
        )
