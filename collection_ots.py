import bpy
from bpy.types import Collection, Operator


def get_collection_index(collection: Collection):
    """ This isn't possible? """
    for index, ref_collection in enumerate(bpy.data.collections):
        if collection == ref_collection:
            return index

