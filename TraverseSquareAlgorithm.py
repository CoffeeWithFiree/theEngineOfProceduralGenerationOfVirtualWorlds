
class TraverseSquareAlgorithm:
    @staticmethod
    def TraverseSquare(side_x, side_y, action):
        """The square passage algorithm"""
        d_x = side_x[0]
        for d_y in range(side_y[0], side_y[1] + 1):
            action(d_x, d_y)

        d_y = side_y[0]
        for d_x in range(side_x[0], side_x[1] + 1):
            action(d_x, d_y)

        d_x = side_x[1]
        for d_y in range(side_y[0], side_y[1] + 1):
            action(d_x, d_y)

        d_y = side_y[1]
        for d_x in range(side_x[0], side_x[1] + 1):
            action(d_x, d_y)

    @staticmethod
    def TraverseSquareExpandingFromPoint(start_x, start_y, matrix_cond, action):
        """A square algorithm that expands from a point and has no explicit boundaries"""
        min_x, max_x = start_x, start_x
        min_y, max_y = start_y, start_y

        while min_x >= 0 or max_x < len(matrix_cond) or min_y >= 0 or max_y < len(matrix_cond[0]):

            x = min_x
            for y in range(min_y, max_y + 1):
                action(x, y)

            x = max_x
            for y in range(min_y, max_y + 1):
                action(x, y)

            y = min_y
            for x in range(min_x, max_x + 1):
                action(x, y)

            y = max_y
            for x in range(min_x, max_x + 1):
                action(x, y)

            min_x -= 1
            max_x += 1
            min_y -= 1
            max_y += 1

            min_x = max(0, min_x)
            max_x = min(max_x, len(matrix_cond) - 1)
            min_y = max(0, min_y)
            max_y = min(max_y, len(matrix_cond[0]) - 1)

        else:
            raise Exception(f"The boundaries of the world have been reached")