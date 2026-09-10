# repro_egl_texture.py
# import pkgutil
import numpy as np
import pybullet as p
import pybullet_data
from PIL import Image


def render(use_egl, output):
    cid = p.connect(p.DIRECT)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    if use_egl:
        # egl = pkgutil.get_loader("eglRenderer")
        plugin_id = p.loadPlugin(
            "/home/iadc/bullet3/bin/libpybullet_eglRendererPlugin_PhyDomain_py39_gmake_x64_release.so",
            "_eglRendererPlugin",
            physicsClientId=cid,
        )

    # plane.urdf already has checker_blue.png
    plane = p.loadURDF("plane.urdf")

    # Dynamically replace it
    tex = p.loadTexture("tex256.png")
    p.changeVisualShape(plane, -1, textureUniqueId=tex)

    view = p.computeViewMatrix(
        [0, 0, 3],
        [0, 0, 0],
        [0, 1, 0],
    )
    proj = p.computeProjectionMatrixFOV(
        60, 1.0, 0.1, 10,
    )

    _, _, rgba, _, _ = p.getCameraImage(
        512,
        512,
        viewMatrix=view,
        projectionMatrix=proj,
        renderer=(
            p.ER_BULLET_HARDWARE_OPENGL
            if use_egl
            else p.ER_TINY_RENDERER
        ),
    )

    rgba = np.asarray(rgba, dtype=np.uint8).reshape(512, 512, 4)
    Image.fromarray(rgba).save(output)
    p.disconnect()


render(False, "tiny.png")
render(True, "egl.png")