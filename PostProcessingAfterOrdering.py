from settings import settings
from BiomesType import BiomesType

class PostProcessingAfterOrdering():
    def __init__(self, matrix, matrix_cond, size_of_land, amounts_land ,np):
        self.matrix_cond = matrix_cond
        self.size_of_land = size_of_land
        self.np = np
        self.matrix = matrix
        self.amounts_lands = amounts_land
        self.FixDiagonalConflict()

        self.need_lands = settings.need_lands
        self.need_size = settings.need_size

        size_of_land_helper = self.size_of_land.copy()
        for key, value in size_of_land_helper.items():
            if value < self.need_size[0]:
                centr, sides_x, sides_y = self.SearchingIslandGeometricCenterAndBorders(key)
                self.DeleteIsland(key, sides_x, sides_y)
                del self.size_of_land[key]
                self.amounts_lands = self.amounts_lands - 1

        for x in range(len(self.matrix_cond)):
            for y in range(len(self.matrix_cond[x])):
                self.matrix[x][0][y] = BiomesType.air_RL if (self.matrix_cond[x][y] == 0) else BiomesType.land_RL

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
        return centr, sides_x, sides_y

    def DeleteIsland(self, number_of_land, sides_x, sides_y):
        """removes the island with the specified number from the matrix"""
        for i in range(sides_x[0], sides_x[1] + 1):
            for j in range(sides_y[0], sides_y[1] + 1):
                if self.matrix_cond[i][j] == number_of_land:
                    self.matrix_cond[i][j] = 0

    def FixDiagonalConflict(self):
        """Removing islands at the corners of other islands"""
        for x in range(len(self.matrix_cond)):
            for y in range(len(self.matrix_cond[x])):
                if self.matrix_cond[x][y] != 0:
                    if self.CheckAround(x, y, self.matrix_cond[x][y]) == False:
                        # [x - 1][y - 1]
                        if (x - 1) >= 0 and (y - 1) >= 0:
                            if self.matrix_cond[x - 1][y - 1] != 0 and self.matrix_cond[x - 1][y - 1] != self.matrix_cond[x][y]:
                                self.CheckZeroIsland(self.matrix_cond[x - 1][y - 1])
                                self.matrix_cond[x - 1][y - 1] = 0

                        # [x + 1][y - 1]
                        if (x + 1) <= (settings.columns - 1) and (y - 1) >= 0:
                            if self.matrix_cond[x + 1][y - 1] != 0 and self.matrix_cond[x + 1][y - 1] != self.matrix_cond[x][y]:
                                self.CheckZeroIsland(self.matrix_cond[x + 1][y - 1])
                                self.matrix_cond[x + 1][y - 1] = 0

                        # [x - 1][y + 1]
                        if (x - 1) >= 0 and (y + 1 <= (settings.rows - 1)):
                            if self.matrix_cond[x - 1][y + 1] != 0 and self.matrix_cond[x - 1][y + 1] != self.matrix_cond[x][y]:
                                self.CheckZeroIsland(self.matrix_cond[x - 1][y + 1])
                                self.matrix_cond[x - 1][y + 1] = 0

                        # [x + 1][y + 1]
                        if ((x + 1) <= (settings.columns - 1)) and (y + 1 <= (settings.rows - 1)):
                            if self.matrix_cond[x + 1][y + 1] != 0 and self.matrix_cond[x + 1][y + 1] != self.matrix_cond[x][y]:
                                self.CheckZeroIsland(self.matrix_cond[x + 1][y + 1])
                                self.matrix_cond[x + 1][y + 1] = 0

    def CheckZeroIsland(self, number_of_land):
        """Checking that the island is no more"""
        self.size_of_land[number_of_land] -= 1
        if self.size_of_land[number_of_land] == 0:
            del self.size_of_land[number_of_land]
            self.amounts_lands -= 1

    def CheckAround(self, x, y, number_of_land):
        """A function that checks that there are no foreign islands around the cell"""
        # [x - 1][y - 1]
        if (x - 1) >= 0 and (y - 1) >= 0:
            if self.matrix_cond[x - 1][y - 1] != 0 and self.matrix_cond[x - 1][y - 1] != number_of_land:
                return False

        # [x][y - 1]
        if (y - 1) >= 0:
            if self.matrix_cond[x][y - 1] != 0 and self.matrix_cond[x][y - 1] != number_of_land:
                return False

        # [x + 1][y - 1]
        if (x + 1) <= (settings.columns - 1) and (y - 1) >= 0:
            if self.matrix_cond[x + 1][y - 1] != 0 and self.matrix_cond[x + 1][y - 1] != number_of_land:
                return False

        # [x - 1][y]
        if (x - 1) >= 0:
            if self.matrix_cond[x - 1][y] != 0 and self.matrix_cond[x - 1][y] != number_of_land:
                return False

        # [x + 1][y]
        if (x + 1) <= (settings.columns - 1):
            if self.matrix_cond[x + 1][y] != 0 and self.matrix_cond[x + 1][y] != number_of_land:
                return False

        # [x - 1][y + 1]
        if (x - 1) >= 0 and (y + 1 <= (settings.rows - 1)):
            if self.matrix_cond[x - 1][y + 1] != 0 and self.matrix_cond[x - 1][y + 1] != number_of_land:
                return False

        # [x][y + 1]
        if (y + 1 <= (settings.rows - 1)):
            if self.matrix_cond[x][y + 1] != 0 and self.matrix_cond[x][y + 1] != number_of_land:
                return False

        # [x + 1][y + 1]
        if ((x + 1) <= (settings.columns - 1)) and (y + 1 <= (settings.rows - 1)):
            if self.matrix_cond[x + 1][y + 1] != 0 and self.matrix_cond[x + 1][y + 1] != number_of_land:
                return False

        return True