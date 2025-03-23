
class TraverseSquareAlgorithm:
    @staticmethod
    def TraverseSquare(side_x, side_y, action):
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