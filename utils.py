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

def prefab_update(self, context):
    update_color(self, self.prefab_type)
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

    # Convert from 0-255 RGB to 0-1 RGB
    object_color = [x/255 for x in object_color]
    obj.color = object_color

def generate_material(obj, filepath):
    material = bpy.data.materials.new(name="Pillar Material")
    material.use_nodes = True

    material.node_tree.nodes.remove(material.node_tree.nodes.get('Principled BSDF'))

    #Create the nodes we need for the material
    material_output = material.node_tree.nodes.get('Material Output')
    emission = material.node_tree.nodes.new('ShaderNodeEmission')
    image_texture = material.node_tree.nodes.new('ShaderNodeTexImage')

    #Link our nodes together to create the tree
    material.node_tree.links.new(emission.inputs[0], image_texture.outputs[0])
    material.node_tree.links.new(material_output.inputs[0], emission.outputs[0])

    #Load the most recent image, this will be our opened image
    image_texture.image = bpy.data.images.load(filepath)
    image_texture.interpolation = 'Closest'
    
    obj.active_material = material

    return {"FINISHED"}
