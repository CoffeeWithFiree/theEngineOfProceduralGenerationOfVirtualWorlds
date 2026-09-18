class SearchingIslandGeometricCenterAndBorders:
    @staticmethod
    def SearcIslGeomCentAndBords(number_of_land, matrix_cond):
        """search for the geometric central cell of the island and borders"""
        sides_x = [len(matrix_cond), 0]  # min and max
        sides_y = [len(matrix_cond[0]), 0]  # min and max

        for x in range(len(matrix_cond)):
            for y in range(len(matrix_cond[x])):
                if matrix_cond[x][y] == number_of_land:
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