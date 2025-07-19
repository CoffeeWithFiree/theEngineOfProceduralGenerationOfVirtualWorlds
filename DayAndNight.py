from CellsAround import CellsAround
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
                            if matrix[x][y + 1][z] == first_type:
                                matrix[x][y][z] = first_type

                    # current cell is air
                    elif matrix[x][y][z] == first_type:
                        if counters["land_counter"] in warning_amounts:
                            matrix[x][y][z] = second_type
        return matrix