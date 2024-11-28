from Rasterization3D import Rasterization3D
from CellularAutomata import CellularAutomata
from RoguelikeKA import RoguelikeKA
# from BiomesType import BiomesType
# from settings import settings

import numpy as np
import pygame as pg


class main():

    def __init__(self):
        self.graphic3D = Rasterization3D(self, pg, np)
        self.screen = self.graphic3D.screen
        #self.cell_automata = CellularAutomata(self, pg, np, self.graphic3D)
        self.cell_automata = RoguelikeKA(self, pg, np, self.graphic3D)

    def run(self):

        pg.init()

        pg.display.set_caption('Rasterization')

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            self.screen.fill((255, 255, 255))

            self.cell_automata.DrawingScene()

            # vertices = {0: np.array([1, 1, 1]),
            #             1: np.array([-1, 1, 1]),
            #             2: np.array([-1, -1, 1]),
            #             3: np.array([1, -1, 1]),
            #             4: np.array([1, 1, -1]),
            #             5: np.array([-1, 1, -1]),
            #             6: np.array([-1, -1, -1]),
            #             7: np.array([1, -1, -1])}
            #
            # triangles = {0: {0: vertices[0], 1: vertices[1], 2: vertices[2], "color": (83, 55, 122)},
            #              1: {0: vertices[0], 2: vertices[2], 3: vertices[3], "color": (83, 88, 122)},
            #              2: {4: vertices[4], 0: vertices[0], 3: vertices[3], "color": (10, 58, 0)},
            #              3: {4: vertices[4], 3: vertices[3], 7: vertices[7], "color": (10, 58, 0)},
            #              4: {5: vertices[5], 4: vertices[4], 7: vertices[7], "color": (0, 55, 100)},
            #              5: {5: vertices[5], 7: vertices[7], 6: vertices[6], "color": (0, 55, 100)},
            #              6: {1: vertices[1], 5: vertices[5], 6: vertices[6], "color": (255, 255, 0)},
            #              7: {1: vertices[1], 6: vertices[6], 2: vertices[2], "color": (255, 255, 0)},
            #              8: {4: vertices[4], 5: vertices[5], 1: vertices[1], "color": (128, 0, 128)},
            #              9: {4: vertices[4], 1: vertices[1], 0: vertices[0], "color": (128, 0, 128)},
            #              10: {2: vertices[2], 6: vertices[6], 7: vertices[7], "color": (0, 255, 255)},
            #              11: {2: vertices[2], 7: vertices[7], 3: vertices[3], "color": (0, 255, 255)}}


            # position = np.array([2, 5, 10])
            # position2 = np.array([4, 5, 10])
            # position3 = np.array([2, 5, 12])
            # position4 = np.array([4, 5, 12])
            # position5 = np.array([3, 3, 11])
            #
            # #Object 2
            #
            # object1 = {
            #     "vertices": vertices,
            #     "triangles": triangles,
            #     "postition": position
            # }
            # object2 = {
            #     "vertices": vertices,
            #     "triangles": triangles,
            #     "postition": position2
            # }
            #
            # object3 = {
            #     "vertices": vertices,
            #     "triangles": triangles,
            #     "postition": position3
            # }
            #
            # object4 = {
            #     "vertices": vertices,
            #     "triangles": triangles,
            #     "postition": position4
            # }
            #
            # object5 = {
            #     "vertices": vertices,
            #     "triangles": triangles,
            #     "postition": position5
            # }
            #
            # objects = {
            #     "object1": object1,
            #     "object2": object2,
            #     "object3": object3,
            #     "object4": object4,
            #     "object5": object5
            # }

            #self.graphic3D.RenderScene(objects)



            pg.display.flip()

        pg.quit()

if __name__ == "__main__":
    app = main()
    app.run()