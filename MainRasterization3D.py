from Rasterization3D import Rasterization3D
from CellularAutomata import CellularAutomata
import numpy as np
import pygame as pg


class main():

    def __init__(self):
        pg.init()
        self.graphic3D = Rasterization3D(self, pg, np)
        self.screen = self.graphic3D.screen
        self.cell_automata = CellularAutomata(pg, np, self.graphic3D)

        self.font = pg.font.SysFont('Arial', 30)

    def run(self):


        pg.display.set_caption('Rasterization')

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            self.screen.fill((255, 255, 255))

            self.cell_automata.DrawingScene()

            text = self.font.render("Generation complete", True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
            self.screen.blit(text, text_rect)

            pg.display.flip()

        pg.quit()

if __name__ == "__main__":
    app = main()
    app.run()