import random
from BiomesType import BiomesType

class StartAndEnd():

    def __init__(self, matrix, matrix_cond, island_centr_sides , size_of_land, np):
        self.matrix_cond = matrix_cond
        self.island_centr_sides = island_centr_sides
        self.size_of_land = size_of_land
        self.tunnel_key = max(self.size_of_land) + 1
        start = max(self.size_of_land) + 2 #key of start island
        end = max(self.size_of_land) + 3  # key of end island
        self.np = np
        self.matrix = matrix

        start_land = self.StartIsland(range(len(self.matrix_cond[0])), range(len(self.matrix_cond)))
        end_land = self.StartIsland(range(len(self.matrix_cond[0]) - 1, 0, -1), range(len(self.matrix_cond) - 1, 0, -1))

        start_land_center_sides = self.island_centr_sides[start_land]
        end_land_center_sides = self.island_centr_sides[end_land]

        self.ChangeBiomesType(BiomesType.start_land, start_land_center_sides[1], start_land_center_sides[2], start,
                              start_land)
        self.ChangeBiomesType(BiomesType.end_land, end_land_center_sides[1], end_land_center_sides[2], end,
                              end_land)



    def StartIsland(self, range_y, range_x):
        """Defining the initial island"""
        was_key = []
        end_counter = 3
        counter = 0
        for y in range_y:
            if was_key:
                counter += 1
            if counter > end_counter:
                break
            for x in range_x:
                if self.matrix_cond[x][y] != 0 and self.matrix_cond[x][y] != self.tunnel_key and self.matrix_cond[x][y] not in was_key:
                    was_key.append(self.matrix_cond[x][y])

        return random.choice(was_key)

    def ChangeBiomesType(self, biome_type, sides_x, sides_y, key, cur_key):
        """changing the key and biome type for the start/end island"""
        for x in range(sides_x[0], sides_x[1] + 1):
            for y in range(sides_y[0], sides_y[1] + 1):
                if self.matrix_cond[x][y] == cur_key:
                    self.matrix_cond[x][y] = key
                    self.matrix[x][0][y] = biome_type

