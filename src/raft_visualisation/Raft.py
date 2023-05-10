import pygame

import Colors
from Window import *
from River import *
from Params import *
import Window


class Raft():
    river = River()
    raft_width = 150
    raft_height = 50
    triangle_width = 20
    triangle_height = 25
    start_x = river.river_corner_x + river.river_width/2 - raft_width/2
    start_y = raft_height/2

    def up_ledge_center_coord(self,x, y):
        l_x = x - params["raft width"] / 2 + params["dist from left"] + params["triangle width"]/2
        l_y = y - params["raft height"]/2 - params["triangle height"]
        return l_x, l_y

    def down_ledge_center_coord(self, x, y):
        l_x = x - params["raft width"] / 2 + params["dist from left"] + params["triangle width"]/2
        l_y = y + params["raft height"]/2
        return l_x, l_y

    def count_coord_y(self, cur_x, cur_y):
        cur_y -= 5
        if cur_y == 0:
            cur_y = HEIGHT
        return cur_y

    def count_coordinates(self, x, y, angle):
        if y > constant_params["river width"] - 3:
            angle = 0
            y -= 5
        elif y > constant_params["river width"]/2:
            angle += 5
            x += 5
            y -=5
        else:
            x += 5
        if x > Window.WIDTH:
           x, y = River.river_corner_x + constant_params["river width"]/2, HEIGHT
           angle = 0
        return x, y, angle
    
    def rotate(self, surface, angle, pivot, offset):
        rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
        rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
        # Add the offset vector to the center/pivot point to shift the rect.
        rect = rotated_image.get_rect(center=pivot + rotated_offset)
        return rotated_image, rect  # Return the rotated image and shifted rect.

    def draw_raft(self, sc, x=start_x, y=start_y, angle=0):
        x, y, angle = self.count_coordinates(x, y, angle)
        rect_surf = pygame.Surface((params["raft width"], params["raft height"]), pygame.SRCALPHA)
        rect_surf.fill(Colors.BROWN)
        # rect_surf.set_colorkey(Colors.BLACK)
        pivot = [x, y]
        offset = pygame.math.Vector2(0, 0)
        rotated_image, rect = self.rotate(rect_surf, angle, pivot, offset)
        sc.blit(rotated_image, rect)

        # Draw protrusions
        triangle_points = [
            (x - params["raft width"]/2 + params["dist from left"], y - params["raft height"]/2),
            (x - params["raft width"]/2 + params["dist from left"] + params["triangle width"], y - params["raft height"]/2 - params["triangle height"]),
            (x - params["raft width"]/2 + params["dist from left"] + 2*params["triangle width"], y - params["raft height"]/2)
        ]
        pygame.draw.polygon(sc, Colors.BROWN, triangle_points)
        triangle_points = [
            (x - params["raft width"]/2 + params["dist from left"], y + params["raft height"]/2),
            (x - params["raft width"]/2 + params["dist from left"] + params["triangle width"], y + params["raft height"]/2 + params["triangle height"]),
            (x - params["raft width"]/2 + params["dist from left"] + 2*params["triangle width"], y + params["raft height"]/2)
        ]
        pygame.draw.polygon(sc, Colors.BROWN, triangle_points)

        return x, y, angle

