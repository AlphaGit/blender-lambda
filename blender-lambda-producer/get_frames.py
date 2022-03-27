import bpy

scene = bpy.context.scene
if scene:
    print('Scene found.')

print(f"Frame range: {scene.frame_start}-{scene.frame_end}")
