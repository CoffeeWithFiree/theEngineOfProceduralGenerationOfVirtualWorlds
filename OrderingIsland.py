from settings import settings
from BiomesType import BiomesType
from FloodFeelCounter import FloodFeelCounter
import random

class OrderingIsland:
    def __init__(self, matrix, matrix_cond, size_of_land, amounts_lands, np):
        """Ordering islands by number and size"""

        self.matrix = matrix
        self.matrix_cond = matrix_cond
        self.size_of_land = size_of_land
        self.amounts_lands = amounts_lands
        self.np = np

        #POST-PROCESSING
        self.FixDiagonalConflict()

        self.need_lands = self.np.array([9, 10, 11, 12, 13])
        self.need_size = self.np.array([18, 19, 20, 21, 22, 23])  # min and max

        status_amount_of_lands = self.SetStatusAmount()
        while (not (self.amounts_lands in self.need_lands)) or (any(v not in self.need_size for v in self.size_of_land.values())):
            signal_was_change = False
            size_of_land_helper = self.size_of_land.copy()
            for key, value in size_of_land_helper.items():
                centr, sides_x, sides_y = self.SearchingIslandGeometricCenterAndBorders(key)
                if value < self.need_size[0]:
                    if status_amount_of_lands == "more":    ####GOOD#####
                        self.DeleteIsland(key, sides_x, sides_y)
                        del self.size_of_land[key]
                        self.amounts_lands = self.amounts_lands - 1
                        status_amount_of_lands = self.SetStatusAmount()
                        signal_was_change = True

                    elif status_amount_of_lands == "less" or status_amount_of_lands == "equel":
                        if self.Expansion(key, sides_x, sides_y): #If True -> Something is preventing it from expanding ####GOOD###
                            self.DeleteIsland(key, sides_x, sides_y)
                            del self.size_of_land[key]
                            self.CreateNewIsland()
                        signal_was_change = True

                elif value > self.need_size[-1]:

                    if status_amount_of_lands == "more" or status_amount_of_lands == "equel":
                        self.ReducingSize(key, sides_x, sides_y) ####GOOD#####
                        signal_was_change = True

                    elif status_amount_of_lands == "less":
                        self.ReducingSize(key, sides_x, sides_y)
                        self.CreateNewIsland()
                        signal_was_change = True

                        # self.Cut(key, centr, sides_x, sides_y) ###WORK INCORRECT###
                        # self.amounts_lands += 1
                        # status_amount_of_lands = self.SetStatusAmount()
                        # del self.size_of_land[key]
                        #
                        # max_key = max(self.size_of_land)
                        # number_of_matrix = max_key + 1
                        #
                        # for x in range(len(self.matrix_cond)):    ###Sides_x and Sides_y
                        #     for y in range(len(self.matrix_cond[x])):
                        #         if self.matrix_cond[x][y] == key:
                        #             flood_feel = FloodFeelCounter(self.matrix, self.matrix_cond, x, y, number_of_matrix, self.np)
                        #             self.matrix_cond, self.size_of_land[number_of_matrix] = flood_feel.Feel()
                        #
                        #             number_of_matrix += 1
                        # signal_was_change = True

            if signal_was_change == False:
                if status_amount_of_lands == "more":
                    key, value = next(iter(self.size_of_land.items()))
                    min = [key, value]
                    for key, value in self.size_of_land.items():
                        if value < min[1]:
                            min = [key, value]

                    centr, sides_x, sides_y = self.SearchingIslandGeometricCenterAndBorders(key)
                    self.DeleteIsland(min[0], sides_x, sides_y)
                    del self.size_of_land[min[0]]
                    self.amounts_lands = self.amounts_lands - 1
                    status_amount_of_lands = self.SetStatusAmount()

                elif status_amount_of_lands == "less":
                    self.CreateNewIsland()
                    self.amounts_lands += 1
                    status_amount_of_lands = self.SetStatusAmount()



    def SetStatusAmount(self):
        """sets the status as to whether the current number of islands is greater, less, or equal to the one we need"""
        if self.amounts_lands > self.need_lands[-1]:
            return "more"
        elif self.amounts_lands < self.need_lands[0]:
            return "less"
        elif self.amounts_lands in self.need_lands:
            return "equel"

    def DeleteIsland(self, number_of_land, sides_x, sides_y):
        """removes the island with the specified number from the matrix"""
        for i in range(sides_x[0], sides_x[1] + 1):
            for j in range(sides_y[0], sides_y[1] + 1):
                if self.matrix_cond[i][j] == number_of_land:
                    self.matrix_cond[i][j] = 0
                    self.matrix[i][0][j] = BiomesType.air_RL

    def Expansion(self, number_of_land, sides_x, sides_y):
        """The expansion of too small islands"""
        iter_ = 0
        max_iter = 20
        while self.size_of_land[number_of_land] < self.need_size[0]:
            iter_ +=1
            if iter_ >= max_iter:
                return True #Something is preventing it from expanding
            for x in range(sides_x[0] - iter_, sides_x[1] + 1 + iter_):
                for y in range(sides_y[0] - iter_, sides_y[1] + iter_):
                    if x >= 0 and x <= (settings.columns - 1) and y >= 0 and y <= (settings.rows - 1):
                        if self.matrix_cond[x][y] == number_of_land:
                            empty_islands = self.CheckZeroAround(x, y)
                            if empty_islands != False:
                                for k in empty_islands:

                                    if self.CheckAround(k[0], k[1], number_of_land):
                                        self.matrix_cond[k[0]][k[1]] = number_of_land
                                        self.matrix[k[0]][0][k[1]] = BiomesType.land_RL
                                        self.size_of_land[number_of_land] = self.size_of_land[number_of_land] + 1
                                        if self.size_of_land[number_of_land] >= self.need_size[0]:
                                            return False

    #WORK INCORRECT
    # def Cut(self, number_of_land, centr, sides_x, sides_y):
    #     """cutting the island into 2 parts either by finding a bottleneck or in the center"""
    #     average_layer = self.UniversalFirstSearch(number_of_land, sides_x, sides_y)
    #     if average_layer != False:
    #         if average_layer[0] == "x":
    #             for x in range((average_layer[1] - 1), (average_layer[1] + 1)):
    #                 for y in range(sides_y[0], sides_y[1] + 1):
    #
    #                     if self.matrix_cond[x][y] == number_of_land:
    #                         self.matrix_cond[x][y] = 0
    #                         self.matrix[x][0][y] = BiomesType.air_RL
    #
    #         elif average_layer[0] == "y":
    #             for x in range(sides_x[0], sides_x[1] + 1):
    #                 for y in range((average_layer[1] - 1), (average_layer[1] + 1)):
    #
    #                     if self.matrix_cond[x][y] == number_of_land:
    #                         self.matrix_cond[x][y] = 0
    #                         self.matrix[x][0][y] = BiomesType.air_RL
    #
    #     else:
    #
    #         if (sides_x[1] - sides_x[0]) >= (sides_y[1] - sides_y[0]):
    #             for x in range((centr[0] - 1), (centr[0] + 1)):
    #                 for y in range(sides_y[0], sides_y[1] + 1):
    #
    #                     if self.matrix_cond[x][y] == number_of_land:
    #                         self.matrix_cond[x][y] = 0
    #                         self.matrix[x][0][y] = BiomesType.air_RL
    #         else:
    #             for x in range(sides_x[0], sides_x[1] + 1):
    #                 for y in range((centr[1] - 1), (centr[1] + 1)):
    #
    #                     if self.matrix_cond[x][y] == number_of_land:
    #                         self.matrix_cond[x][y] = 0
    #                         self.matrix[x][0][y] = BiomesType.air_RL

    def ReducingSize(self, number_of_land, sides_x, sides_y):
        """reduces the size of too large islands"""

        while self.size_of_land[number_of_land] > self.need_size[-1]:
            x = sides_x[0]
            for y in range(sides_y[0], sides_y[1] + 1):
                self.CheckCurCellIsCurIsland(x, y, number_of_land)
                if self.size_of_land[number_of_land] <= self.need_size[-1]:
                    return

            y = sides_y[0]
            for x in range(sides_x[0], sides_x[1] + 1):
                self.CheckCurCellIsCurIsland(x, y, number_of_land)
                if self.size_of_land[number_of_land] <= self.need_size[-1]:
                    return

            x = sides_x[1]
            for y in range(sides_y[0], sides_y[1] + 1):
                self.CheckCurCellIsCurIsland(x, y, number_of_land)
                if self.size_of_land[number_of_land] <= self.need_size[-1]:
                    return

            y = sides_y[1]
            for x in range(sides_x[0], sides_x[1] + 1):
                self.CheckCurCellIsCurIsland(x, y, number_of_land)
                if self.size_of_land[number_of_land] <= self.need_size[-1]:
                    return

            sides_x[0] += 1
            sides_x[1] -= 1
            sides_y[0] += 1
            sides_y[1] -= 1

    def CheckCurCellIsCurIsland(self, x, y, number_of_land):
        """a function that verifies that the current cell is the current island"""
        if self.matrix_cond[x][y] == number_of_land:
            self.matrix_cond[x][y] = 0
            self.matrix[x][0][y] = BiomesType.air_RL
            self.size_of_land[number_of_land] -= 1


    def CreateNewIsland(self):
        """Creating a new island in a suitable empty area"""
        start_x = random.randint(0, (len(self.matrix_cond) - 1))
        start_y = random.randint(0, (len(self.matrix_cond[0]) - 1))

        min_x, max_x = start_x, start_x
        min_y, max_y = start_y, start_y

        while min_x >= 0 or max_x < len(self.matrix_cond) or min_y >= 0 or max_y < len(self.matrix_cond[0]):
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    if 0 <= x < len(self.matrix_cond) and 0 <= y < len(self.matrix_cond[x]):
                        if self.matrix_cond[x][y] == 0:
                            if self.Counter_Islands(0, x, y) >= self.need_size[0]:
                                max_key = max(self.size_of_land)
                                number_of_land = max_key + 1
                                self.size_of_land[number_of_land] = self.FeelNewLand(number_of_land, x, y)
                                return

            min_x -= 1
            max_x += 1
            min_y -= 1
            max_y += 1

            min_x = max(0, min_x)
            max_x = min(max_x, len(self.matrix_cond) - 1)
            min_y = max(0, min_y)
            max_y = min(max_y, len(self.matrix_cond[0]) - 1)
                    
    def FeelNewLand(self, number_of_land, x, y):
        stack_ = [(x, y)]
        counter = 0

        min_x, max_x = x, x
        min_y, max_y = y, y

        while stack_:
            r, c = stack_.pop(0)
            if self.matrix_cond[r][c] == 0 and (self.Check4CellsAround(number_of_land, r, c) or counter == 0):
                if self.CheckAround(r, c, number_of_land):
                    self.matrix_cond[r][c] = number_of_land
                    self.matrix[r][0][c] = BiomesType.land_RL
                    counter += 1

                    if counter >= self.need_size[0]:
                        return counter

                    min_x, max_x = min(min_x, r), max(max_x, r)
                    min_y, max_y = min(min_y, c), max(max_y, c)

                    for nx in range(min_x, max_x + 2):
                        if 0 <= nx < len(self.matrix_cond):
                            if min_y - 1 >= 0:
                                stack_.append((nx, min_y - 1))
                            if max_y + 1 < len(self.matrix_cond[x]):
                                stack_.append((nx, max_y + 1))

                    for ny in range(min_y, max_y + 2):
                        if 0 <= ny < len(self.matrix_cond[0]):
                            if min_x - 1 >= 0:
                                stack_.append((min_x - 1, ny))
                            if max_x + 1 < len(self.matrix_cond):
                                stack_.append((max_x + 1, ny))

        return counter

    def Check4CellsAround(self, number_of_land, x, y):
        """checking that the lower, upper, right or left cell is part of the island"""
        # [x][y - 1]
        if (y - 1) >= 0:
            if self.matrix_cond[x][y - 1] == number_of_land:
                return True

        # [x - 1][y]
        if (x - 1) >= 0:
            if self.matrix_cond[x - 1][y] == number_of_land:
                return True

        # [x + 1][y]
        if (x + 1) <= (settings.columns - 1):
            if self.matrix_cond[x + 1][y] == number_of_land:
                return True

        # [x][y + 1]
        if (y + 1 <= (settings.rows - 1)):
            if self.matrix_cond[x][y + 1] == number_of_land:
                return True

        return False

    def Counter_Islands(self, number_of_land, x, y):
        """Counts the number of cells of an island or a void"""
        stack_ = [(x, y)]
        counter = 0
        help_matrix = self.np.zeros((len(self.matrix_cond), len(self.matrix_cond[x])))
        while stack_:

            r, c = stack_.pop()
            if self.matrix_cond[r][c] == number_of_land and help_matrix[r][c] == 0 and self.Check4CellsAround(number_of_land, r, c):
                if self.CheckAround(r, c, number_of_land):
                    help_matrix[r][c] = 1
                    counter += 1

                    if r + 1 < len(self.matrix_cond):
                        stack_.append((r + 1, c))
                    if r - 1 >= 0:
                        stack_.append((r - 1, c))
                    if c + 1 < len(self.matrix_cond[x]):
                        stack_.append((r, c + 1))
                    if c - 1 >= 0:
                        stack_.append((r, c - 1))

        return counter


    # def UniversalFirstSearch(self, number_of_land, sides_x, sides_y):
    #     """a graph-wide traversal algorithm in width and height"""
    #     layers_x = dict()
    #     layers_y = dict()
    #     for x in range(sides_x[0], sides_x[1] + 1):
    #         for y in range(sides_y[0], sides_y[1] + 1):
    #             if self.matrix_cond[x][y] == number_of_land:
    #                 layers_x[x] = layers_x.get(x, 0) + 1 #If the key exists, it will return the value + 1, otherwise the default value is (0) + 1
    #                 layers_y[y] = layers_y.get(y, 0) + 1
    #
    #     key, value = next(iter(layers_x.items()))
    #     min_x = [key, value]
    #     max_x = [key, value]
    #
    #     key, value = next(iter(layers_y.items()))
    #     min_y = [key, value]
    #     max_y = [key, value]
    #
    #     for key, value in layers_x.items():
    #         if value > max_x[1]:
    #             max_x = [key, value]
    #         if value < min_x[1]:
    #             min_x = [key, value]
    #
    #     for key, value in layers_y.items():
    #         if value > max_y[1]:
    #             max_y = [key, value]
    #         if value < min_y[1]:
    #             min_y = [key, value]
    #
    #     choice = "x" if (max_x[1] - min_x[1]) >= (max_y[1] - min_y[1]) else "y"
    #
    #     average_layer = []
    #     if choice == "x":
    #         if min_x[1] * 2 <= max_x[1]:
    #             average_layer = ["x", min_x[1]]
    #     else:
    #         if min_y[1] * 2 <= max_y[1]:
    #             average_layer = ["y", min_y[1]]
    #     return False if bool(average_layer) == False else average_layer

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

    def CheckZeroAround(self, x, y):
        """A function that checks that the cells around are not islands"""
        indexes = []
        # [x - 1][y - 1]
        if (x - 1) >= 0 and (y - 1) >= 0:
            if self.matrix_cond[x - 1][y - 1] == 0:
                indexes.append([x - 1, y - 1])

        # [x][y - 1]
        if (y - 1) >= 0:
            if self.matrix_cond[x][y - 1] == 0:
                indexes.append([x, y - 1])

        # [x + 1][y - 1]
        if (x + 1) <= (settings.columns - 1) and (y - 1) >= 0:
            if self.matrix_cond[x + 1][y - 1] == 0:
                indexes.append([x + 1, y - 1])

        # [x - 1][y]
        if (x - 1) >= 0:
            if self.matrix_cond[x - 1][y] == 0:
                indexes.append([x - 1, y])

        # [x + 1][y]
        if (x + 1) <= (settings.columns - 1):
            if self.matrix_cond[x + 1][y] == 0:
                indexes.append([x + 1, y])

        # [x - 1][y + 1]
        if (x - 1) >= 0 and (y + 1 <= (settings.rows - 1)):
            if self.matrix_cond[x - 1][y + 1] == 0:
                indexes.append([x - 1, y + 1])

        # [x][y + 1]
        if (y + 1 <= (settings.rows - 1)):
            if self.matrix_cond[x][y + 1] == 0:
                indexes.append([x, y + 1])

        # [x + 1][y + 1]
        if ((x + 1) <= (settings.columns - 1)) and (y + 1 <= (settings.rows - 1)):
            if self.matrix_cond[x + 1][y + 1] == 0:
                indexes.append([x + 1, y + 1])

        return False if (len(indexes) == 0) else indexes

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
                                self.matrix[x - 1][0][y - 1] = BiomesType.air_RL

                        # [x + 1][y - 1]
                        if (x + 1) <= (settings.columns - 1) and (y - 1) >= 0:
                            if self.matrix_cond[x + 1][y - 1] != 0 and self.matrix_cond[x + 1][y - 1] != self.matrix_cond[x][y]:
                                self.CheckZeroIsland(self.matrix_cond[x + 1][y - 1])
                                self.matrix_cond[x + 1][y - 1] = 0
                                self.matrix[x - 1][0][y - 1] = BiomesType.air_RL

                        # [x - 1][y + 1]
                        if (x - 1) >= 0 and (y + 1 <= (settings.rows - 1)):
                            if self.matrix_cond[x - 1][y + 1] != 0 and self.matrix_cond[x - 1][y + 1] != self.matrix_cond[x][y]:
                                self.CheckZeroIsland(self.matrix_cond[x - 1][y + 1])
                                self.matrix_cond[x - 1][y + 1] = 0
                                self.matrix[x - 1][0][y - 1] = BiomesType.air_RL

                        # [x + 1][y + 1]
                        if ((x + 1) <= (settings.columns - 1)) and (y + 1 <= (settings.rows - 1)):
                            if self.matrix_cond[x + 1][y + 1] != 0 and self.matrix_cond[x + 1][y + 1] != self.matrix_cond[x][y]:
                                self.CheckZeroIsland(self.matrix_cond[x + 1][y + 1])
                                self.matrix_cond[x + 1][y + 1] = 0
                                self.matrix[x - 1][0][y - 1] = BiomesType.air_RL

    def CheckZeroIsland(self, number_of_land):
        """Checking that the island is no more"""
        self.size_of_land[number_of_land] -= 1
        if self.size_of_land[number_of_land] == 0:
            del self.size_of_land[number_of_land]
            self.amounts_lands -= 1