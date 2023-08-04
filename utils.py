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

import bpy

def on_enum_color(self, context):
    update_color(context.active_object, context.active_object.prefab_type)
    return None

def update_color(obj, prefab):
    match prefab:
        case 'n':
            object_color = [230, 124, 115, 255]
        case 'p':
            object_color = [247, 203, 77, 255]
        case 'J':
            object_color = [65, 179, 117, 255]
        case 's':
            object_color = [123, 170, 247, 255]
        case 'H':
            object_color = [186, 103, 200, 255]
        case _:
            object_color = [255, 255, 255, 255]

    # Blender wants colors as a float > 1
    # So I need to do this to convert from regular 255 RGB
    object_color = [x/255 for x in object_color]
    obj.color = object_color
