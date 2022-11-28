from typing import Iterable, Set, Generator
from itertools import count
from functools import partial

import bpy
import bmesh
from bpy.types import Operator, Context, Object, Mesh
from bpy.props import BoolProperty, IntVectorProperty

from commonfield import filters
from commonfield.mesh.context_mesh import edit_mesh


class OBJECT_OT_assign_object_ids(Operator):
    """ TODO: Test """

    bl_idname = "object.assign_object_Ids"
    bl_label = "Assign Object ID"
    bl_description = "Assign object ids"
    bl_options = {"REGISTER", "UNDO"}

    keep_non_zero: BoolProperty(
        name="Keep Non-zero",
        description="Keep existing id values if they have a value other than 0",
    )
    only_selected: BoolProperty(name="Only selected", default=True)
    unique_values: BoolProperty(name="Unique Values", default=True)

    @staticmethod
    def _get_existing_ids(context: Context):
        scene_objs = context.scene.objects
        return set((obj.pass_index for obj in scene_objs))

    @classmethod
    def _unique_ids(cls, context: Context) -> Generator[int, None, None]:
        existing_ids = cls._get_existing_ids(context)
        counter = count(start=1)

        while True:
            unique_id = next(counter)
            while unique_id in existing_ids:
                unique_id = next(counter)
            yield unique_id

    def execute(self, context: Context):
        scene_objs = context.scene.objects
        selected_objs = context.selected_objects
        targets = scene_objs if self.only_selected else selected_objs

        if self.keep_non_zero:
            targets = (t for t in targets if t.pass_index == 0)

        unique_ids = self._unique_ids(context)
        for target in targets:
            target.pass_index = next(unique_ids)

        return {"FINISHED"}


class OBJECT_OT_recalc_normals(Operator):
    """ TODO: Test """

    bl_idname = "object.recalculate_normals"
    bl_label = "Recalculate Normals"
    bl_description = "Recalculate Normals"
    bl_options = {"REGISTER", "UNDO"}

    flip: BoolProperty(name="Flip", default=False)

    def recalc_normals(self, context: Context, obj: Mesh):
        with edit_mesh(context, obj) as bm:
             bmesh.ops.recalc_face_normals(bm, bm.faces)
             if self.flip:
                bmesh.ops.reverse_faces(bm, bm.faces)

    def execute(self, context: Context):
        meshes = filter(filters.is_mesh, context.selected_objects)
        for mesh in meshes:
            self.recalc_normals(context, mesh)

        return {"FINISHED"}


registered_classes = OBJECT_OT_assign_object_ids, OBJECT_OT_recalc_normals
register, unregister = bpy.utils.register_classes_factory(registered_classes)
