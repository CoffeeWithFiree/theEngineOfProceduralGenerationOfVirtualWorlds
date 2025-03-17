import pandas as pd

class WriteExcel:
    def __init__(self, matrix, matrix_cond, matrix_filename = "matrix.xlsx", cond_filename = "matrix_cond.xlsx"):
        self.matrix = matrix
        self.matrix_cond = matrix_cond
        self.matrix_filename = matrix_filename
        self.cond_filename = cond_filename
        self.ExportMatricesToExcel()

    def ExportMatricesToExcel(self):
        """a function that exports 2 matrices (self.matrix and self.matrix_cond) to excel"""
        matrix_lower_layer = [[self.matrix[x][0][y] for y in range(len(self.matrix[x][0]))] for x in
                              range(len(self.matrix))]

        df_matrix = pd.DataFrame(matrix_lower_layer)
        df_matrix_cond = pd.DataFrame(self.matrix_cond)

        df_matrix.to_excel(self.matrix_filename, index=False, header=False)
        df_matrix_cond.to_excel(self.cond_filename, index=False, header=False)
