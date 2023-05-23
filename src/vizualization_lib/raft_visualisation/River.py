from vizualization_lib.raft_visualisation.Window import *

class River():
    # river_width = 100
    river_corner_x = WIDTH / 2
    # river_corner_x = WIDTH / 2 - 1.5 * river_width / 2

    def draw_river(self, sc, river_width, river_height, HEIGHT, WIDTH):
        x, y = WIDTH / 2 - 1.5 * river_width / 2, 0
        pygame.draw.rect(sc, Colors.BLUE, (self.river_corner_x, river_height, river_width, HEIGHT))
        pygame.draw.rect(sc, Colors.BLUE, (self.river_corner_x, river_height, WIDTH, river_height))