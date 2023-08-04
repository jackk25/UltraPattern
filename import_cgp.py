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
import os
from mathutils import Vector
from . import utils

def build_grid(context, height_map, prefab_map, name):
    PILLAR_VERTICAL_SCALE = 10
    BASE_PILLAR_SIZE = 2

    #Create the collection for our pillars, and register it as a pattern
    collection = bpy.data.collections.new(name)
    collection.is_pattern = True
    context.collection.children.link(collection)

    bpy.ops.mesh.primitive_cube_add(size=BASE_PILLAR_SIZE, location=Vector((0,0, -PILLAR_VERTICAL_SCALE)), scale=Vector((1, 1, PILLAR_VERTICAL_SCALE)))

    # Changing the pillar origin
    old_cursor_position = context.scene.cursor.location
    context.scene.cursor.location = Vector((0, 0, 0))
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    context.scene.cursor.location = old_cursor_position

    original_pillar = context.object

    #Locking the object position
    original_pillar.lock_location[0] = True
    original_pillar.lock_location[1] = True

    for x, row in enumerate(height_map):
        position_offset = Vector((x * BASE_PILLAR_SIZE, 0, 0))
        for y, height in enumerate(row):
            position_offset.y = y * BASE_PILLAR_SIZE
            position_offset.z = height
            prefab = prefab_map[x][y]

            pillar_copy = original_pillar.copy()

            pillar_copy.location += position_offset

            pillar_copy.is_pillar = True
            pillar_copy.prefab_type = str(prefab)
            utils.update_color(pillar_copy, str(prefab))
            collection.objects.link(pillar_copy)

    bpy.data.objects.remove(original_pillar)
    return {'FINISHED'}

def parse_height_map(height_map):
    parsed_map = []
    for row in height_map:
        row_storage = []
        temp_storage = ""
        in_block = False
        row = row.replace('\n', "")
        for x, char in enumerate(row):
            if char == '(':
                in_block = True
                continue
            if char == ')':
                in_block = False
                row_storage.append(int(temp_storage))
                temp_storage = ""
                continue
            if in_block == False:
                row_storage.append(int(char))
            if in_block:
                temp_storage += char
        parsed_map.append(row_storage)
    return parsed_map

def parse_object_map(object_map):
    parsed_map = []
    for x in object_map:
        x = x.replace('\n', '')
        row_storage = []
        for y in x:
            row_storage.append(y)
        parsed_map.append(row_storage)
    parsed_map.pop(0)
    return parsed_map

def load(operator, context, filepath=""):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = f.readlines()

        height_map = data[:16]
        object_map = data[16:]

        height_map = parse_height_map(height_map)
        object_map = parse_object_map(object_map)

        name = os.path.basename(filepath)

        return build_grid(context, height_map, object_map, name)