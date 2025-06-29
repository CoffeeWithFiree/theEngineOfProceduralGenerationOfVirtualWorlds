import numpy as np
class settings():
    Vw = 1400
    Vh = 1000

    # Cw, Ch: the viewing window
    d = 1000
    Cw = 800
    Ch = 600

    #Standart CeccularAutomata

    #y is height

    Res = [80, 24, 80] #x #y #z

    width = 40  #x
    height = 12#y
    length = 40 #z

    color_land = (0, 153, 0)
    color_sea = (0, 102, 255)

    #RougeLikeKA

    need_lands = np.array([9, 10, 11, 12, 13])
    need_size = np.array([18, 19, 20, 21, 22, 23])  # min and max

    Res_RL = [48, 4, 48] #x #y # z

    rows = 24
    heights = 2
    columns = 24

    basicX = Res_RL[0] / rows
    basicY = Res_RL[1] / heights
    basicZ = Res_RL[2] / columns

    width_RL = 24 #x
    height_RL = 2 #y
    length_RL = 24 #z

    color_land_RL = (0, 153, 0)
    color_tunnel = (255, 0, 0)
    color_start = (0, 42, 255)
    color_end = (0, 238, 255)

