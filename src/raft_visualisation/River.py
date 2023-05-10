from Window import *

class River():
    river_width = 200
    river_corner_x = WIDTH / 2
    # river_corner_x = WIDTH / 2 - 1.5 * river_width / 2

    def draw_river(self, sc, river_width=200):
        x, y = WIDTH / 2 - 1.5 * river_width / 2, 0
        pygame.draw.rect(sc, Colors.BLUE, (self.river_corner_x, 0, river_width, HEIGHT))
        pygame.draw.rect(sc, Colors.BLUE, (self.river_corner_x, 0, WIDTH, river_width))