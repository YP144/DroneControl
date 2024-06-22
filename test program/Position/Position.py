from ctypes.wintypes import RECT
import pygame as py


class PositionSystem:
    def __init__(self):
        self.font = py.font.SysFont('timesnewroman', 16)
        self.total_row = 15
        self.total_col = 4
        self.image = py.Surface((960, 500), py.SRCALPHA).convert_alpha()
        x_text = self.font.render(
            "x (cm)", True, (0, 0, 0)).convert_alpha()
        y_text = self.font.render(
            "y (cm)", True, (0, 0, 0)).convert_alpha()
        self.x_img = py.transform.rotozoom(x_text, 0, 1).convert_alpha()
        self.y_img = py.transform.rotozoom(y_text, 90, 1).convert_alpha()
        self.pos = py.Vector2(50, 70)
        self.all_rect = []
        self.draw_rect_pos = False
        id = 1
        for col in range(self.total_col):
            for row in range(self.total_row):
                x = 60*row
                y = 90*col
                pos = py.Vector2(x, y)
                rect = PosRect(self.image, 55+(50*row), 105 +
                               (75*col), id, pos)
                self.all_rect.append(rect)
                id += 1

    def draw(self, surface):
        self.image.fill((255, 255, 255))
        self.draw_coord()
        self.draw_rect()
        self.rot_img = py.transform.rotozoom(
            self.image, 0, 1).convert_alpha()

        surface.blit(self.rot_img, self.pos)
        surface.blit(self.y_img, self.pos+py.Vector2(-20, 190))
        surface.blit(self.x_img, self.pos+py.Vector2(380, 10))

    def draw_rect(self):
        if self.draw_rect_pos:
            for rect in self.all_rect:
                rect.draw()

    def draw_coord(self):
        for col in range(self.total_col):
            py.draw.line(self.image, (0, 0, 0),
                         (5, 105 + (75*col)), (15, 105 + (75*col)), 2)
            py.draw.line(self.image, (0, 0, 0),
                         (45, 105 + (75*col)), (842, 105 + (75*col)), 2)
            text = self.font.render(
                str(90*col), True, (0, 0, 0)).convert_alpha()
            self.image.blit(text, (20, 95+(75*col)))
            for row in range(self.total_row):
                if col == 0:
                    py.draw.line(self.image, (0, 0, 0),
                                 (55+(50*row), 42), (55+(50*row), 50), 2)
                    py.draw.line(self.image, (0, 0, 0),
                                 (55+(50*row), 75), (55+(50*row), 390), 2)
                    text = self.font.render(
                        str(60*row), True, (0, 0, 0)).convert_alpha()
                    self.image.blit(text, (50+(50*row), 55))
        py.draw.rect(
            self.image, (0, 0, 0), (5, 40, 840, 350), 2)


class PosRect:
    def __init__(self, surface, x, y, id, carried_pos):
        self.width, self.height = 10, 10
        self.id = id
        self.pos = py.Vector2(x, y)
        self.surface = surface
        self.rect = py.Rect(self.pos.x, self.pos.y, self.width, self.height)
        self.rect.center = self.pos
        self.carried_pos = carried_pos

    def draw(self):
        self.rect = py.draw.rect(self.surface, (255, 0, 0), self.rect)
