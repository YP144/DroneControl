import pygame as py


class Button(py.sprite.Sprite):
    def __init__(self, position, text, type='push', condition=True, * groups):
        super().__init__(*groups)
        self.position = py.Vector2(position)
        self.default_color = (53, 123, 174)
        self.pushed_color = (255, 105, 97)
        self.disabled_color = (174, 198, 207)
        self.font_default_color = (255, 255, 255)
        self.font_disable_color = (0, 0, 0)
        self.color = self.default_color
        self.font_color = self.font_default_color
        self.text = text
        self.disable_text = "Disabled"
        self.scale = 1
        self.font_scale = 1
        self.font = py.font.SysFont(
            'timesnewroman', int(18 * self.font_scale), bold=True)
        self.clicked = False
        self.type = type
        self.action = False
        self.enable = condition
        text = self.font.render(
            self.text, True, self.font_color).convert_alpha()
        text_rect = text.get_rect()
        w, h = text_rect.size
        self.image = py.Surface(
            (w+30, h+30), py.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect(center=self.position)
        self.id = (self.text.replace(" ", "")).lower()

    def update(self, surface, surface_position, scale=1):
        text = self.font.render(
            self.text, True, self.font_color).convert_alpha()
        text_rect = text.get_rect()
        w, h = text_rect.size
        self.image = py.Surface(
            (w+21, h+21), py.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect(center=self.position)
        self.bg_rect_value = py.Rect(0, 0, w+20, h+20)
        self.bg_rect = py.draw.rect(
            self.image, self.color, self.bg_rect_value, border_radius=15)
        self.image.blit(text, (0.1*w, 0.4*h))
        self.orig_image = self.image
        self.image = py.transform.rotozoom(
            self.orig_image, 0, self.scale).convert_alpha()
        self.surface = surface
        self.surface_position = surface_position
        self.scale = scale

    def isClicked(self, surface_position):
        self.surface_position = surface_position

        mouse_pos = py.mouse.get_pos() - self.surface_position
        if self.enable:
            if self.type == 'push':
                self.action = False
                if self.rect.collidepoint(mouse_pos) and not self.clicked:
                    if py.mouse.get_pressed()[0]:
                        self.action = True
                        self.clicked = True
                if not py.mouse.get_pressed()[0]:
                    self.clicked = False
            if self.type == 'toggle':
                if self.rect.collidepoint(mouse_pos) and py.mouse.get_pressed()[0]:
                    if not self.clicked and not self.action:
                        self.action = True
                        self.clicked = True
                    if not self.clicked and self.action:
                        self.action = False
                        self.clicked = True
                if not py.mouse.get_pressed()[0]:
                    self.clicked = False
            if self.type == 'hold':
                self.action = False
                if self.rect.collidepoint(mouse_pos) and py.mouse.get_pressed()[0]:
                    self.action = True

            if self.action:
                self.color = self.pushed_color
                self.font_color = self.font_default_color
            else:
                self.color = self.default_color
                self.font_color = self.font_default_color
        else:
            # disable_text = self.font.render(
            #     self.disable_text, True, self.font_disable_color)
            # disable_text_rect = disable_text.get_rect()
            # w, h = disable_text_rect.size
            # if self.rect.collidepoint(mouse_pos):
            #     py.draw.rect(self.surface, (255, 184, 97),
            #                  py.Rect(mouse_pos[0]+10, mouse_pos[1]+10, w, h), border_radius=5)
            #     self.surface.blit(
            #         disable_text, mouse_pos + py.Vector2(10, 10))
            self.color = self.disabled_color
            self.font_color = self.font_disable_color
        return self.action

    def update_position(self, position):
        self.position = py.Vector2(position)

    def update_size(self, multiplier=1):
        ws, hs = self.surface.get_size()
        screen_area = (ws*hs)/304618
        self.scale = max(0.6, round(screen_area, 1)*multiplier)

    def get_size(self):
        ws, hs = self.image.get_size()
        return (ws, hs)
