import sys
import bpy

argv = sys.argv
argv = argv[argv.index("--") + 1:]

input_file = argv[0]
output_file = argv[1]
frame_number = int(argv[2])

bpy.ops.wm.open_mainfile(filepath=input_file, load_ui=False)

bpy.context.scene.frame_set(frame_number)
bpy.context.scene.render.filepath = output_file

bpy.ops.render.render(write_still = True)
