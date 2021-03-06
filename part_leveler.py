import sys
import bpy
import time
import os

argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"

print(argv) 

folder_name = argv[0]
counter = 0

if '--windows' in argv:
    slash_style = '\\'
elif '--unix' in argv:
    slash_style = '/'
else:
    print("Please choose a path style by appending --windows or --unix.")
    exit()

if '--in_place' in argv:
    in_place = True
else:
    in_place = False

for filename in os.listdir(folder_name):
    if filename.endswith(".stl") and 'leveled_' not in filename:
        counter += 1
        print("({} of {}) processing {}...".format(counter, len(os.listdir(folder_name)), filename))
        #for good measure, delete everything
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

        #create a plane and assign properties
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.transform.resize(value=(40, 40, 40))
        bpy.ops.rigidbody.object_add()
        bpy.context.object.rigid_body.mass = 1000
        bpy.context.object.rigid_body.type = 'PASSIVE'
        bpy.ops.object.select_all(action='DESELECT')

        #import stl and assign properties
        file_path = folder_name + slash_style + filename
        export_file_path = folder_name + slash_style + 'leveled_' + filename
        bpy.ops.import_mesh.stl(filepath = file_path)
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME')
        bpy.context.object.location[0] = 0
        bpy.context.object.location[1] = 0
        z_size = int(bpy.context.object.dimensions[2])
        bpy.context.object.location[2] = (z_size / 2) + 2
        bpy.ops.rigidbody.object_add()
        bpy.context.object.rigid_body.mass = 1000

        #simulate 249 frames of animation
        bpy.context.scene.frame_current = 249
        bpy.ops.ptcache.bake_all(bake=False)

        #export settled mesh in place
        if not in_place:
            bpy.ops.export_mesh.stl(filepath = export_file_path, use_selection = True)
        else:
            bpy.ops.export_mesh.stl(filepath = file_path, use_selection = True)

        #delete everything again in preparation for the next stl
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
print("Finished leveling {} parts.".format(counter))
