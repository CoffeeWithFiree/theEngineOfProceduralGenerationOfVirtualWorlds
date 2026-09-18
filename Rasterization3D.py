from Rasterization2D import Rasterization2D
from settings import settings

class Rasterization3D:
    #Persp Equel
    def __init__(self, main, pg, np):
        self.pg = pg
        self.main = main
        self.np = np

        # The viewing window has a size of Vw by Vh at a distance "d" from the camera
        self.Vw = settings.Vw
        self.Vh = settings.Vh

        # Cw, Ch: the viewing window
        self.d = settings.d
        self.Cw = settings.Cw
        self.Ch = settings.Ch

        self.screen = self.pg.display.set_mode((self.Vw, self.Vh))
        self.graphic = Rasterization2D(self.screen, self.pg)

    def ViewportToCanvas(self, x, y):
        return (x * self.Cw / self.Vw, y * self.Ch / self.Vh)

    def ProjectVertex(self, v):
        """V[0]: v.x; V[1]: v.y; V[2]: v.z"""
        return self.ViewportToCanvas(v[0] * self.d / v[2], v[1] * self.d / v[2])

    #Poligon render

    def RenderObject(self, vertices, triangles):
        projected = dict()
        for key, item in vertices.items():
            projected[key] = self.ProjectVertex(item)

        for T in triangles.values():
            self.RenderTriangle(T, projected)

    def RenderTriangle(self, triangle, projected):
        projected_coords = []
        for key in triangle.keys():
            if key != "color":
                projected_coords.append(projected[key])
        self.graphic.DrawTriangle(projected_coords[0], projected_coords[1], projected_coords[2], triangle["color"])


    ###Drawing all scene with several objects

    def RenderScene(self, objects):
        """object's characteristics: coordinates and size with center (0, 0, 0) (with verticles and triangles)"""
        for i in objects.values():  # Все объекты в сцене
            self.RenderInstance(i)

    def RenderInstance(self, object):
        """Render every object after translation"""
        projected = []
        for v in object["vertices"].values():
            V_coordinates = v + object["position"]
            projected.append(self.ProjectVertex(V_coordinates))

        for t in object["triangles"].values():
            self.RenderTriangle(t, projected)

    ###Drawing several objects with transforms

    def RenderSceneV2(self, objects):
        """object's characteristics: coordinates and size with center (0, 0, 0) (with verticles and triangles)"""
        for i in objects.values():  # Все объекты в сцене
            self.RenderInstanceV2(i)

    def RenderInstanceV2(self, object):
        projected = []
        for v in object["vertices"].values():
            V_trans = self.ApplyTransforms(v, object["transforms"])
            projected.append(self.ProjectVertex(V_trans))

        for t in object["triangles"].values():
            self.RenderTriangle(t, projected)

    def ApplyTransforms(self, vertex, transform):
        scaled = self.Scale(vertex, transform["scale"])
        rotated = self.Rotate(scaled, transform["rotation"])
        traslated = self.Translate(rotated, transform["translation"])
        return traslated
        ###

    def Scale(self, vertex, scale):
        """scale one vertex"""
        return vertex * scale

    def Rotate(self, scale, rotation):
        """Rotation one vertex"""

        #Matrix of the rotation around axis X
        Rx = self.np.array([
            [1, 0, 0],
            [0, self.np.cos(rotation[0]), -self.np.sin(rotation[0])],
            [0, self.np.sin(rotation[0]), self.np.cos(rotation[0])]
        ])

        # Matrix of the rotation around axis Y
        Ry = self.np.array([
            [self.np.cos(rotation[1]), 0, self.np.sin(rotation[1])],
            [0, 1, 0],
            [-self.np.sin(rotation[1]), 0, self.np.cos(rotation[1])]
        ])

        #Matrix of the rotation around axis Z
        Rz = self.np.array([
            [self.np.cos(rotation[2]), -self.np.sin(rotation[2]), 0],
            [self.np.sin(rotation[2]), self.np.cos(rotation[2]), 0],
            [0, 0, 1]
        ])

        R = Rz @ Ry @ Rx

        return R @ scale

    def Translate(self, rotation, translation):
        """translation one vertex"""
        return rotation + translation