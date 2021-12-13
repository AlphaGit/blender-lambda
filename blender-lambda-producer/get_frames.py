import bpy

scene = bpy.context.scene
print(f"Frame range: {scene.frame_start}-{scene.frame_end}")
