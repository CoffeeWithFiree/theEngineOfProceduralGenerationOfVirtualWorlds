from Rasterization3D import Rasterization3D
from RoguelikeKA import RoguelikeKA

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

            pg.display.flip()

        pg.quit()

if __name__ == "__main__":
    app = main()
    app.run()