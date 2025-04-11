from settings import settings
from BiomesType import BiomesType
from WriteExcel import WriteExcel
from TraverseSquareAlgorithm import TraverseSquareAlgorithm

class Tunneling():

    def __init__(self, matrix, matrix_cond, size_of_land, amounts_land ,np):
        self.matrix_cond = matrix_cond
        self.size_of_land = size_of_land
        self.num_key = max(self.size_of_land) + 1 #tunnel key
        self.np = np
        self.matrix = matrix
        self.amounts_lands = amounts_land

        Res_x = settings.width_RL  # Right
        Res_y = settings.height_RL  # Up
        Res_z = settings.length_RL  # forwardd

        #self.graph = self.np.zeros((Res_x, Res_y, Res_z))
        self.island_centr_sides = dict() #[centr, side_x, side_y] of the key island
        self.roads = [] #Which islands have paths between them? [min(key1), max(key2)]

        size_of_land_helper = self.size_of_land.copy()
        for key, value in size_of_land_helper.items():
            self.island_centr_sides[key] = self.SearchingIslandGeometricCenterAndBorders(key)

        was_key = []

        for x in range(len(self.matrix_cond)):
            for y in range(len(self.matrix_cond[x])):
                if self.matrix_cond[x][y] != 0 and self.matrix_cond[x][y] not in was_key and self.matrix_cond[x][y] != self.num_key:
                    was_key.append(int(self.matrix_cond[x][y]))
                    cur_key = int(self.matrix_cond[x][y])
                    have_road = False
                    counter = 0
                    cur_isl_sides = self.island_centr_sides[cur_key] #[centr, side_x, side_y] #Первый раз вытаскиваем границы
                    side_x = [(cur_isl_sides[1][0] - 1) if (cur_isl_sides[1][0] - 1) >= 0 else cur_isl_sides[1][0],
                              (cur_isl_sides[1][1] + 1) if (cur_isl_sides[1][1] + 1) < len(self.matrix_cond) else cur_isl_sides[1][1]]

                    side_y = [(cur_isl_sides[2][0] - 1) if (cur_isl_sides[2][0] - 1) >= 0 else cur_isl_sides[2][0],
                              (cur_isl_sides[2][1] + 1) if (cur_isl_sides[2][1] + 1) < len(self.matrix_cond[0]) else cur_isl_sides[2][1]]


                    while counter < 3:
                        print(f"Beginning while counter. counter = {counter}")

                        def BuildTunnel(x, y):
                            nonlocal have_road
                            have_road = self.CanBuildTunnel(x, y, cur_key, have_road)

                        TraverseSquareAlgorithm.TraverseSquare(side_x, side_y, BuildTunnel)

                        if have_road:
                            counter += 1
                        side_x[0] = max(0, side_x[0] - 1)
                        side_x[1] = min(len(self.matrix_cond) - 1, side_x[1] + 1)
                        side_y[0] = max(0, side_y[0] - 1)
                        side_y[1] = min(len(self.matrix_cond[0]) - 1, side_y[1] + 1)

        for x in range(len(self.matrix_cond)):
            for y in range(len(self.matrix_cond[x])):
                self.matrix[x][0][y] = BiomesType.air_RL if (self.matrix_cond[x][y] == 0) \
                    else BiomesType.tunnel_RL if (self.matrix_cond[x][y] == self.num_key) \
                    else BiomesType.land_RL

    def CanBuildTunnel(self, d_x, d_y, cur_key, have_road):
        """We are checking whether it is possible to build a tunnel. If possible, we are building"""
        if self.matrix_cond[d_x][d_y] != 0 and self.matrix_cond[d_x][d_y] != cur_key and self.matrix_cond[d_x][d_y] != self.num_key:
            sec_key = int(self.matrix_cond[d_x][d_y])
            if [min(cur_key, sec_key), max(cur_key, sec_key)] not in self.roads:
                self.Tunnel(cur_key, sec_key)
                self.roads.append([min(cur_key, sec_key), max(cur_key, sec_key)])
                return True
        return have_road

    def SearchingIslandGeometricCenterAndBorders(self, number_of_land):
        """search for the geometric central cell of the island and borders"""
        sides_x = [len(self.matrix_cond), 0] #min and max
        sides_y = [len(self.matrix_cond[0]), 0] #min and max

        for x in range(len(self.matrix_cond)):
            for y in range(len(self.matrix_cond[x])):
                if self.matrix_cond[x][y] == number_of_land:
                    if x < sides_x[0]:
                        sides_x[0] = x
                    if x > sides_x[1]:
                        sides_x[1] = x

                    if y < sides_y[0]:
                        sides_y[0] = y
                    if y > sides_y[1]:
                        sides_y[1] = y

        centr = [int(sum(sides_x) / 2), int(sum(sides_y) / 2)]
        return [centr, sides_x, sides_y]

    def Tunnel(self, key1, key2):
        """laying a path between two islands"""
        sides_key1 = self.island_centr_sides[key1] #Второй раз вытаскиваем границы
        sides_key2 = self.island_centr_sides[key2]

        if sides_key1[0][1] >= sides_key2[0][1] + 3:
            start_y = sides_key1[2][0]
            end_y = sides_key2[2][1]
        elif sides_key1[0][1] + 3 <= sides_key2[0][1]:
            start_y = sides_key1[2][1]
            end_y = sides_key2[2][0]
        else:
            start_y = sides_key1[0][1]
            end_y = sides_key2[0][1]

        if sides_key1[0][0] >= sides_key2[0][0] + 3:
            start_x = sides_key1[1][0]
            end_x = sides_key2[1][1]
        elif sides_key1[0][0] + 3 <= sides_key2[0][0]:
            start_x = sides_key1[1][1]
            end_x = sides_key2[1][0]
        else:
            start_x = sides_key1[0][0]
            end_x = sides_key2[0][0]

        x, y = self.SearchNearestBoundaryCell(key1, start_x, start_y, sides_key1[0])
        end_x, end_y = self.SearchNearestBoundaryCell(key2, end_x, end_y, sides_key2[0])

        def_x = 1 if end_x > x else -1
        def_y = 1 if end_y > y else - 1

        while True:  ####ЗДЕСЬ ПРОИСХОДИТ БЕСКОНЕЧНЫЙ ЦИКЛ
            print(f"Tunnel: x = {x}, y = {y}, end_x = {end_x}, end_y = {end_y}")
            if (x, y) == (end_x, end_y):
                print(f"The last point has been reached: x = {x}, y = {y}")
                break

            if x != end_x:
                if 0 <= x + def_x < len(self.matrix_cond):
                    x += def_x
                    if self.matrix_cond[x][y] == 0:
                        self.matrix_cond[x][y] = self.num_key

                else:
                    print(f"going abroad by x, where x = {x + def_x}")

            if y != end_y:
                if 0 <= y + def_y < len(self.matrix_cond[0]):
                    y += def_y
                    if self.matrix_cond[x][y] == 0:
                        self.matrix_cond[x][y] = self.num_key
                else:
                    print(f"going abroad by y, where y = {y + def_y}")

    def SearchNearestBoundaryCell(self, key, x, y, center):
        """If there is no island in the corner cell, go up (down) and right (left) and diagonal
        at the same time in search of the first available island cell."""
        if self.matrix_cond[x][y] == key:
            return x, y
        else:
            result = []
            def Check(dx, dy):
                if self.matrix_cond[dx][dy] == key:
                    result.append(dx)
                    result.append(dy)
                    raise StopIteration
            try:
                TraverseSquareAlgorithm.TraverseSquareExpandingFromPoint(x, y, self.matrix_cond, Check)
            except StopIteration:
                return result[0], result[1]