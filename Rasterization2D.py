from math import floor

class Rasterization2D:

    def __init__(self, screen, pg):
        self.screen = screen
        self.pg = pg

    def DrawLine(self, P0, P1, color):
       x0 = P0[0]
       x1 = P1[0]
       y0 = P0[1]
       y1 = P1[1]
       a = (y1 - y0) / (x1 - x0)
       b = y0 - a * x0
       for x in range(x0, x1):
          y = a * x + b
          self.pg.draw.circle(self.screen, color, (x, y), 1)

    def DrawLineV2(self, P0, P1, color):
        x0 = P0[0]
        x1 = P1[0]
        y0 = P0[1]
        y1 = P1[1]
        a = (y1 - y0) / (x1 - x0)
        y = y0
        for x in range(x0, x1):
            self.pg.draw.circle(self.screen, color, (x, y), 1)
            y += a

    def DrawLineV3(self, P0, P1, color):
        if P0[0] > P1[0]:
            cur = P0
            P0 = P1
            P1 = cur
        x0 = P0[0]
        x1 = P1[0]
        y0 = P0[1]
        y1 = P1[1]
        a = (y1 - y0) / (x1 - x0)
        y = y0
        for x in range(x0, x1):
            self.pg.draw.circle(self.screen, color, (x, y), 1)
            y += a

    def DrawLineV4(self, P0, P1, color):
        x0 = P0[0]
        x1 = P1[0]
        y0 = P0[1]
        y1 = P1[1]
        dx = x1 - x0
        dy = y1 - y0
        if abs(dx) > abs(dy):
            #The straight line is closer to the horizontal
            if P0[0] > P1[0]:
                cur = P0
                P0 = P1
                P1 = cur
                x0 = P0[0]
                x1 = P1[0]
                y0 = P0[1]
                y1 = P1[1]
            a = (y1 - y0) / (x1 - x0)
            y = y0
            for x in range(x0, x1):
                self.pg.draw.circle(self.screen, color, (x, y), 1)
                y += a
        else:
            #The straight line is closer to the vertical
            if P0[1] > P1[1]:
                cur = P0
                P0 = P1
                P1 = cur
                x0 = P0[0]
                x1 = P1[0]
                y0 = P0[1]
                y1 = P1[1]
            a = (x1 - x0) / (y1 - y0)
            x = x0
            for y in range(y0, y1):
                self.pg.draw.circle(self.screen, color, (x, y), 1)
                x += a

    def DrawLineV5(self, P0, P1, color):
        x0 = P0[0]
        x1 = P1[0]
        y0 = P0[1]
        y1 = P1[1]
        dx = x1 - x0
        dy = y1 - y0
        if abs(dx) > abs(dy):
            #The straight line is closer to the horizontal
            if P0[0] > P1[0]:
                cur = P0
                P0 = P1
                P1 = cur
                x0 = P0[0]
                x1 = P1[0]
                y0 = P0[1]
                y1 = P1[1]
            ys = self.Interpolate(x0, y0, x1, y1)
            for x in range(int(x0), int(x1)):
                self.pg.draw.circle(self.screen, color, (x, ys[x-int(x0)]), 1)
        else:
            #The straight line is closer to the vertical
            if P0[1] > P1[1]:
                cur = P0
                P0 = P1
                P1 = cur
                x0 = P0[0]
                x1 = P1[0]
                y0 = P0[1]
                y1 = P1[1]
            xs = self.Interpolate(y0, x0, y1, x1)
            for y in range(int(y0), int(y1)):
                self.pg.draw.circle(self.screen, color, (xs[y - int(y0)], y), 1)

    def DrawLineBresenham(self, P0, P1, color):
        x0 = P0[0]
        x1 = P1[0]
        y0 = P0[1]
        y1 = P1[1]
        a = (y1 - y0) / (x1 - x0)
        y = y0
        c = 0
        for x in range(x0, x1):
            c += a
            if c > 0.5:
                c -= 1
                y += 1
            self.pg.draw.circle(self.screen, color, (x, y), 1)

    def DrawLineBresenhamV2(self, P0, P1, color):
        x0 = P0[0]
        x1 = P1[0]
        y0 = P0[1]
        y1 = P1[1]
        a = (y1 - y0) / (x1 - x0)
        y = y0
        d = 2*a - 1
        for x in range(x0, x1):
            if d > 0:
                d += 2 * a + 2
                y += 1
            else:
                d += 2 * a
            self.pg.draw.circle(self.screen, color, (x, y), 1)

    def DrawLineBresenhamV3(self, P0, P1, color):
        x0 = P0[0]
        x1 = P1[0]
        y0 = P0[1]
        y1 = P1[1]

        dx = x1 - x0
        dy = y1 - y0
        d1 = dy * 2
        d2 = (dy - dx) * 2
        d = (dy * 2) - dx
        y = y0

        for x in range(x0, x1):
            if d > 0:
                d += d2
                y += 1
            else:
                d += d1
            self.pg.draw.circle(self.screen, color, (x, y), 1)

    def DrawLineBresenhamV4(self, P0, P1, color):
        x0 = P0[0]
        x1 = P1[0]
        y0 = P0[1]
        y1 = P1[1]

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        d = (dy * 2) - dx

        if x1 >= x0:
            sx = 1
        else:
            sx = -1

        if y1 >= y0:
            sy = 1
        else:
            sy = -1

        if dy <= dx:
            d = (dy * 2) - dx
            d1 = dy * 2
            d2 = (dy - dx) * 2
            x = x0 + sx
            y = y0

            for x in range(x0, x1, sx):
                if d > 0:
                    d += d2
                    y += sy
                else:
                    d += d1
                self.pg.draw.circle(self.screen, color, (x, y), 1)

        else:
            d = (dx * 2) - dy
            d1 = dx * 2
            d2 = (dx - dy) * 2
            x = x0
            y = y0 + sy

            for y in range(y0, y1, sy):
                if d > 0:
                    d += d2
                    x += sx
                else:
                    d += d1
                self.pg.draw.circle(self.screen, color, (x, y), 1)

    def Interpolate(self, i0, d0, i1, d1): ######
        if i0 == i1:
            return [d0]
        values = []
        a = (d1 - d0) / (i1 - i0)
        d = d0
        for i in range(int(i0), int(i1)):
            values.append(d)
            d += a
        return values

    def DrawTriangle(self, P0, P1, P2, color):
        self.DrawLineV5(P0, P1, color)
        self.DrawLineV5(P1, P2, color)
        self.DrawLineV5(P2, P0, color)

    def DrawFilledTriangle(self, P0, P1, P2, color):
        #Sort y0 <= y1 <= y2
        if P1[1] < P0[1]:
            cur = P1
            P1 = P0
            P0 = cur
        if P2[1] < P0[1]:
            cur = P2
            P2 = P0
            P0 = cur
        if P2[1] < P1[1]:
            cur = P2
            P2 = P1
            P1 = cur

        #Calculate Coordinates x of the edges of the triangle
        x01 = self.Interpolate(P0[1], P0[0], P1[1], P1[0])
        x12 = self.Interpolate(P1[1], P1[0], P2[1], P2[0])
        x02 = self.Interpolate(P0[1], P0[0], P2[1], P2[0])

        #Concatenation of short sides
        x01.pop()
        x012 = x01 + x12

        #Definde what side is left and right
        m = floor(len(x012) / 2)
        if x02[m] < x012[m]:
            x_left = x02
            x_right = x012
        else:
            x_left = x012
            x_right = x02
        #Drawing horizontal segments
        for y in range(P0[1], P2[1] - 1): 
            for x in range(floor(x_left[y - P0[1]]), floor(x_right[y - P0[1]])):
                self.pg.draw.circle(self.screen, color, (x,y), 1)

    def DrawShadedTriangle(self, P0, P1, P2, color):
        """P = [x, y, h]"""
        # Sort y0 <= y1 <= y2
        if P1[1] < P0[1]:
            cur = P1
            P1 = P0
            P0 = cur
        if P2[1] < P0[1]:
            cur = P2
            P2 = P0
            P0 = cur
        if P2[1] < P1[1]:
            cur = P2
            P2 = P1
            P1 = cur
        # Calculate Coordinates x and h of the edges of the triangle
        x01 = self.Interpolate(P0[1], P0[0], P1[1], P1[0])
        h01 = self.Interpolate(P0[1], P0[2], P1[1], P1[2])

        x12 = self.Interpolate(P1[1], P1[0], P2[1], P2[0])
        h12 = self.Interpolate(P1[1], P1[2], P2[1], P2[2])

        x02 = self.Interpolate(P0[1], P0[0], P2[1], P2[0])
        h02 = self.Interpolate(P0[1], P0[2], P2[1], P2[2])

        # Concatenation of short sides
        x01.pop()
        x012 = x01 + x12
        h01.pop()
        h012 = h01 + h12

        # Definde what side is left and right
        m = floor(len(x012) / 2)
        if x02[m] < x012[m]:
            x_left = x02
            h_left = h02
            x_right = x012
            h_right = h012
        else:
            x_left = x012
            h_left = h012
            x_right = x02
            h_right = h02

        # Drawing horizontal segments
        for y in range(P0[1], P2[1] - 1):
            x_l = x_left[y - P0[1]]
            x_r = x_right[y - P0[1]]

            h_segment = self.Interpolate(x_l, h_left[y - P0[1]],
                                    x_r, h_right[y - P0[1]])
            for x in range(int(x_l), int(x_r)):
                c1 = color[0] * h_segment[x - int(x_l)]
                c2 = color[1] * h_segment[x - int(x_l)]
                c3 = color[2] * h_segment[x - int(x_l)]
                shaded_color = [c1, c2, c3]
                self.pg.draw.circle(self.screen, shaded_color, (x, y), 1)

    def DrawGradientTriangle(self, P0, P1, P2, color0, color1, color2):
        # Sort vertices by y-coordinate
        if P1[1] < P0[1]:
            P0, P1 = P1, P0
            color0, color1 = color1, color0
        if P2[1] < P0[1]:
            P0, P2 = P2, P0
            color0, color2 = color2, color0
        if P2[1] < P1[1]:
            P1, P2 = P2, P1
            color1, color2 = color2, color1

        # Calculate x and color interpolation for the edges of the triangle
        x01 = self.Interpolate(P0[1], P0[0], P1[1], P1[0])
        color01_r = self.Interpolate(P0[1], color0[0], P1[1], color1[0])
        color01_g = self.Interpolate(P0[1], color0[1], P1[1], color1[1])
        color01_b = self.Interpolate(P0[1], color0[2], P1[1], color1[2])

        x12 = self.Interpolate(P1[1], P1[0], P2[1], P2[0])
        color12_r = self.Interpolate(P1[1], color1[0], P2[1], color2[0])
        color12_g = self.Interpolate(P1[1], color1[1], P2[1], color2[1])
        color12_b = self.Interpolate(P1[1], color1[2], P2[1], color2[2])

        x02 = self.Interpolate(P0[1], P0[0], P2[1], P2[0])
        color02_r = self.Interpolate(P0[1], color0[0], P2[1], color2[0])
        color02_g = self.Interpolate(P0[1], color0[1], P2[1], color2[1])
        color02_b = self.Interpolate(P0[1], color0[2], P2[1], color2[2])

        # Concatenate short sides
        x01.pop()
        x012 = x01 + x12
        color01_r.pop()
        color012_r = color01_r + color12_r
        color01_g.pop()
        color012_g = color01_g + color12_g
        color01_b.pop()
        color012_b = color01_b + color12_b

        # Determine which side is left and which is right
        m = floor(len(x012) / 2)
        if x02[m] < x012[m]:
            x_left = x02
            color_left_r = color02_r
            color_left_g = color02_g
            color_left_b = color02_b
            x_right = x012
            color_right_r = color012_r
            color_right_g = color012_g
            color_right_b = color012_b
        else:
            x_left = x012
            color_left_r = color012_r
            color_left_g = color012_g
            color_left_b = color012_b
            x_right = x02
            color_right_r = color02_r
            color_right_g = color02_g
            color_right_b = color02_b

        # Drawing horizontal segments
        for y in range(P0[1], P2[1]):
            if y - P0[1] < len(x_left) and y - P0[1] < len(x_right):
                x_l = x_left[y - P0[1]]
                x_r = x_right[y - P0[1]]

                color_segment_r = self.Interpolate(int(x_l), color_left_r[y - P0[1]],
                                              int(x_r), color_right_r[y - P0[1]])
                color_segment_g = self.Interpolate(int(x_l), color_left_g[y - P0[1]],
                                              int(x_r), color_right_g[y - P0[1]])
                color_segment_b = self.Interpolate(int(x_l), color_left_b[y - P0[1]],
                                              int(x_r), color_right_b[y - P0[1]])

                for x in range(int(x_l), int(x_r)):
                    c1 = color_segment_r[x - int(x_l)]
                    c2 = color_segment_g[x - int(x_l)]
                    c3 = color_segment_b[x - int(x_l)]
                    gradient_color = [int(c1), int(c2), int(c3)]
                    self.pg.draw.circle(self.screen, gradient_color, (x, y), 1)
