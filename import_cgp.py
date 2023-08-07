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
import bmesh
import json
from mathutils import Vector

if "bpy" in locals():
    import importlib
    if "utils" in locals():
        importlib.reload(utils)

from . import utils

def make_base_pillar(context, BASE_PILLAR_SIZE, PILLAR_VERTICAL_SCALE):
    bpy.ops.mesh.primitive_cube_add(
        size=BASE_PILLAR_SIZE, 
        location=Vector((0,0, -PILLAR_VERTICAL_SCALE)), 
        scale=Vector((1, 1, PILLAR_VERTICAL_SCALE))
    )

    # Changing the pillar origin
    old_cursor_position = context.scene.cursor.location
    context.scene.cursor.location = Vector((0, 0, 0))
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    context.scene.cursor.location = old_cursor_position

    original_pillar = context.object

    #Locking the object position
    original_pillar.lock_location[0] = True
    original_pillar.lock_location[1] = True

    fix_uvs(original_pillar.data)

    return original_pillar

def build_grid(context, height_map, prefab_map, name):
    PILLAR_VERTICAL_SCALE = 10
    BASE_PILLAR_SIZE = 2

    #Create the collection for our pillars, and register it as a pattern
    collection = bpy.data.collections.new(name)
    collection.is_pattern = True
    context.collection.children.link(collection)

    original_pillar = make_base_pillar(context, BASE_PILLAR_SIZE, PILLAR_VERTICAL_SCALE)

    for x, row in enumerate(height_map):
        position_offset = Vector((x * BASE_PILLAR_SIZE, 0, 0))
        for y, height in enumerate(row):
            position_offset.y = y * BASE_PILLAR_SIZE
            position_offset.z = height
            prefab = prefab_map[x][y]

            pillar_copy = original_pillar.copy()

            pillar_copy.location += position_offset
            collection.objects.link(pillar_copy)
            
            pillar_copy.is_pillar = True
            pillar_copy.prefab_type = str(prefab)

    bpy.data.objects.remove(original_pillar)
    return {'FINISHED'}

def parse_height_map(height_map):
    parsed_map = []
    for row in height_map:
        row_storage = []
        block_storage = ""
        in_block = False
        for char in row:
            if char == '(':
                in_block = True
                continue
            if char == ')':
                in_block = False
                row_storage.append(int(block_storage))
                block_storage = ""
                continue
            if in_block == False:
                row_storage.append(int(char))
            if in_block:
                block_storage += char
        parsed_map.append(row_storage)
    return parsed_map

def parse_object_map(object_map):
    parsed_map = []
    for row in object_map:
        row_storage = []
        for col in row:
            row_storage.append(col)
        parsed_map.append(row_storage)
    return parsed_map

def fix_uvs(mesh_data):
    bm = bmesh.new()
    bm.from_mesh(mesh_data)

    uv_layer = bm.loops.layers.uv.active

    loaded_uvs = []

    current_file_dir = os.path.dirname(__file__)
    uv_filepath = os.path.join(current_file_dir, "resources", "cube.json")

    with open(uv_filepath,'r') as f:
        loaded_uvs = json.load(f)
    
    for index, face in enumerate(bm.faces):
        face_uvs = loaded_uvs[index]
        for loop_index, loop in enumerate(face.loops):
            uv = loop[uv_layer].uv
            loop_uv = face_uvs[loop_index]
            uv.x = loop_uv[0]
            uv.y = loop_uv[1]
    
    bm.to_mesh(mesh_data)
    mesh_data.update()
    bm.free()

def load(context, filepath=""):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = f.read().splitlines()

        height_map = data[:16]
        object_map = data[17:]

        height_map = parse_height_map(height_map)
        object_map = parse_object_map(object_map)

        name = os.path.basename(filepath)

        return build_grid(context, height_map, object_map, name)