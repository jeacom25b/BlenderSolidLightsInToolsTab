bl_info = {
    "name": "Solid Lights Protoshader",
    "description": "utilities for solid shading",
    "author": "Jean Da Costa Machado",
    "version": (0, 0, 1),
    "blender": (2, 78, 0),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Render" }


import bpy
from bpy import context
from mathutils import Vector
from mathutils import Euler


def protoshader_update (self, context):
    
    if context.scene.solid_ligths_protosahder_enable == False:
        return None
    
    ligths = context.user_preferences.system.solid_lights
    scene = context.scene
    f_dcol = scene.solid_ligths_protoshader_front_diffcol
    f_scol = scene.solid_ligths_protoshader_front_speccol
    b_dcol = scene.solid_ligths_protoshader_back_diffcol
    b_scol = scene.solid_ligths_protoshader_back_speccol
    h_shift = scene.solid_ligths_protoshader_back_hueshift
    
    b_dcol_hp = Vector((b_dcol[0] + (h_shift[0]- 0.5) * 0.5 ,
                        b_dcol[1] + (h_shift[1]- 0.5) * 0.5 ,
                        b_dcol[2] + (h_shift[2]- 0.5) * 0.5 ))
    
    b_dcol_hm = Vector((b_dcol[0] - (h_shift[0]- 0.5) * 0.5 ,
                        b_dcol[1] - (h_shift[1]- 0.5) * 0.5 ,
                        b_dcol[2] - (h_shift[2]- 0.5) * 0.5 ))
    
        
    if context.scene.solid_lights_protoshader_type == 'PLASTIC':
        dir = context.scene.solid_lights_protoshader_direction
        back_dir = Vector((-dir.x, -dir.y, -dir.z + 1))
        fill_dir = Vector((dir.x, dir.y, dir.z + 0.5))
        ligths[0].direction = dir
        ligths[1].direction = fill_dir
        ligths[2].direction = back_dir
        ligths[0].diffuse_color = f_dcol
        ligths[0].specular_color = Vector((f_scol[0] / 2,
                                           f_scol[1] / 2,
                                           f_scol[2] / 2,))
        ligths[1].diffuse_color = Vector((
            b_dcol_hp[0] * 0.25 + f_dcol[0] * 0.25,
            b_dcol_hp[1] * 0.25 + f_dcol[1] * 0.25,
            b_dcol_hp[2] * 0.25 + f_dcol[2] * 0.25))
        ligths[1].specular_color = Vector((b_scol[0] / 5,
                                           b_scol[1] / 5,
                                           b_scol[2] / 5))
        ligths[2].diffuse_color = b_dcol_hm
        ligths[2].specular_color = b_scol
    
    if context.scene.solid_lights_protoshader_type == 'WAX':
        
        dir = context.scene.solid_lights_protoshader_direction
        rotation_euler1 = Euler((0, 0, 1), "XYZ")
        rotation_euler2 = Euler((0, 0, -1), "XYZ")
        back_dir1 = Vector((-dir.x * 2, -dir.y * 2, -dir.z + 0.9))
        back_dir1.rotate(rotation_euler1)
        back_dir2 = Vector((-dir.x * 2, -dir.y * 2, -dir.z + 0.9))
        back_dir2.rotate(rotation_euler2)
        ligths[0].direction = dir
        ligths[1].direction = back_dir1
        ligths[2].direction = back_dir2
        ligths[0].diffuse_color = f_dcol
        ligths[0].specular_color = f_scol
        ligths[1].diffuse_color = b_dcol_hp
        ligths[1].specular_color = b_scol
        ligths[2].diffuse_color = b_dcol_hm
        ligths[2].specular_color = b_scol
    
    if context.scene.solid_lights_protoshader_type == 'METAL':
        
        dir = context.scene.solid_lights_protoshader_direction
        rotation_euler1 = Euler((0, 0, 1), "XYZ")
        rotation_euler2 = Euler((0, 0, -1), "XYZ")
        back_dir1 = Vector((-dir.x * 2, -dir.y * 2, -dir.z + 0.5))
        back_dir1.rotate(rotation_euler1)
        back_dir2 = Vector((-dir.x * 2, -dir.y * 2, -dir.z + 0.5))
        back_dir2.rotate(rotation_euler2)
        ligths[0].direction = dir
        ligths[1].direction = back_dir1
        ligths[2].direction = back_dir2
        ligths[0].diffuse_color = Vector((f_dcol[0] * 1.2,
                                          f_dcol[1] * 1.2,
                                          f_dcol[2] * 1.2))
        ligths[0].specular_color = Vector((f_scol[0] * 2,
                                           f_scol[1] * 2,
                                           f_scol[2] * 2))
        ligths[1].diffuse_color = b_dcol_hp
        ligths[1].specular_color = Vector((f_scol[0] * 2,
                                           f_scol[1] * 2,
                                           f_scol[2] * 2))
        ligths[2].diffuse_color = b_dcol_hm
        ligths[2].specular_color = Vector((f_scol[0] * 2,
                                           f_scol[1] * 2,
                                           f_scol[2] * 2))
        
    return None

class SolidLights(bpy.types.Panel):
    bl_idname = "solid_lights"
    bl_label = "Solid Lights"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Lights"

    def draw(self, context):
        
        ligths = context.user_preferences.system.solid_lights
        
        layout = self.layout
        
        for ligth in ligths:
            col = layout.column()
            row = col.row()
            
            label_row = col.row(align = True)
            color_row = col.row(align = True)
            ligth_row = col.row(align = False)
            
            label_row.label("diffuse")
            label_row.label("specular")
            color_row.prop(ligth, "diffuse_color", text = "")
            color_row.prop(ligth, "specular_color", text = "")
            ligth_row.prop(ligth, "use", text = "", toggle = True, expand = True, icon = "LAMP")
            ligth_row.prop(ligth, "direction", text = "")

class SolidLightsProtoShader(bpy.types.Panel):
    bl_idname = "solid_lights_ProtoShader"
    bl_label = "Solid Lights protoshader"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Lights"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.prop(scene, "solid_ligths_protosahder_enable")
        layout.prop(scene, "solid_lights_protoshader_direction",
            text = "")
        layout.prop(scene, "solid_lights_protoshader_type",)
        row = layout.row()
        row.label("")
        row.label("Diffuse")
        row.label("Specular")
        row = layout.row()
        col = layout.column()
        row = col.row()
        row.label("Front")
        row.prop(scene, "solid_ligths_protoshader_front_diffcol", text = "")
        row.prop(scene, "solid_ligths_protoshader_front_speccol", text = "")
        row = col.row()
        row.label("back")
        row.prop(scene, "solid_ligths_protoshader_back_diffcol", text = "")
        row.prop(scene, "solid_ligths_protoshader_back_speccol", text = "")
        layout.prop(scene, "solid_ligths_protoshader_back_hueshift")

def register():
    bpy.utils.register_class(SolidLights)
    bpy.utils.register_class(SolidLightsProtoShader)
    bpy.types.Scene.solid_ligths_protosahder_enable = bpy.props.BoolProperty(
        name = "Enable Protoshader",
        default = False,
        update = protoshader_update)
    bpy.types.Scene.solid_lights_protoshader_type = bpy.props.EnumProperty(
        name = "Type",
        items = [("PLASTIC", "Plastic", "Plastic material"), 
                ("WAX", "Wax", "Wax scatter material"),
                ("METAL", "Metal", "Metalic material")],
        default = "PLASTIC",
        update = protoshader_update)
    
    bpy.types.Scene.solid_lights_protoshader_direction =\
        bpy.props.FloatVectorProperty(
        name = "Light Direction",
        default = (-0.1, 0.5, 1),
        subtype = "DIRECTION",
        min = 0,
        max = 1,
        update = protoshader_update)
    
    bpy.types.Scene.solid_ligths_protoshader_front_diffcol =\
        bpy.props.FloatVectorProperty(
        name = "Front Diffuse Color",
        default = (0.8, 0.8, 0.9),
        subtype = "COLOR",
        min = 0,
        max = 1,
        update = protoshader_update)
    
    bpy.types.Scene.solid_ligths_protoshader_back_diffcol =\
        bpy.props.FloatVectorProperty(
        name = "Back Diffuse Color",
        default = (0.32, 0.24, 0.24),
        subtype = "COLOR",
        min = 0,
        max = 1,
        update = protoshader_update)
    
    bpy.types.Scene.solid_ligths_protoshader_front_speccol =\
        bpy.props.FloatVectorProperty(
        name = "Front Specular Color",
        default = (0.45, 0.45, 0.51),
        subtype = "COLOR",
        min = 0,
        max = 1,
        update = protoshader_update)
    
    bpy.types.Scene.solid_ligths_protoshader_back_speccol =\
        bpy.props.FloatVectorProperty(
        name = "Back Specular Color",
        default = (0.045, 0.029, 0.028),
        subtype = "COLOR",
        min = 0,
        max = 1,
        update = protoshader_update)
    bpy.types.Scene.solid_ligths_protoshader_back_hueshift =\
        bpy.props.FloatVectorProperty(
        name = "Hue Shift",
        default = (0.398, 0.463, 0.495),
        subtype = "COLOR",
        min = 0,
        max = 1,
        update = protoshader_update)

def unregister():
    bpy.utils.unregister_class(SolidLights)
    bpy.utils.unregister_class(SolidLightsProtoShader)
    del bpy.types.Scene.solid_ligths_protosahder_enable
    del bpy.types.Scene.solid_lights_protoshader_type
    del bpy.types.Scene.solid_lights_protoshader_direction
    
    del bpy.types.Scene.solid_ligths_protoshader_front_diffcol
    del bpy.types.Scene.solid_ligths_protoshader_back_diffcol
    del bpy.types.Scene.solid_ligths_protoshader_front_speccol
    del bpy.types.Scene.solid_ligths_protoshader_back_speccol
    del bpy.types.Scene.solid_ligths_protoshader_back_hueshift

if __name__ == "__main__":
    register()
