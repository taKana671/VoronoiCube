import sys

from panda3d.core import Point3, NodePath, Vec3, Vec2
from panda3d.core import TextureStage, AntialiasAttrib, TransparencyAttrib, Texture
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock

from shapes import Box


class VoronoiCube(ShowBase):

    def __init__(self):
        super().__init__()
        self.disable_mouse()
        self.render.set_antialias(AntialiasAttrib.MAuto)

        self.camera_root = NodePath('camera_root')
        self.camera_root.reparent_to(self.render)

        self.camera.set_pos(0, -100, 50)
        # self.camera.set_pos(0, 100, 50)
        self.camera.look_at(Point3(0, 0, 0))
        self.camera.reparent_to(self.camera_root)

        self.dragging = False
        self.before_mouse_pos = None
        self.show_wireframe = False

        self.accept('d', self.toggle_wireframe)
        self.accept('mouse1', self.mouse_click)
        self.accept('mouse1-up', self.mouse_release)
        self.accept('escape', sys.exit)
        self.task_mgr.add(self.update, 'update')

        self.create_box()
        # self.create_vertices()

    def toggle_wireframe(self):
        if self.show_wireframe:
            self.box.set_render_mode_filled()
        else:
            self.box.set_render_mode_wireframe()

        # self.toggle_wireframe()
        self.show_wireframe = not self.show_wireframe

    def change_uv(self, segs):
        points = (segs + 1) * (segs + 1)

        # bottom
        u_end, v_end = 1 / 4, 1 / 2

        for i in range(points):
            u = u_end - (segs - i % (segs + 1)) * (0.25 / segs)
            v = v_end - i // (segs + 1) * (0.5 / segs)
            yield (u, v)

        # top
        u_end, v_end = 1 / 2, 1 / 2

        for i in range(points):
            u = u_end - (segs - i % (segs + 1)) * (0.25 / segs)
            v = v_end - (segs - i // (segs + 1)) * (0.5 / segs)
            yield (u, v)

        # back
        u_end, v_end = 1 / 4, 1

        for i in range(points):
            u = u_end - (segs - i // (segs + 1)) * (0.25 / segs)
            v = v_end - (segs - i % (segs + 1)) * (0.5 / segs)
            yield (u, v)

        # front
        u_end, v_end = 0.5, 1

        for i in range(points):
            u = u_end - i // (segs + 1) * (0.25 / segs)
            v = v_end - (segs - i % (segs + 1)) * (0.5 / segs)
            yield (u, v)

        # left
        u_end, v_end = 0.75, 1

        for i in range(points):
            u = u_end - i % (segs + 1) * (0.25 / segs)
            v = v_end - (segs - i // (segs + 1)) * (0.5 / segs)
            yield (u, v)

        # right
        u_end, v_end = 1.0, 1.0

        for i in range(points):
            u = u_end - (segs - i % (segs + 1)) * (0.25 / segs)
            v = v_end - (segs - i // (segs + 1)) * (0.5 / segs)
            yield (u, v)

    def create_box(self):
        segs = 4
        stride = 12
        box = Box(width=30, depth=30, height=30, segs_d=segs, segs_w=segs, segs_z=segs).create()
        box.set_pos_hpr(Point3(0, 0, 0), Vec3(0, 0, 0))
        box.reparent_to(self.render)
        box.set_transparency(TransparencyAttrib.MAlpha)
        # box.set_scale(0.1)

        geom_node = box.node()
        geom = geom_node.modify_geom(0)
        vdata = geom.modify_vertex_data()
        vdata_arr = vdata.modify_array(0)
        vdata_mem = memoryview(vdata_arr).cast('B').cast('f')

        for i, (u, v) in enumerate(self.change_uv(segs)):
            idx = i * stride
            vdata_mem[idx + 10] = u
            vdata_mem[idx + 11] = v
            # print(f"u: {u}, v: {v}")

        tex = self.loader.load_texture('atras.png')
        # voronoi = VoronoiEdges()
        # image_generator = TextureAtlasGenerator(voronoi.vmix3)
        # t = random.uniform(0, 1000)
        # img = image_generator.generate_texture(t)
        # img = cv2.rotate(img, cv2.ROTATE_180)
        # img = cv2.flip(img, 1)

        # tex = Texture('image')
        # tex.setup_2d_texture(
        #     256 * 4,
        #     256 * 2,
        #     Texture.T_unsigned_byte,
        #     Texture.F_rgb
        # )

        # tex.set_ram_image(img)

        # read documents！
        tex.setWrapU(Texture.WM_clamp)
        tex.setWrapV(Texture.WM_clamp)
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        box.set_texture(tex)
        box.set_tex_hpr(TextureStage.get_default(), -180)

        # box.hprInterval(20, (720, 0, 0)).start()
        self.box = box
        # self.box.hprInterval(20, 360).loop()

    def mouse_click(self):
        self.dragging = True
        self.dragging_start_time = globalClock.get_frame_time()

    def mouse_release(self):
        self.dragging = False
        self.before_mouse_pos = None

    def rotate_camera(self, mouse_pos, dt):
        if self.before_mouse_pos:
            angle = Vec3()

            if (delta := mouse_pos.x - self.before_mouse_pos.x) < 0:
                angle.x += 180
            elif delta > 0:
                angle.x -= 180

            if (delta := mouse_pos.y - self.before_mouse_pos.y) < 0:
                angle.z -= 180
            elif delta > 0:
                angle.z += 180

            angle *= dt
            self.camera_root.set_hpr(self.camera_root.get_hpr() + angle)

        self.before_mouse_pos = Vec2(mouse_pos.xy)

    def update(self, task):
        dt = globalClock.get_dt()

        if self.mouseWatcherNode.has_mouse():
            mouse_pos = self.mouseWatcherNode.get_mouse()

            if self.dragging:
                if globalClock.get_frame_time() - self.dragging_start_time >= 0.2:
                    self.rotate_camera(mouse_pos, dt)

        return task.cont



if __name__ == '__main__':
    app = VoronoiCube()
    app.run()