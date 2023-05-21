import pygame
import math

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
    x_turn = []
    y_turn= []
    angle_coords = []

    def up_ledge_center_coord(self, x, y):
        l_x = x + params["raft width"]/2
        l_y = y - params["triangle height"]/2
        return l_x, l_y

    def down_ledge_center_coord(self, x, y):
        l_x = x + params["raft width"]/2
        l_y = y + params["raft height"] + params["triangle height"]/2
        return l_x, l_y


    def count_coord_y(self, cur_x, cur_y):
        cur_y -= 5
        if cur_y == 0:
            cur_y = HEIGHT
        return cur_y
    

    def turn_coords(self, i):
        x = self.x_turn[i]
        y = self.y_turn[i]
        angle = self.angle_turn[i]
        return angle


    def count_coordinates(self, x, y, angle, i):
        if y > params["river width"] - 3:
            angle = 0
            y -= 5
        elif y > params["raft width"] - 20:
            angle = self.turn_coords(i)
            # angle += 5
            x += 5
            y -=5
            i += 1
        else:
            angle = 90
            # y = 0
            x += 5
        if x > Window.WIDTH:
           x, y = River.river_corner_x + params["river width"]/4, HEIGHT
           angle = 0
        return x, y, angle, i
    
    def rotate(self, surface, angle, pivot, offset):
        rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
        rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
        # Add the offset vector to the center/pivot point to shift the rect.
        rect = rotated_image.get_rect(center=pivot + rotated_offset)
        return rotated_image, rect  # Return the rotated image and shifted rect.

    def draw_raft(self, sc, x=start_x, y=start_y, angle=0, i = 0):
        x, y, angle, i = self.count_coordinates(x, y, angle, i)
        rect_surf = pygame.Surface((params["raft width"], params["raft height"]), pygame.SRCALPHA)
        rect_surf.fill(Colors.BROWN)
        # rect_surf.set_colorkey(Colors.BLACK)
        pivot = [x, y]
        offset = pygame.math.Vector2(0, 0)
        rotated_image, rect = self.rotate(rect_surf, angle, pivot, offset)
        sc.blit(rotated_image, rect)

        # Draw protrusions
        rotated_triangle_points = []
        triangle_points = [
            (x - params["triangle width"]/2, y - params["raft height"]/2),
            (x, y - params["raft height"]/2 - params["triangle height"]),
            (x  + params["triangle width"]/2, y - params["raft height"]/2)
        ]
        for point in triangle_points:
            rotated_point = self.rotate_point(point, angle, pivot)
            rotated_triangle_points.append(rotated_point)
        pygame.draw.polygon(sc, Colors.BROWN, rotated_triangle_points)

        triangle_points = [
            (x - params["triangle width"]/2, y + params["raft height"]/2),
            (x, y + params["raft height"]/2 + params["triangle height"]),
            (x + params["triangle width"]/2, y + params["raft height"]/2)
        ]
        for point in triangle_points:
            rotated_point = self.rotate_point(point, angle, pivot)
            rotated_triangle_points.append(rotated_point)
        pygame.draw.polygon(sc, Colors.BROWN, rotated_triangle_points)

        return x, y, angle, i
    

    def rotate_point(self, point, angle, pivot):
        x, y = point
        px, py = pivot
        nx = px + (x - px) * math.cos(math.radians(angle)) - (y - py) * math.sin(math.radians(angle))
        ny = py + (x - px) * math.sin(math.radians(angle)) + (y - py) * math.cos(math.radians(angle))
        return int(nx), int(ny)

