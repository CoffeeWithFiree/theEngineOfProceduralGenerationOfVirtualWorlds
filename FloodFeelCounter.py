from BiomesType import BiomesType


class FloodFeelCounter:
    def __init__(self, matrix, matrix_cond, x, z, value, np, min_limit = 0):
        self.matrix = matrix
        self.matrix_cond = matrix_cond
        self.x = x
        self.z = z
        self.x_len = len(matrix)
        self.z_len = len(matrix[0][0])
        self.condition = matrix[x][0][z]
        self.value = value
        self.np = np
        self.min_limit = min_limit


    def Feel(self):
        stack_ = [(self.x, self.z)]
        counter = 0
        while stack_:

            r, c = stack_.pop()
            if self.matrix[r][0][c] == self.condition and self.matrix_cond[r][c] == 0:
                self.matrix_cond[r][c] = self.value
                counter += 1

                if r + 1 < self.x_len:
                    stack_.append((r + 1, c))
                if r - 1 >= 0:
                    stack_.append((r - 1, c))
                if c + 1 < self.z_len:
                    stack_.append((r, c + 1))
                if c - 1 >= 0:
                    stack_.append((r, c - 1))

        return self.matrix_cond, counter
