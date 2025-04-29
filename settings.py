class settings():
    Vw = 1400
    Vh = 1000

    # Cw, Ch: the viewing window
    d = 1000
    Cw = 800
    Ch = 600

    #Standart CeccularAutomata

    #y is height

    Res = [24, 12, 24] #x #y #z

    width = 12  #x
    height = 6 #y
    length = 12 #z

    color_land = (0, 153, 0)
    color_sea = (0, 102, 255)

    #RougeLikeKA

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

