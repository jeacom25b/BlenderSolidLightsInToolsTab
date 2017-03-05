'''
Copyright (C) 2017 Jean Da Costa Machado
jean3dimenshonal@gmail.com

Created by Jean Da Costa Machado

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
'''

bl_info = {
    "name": "Solid Lights studio",
    "description": "utilities for solid shading",
    "author": "Jean Da Costa Machado",
    "version": (0, 0, 1),
    "blender": (2, 78, 0),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Render"}

import bpy
from bpy import context
from mathutils import Vector
from mathutils import Euler


def studio_update(self, context):
    if context.scene.solid_lights_studio_enable == False:
        return None
    
    lights = context.user_preferences.system.solid_lights
    scene = context.scene
    f_dcol = scene.solid_lights_studio_front_diffcol
    f_scol = scene.solid_lights_studio_front_speccol
    b_dcol = scene.solid_lights_studio_back_diffcol
    b_scol = scene.solid_lights_studio_back_speccol
    h_shift = scene.solid_lights_studio_back_hueshift
    
    b_dcol_hp = Vector((b_dcol[0] + (h_shift[0] - 0.5) * 0.5,
                        b_dcol[1] + (h_shift[1] - 0.5) * 0.5,
                        b_dcol[2] + (h_shift[2] - 0.5) * 0.5))
    
    b_dcol_hm = Vector((b_dcol[0] - (h_shift[0] - 0.5) * 0.5,
                        b_dcol[1] - (h_shift[1] - 0.5) * 0.5,
                        b_dcol[2] - (h_shift[2] - 0.5) * 0.5))
    
    f_dcol_hp = Vector((f_dcol[0] * 0.7 + (h_shift[0] - 0.5),
                        f_dcol[1] * 0.7 + (h_shift[1] - 0.5),
                        f_dcol[2] * 0.7 + (h_shift[2] - 0.5)))
    
    f_dcol_hm = Vector((f_dcol[0] * 0.7 - (h_shift[0] - 0.5),
                        f_dcol[1] * 0.7 - (h_shift[1] - 0.5),
                        f_dcol[2] * 0.7 - (h_shift[2] - 0.5)))
    
    if context.scene.solid_lights_studio_type == '2K1F':
        dir = context.scene.solid_lights_studio_direction
        back_dir = Vector((-dir.x, -dir.y, -dir.z + 1))
        fill_dir = Vector((dir.x, dir.y, dir.z + 0.5))
        lights[0].direction = dir
        lights[1].direction = fill_dir
        lights[2].direction = back_dir
        lights[0].diffuse_color = f_dcol
        lights[0].specular_color = Vector((f_scol[0] / 2,
                                           f_scol[1] / 2,
                                           f_scol[2] / 2,))
        lights[1].diffuse_color = Vector((
            b_dcol_hp[0] * 0.25 + f_dcol[0] * 0.25,
            b_dcol_hp[1] * 0.25 + f_dcol[1] * 0.25,
            b_dcol_hp[2] * 0.25 + f_dcol[2] * 0.25))
        lights[1].specular_color = Vector((b_scol[0] / 5,
                                           b_scol[1] / 5,
                                           b_scol[2] / 5))
        lights[2].diffuse_color = b_dcol_hm
        lights[2].specular_color = b_scol
    
    if context.scene.solid_lights_studio_type == '1K2FW':
        
        dir = context.scene.solid_lights_studio_direction
        rotation_euler1 = Euler((0, 0, 1), "XYZ")
        rotation_euler2 = Euler((0, 0, -1), "XYZ")
        back_dir1 = Vector((-dir.x * 2, -dir.y * 2, -dir.z + 0.9))
        back_dir1.rotate(rotation_euler1)
        back_dir2 = Vector((-dir.x * 2, -dir.y * 2, -dir.z + 0.9))
        back_dir2.rotate(rotation_euler2)
        lights[0].direction = dir
        lights[1].direction = back_dir1
        lights[2].direction = back_dir2
        lights[0].diffuse_color = f_dcol
        lights[0].specular_color = f_scol
        lights[1].diffuse_color = b_dcol_hp
        lights[1].specular_color = b_scol
        lights[2].diffuse_color = b_dcol_hm
        lights[2].specular_color = b_scol
    
    if context.scene.solid_lights_studio_type == '1K2FM':
        
        dir = context.scene.solid_lights_studio_direction
        rotation_euler1 = Euler((0, 0, 1), "XYZ")
        rotation_euler2 = Euler((0, 0, -1), "XYZ")
        back_dir1 = Vector((-dir.x * 2, -dir.y * 2, -dir.z + 0.5))
        back_dir1.rotate(rotation_euler1)
        back_dir2 = Vector((-dir.x * 2, -dir.y * 2, -dir.z + 0.5))
        back_dir2.rotate(rotation_euler2)
        lights[0].direction = dir
        lights[1].direction = back_dir1
        lights[2].direction = back_dir2
        lights[0].diffuse_color = Vector((f_dcol[0] * 1.2,
                                          f_dcol[1] * 1.2,
                                          f_dcol[2] * 1.2))
        lights[0].specular_color = Vector((f_scol[0] * 2,
                                           f_scol[1] * 2,
                                           f_scol[2] * 2))
        lights[1].diffuse_color = b_dcol_hp
        lights[1].specular_color = Vector((f_scol[0] * 2,
                                           f_scol[1] * 2,
                                           f_scol[2] * 2))
        lights[2].diffuse_color = b_dcol_hm
        lights[2].specular_color = Vector((f_scol[0] * 2,
                                           f_scol[1] * 2,
                                           f_scol[2] * 2))
    
    if context.scene.solid_lights_studio_type == '1K2F':
        
        dir = context.scene.solid_lights_studio_direction
        rotation_euler1 = Euler((0, 0, 1.69296), "XYZ")
        rotation_euler2 = Euler((0, 0, -1.69296), "XYZ")
        back_dir1 = Vector((dir.x * 2, dir.y * 2, 0.5))
        back_dir1.rotate(rotation_euler1)
        back_dir2 = Vector((dir.x * 2, dir.y * 2, 0.5))
        back_dir2.rotate(rotation_euler2)
        lights[0].direction = dir
        lights[1].direction = back_dir1
        lights[2].direction = back_dir2
        lights[0].diffuse_color = f_dcol
        lights[0].specular_color = f_scol
        lights[1].diffuse_color = b_dcol_hp
        lights[1].specular_color = b_scol
        lights[2].diffuse_color = b_dcol_hm
        lights[2].specular_color = b_scol

    if context.scene.solid_lights_studio_type == '2K1FR':
        
        dir = context.scene.solid_lights_studio_direction
        dir = context.scene.solid_lights_studio_direction
        rotation_euler1 = Euler((0, 0, 0.5), "XYZ")
        rotation_euler2 = Euler((0, 0, -0.5), "XYZ")
        front_dir1 = Vector((dir.x * 1.3, dir.y * 1.3, dir.z))
        front_dir1.rotate(rotation_euler1)
        front_dir2 = Vector((dir.x * 1.3, dir.y * 1.3, dir.z))
        front_dir2.rotate(rotation_euler2)
        back_dir = Vector((-dir.x, -dir.y, -dir.z + 1))
        lights[0].direction = front_dir1
        lights[1].direction = front_dir2
        lights[2].direction = back_dir
        lights[0].diffuse_color = f_dcol_hm
        lights[0].specular_color = f_scol
        lights[1].diffuse_color = f_dcol_hp
        lights[1].specular_color = b_scol
        lights[2].diffuse_color = b_dcol
        lights[2].specular_color = b_scol
    
    return None


class SolidLights(bpy.types.Panel):
    bl_idname = "solid_lights"
    bl_label = "Solid Lights"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Lights"
    
    def draw(self, context):
        
        lights = context.user_preferences.system.solid_lights
        
        layout = self.layout
        
        for light in lights:
            col = layout.column()
            row = col.row()
            
            label_row = col.row(align = True)
            color_row = col.row(align = True)
            light_row = col.row(align = False)
            
            label_row.label("diffuse")
            label_row.label("specular")
            color_row.prop(light, "diffuse_color", text = "")
            color_row.prop(light, "specular_color", text = "")
            light_row.prop(light, "use",
                           text = "",
                           toggle = True,
                           expand = True,
                           icon = "LAMP")
            light_row.prop(light, "direction", text = "")


class SolidLightsStudio(bpy.types.Panel):
    bl_idname = "solid_lights_studio"
    bl_label = "Solid Lights studio"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Lights"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.prop(scene, "solid_lights_studio_enable")
        layout.prop(scene, "solid_lights_studio_direction",
                    text = "")
        layout.prop(scene, "solid_lights_studio_type", )
        row = layout.row()
        row.label("")
        row.label("Diffuse")
        row.label("Specular")
        row = layout.row()
        col = layout.column()
        row = col.row()
        row.label("Front")
        row.prop(scene, "solid_lights_studio_front_diffcol", text = "")
        row.prop(scene, "solid_lights_studio_front_speccol", text = "")
        row = col.row()
        row.label("back")
        row.prop(scene, "solid_lights_studio_back_diffcol", text = "")
        row.prop(scene, "solid_lights_studio_back_speccol", text = "")
        layout.prop(scene, "solid_lights_studio_back_hueshift")


def register():
    bpy.utils.register_class(SolidLights)
    bpy.utils.register_class(SolidLightsStudio)
    bpy.types.Scene.solid_lights_studio_enable = \
        bpy.props.BoolProperty(
                name = "Enable studio",
                default = False,
                update = studio_update)
    bpy.types.Scene.solid_lights_studio_type = \
        bpy.props.EnumProperty(
                name = "Type",
                items = [("2K1F", "2Keys 1Fill", "Plastic Like material"),
                         ("1K2FW", "Wax 1Key 2Fill", "Fake Wax scatter material"),
                         ("1K2FM", "Metallic 1Key 2Fill", "Metallic material"),
                         ("1K2F", "1Key 2Fill", "Smooth Diffuse Material"),
                         ("2K1FR", "2keys 1fill Rotated", "Flat Diffuse Material")],
                default = "2K1F",
                update = studio_update)
    
    bpy.types.Scene.solid_lights_studio_direction = \
        bpy.props.FloatVectorProperty(
                name = "Light Direction",
                default = (-0.1, 0.5, 1),
                subtype = "DIRECTION",
                min = 0,
                max = 1,
                update = studio_update)
    
    bpy.types.Scene.solid_lights_studio_front_diffcol = \
        bpy.props.FloatVectorProperty(
                name = "Front Diffuse Color",
                default = (0.8, 0.8, 0.9),
                subtype = "COLOR",
                min = 0,
                max = 1,
                update = studio_update)
    
    bpy.types.Scene.solid_lights_studio_back_diffcol = \
        bpy.props.FloatVectorProperty(
                name = "Fill Diffuse Color",
                default = (0.32, 0.24, 0.24),
                subtype = "COLOR",
                min = 0,
                max = 1,
                update = studio_update)
    
    bpy.types.Scene.solid_lights_studio_front_speccol = \
        bpy.props.FloatVectorProperty(
                name = "Front Specular Color",
                default = (0.45, 0.45, 0.51),
                subtype = "COLOR",
                min = 0,
                max = 1,
                update = studio_update)
    
    bpy.types.Scene.solid_lights_studio_back_speccol = \
        bpy.props.FloatVectorProperty(
                name = "Fill Specular Color",
                default = (0.045, 0.029, 0.028),
                subtype = "COLOR",
                min = 0,
                max = 1,
                update = studio_update)
    bpy.types.Scene.solid_lights_studio_back_hueshift = \
        bpy.props.FloatVectorProperty(
                name = "Hue Shift",
                default = (0.398, 0.463, 0.495),
                subtype = "COLOR",
                min = 0,
                max = 1,
                update = studio_update)


def unregister():
    bpy.utils.unregister_class(SolidLights)
    bpy.utils.unregister_class(SolidLightsStudio)
    del bpy.types.Scene.solid_lights_studio_enable
    del bpy.types.Scene.solid_lights_studio_type
    del bpy.types.Scene.solid_lights_studio_direction
    
    del bpy.types.Scene.solid_lights_studio_front_diffcol
    del bpy.types.Scene.solid_lights_studio_back_diffcol
    del bpy.types.Scene.solid_lights_studio_front_speccol
    del bpy.types.Scene.solid_lights_studio_back_speccol
    del bpy.types.Scene.solid_lights_studio_back_hueshift


if __name__ == "__main__":
    register()
