from Rasterization3D import Rasterization3D
from CellularAutomata import CellularAutomata
import numpy as np
import pygame as pg

import time


class main():

    def __init__(self):
        self.start_time = time.time()
        pg.init()
        self.graphic3D = Rasterization3D(self, pg, np)
        self.screen = self.graphic3D.screen
        self.cell_automata = CellularAutomata(pg, np, self.graphic3D)

        #self.font = pg.font.SysFont('Arial', 30)

    def run(self):

        pg.display.set_caption('Rasterization')

        self.cell_automata.DrawingScene()

        print(f"Generation completed in {time.time() - self.start_time} seconds")
        # running = True
        # while running:
        #     for event in pg.event.get():
        #         if event.type == pg.QUIT:
        #             running = False
        #
        #     self.screen.fill((255, 255, 255))
        #     text = self.font.render(f"Generation complete: {end_time-start_time}", True, (0, 0, 0))
        #     text_rect = text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        #     self.screen.blit(text, text_rect)
        #
        #     pg.display.flip()
        #
        # pg.quit()

if __name__ == "__main__":
    app = main()
    app.run()