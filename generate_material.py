import bpy

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
