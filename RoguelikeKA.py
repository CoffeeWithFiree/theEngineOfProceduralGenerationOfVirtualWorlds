from settings import settings
from BiomesType import BiomesType
import random
from FloodFeelCounter import FloodFeelCounter
from OrderingIsland import OrderingIsland

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
            self.NextGenerationLands()

        #Every Land ~18-23 cells, 9-13 lands
        self.matrix_cond, self.size_of_land, self.amounts_lands = self.CounterLand()



        ord_island = OrderingIsland(self.matrix, self.matrix_cond, self.size_of_land, self.amounts_lands, self.np)

        self.matrix = ord_island.matrix
        self.matrix_cond = ord_island.matrix_cond
        self.size_of_land = ord_island.size_of_land
        self.amounts_lands = ord_island.amounts_lands

        print(f"amount of lands = {self.amounts_lands}")
        print(f"size of lands = {self.size_of_land}")
        print(f"matrix_cond =")
        for i in self.matrix_cond:
            print(i)


        print("Matrix was create")

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

        objects = dict()

        Res_x, Res_y, Res_z = self.matrix.shape
        i = 0
        for x in range(Res_x):
            for z in range(Res_z):
                for y in range(Res_y):
                    #print(x, y, z)
                    if self.matrix[x, y, z] == BiomesType.land_RL:
                        vertices_cur = vertices
                        triangles_cur = triangles_land
                        position_cur = self.np.array([x * 2 + 15, y * 2 + 35, z * 2 + 25])
                        object_cur = {"vertices": vertices_cur, "triangles": triangles_cur, "postition": position_cur}

                        objects[f"object{i}"] = object_cur

                        i += 1

        self.graphic3D.RenderScene(objects)

    def NextGenerationLands(self):
        """the ordered state of land and sea"""
        y = 0 #Use just for first layer
        warning_amounts = [3, 6, 7, 8]
        for x in range(len(self.matrix)):
            for z in range(len(self.matrix[x, y])):
                land_counter = 0
                air_counter = 0

                #[x - 1][z - 1]
                if (x - 1) >= 0 and (z - 1) >= 0:
                    if self.matrix[x - 1][y][z - 1] == BiomesType.land_RL:
                        land_counter += 1
                    else:
                        air_counter += 1

                #[x][z - 1]
                if (z - 1) >= 0:
                    if self.matrix[x][y][z - 1] == BiomesType.land_RL:
                        land_counter += 1
                    else:
                        air_counter += 1

                #[x + 1][z - 1]
                if (x + 1) <= (settings.columns - 1) and (z - 1) >= 0:
                    if self.matrix[x + 1][y][z - 1] == BiomesType.land_RL:
                        land_counter += 1
                    else:
                        air_counter += 1

                #[x - 1][z]
                if (x - 1) >= 0:
                    if self.matrix[x - 1][y][z] == BiomesType.land_RL:
                        land_counter += 1
                    else:
                        air_counter += 1

                #[x + 1][z]
                if (x + 1) <= (settings.columns - 1):
                    if self.matrix[x + 1][y][z] == BiomesType.land_RL:
                        land_counter += 1
                    else:
                        air_counter += 1

                # [x - 1][z + 1]
                if (x - 1) >= 0 and (z + 1 <= (settings.rows - 1)):
                    if self.matrix[x - 1][y][z + 1] == BiomesType.land_RL:
                        land_counter += 1
                    else:
                        air_counter += 1

                # [x][z + 1]
                if (z + 1 <= (settings.rows - 1)):
                    if self.matrix[x][y][z + 1] == BiomesType.land_RL:
                        land_counter += 1
                    else:
                        air_counter += 1

                # [x + 1][z + 1]
                if ((x + 1) <= (settings.columns - 1)) and (z + 1 <= (settings.rows - 1)):
                    if self.matrix[x + 1][y][z + 1] == BiomesType.land_RL:
                        land_counter += 1
                    else:
                        air_counter += 1

                #current cell is land
                if self.matrix[x][y][z] == BiomesType.land_RL:
                    if air_counter in warning_amounts:
                        self.matrix[x][y][z] = BiomesType.air_RL

                #current cell is air
                elif self.matrix[x][y][z] == BiomesType.air_RL:
                    if land_counter in warning_amounts:
                        self.matrix[x][y][z] = BiomesType.land_RL


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
