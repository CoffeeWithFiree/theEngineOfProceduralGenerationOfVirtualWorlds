from CellsAround import CellsAround
import numpy as np
from scipy.ndimage import convolve
class DayAndNight():
    @staticmethod
    def NextGenerationLands(matrix, columns, rows, first_type, second_type):
        """the ordered state of land and sea"""
        y = 0 #Use just for first layer
        warning_amounts = [3, 6, 7, 8]

        for x in range(len(matrix)):
            for z in range(len(matrix[x, y])):
                counters = {"land_counter": 0,
                            "air_counter": 0}


                def NextGenHelper(x, z):
                    if matrix[x][y][z] == second_type:
                        counters["land_counter"] += 1
                    else:
                        counters["air_counter"] += 1

                CellsAround.EightCellsAround(x, z, NextGenHelper, columns, rows)

                #current cell is land
                if matrix[x][y][z] == second_type:
                    if counters["air_counter"] in warning_amounts:
                        matrix[x][y][z] = first_type

                #current cell is air
                elif matrix[x][y][z] == first_type:
                    if counters["land_counter"] in warning_amounts:
                        matrix[x][y][z] = second_type
        return matrix

    @staticmethod
    def NextGenerationLandsVectorized(matrix, first_type, second_type, y = 0):
        """the ordered state of land and sea with vectorized"""
        layer = matrix[:,y,:]

        second_mask = (layer == second_type).astype(np.int8)

        # 8 neighbors without center
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]], dtype=np.int8)

        #count the number of neighboring second type cells for each cell
        second_neighbors = convolve(second_mask, kernel, mode="constant")
        first_neighbors = 8 - second_neighbors

        #vector substitution
        new_layer = layer.copy()
        new_layer[(layer == second_type) & np.isin(first_neighbors, [3, 6, 7, 8])] = first_type
        new_layer[(layer == first_type) & np.isin(second_neighbors, [3, 6, 7, 8])] = second_type

        matrix[:,y,:] = new_layer
        return matrix

    @staticmethod
    def NextGenerationLandsForHigh(matrix, columns, rows, first_type, second_type, y):
        """the ordered state of land and sea"""
        warning_amounts = [3, 6, 7, 8]

        for x in range(len(matrix)):
            for z in range(len(matrix[x, y])):

                if matrix[x][y][z] == second_type or matrix[x][y][z] == first_type:

                    counters = {"land_counter": 0,
                                "air_counter": 0}

                    def NextGenHelper(x, z):
                        if matrix[x][y][z] == second_type:
                            counters["land_counter"] += 1
                        else:
                            counters["air_counter"] += 1

                    CellsAround.EightCellsAround(x, z, NextGenHelper, columns, rows)


                    # current cell is land
                    if matrix[x][y][z] == second_type:
                        if counters["air_counter"] in warning_amounts:
                            if y + 1 < matrix.shape[1] and matrix[x][y + 1][z] == first_type:
                                matrix[x][y][z] = first_type

                    # current cell is air
                    elif matrix[x][y][z] == first_type:
                        if counters["land_counter"] in warning_amounts:
                            if y > 0 and matrix[x][y - 1][z] == second_type:
                                matrix[x][y][z] = second_type
        return matrix

    @staticmethod
    def NextGenerationLandsForHighVectorized(matrix, first_type, second_type, y):
        """the ordered state of land and sea with vectorized"""
        layer = matrix[:, y, :]

        second_mask = (layer == second_type).astype(np.int8)

        # 8 neighbors without center
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]], dtype=np.int8)

        # count the number of neighboring second type cells for each cell
        second_neighbors = convolve(second_mask, kernel, mode="constant")
        first_neighbors = 8 - second_neighbors

        # vector substitution
        new_layer = layer.copy()
        #Land->Air
        if y + 1 < matrix.shape[1]:
            vector_above = matrix[:, y + 1, :]
            vector_above_is_air = (vector_above == first_type)
            new_layer[(layer == second_type) & np.isin(first_neighbors, [3, 6, 7, 8]) & vector_above_is_air] = first_type
        #Air->Land
        if y - 1 >= 0:
            vector_below = matrix[:, y - 1, :]
            vector_below_is_earth = vector_below == second_type
            new_layer[(layer == first_type) & np.isin(second_neighbors, [3, 6, 7, 8]) & vector_below_is_earth] = second_type


        matrix[:, y, :] = new_layer
        return matrix
