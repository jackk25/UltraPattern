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
import numpy as np
import math

def save(operator, context, filepath):
    height_map = np.array([], str)
    object_map = np.array([], str)
    for obj in context.collection.objects:
        if obj.is_pillar:
            pillar_height = obj.location.z
            match operator.rounding_type:
                case 'ROUND_TYPE_NEAREST':
                    pillar_height = round(pillar_height)
                case 'ROUND_TYPE_FLOOR':
                    pillar_height = math.floor(pillar_height)
                case 'ROUND_TYPE_CEIL':
                    pillar_height = math.ceil(pillar_height)

            height_map = np.append(height_map, pillar_height)
            object_map = np.append(object_map, obj.prefab_type)
    height_map = height_map.reshape(16, 16)
    object_map = object_map.reshape(16, 16)

    with open(filepath, "w") as f:
        #Write the height map
        for row in height_map:
            row_storage = ''
            for col in row:
                if len(col) > 1:
                    col = f'({col})'
                row_storage += col
            f.write(row_storage + '\n')

        f.write('\n')

        for row in object_map:
            row_storage = ''
            for col in row:
                row_storage += col
            f.write(row_storage + '\n')

    return {'FINISHED'}