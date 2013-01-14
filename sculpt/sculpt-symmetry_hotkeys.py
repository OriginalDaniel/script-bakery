bl_info = {
    "name": "Sculpting Tools",
    "description": "Provides tools and hotkeys for accellerating the sculpt workflow",
    "author": "Jonathan Williamson",
    "version": (0,1),
    "blender": (2, 6, 5),
    "category": "3D View",
}
  
import bpy




### ------------ New Operators ------------ ###

### creates an operator for applying subsurf modifiers ###
class applySubsurf(bpy.types.Operator):
    bl_label = "Apply Only Subsurf Modifiers"
    bl_idname = "object.apply_subsurf"
    bl_options = {'REGISTER', 'UNDO'}
    
    # test if it is possible to apply a subsurf modifier, thanks to Richard Van Der Oost
    @classmethod    
    def poll(cls, context):
       
       # get the active object
       obj = scene.objects.active
       
       # test if there's an active object
       if obj:
           
           # find modifiers with "SUBSURF" type
           for mod in obj.modifiers:
               if mod.type == 'SUBSURF':
                   return True
       return False
    
    def execute(self, context):
        
        #check for active object
        obj = context.scene.objects.active
        
        applyModifier = bpy.ops.object.modifier_apply
        
        # If any subsurf modifiers exist on object, apply them.
        for mod in obj.modifiers:
            if mod.type=='SUBSURF':

        # Old code that was dependent on names, rather than type. So if the modifier was renamed it would fail.
#        for mod in obj.modifiers:
#            if "Subsurf" in mod.name:
                print (mod)
                applyModifier(apply_as='DATA', modifier=mod.name)
        return {"FINISHED"}


### Creating operators for toggling Sculpt Symmetry ###

class sculptSymmetryX(bpy.types.Operator):
    bl_label = "Toggle X-axis Symmetry"
    bl_idname = "sculpt.symmetry_x"
    
    def execute(self, context):
       
       # checks the current state of x-axis symmetry then toggles it. 
        symmetry_x = bpy.context.tool_settings.sculpt.use_symmetry_x
        if symmetry_x:
            context.tool_settings.sculpt.use_symmetry_x = False
        else:
            context.tool_settings.sculpt.use_symmetry_x = True
        
        return {"FINISHED"}

class sculptSymmetryY(bpy.types.Operator):
    bl_label = "Toggle Y-axis Symmetry"
    bl_idname = "sculpt.symmetry_y"
    
    def execute(self, context):
        
        symmetry_y = bpy.context.tool_settings.sculpt.use_symmetry_y
        if symmetry_y:
            context.tool_settings.sculpt.use_symmetry_y = False
        else:
            context.tool_settings.sculpt.use_symmetry_y = True
        
        return {"FINISHED"}   
    
class sculptSymmetryZ(bpy.types.Operator):
    bl_label = "Toggle Z-axis Symmetry"
    bl_idname = "sculpt.symmetry_z"
    
    def execute(self, context):
        
        symmetry_z = bpy.context.tool_settings.sculpt.use_symmetry_z
        if symmetry_z:
            context.tool_settings.sculpt.use_symmetry_z = False
        else:
            context.tool_settings.sculpt.use_symmetry_z = True
        
        return {"FINISHED"}       
        
 



### ------------ New Menus ------------ ###        
        
# creates a menu for Sculpt mode tools
class JWSculptTools(bpy.types.Menu):
    bl_label = "Jonathan's Sculpt Tools"
    bl_idname = "sculpt.tools_menu"

    def draw(self, context):
        layout = self.layout
        
        layout.operator("object.modifier_add", 'Add Subsurf', icon='MOD_SUBSURF').type='SUBSURF'
        layout.operator("object.apply_subsurf", 'Apply Subsurf', icon='MOD_SUBSURF')
        
        layout.separator()
        
        layout.operator("sculpt.symmetry_x", icon='MOD_MIRROR')
        layout.operator("sculpt.symmetry_y")
        layout.operator("sculpt.symmetry_z")     





### ------------ New Hotkeys and registration ------------ ###   

addon_keymaps = []

def register():
    bpy.utils.register_class(JWSculptTools)
    bpy.utils.register_class(sculptSymmetryX)
    bpy.utils.register_class(sculptSymmetryY)
    bpy.utils.register_class(sculptSymmetryZ)
    bpy.utils.register_class(applySubsurf)
    
    wm = bpy.context.window_manager
        
    # create the Sculpt hotkeys
    km = wm.keyconfigs.addon.keymaps.new(name='Sculpt', space_type='EMPTY')
    kmi = km.keymap_items.new('sculpt.symmetry_x', 'X', 'PRESS', shift=True)
    kmi = km.keymap_items.new('sculpt.symmetry_y', 'Y', 'PRESS', shift=True)
    kmi = km.keymap_items.new('sculpt.symmetry_z', 'Z', 'PRESS', shift=True)
    
    # create sculpt menu hotkey
    kmi = km.keymap_items.new('wm.call_menu', 'T', 'PRESS', oskey=True)
    kmi.properties.name = 'sculpt.tools_menu' 
    
    addon_keymaps.append(km)
    
def unregister():

    #unregister the new operators 
    bpy.utils.unregister_class(JWSculptTools)
    bpy.utils.register_class(sculptSymmetryX)
    bpy.utils.register_class(sculptSymmetryY)
    bpy.utils.register_class(sculptSymmetryZ)
    bpy.utils.register_class(applySubsurf)
    
    # remove keymaps when add-on is deactivated
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    del addon_keymaps[:]
    
if __name__ == "__main__":
    register()
    