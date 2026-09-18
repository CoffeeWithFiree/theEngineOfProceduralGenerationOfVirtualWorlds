class CellsAround:
    @staticmethod
    def EightCellsAround(x, y, action, columns, rows):
        # [x - 1][z - 1]
        if (x - 1) >= 0 and (y - 1) >= 0:
            action(x - 1, y - 1)

        # [x][z - 1]
        if (y - 1) >= 0:
            action(x, y - 1)

        # [x + 1][z - 1]
        if (x + 1) <= (columns - 1) and (y - 1) >= 0:
            action(x + 1, y - 1)

        # [x - 1][z]
        if (x - 1) >= 0:
            action(x - 1, y)

        # [x + 1][z]
        if (x + 1) <= (columns - 1):
            action(x + 1, y)

        # [x - 1][z + 1]
        if (x - 1) >= 0 and (y + 1 <= (rows - 1)):
            action(x - 1, y + 1)

        # [x][z + 1]
        if (y + 1 <= (rows - 1)):
            action(x, y + 1)

        # [x + 1][z + 1]
        if ((x + 1) <= (columns - 1)) and (y + 1 <= (rows - 1)):
            action(x + 1, y + 1)

    @staticmethod
    def FourCellsAround(x, y, action, columns, rows):

        # [x][z - 1]
        if (y - 1) >= 0:
            action(x, y - 1)

        # [x - 1][z]
        if (x - 1) >= 0:
            action(x - 1, y)

        # [x + 1][z]
        if (x + 1) <= (columns - 1):
            action(x + 1, y)


        # [x][z + 1]
        if (y + 1 <= (rows - 1)):
            action(x, y + 1)

