from Window import *

class River():
    river_width = params['river width']
    river_height = params['river height']
    river_corner_x = WIDTH / 2
    # river_corner_x = WIDTH / 2 - 1.5 * river_width / 2

    def draw_river(self, sc):
        x, y = WIDTH / 2 - 1.5 * self.river_width / 2, 0
        pygame.draw.rect(sc, Colors.BLUE, (self.river_corner_x, 0, self.river_width, HEIGHT))
        pygame.draw.rect(sc, Colors.BLUE, (self.river_corner_x, 0, WIDTH, self.river_height))