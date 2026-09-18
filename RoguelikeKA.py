from settings import settings
from BiomesType import BiomesType
import random
from FloodFeelCounter import FloodFeelCounter
from OrderingIsland import OrderingIsland
from PostProcessingAfterOrdering import PostProcessingAfterOrdering
from Tunneling import Tunneling
from WriteExcel import WriteExcel
from StartAndEnd import StartAndEnd
from DayAndNight import DayAndNight

class RoguelikeKA:
    def __init__(self, main, pg, np, graphic3D):
        self.main = main
        self.pg = pg
        self.np = np
        self.graphic3D = graphic3D

        #Start random matrix
        self.matrix = self.CreateStartMatrix()

        #Order out of chaos
        for _ in range(20):
            DayAndNight.NextGenerationLands(self.matrix, settings.columns, settings.rows, BiomesType.air_RL, BiomesType.land_RL)

        #2 iterations of island ordering
        for i in range(2):
            self.OrdIsland()

        #Post-Processing after Ordering
        self.matrix_cond, self.size_of_land, self.amounts_lands = self.CounterLand()
        post_proc = PostProcessingAfterOrdering(self.matrix, self.matrix_cond, self.size_of_land,self.amounts_lands, self.np)

        self.matrix = post_proc.matrix
        self.matrix_cond = post_proc.matrix_cond
        self.size_of_land = post_proc.size_of_land
        self.amounts_lands = post_proc.amounts_lands

        with_tunnels = Tunneling(self.matrix, self.matrix_cond, self.size_of_land, self.amounts_lands, self.np)

        self.matrix = with_tunnels.matrix
        self.matrix_cond = with_tunnels.matrix_cond
        self.island_centr_sides = with_tunnels.island_centr_sides

        with_start_end_lands = StartAndEnd(self.matrix, self.matrix_cond, self.island_centr_sides , self.size_of_land, self.np)

        self.matrix = with_start_end_lands.matrix
        self.matrix_cond = with_start_end_lands.matrix_cond

        WriteExcel(self.matrix, self.matrix_cond, f"matrix{2}.xlsx", f"matrix_cond{2}.xlsx")

    def CreateStartMatrix(self):
        Res_x = settings.width_RL  # Right
        Res_y = settings.height_RL  # Up
        Res_z = settings.length_RL  # forwardd

        matrix = self.np.zeros((Res_x, Res_y, Res_z))
        for y in range(Res_y):
            for x in range(Res_x):
                for z in range(Res_z):
                    if y == 0:
                        r = random.randint(1, 3)
                        matrix[x, y, z] = BiomesType.land_RL if (r == 1) else BiomesType.air_RL
                    else:
                        matrix[x, y, z] = BiomesType.air_RL

        return matrix

    def DrawingScene(self):

        vertices = {0: self.np.array([1, 1, 1]),
                    1: self.np.array([-1, 1, 1]),
                    2: self.np.array([-1, -1, 1]),
                    3: self.np.array([1, -1, 1]),
                    4: self.np.array([1, 1, -1]),
                    5: self.np.array([-1, 1, -1]),
                    6: self.np.array([-1, -1, -1]),
                    7: self.np.array([1, -1, -1])}

        triangles_land = {0: {0: vertices[0], 1: vertices[1], 2: vertices[2], "color": settings.color_land_RL},
                     1: {0: vertices[0], 2: vertices[2], 3: vertices[3], "color": settings.color_land_RL},
                     2: {4: vertices[4], 0: vertices[0], 3: vertices[3], "color": settings.color_land_RL},
                     3: {4: vertices[4], 3: vertices[3], 7: vertices[7], "color": settings.color_land_RL},
                     4: {5: vertices[5], 4: vertices[4], 7: vertices[7], "color": settings.color_land_RL},
                     5: {5: vertices[5], 7: vertices[7], 6: vertices[6], "color": settings.color_land_RL},
                     6: {1: vertices[1], 5: vertices[5], 6: vertices[6], "color": settings.color_land_RL},
                     7: {1: vertices[1], 6: vertices[6], 2: vertices[2], "color": settings.color_land_RL},
                     8: {4: vertices[4], 5: vertices[5], 1: vertices[1], "color": settings.color_land_RL},
                     9: {4: vertices[4], 1: vertices[1], 0: vertices[0], "color": settings.color_land_RL},
                     10: {2: vertices[2], 6: vertices[6], 7: vertices[7], "color": settings.color_land_RL},
                     11: {2: vertices[2], 7: vertices[7], 3: vertices[3], "color": settings.color_land_RL}}

        triangles_tunnel = {0: {0: vertices[0], 1: vertices[1], 2: vertices[2], "color": settings.color_tunnel},
                            1: {0: vertices[0], 2: vertices[2], 3: vertices[3], "color": settings.color_tunnel},
                            2: {4: vertices[4], 0: vertices[0], 3: vertices[3], "color": settings.color_tunnel},
                            3: {4: vertices[4], 3: vertices[3], 7: vertices[7], "color": settings.color_tunnel},
                            4: {5: vertices[5], 4: vertices[4], 7: vertices[7], "color": settings.color_tunnel},
                            5: {5: vertices[5], 7: vertices[7], 6: vertices[6], "color": settings.color_tunnel},
                            6: {1: vertices[1], 5: vertices[5], 6: vertices[6], "color": settings.color_tunnel},
                            7: {1: vertices[1], 6: vertices[6], 2: vertices[2], "color": settings.color_tunnel},
                            8: {4: vertices[4], 5: vertices[5], 1: vertices[1], "color": settings.color_tunnel},
                            9: {4: vertices[4], 1: vertices[1], 0: vertices[0], "color": settings.color_tunnel},
                            10: {2: vertices[2], 6: vertices[6], 7: vertices[7], "color": settings.color_tunnel},
                            11: {2: vertices[2], 7: vertices[7], 3: vertices[3], "color": settings.color_tunnel}}

        triangles_start = {0: {0: vertices[0], 1: vertices[1], 2: vertices[2], "color": settings.color_start},
                            1: {0: vertices[0], 2: vertices[2], 3: vertices[3], "color": settings.color_start},
                            2: {4: vertices[4], 0: vertices[0], 3: vertices[3], "color": settings.color_start},
                            3: {4: vertices[4], 3: vertices[3], 7: vertices[7], "color": settings.color_start},
                            4: {5: vertices[5], 4: vertices[4], 7: vertices[7], "color": settings.color_start},
                            5: {5: vertices[5], 7: vertices[7], 6: vertices[6], "color": settings.color_start},
                            6: {1: vertices[1], 5: vertices[5], 6: vertices[6], "color": settings.color_start},
                            7: {1: vertices[1], 6: vertices[6], 2: vertices[2], "color": settings.color_start},
                            8: {4: vertices[4], 5: vertices[5], 1: vertices[1], "color": settings.color_start},
                            9: {4: vertices[4], 1: vertices[1], 0: vertices[0], "color": settings.color_start},
                            10: {2: vertices[2], 6: vertices[6], 7: vertices[7], "color": settings.color_start},
                            11: {2: vertices[2], 7: vertices[7], 3: vertices[3], "color": settings.color_start}}

        triangles_end = {0: {0: vertices[0], 1: vertices[1], 2: vertices[2], "color": settings.color_end},
                           1: {0: vertices[0], 2: vertices[2], 3: vertices[3], "color": settings.color_end},
                           2: {4: vertices[4], 0: vertices[0], 3: vertices[3], "color": settings.color_end},
                           3: {4: vertices[4], 3: vertices[3], 7: vertices[7], "color": settings.color_end},
                           4: {5: vertices[5], 4: vertices[4], 7: vertices[7], "color": settings.color_end},
                           5: {5: vertices[5], 7: vertices[7], 6: vertices[6], "color": settings.color_end},
                           6: {1: vertices[1], 5: vertices[5], 6: vertices[6], "color": settings.color_end},
                           7: {1: vertices[1], 6: vertices[6], 2: vertices[2], "color": settings.color_end},
                           8: {4: vertices[4], 5: vertices[5], 1: vertices[1], "color": settings.color_end},
                           9: {4: vertices[4], 1: vertices[1], 0: vertices[0], "color": settings.color_end},
                           10: {2: vertices[2], 6: vertices[6], 7: vertices[7], "color": settings.color_end},
                           11: {2: vertices[2], 7: vertices[7], 3: vertices[3], "color": settings.color_end}}

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
                        object_cur = {"vertices": vertices_cur, "triangles": triangles_cur, "position": position_cur}
                        objects[f"object{i}"] = object_cur
                        i += 1

                    if self.matrix[x, y, z] == BiomesType.land_RL:
                        CreateObj(triangles_land)

                    elif self.matrix[x, y, z] == BiomesType.tunnel_RL:
                        CreateObj(triangles_tunnel)

                    elif self.matrix[x, y, z] == BiomesType.start_land:
                        CreateObj(triangles_start)

                    elif self.matrix[x, y, z] == BiomesType.end_land:
                        CreateObj(triangles_end)

        self.graphic3D.RenderScene(objects)

    def CounterLand(self):
        """a counter for the number of islands and their sizes"""
        Res_x = settings.width_RL  # Right
        Res_y = settings.height_RL  # Up
        Res_z = settings.length_RL  # forward
        matrix_cond = self.np.zeros((Res_x, Res_z))

        number_of_matrix = 1
        size_of_land = dict()
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i][0])):
                if matrix_cond[i][j] == 0 and self.matrix[i][0][j] == BiomesType.land_RL:
                    flood_feel = FloodFeelCounter(self.matrix, matrix_cond, i, j, number_of_matrix, self.np)
                    matrix_cond, size_of_land[number_of_matrix] = flood_feel.Feel()
                    number_of_matrix += 1
        return matrix_cond, size_of_land, number_of_matrix - 1

    def OrdIsland(self):
        """the function that causes the islands to be ordered"""
        self.matrix_cond, self.size_of_land, self.amounts_lands = self.CounterLand()

        ord_island = OrderingIsland(self.matrix, self.matrix_cond, self.size_of_land, self.amounts_lands, self.np)

        self.matrix = ord_island.matrix
        self.matrix_cond = ord_island.matrix_cond
        self.size_of_land = ord_island.size_of_land
        self.amounts_lands = ord_island.amounts_lands
