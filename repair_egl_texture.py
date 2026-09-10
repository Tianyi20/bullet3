import pybullet as p

cid = p.connect(p.DIRECT)

plugin_id = p.loadPlugin(
    "/home/iadc/bullet3/bin/libpybullet_eglRendererPlugin_gmake_x64_release.so",
    "_eglRendererPlugin",
    physicsClientId=cid,
)

if plugin_id < 0:
    raise RuntimeError("Failed to load patched EGL renderer")

from repro_egl_texture import render

render(False, "tiny.png")
render(True, "egl.png")