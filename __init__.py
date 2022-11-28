"""
Copyright (C) 2022 Missing Field
the.missing.field@gmail.com

Created by Missing Field

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


bl_info = {
    "name": "Fields Box",
    "author": "missing_field",
    "description": "Fields Little Bag",
    "blender": (3, 3, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Object",
}

# import bpy

from . import (
    object_ots,
    script_runner,
    # operators,
    # ui,
    # object_ots,
)


registered_classes = (
    object_ots,
    script_runner,
    # props,
    # operators,
    # ui,
)

def register():
    for cls in registered_classes:
        cls.register()


def register():
    for cls in registered_classes:
        cls.unregister()