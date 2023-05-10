import pygame
import Colors
import random
from River import *
from Window import *
from Raft import *
import Params


param_window = ParamWindow()
river = River()
raft = Raft()

def get_labels():
    labels = []
    for key in Params.params:
        down = params_limits[key + " down"]
        up = params_limits[key + " up"]
        label = "[" + str(down) + " : " + str(up) + "]"
        labels.append(label)
        print(label)
    return labels


def game_loop(sc, clock):
    running = True
    input_boxes = param_window.create_input_boxes()
    x, y = river.river_corner_x + constant_params["river width"]/2, HEIGHT/2
    labels = get_labels()
    angle = 0
    while running:
        sc.fill(Colors.GREEN)
        river.draw_river(sc)

        x, y, angle = raft.draw_raft(sc, x, y, angle)
        param_window.draw_param_window(sc)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            for box in input_boxes:
                box.handle_event(event, sc)
        for i in range(len(input_boxes)):
            input_boxes[i].update()
            input_boxes[i].draw_limits(sc, labels[i])

        for box in input_boxes:
            box.draw(sc)

        pygame.display.flip()
        clock.tick(FPS)

def main():
    pygame.init()
    sc = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Raft simulator")
    clock = pygame.time.Clock()
    game_loop(sc, clock)
    pygame.quit()


if __name__ == '__main__':
    main()
