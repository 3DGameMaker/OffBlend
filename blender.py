import bpy
import socket
import json
from mathutils import Vector, Matrix

CAMERA_NAME = "Camera"
PLANE_NAME = "Plane"
OFFSET = Vector((0.0, 0.0, 2.0))  # Move back behind head
ALPHA = 0.15  # smoothing

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 9001))
sock.setblocking(False)

cam = bpy.data.objects.get(CAMERA_NAME)
plane = bpy.data.objects.get(PLANE_NAME)
smoothed_pos = Vector((0.0, 0.0, 0.0))

def get_lens_shift(camera, bl, br, tl, resx, resy):
    vr = br - bl
    vu = tl - bl
    vr.normalize(); vu.normalize()
    assert abs(vr.dot(vu)) < 1e-4, "Plane isn't rectangular"
    vn = vr.cross(vu).normalized()

    va = bl - camera.location
    vb = br - camera.location
    vc = tl - camera.location
    d = -va.dot(vn)
    near = camera.data.clip_start
    l = vr.dot(va) * near / d
    r = vr.dot(vb) * near / d
    b = vu.dot(va) * near / d
    t = vu.dot(vc) * near / d

    # camera rotation
    quat_u = Vector((0,1,0)).rotation_difference(vu)
    quat_n = (quat_u @ Vector((0,0,1))).rotation_difference(vn)
    mat = (quat_n @ quat_u).to_matrix().to_4x4()
    mat.translation = camera.location

    # lens shift
    sensor_fit = camera.data.sensor_fit
    if sensor_fit == 'AUTO':
        sensor_fit = 'HORIZONTAL' if resx >= resy else 'VERTICAL'
    viewfac = resx if sensor_fit == 'HORIZONTAL' else resy * (camera.data.sensor_height / camera.data.sensor_width)
    sensor_size = camera.data.sensor_width if sensor_fit == 'HORIZONTAL' else camera.data.sensor_height
    lens = (sensor_size * near) / viewfac * resx / (r - l)
    shift_x = resx*(l+r)/(r-l)/2 / viewfac
    shift_y = resy*(t+b)/(t-b)/2 / viewfac

    return mat, lens, (shift_x, shift_y)

def update_camera():
    global smoothed_pos

    try:
        data, _ = sock.recvfrom(1024)
        pos = json.loads(data.decode())

        raw_pos = Vector((
            -(pos['x'] - 0.5) * 4,
            (0.5 - pos['y']) * 3,
            (-pos['z']) * 10
        ))


        smoothed_pos = smoothed_pos.lerp(raw_pos, ALPHA)
        cam.location = smoothed_pos + OFFSET

        # Update off-axis projection
        verts = [plane.matrix_world @ v.co for v in plane.data.vertices[:3]]
        bl, br, tl = verts
        resx = bpy.context.scene.render.resolution_x
        resy = bpy.context.scene.render.resolution_y
        mat, lens, (shift_x, shift_y) = get_lens_shift(cam, bl, br, tl, resx, resy)

        cam.matrix_world = mat
        cam.data.type = 'PERSP'
        cam.data.lens = lens
        cam.data.shift_x = shift_x
        cam.data.shift_y = shift_y

    except BlockingIOError:
        pass
    except Exception as e:
        print("Error:", e)

    return 0.01

bpy.app.timers.register(update_camera, persistent=True)
print("✅ Live off-axis tracking with projection started.")
