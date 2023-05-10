import pygame
from Params import *
import Colors

WIDTH = 1000  # ширина игрового окна
HEIGHT = 800 # высота игрового окна
FPS = 30 # частота кадров в секунду



class ParamWindow():
    param_window_x = 0
    param_window_y = 0
    param_window_width = 350
    param_window_height = HEIGHT
    space = 10
    btn_width = param_window_width
    btn_height = 32
    coord_x = 30
    coord_y = 100
    btn_x = coord_x
    btn_y = (btn_height + space)*len(params)


    def create_input_boxes(self):
        boxes = []
        x, y = 10, self.btn_height * 2
        for key in params:
            box = InputBox(x, y, 10, self.btn_height, text=key+"="+str(params[key]))
            y += self.btn_height * 2.5
            boxes.append(box)
        return boxes

    def draw_header(self, sc):
        pygame.draw.rect(sc, Colors.DARK_GREY, (
            0, 0, self.param_window_width, self.btn_height))


    def draw_param_window(self, sc):
        pygame.draw.rect(sc, Colors.GREY, (
            self.param_window_x, self.param_window_y, self.param_window_width, self.param_window_height))
        self.draw_header(sc)


class InputBox:
    pygame.init()
    FONT = pygame.font.Font(None, 32)

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = Colors.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.label = text.partition('=')[0] + text.partition('=')[1]
        self.active = False

    def handle_event(self, event, sc):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = True
                # self.active = not self.actived

            else:
                self.active = False

            # Change the current color of the input box.
            self.color = Colors.COLOR_ACTIVE if self.active else Colors.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # print(self.text)
                    if self.check_params(self.text):
                        print(self.text)
                        self.color = Colors.COLOR_ACTIVE if self.active else Colors.COLOR_INACTIVE
                        params[self.text.partition("=")[0]] = int(self.text.partition("=")[2])
                    else:
                        text = self.get_limits_text(self.text)
                        print(text)
                        text1 = self.FONT.render(text, True, Colors.RED)
                        sc.blit(text1, (self.rect.x, self.rect.y))
                        self.color = Colors.ERROR
                elif event.key == pygame.K_BACKSPACE:
                    if len(self.text) >= len(self.label)+1:
                        self.text = self.text[:-1]
                else:
                    new_txt = event.unicode
                    if len(self.text) < 18:
                        self.text += new_txt
                # Re-render the text.

                self.txt_surface = self.FONT.render(self.text, True, Colors.BLACK)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        if width < 220:
            self.rect.w = width

    def draw_limits(self, sc, label):
        text =self.FONT.render(label, False,Colors.BLACK)
        sc.blit(text, (self.rect.x + self.rect.width * 1.1, self.rect.y) )

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_limits_text(self, text):
        lbl = text.partition("=")[0]
        value = text.partition("=")[2]
        down = params_limits[lbl + " down"]
        up = params_limits[lbl + " up"]
        label = "[" + str(down) +" : "  +  str(up) + "]"

    def check_params(self, text):
        label = text.partition("=")[0]
        value = text.partition("=")[2]
        return int(value) > params_limits[label + " down"] and int(value) < params_limits[label + " up"]
