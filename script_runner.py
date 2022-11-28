"""
TODO: Needs to take multiple script locations
"""

#%% py imports
from pathlib import Path
from pathlib import Path
from typing import Iterable, Tuple, List
import ast

#%% bpy imports

try:
    import bpy
    from bpy.types import Operator, Context, Event
    from bpy.props import EnumProperty
except ImportError:
    pass



#%% main
_ADDON_SCRIPT_DIR = Path(__file__).parent / 'scripts'
EnumItem = Tuple[str, str, str, int]


def get_script_paths() -> Iterable[Path]:
    """ Get script paths from _SCRIPT_DIR """
    def _is_py(f: Path) -> bool:
        return f.suffix.lower() == ".py"
    return filter(_is_py, _ADDON_SCRIPT_DIR.iterdir())


def get_scripts_enum() -> List[EnumItem]:
    """ Return an enum of (script, label, docstring, index)"""
    enum = []
    for indx, script in enumerate(get_script_paths()):
        value = str(script)
        label = script.stem.title().replace("_", " ")
        description = read_docstring(script)
        enum.append((value, label, description, indx))
    return enum


def read_docstring(filepath: Path):
    """ Read docstring of file. Return empty string if file has no docstring.  """
    with open(filepath, 'r') as file:
        docstring = ast.get_docstring(ast.parse(file.read()))
        if docstring is None:
            return ""
        return docstring


#%% operator
class SCRIPT_OT_script_runner(Operator):
    bl_idname = "script.script_runner"
    bl_label = "Script Runner"
    bl_description = "Run script from scripts directory"
    bl_options = {"REGISTER", "UNDO"}
    bl_property = "script"

    script = EnumProperty(items=get_scripts_enum)

    def invoke(self, context, event: Event):
        wm = context.window_manager
        wm.invoke_search_popup(self)
        return {'FINISHED'}

    def execute(self, context: Context):
        print(self.script)
        bpy.ops.script.python_file_run(filepath=self.script)
        return {"FINISHED"}


operators = (SCRIPT_OT_script_runner,)
register, unregister = bpy.utils.register_classes_factory(operators)
