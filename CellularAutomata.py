from settings import settings
from BiomesType import BiomesType
from DayAndNight import DayAndNight
import random

class CellularAutomata():
    def __init__(self, main, pg, np, graphic3D):
        self.main = main
        self.pg = pg
        self.np = np
        self.graphic3D = graphic3D

        self.matrix = self.CreateStartMatrix()

        for _ in range(100):
            self.matrix = DayAndNight.NextGenerationLands(self.matrix, settings.width, settings.length, BiomesType.sea, BiomesType.land)

    def CreateStartMatrix(self):
        Res_x = settings.width  #Right
        Res_y = settings.height  #Up
        Res_z = settings.length  #forward

        matrix = self.np.zeros((Res_x, Res_y, Res_z))  #y-axis fixation: matrix[:, y, :]

        for x in range(Res_x):
            for z in range(Res_z):
                ver = 50
                r = random.randint(1, 100)
                if r > ver:
                    matrix[x, 0, z] = BiomesType.land
                else:
                    matrix[x, 0, z] = BiomesType.sea
        return matrix

    # def CreateStartMatrixHigh(self): #ИСПОЛЬЗОВАТЬ ПРИ СОЗДАНИИ ВЫСОТ
    #     Res_x = settings.width  #Right
    #     Res_y = settings.height  #Up
    #     Res_z = settings.length  #forward
    #
    #     matrix = self.np.zeros((Res_x, Res_y, Res_z))  #y-axis fixation: matrix[:, y, :]
    #
    #     for x in range(Res_x):
    #         for z in range(Res_z):
    #             ver = 0
    #             step = 100 / Res_y
    #             for y in range(Res_y -1, -1, -1):
    #                 r = random.randint(1, 100)
    #                 if r > ver:
    #                     matrix[x, y, z] = BiomesType.land
    #                     ver += step
    #                 else:
    #                     break
    #     return matrix

    def DrawingScene(self):

        vertices = {0: self.np.array([1, 1, 1]),
                    1: self.np.array([-1, 1, 1]),
                    2: self.np.array([-1, -1, 1]),
                    3: self.np.array([1, -1, 1]),
                    4: self.np.array([1, 1, -1]),
                    5: self.np.array([-1, 1, -1]),
                    6: self.np.array([-1, -1, -1]),
                    7: self.np.array([1, -1, -1])}

        triangles_land = {0: {0: vertices[0], 1: vertices[1], 2: vertices[2], "color": settings.color_land},
                     1: {0: vertices[0], 2: vertices[2], 3: vertices[3], "color": settings.color_land},
                     2: {4: vertices[4], 0: vertices[0], 3: vertices[3], "color": settings.color_land},
                     3: {4: vertices[4], 3: vertices[3], 7: vertices[7], "color": settings.color_land},
                     4: {5: vertices[5], 4: vertices[4], 7: vertices[7], "color": settings.color_land},
                     5: {5: vertices[5], 7: vertices[7], 6: vertices[6], "color": settings.color_land},
                     6: {1: vertices[1], 5: vertices[5], 6: vertices[6], "color": settings.color_land},
                     7: {1: vertices[1], 6: vertices[6], 2: vertices[2], "color": settings.color_land},
                     8: {4: vertices[4], 5: vertices[5], 1: vertices[1], "color": settings.color_land},
                     9: {4: vertices[4], 1: vertices[1], 0: vertices[0], "color": settings.color_land},
                     10: {2: vertices[2], 6: vertices[6], 7: vertices[7], "color": settings.color_land},
                     11: {2: vertices[2], 7: vertices[7], 3: vertices[3], "color": settings.color_land}}

        triangles_sea = {0: {0: vertices[0], 1: vertices[1], 2: vertices[2], "color": settings.color_sea},
                          1: {0: vertices[0], 2: vertices[2], 3: vertices[3], "color": settings.color_sea},
                          2: {4: vertices[4], 0: vertices[0], 3: vertices[3], "color": settings.color_sea},
                          3: {4: vertices[4], 3: vertices[3], 7: vertices[7], "color": settings.color_sea},
                          4: {5: vertices[5], 4: vertices[4], 7: vertices[7], "color": settings.color_sea},
                          5: {5: vertices[5], 7: vertices[7], 6: vertices[6], "color": settings.color_sea},
                          6: {1: vertices[1], 5: vertices[5], 6: vertices[6], "color": settings.color_sea},
                          7: {1: vertices[1], 6: vertices[6], 2: vertices[2], "color": settings.color_sea},
                          8: {4: vertices[4], 5: vertices[5], 1: vertices[1], "color": settings.color_sea},
                          9: {4: vertices[4], 1: vertices[1], 0: vertices[0], "color": settings.color_sea},
                          10: {2: vertices[2], 6: vertices[6], 7: vertices[7], "color": settings.color_sea},
                          11: {2: vertices[2], 7: vertices[7], 3: vertices[3], "color": settings.color_sea}}

        objects = dict()

        Res_x, Res_y, Res_z = self.matrix.shape
        i = 0
        for x in range(Res_x):
            for z in range(Res_z):
                for y in range(Res_y):

                    def CreateObj(triangles):
                        nonlocal i
                        vertices_cur = vertices
                        triangles_cur = triangles
                        position_cur = self.np.array([x * 2 + 15, y * 2 + 35, z * 2 + 25])
                        object_cur = {"vertices": vertices_cur, "triangles": triangles_cur, "postition": position_cur}
                        objects[f"object{i}"] = object_cur
                        i += 1

                    if self.matrix[x, y, z]:
                        if self.matrix[x, y, z] == BiomesType.land:
                            CreateObj(triangles_land)
                        elif self.matrix[x, y, z] == BiomesType.sea:
                            CreateObj(triangles_sea)

        self.graphic3D.RenderScene(objects)
