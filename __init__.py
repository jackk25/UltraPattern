# Copyright (C) 2023 jackk25

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

bl_info = {
        "name": "UltraPattern",
        "author": "jackk25",
        "version": (1, 0, 0),
        "blender": (3, 6, 0),
        "category": "3D View",
        "location": "3D View > Sidebar > UltraPattern",
        "description": "Import, create, modify, and export Cyber Grind Pattern files to ULTRAKILL"
}

# Allows reloading through F8, "Reload Script", etc. without breaking
if "bpy" in locals():
    import importlib
    if "import_cgp" in locals():
        importlib.reload(import_cgp)
    if "export_cgp" in locals():
        importlib.reload(export_cgp)

# Imports
import bpy

from bpy.props import (
    StringProperty,
    BoolProperty,
    EnumProperty
    )

from bpy_extras.io_utils import (
    ImportHelper,
    ExportHelper
    )

from mathutils import Vector
from . import utils

class ImportCGP(bpy.types.Operator, ImportHelper):
    """Load a Cyber Grind Pattern file"""
    bl_idname = "cgp_editor.import"
    bl_label = "Import CGP"
    bl_options = {'UNDO'}

    filename_ext = ".cgp"
    filter_glob: StringProperty(
        default="*.cgp",
        options={'HIDDEN'}
    )

    def execute(self, context):
        from . import import_cgp
        return import_cgp.load(self, context, self.filepath)

class ExportCGP(bpy.types.Operator, ExportHelper):
    """Write a Cyber Grind Pattern file"""
    bl_idname = "cgp_editor.export"
    bl_label = "Export CGP"
    bl_options = {'UNDO'}

    filename_ext = ".cgp"
    filter_glob: StringProperty(
        default="*.cgp",
        options={'HIDDEN'}
    )

    rounding_type: EnumProperty(
        name="Rounding Type",
        description="How to round any non integer height values",
        items=(('ROUND_TYPE_NEAREST', "Nearest",
                "Round to the nearest integer"),
                ('ROUND_TYPE_FLOOR', "Floor",
                 "Round down to the nearest integer"),
                ('ROUND_TYPE_CEIL', "Ceiling",
                 "Round up to the nearest integer")
              )
    )

    @classmethod
    def poll(cls, context):
        return context.collection.is_pattern

    def execute(self, context):
        from . import export_cgp
        return export_cgp.save(self, context, self.filepath)

class GenerateCGP(bpy.types.Operator):
    """Generate a blank CGP file"""
    bl_idname = "cgp_editor.generate"
    bl_label = "Create Blank Pattern"
    bl_options = {'UNDO'}

    def execute(self, context):
        from . import import_cgp
        blank_grid = []
        # This could be done with list comprehension
        # But I think the readability is better here
        for x in range(16):
            row_storage = []
            for y in range(16):
                row_storage.append(0)
            blank_grid.append(row_storage)
        return import_cgp.build_grid(bpy.context, blank_grid, blank_grid, "Blank Pattern")

class CGP_EDITOR_PT_Mesh(bpy.types.Panel):
    bl_label = "Mesh"
    bl_category = "UltraPattern"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.operator(ImportCGP.bl_idname)
        row.operator(ExportCGP.bl_idname)

        row = layout.row()
        row.operator(GenerateCGP.bl_idname)

class CGP_EDITOR_PT_Pillar(bpy.types.Panel):
    bl_label = "Pillar"
    bl_category = "UltraPattern"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"

    # Only avalible if the user has selected a pillar
    @classmethod
    def poll(cls, context):
        # Error checking
        try:
            return context.active_object.is_pillar
        except AttributeError:
            return False

    def draw(self, context):
        layout = self.layout
        pillar = context.object

        row = layout.row(align=True, heading="")
        row.prop(pillar, "prefab_type")

classes = (
    ImportCGP,
    ExportCGP,
    GenerateCGP,
    CGP_EDITOR_PT_Mesh,
    CGP_EDITOR_PT_Pillar
)

def register():
    bpy.types.Collection.is_pattern = BoolProperty("Is Pattern")
    bpy.types.Object.prefab_type = EnumProperty(
        name="Prefab Type",
        description="The type of prefab to give the pillar",
        items=(
        ('0', "None", "No prefab will be created"),
        ('n', "Melee", "Melee enemy spawn point"),
        ('p', "Projectile", "Projectile enemy spawn point"),
        ('J', "Jump Pad", ""),
        ('s', "Stairs", ""),
        ('H', "Hideous Mass","Hideous Mass spawn point")
        ),
        default='0', update=utils.on_enum_color)
    bpy.types.Object.is_pillar = BoolProperty(name="Is Pillar")

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Collection.is_pattern
    del bpy.types.Object.prefab_type
    del bpy.types.Object.is_pillar

if __name__ == "__main__":
    register()