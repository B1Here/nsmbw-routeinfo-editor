import bpy
from typing import Literal
from routeinfogen.csvgen.utilities import isDefined, isPoint

class RouteInfoRouteAddOperator(bpy.types.Operator):
    bl_idname = "routeinfo.add_route"
    bl_label = "Add Route"

    def execute(self, context: bpy.types.Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        armature = context.armature
        if not isDefined(armature):
            self.report({'ERROR'}, "No armature found")
            return {'CANCELLED'}
        routeSettings = armature.route_info_route_settings
        routeSettings.routes.add().name = "New Route"
        routeSettings.active_route_index = len(routeSettings.routes) - 1
        return {'FINISHED'}

class RouteInfoRouteRemoveOperator(bpy.types.Operator):
    bl_idname = "routeinfo.remove_route"
    bl_label = "Remove Route"

    def execute(self, context: bpy.types.Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        armature = context.armature
        if not isDefined(armature):
            self.report({'ERROR'}, "No armature found")
            return {'CANCELLED'}
        routeSettings = armature.route_info_route_settings
        if routeSettings.active_route_index < len(routeSettings.routes):
            routeSettings.routes.remove(routeSettings.active_route_index)
            routeSettings.active_route_index = max(0, routeSettings.active_route_index - 1)
        return {'FINISHED'}

class RouteInfoRouteDuplicateOperator(bpy.types.Operator):
    bl_idname = "routeinfo.duplicate_route"
    bl_label = "Duplicate Route"

    def execute(self, context: bpy.types.Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        armature = context.armature
        if not isDefined(armature):
            self.report({'ERROR'}, "No armature found")
            return {'CANCELLED'}
        routeSettings = armature.route_info_route_settings
        if routeSettings.active_route_index < len(routeSettings.routes):
            routeToDuplicate = routeSettings.routes[routeSettings.active_route_index]
            newRoute = routeSettings.routes.add()
            newRoute.name = f"{routeToDuplicate.name} Copy"
            routeSettings.active_route_index = len(routeSettings.routes) - 1
        return {'FINISHED'}

class RouteInfoRouteMoveUpOperator(bpy.types.Operator):
    bl_idname = "routeinfo.move_route_up"
    bl_label = "Move Route Up"

    def execute(self, context: bpy.types.Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        armature = context.armature
        if not isDefined(armature):
            self.report({'ERROR'}, "No armature found")
            return {'CANCELLED'}
        routeSettings = armature.route_info_route_settings
        index = routeSettings.active_route_index
        if index > 0 and index < len(routeSettings.routes):
            routeSettings.routes.move(index, index - 1)
            routeSettings.active_route_index = index - 1
        return {'FINISHED'}

class RouteInfoRouteMoveDownOperator(bpy.types.Operator):
    bl_idname = "routeinfo.move_route_down"
    bl_label = "Move Route Down"

    def execute(self, context: bpy.types.Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        armature = context.armature
        if not isDefined(armature):
            self.report({'ERROR'}, "No armature found")
            return {'CANCELLED'}
        routeSettings = armature.route_info_route_settings
        index = routeSettings.active_route_index
        if index >= 0 and index < len(routeSettings.routes) - 1:
            routeSettings.routes.move(index, index + 1)
            routeSettings.active_route_index = index + 1
        return {'FINISHED'}

class RouteInfoRouteRefreshOperator(bpy.types.Operator):
    bl_idname = "routeinfo.refresh_routes"
    bl_label = "Refresh"

    def execute(self, context: bpy.types.Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        armature = context.armature
        if not isDefined(armature):
            self.report({'ERROR'}, "No armature found")
            return {'CANCELLED'}
        routeSettings = armature.route_info_route_settings

        bones = self.__getBones(context)
        newRouteNames = self._fetchNames(bones)

        # Keep routes where both bones still exist, remove routes where either bone doesn't exist, and add routes for new bone pairs
        indiciesToRemove = []
        for i in range(len(routeSettings.routes)):
            route = routeSettings.routes[i]
            if route.name not in newRouteNames:
                indiciesToRemove.append(i)

        print(indiciesToRemove, routeSettings.routes)

        for i in reversed(indiciesToRemove):
            routeSettings.routes.remove(i)
        bones = self.__getBones(context)
        existingRouteNames = {route.name for route in routeSettings.routes}

        if bones:
            for boneName in newRouteNames:
                if boneName not in existingRouteNames:
                    routeSettings.routes.add().name = boneName

        self.report({'INFO'}, f"Routes refreshed, {len(indiciesToRemove)} removed, {len(routeSettings.routes) - len(existingRouteNames)} added.")
        return {'FINISHED'}

    def _fetchNames(self, bones) -> list[str]:
        routeBones: list[bpy.types.Bone] = []
        for bone in bones:
            if bone.name.startswith("R") and isPoint(bone.name[1:5]) and isPoint(bone.name[5:9]):
                routeBones.append(bone)

        result: list[str] = []
        for bone in routeBones:
            self.__addRouteForBone(bone, result)

        return result

    def __addRouteForBone(self, bone: bpy.types.Bone, routeNames: list[str]):
        if isDefined(bone.children) and len(bone.children) > 0 and filter(lambda child: isPoint(child.name), bone.children):
            self.__addRouteViaChild(bone, routeNames)
            return
        routeNames.append(bone.name)

    def __addRouteViaChild(self, bone: bpy.types.Bone, routeNames: list[str]):
        if not isDefined(bone.children) or len(bone.children) == 0:
            return
        boneName = bone.name
        if boneName.startswith("R"):
            boneName = boneName[1:5]
        routeNames.append(f"R{boneName}{bone.children[0].name}")
        self.__addRouteViaChild(bone.children[0], routeNames)

        if bone.name.startswith("R"):
            lastChild: bpy.types.Bone = self.__getLastPointChild(bone)
            if bone.name[1:5] != bone.children[0].name and bone.name[5:9] != lastChild.name:
                routeNames.append(f"R{lastChild.name}{bone.name[5:9]}")

    def __getLastPointChild(self, bone: bpy.types.Bone) -> bpy.types.Bone:
        if not isDefined(bone.children) or len(bone.children) == 0:
            return bone
        return self.__getLastPointChild(bone.children[0])

    def __getBones(self, context: bpy.types.Context):
        if (context.object.mode == 'EDIT'):
            return context.armature.edit_bones
        if (context.object.mode == 'POSE'):
            return context.armature.pose.bones
        return context.armature.bones

class RouteInfoRouteSelectBonesOperator(bpy.types.Operator):
    bl_idname = "routeinfo.route_select_bones"
    bl_label = "Select Bones"

    def execute(self, context: bpy.types.Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        armature = context.armature
        if not isDefined(armature) or not isDefined(context.object):
            self.report({'ERROR'}, "No armature found")
            return {'CANCELLED'}
        routeSettings = armature.route_info_route_settings
        index = routeSettings.active_route_index
        if index < 0 or index >= len(routeSettings.routes):
            self.report({'ERROR'}, "No route selected")
            return {'CANCELLED'}
        routeName: str = routeSettings.routes[index].name
        bonesToSelect: list[bpy.types.Bone] = [bone for bone in armature.bones if routeName.__contains__(bone.name)]

        if context.object.mode == 'POSE':
            for bone in context.object.pose.bones:
                selectable = len(list(filter(lambda b: b.name == bone.name, bonesToSelect))) > 0
                bone.bone.select = selectable
            if len(list(filter(lambda b: b.bone.select, context.object.pose.bones))) < 2:
                self.report({'WARNING'}, 'Not all bones were selected. Make sure to refresh the list.')
        elif context.object.mode == 'EDIT':
            for bone in armature.edit_bones:
                selectable = len(list(filter(lambda b: b.name == bone.name, bonesToSelect))) > 0
                bone.select = selectable
                bone.select_head = selectable
                bone.select_tail = selectable
            if len(list(filter(lambda b: b.select, armature.edit_bones))) < 2:
                self.report({'WARNING'}, 'Not all bones were selected. Make sure to refresh the list.')

        return {'FINISHED'}
