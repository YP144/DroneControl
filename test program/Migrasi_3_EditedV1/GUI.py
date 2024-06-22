import pygame as py


class GUI:
    """Graphical User Interface packaging"""
    default_width_value, default_height_value = 1, 1
    default_x_value, default_y_value = 1, 1
    default_color = (245, 243, 231)
    title_pos = py.Vector2(10, 10)

    def __init__(self, id, title):
        self.id = id
        self.title = title
        self.color_cream = (255, 253, 208)
        self.color_grey = (207, 207, 196)
        self.color_black = (0, 0, 0)
        self.color_red = (255, 87, 51)
        self.color_white = (255, 255, 255)
        self.disp_width, self.disp_height = py.display.get_surface().get_size()
        self.width_value, self.height_value = self.default_width_value, self.default_height_value
        self.font = py.font.SysFont('timesnewroman', 20)
        self.control_screen_state = 'main'
        self.width, self.height = self.width_value * \
            self.disp_width, self.height_value*self.disp_height
        self.screen_surface = py.Surface(
            (self.width, self.height), py.SRCALPHA).convert_alpha()
        self.x_value, self.y_value = self.default_x_value, self.default_y_value
        self.position = py.Vector2(
            self.x_value*self.disp_width, self.y_value*self.disp_height)
        self.screen_image = self.screen_surface
        self.screen_image.fill(self.default_color)
        self.screen_scale = 1

    def get_size(self):
        w, h = self.width, self.height
        return (w, h)

    def get_screen(self):
        screen = self.screen_surface
        size_screen = screen.get_size()
        return size_screen

    def update_screen(self):
        self.disp_width, self.disp_height = py.display.get_surface().get_size()
        self.width, self.height = self.width_value * \
            self.disp_width, self.height_value*self.disp_height
        self.position = py.Vector2(
            self.x_value*self.disp_width, self.y_value*self.disp_height)
        self.screen_image = py.Surface(
            (self.width, self.height), py.SRCALPHA).convert_alpha()

        self.rect = self.screen_image.get_rect()
        self.screen_image.fill(self.default_color)

        """ Title """
        title_image = self.font.render(
            self.title, True, (110, 110, 110)).convert_alpha()  # ini buat ganti warna judul screen
        cs_title_rect = title_image.get_rect()
        csw, csh = cs_title_rect.size
        self.cs_surface = py.Surface(
            (csw+30, csh+30), py.SRCALPHA).convert_alpha()
        py.draw.rect(self.cs_surface,
                     self.color_white, (2.5, 2.5, csw+15, csh+15), 1, border_radius=5) # ini buat ganti border judul screen
        
        self.cs_surface.blit(
            title_image, (10, 10))
        self.cs_surface = py.transform.rotozoom(
            self.cs_surface, 0, 1).convert_alpha()
        self.screen_image.blit(self.cs_surface, self.title_pos)


class MainScreen(GUI):
    """Graphical User Interface for main screen/center windows"""
    default_width_value, default_height_value = 0.7, 0.7
    default_x_value, default_y_value = 0.15, 0
    # default_color = (255, 255, 255)
    default_color = (248, 253, 255)
    cust_color = (245, 243, 231)

    def __init__(self, id, title, active=True):
        super().__init__(id, title)
        self.x_value, self.y_value = self.default_x_value, self.default_y_value
        self.width_value, self.height_value = self.default_width_value, self.default_height_value
        self.active = active
        self.title_pos = py.Vector2(self.width*0.85, 10)
        pass

    def change_mode(self, mode_num):
        if mode_num == 1:
            self.x_value, self.y_value = self.default_x_value, self.default_y_value
            self.width_value, self.height_value = self.default_width_value, self.default_height_value
            self.title_pos = py.Vector2(self.width*0.85, 10)

        elif mode_num == 2:
            self.x_value, self.y_value = 0, 0
            self.width_value, self.height_value = 0.42, self.default_height_value
            self.title_pos = py.Vector2(self.width*0.75, 10)
        elif mode_num == 3:
            self.x_value, self.y_value = 0, 0
            self.width_value, self.height_value = 0.42, self.default_height_value
            self.title_pos = py.Vector2(self.width*0.75, 10)
        else:
            self.active = False


class BottomScreen(GUI):
    """Graphical User Interface for bottom of windows"""
    default_width_value, default_height_value = 1, 0.3
    default_x_value, default_y_value = 0, 0.7
    default_color = (28, 62, 90)
    

    def __init__(self, id, title, active=True):
        super().__init__(id, title)
        self.active = active
        self.width_value, self.height_value = self.default_width_value, self.default_height_value
        self.x_value, self.y_value = self.default_x_value, self.default_y_value
        
        pass

    def change_mode(self, mode_num):
        pass


class RightSideScreen(GUI):
    """Graphical User Interface for right side of windows"""
    default_width_value, default_height_value = 0.15, 0.7
    default_x_value, default_y_value = 0.85, 0
    default_color = (183, 213, 255)

    def __init__(self, id, title, active=True):
        super().__init__(id, title)
        self.active = active
        self.width_value, self.height_value = self.default_width_value, self.default_height_value
        self.x_value, self.y_value = self.default_x_value, self.default_y_value
        self.content_width, self.content_height = 0.95*self.width, 0.75*self.height
        self.content_size = (self.content_width, self.content_height)
        self.content_position = py.Vector2(0, 0.12 * self.height)
        self.content_surface = py.Surface(
            self.content_size, py.SRCALPHA).convert_alpha()
        self.content_rect = self.content_surface.get_rect()
        self.content_scale = 1
        self.point_group_total = 1
        self.point_group_total_new = 1

        self.default_text = "No Data"
        self.text = self.default_text
        self.point_font = py.font.SysFont('timesnewroman', 18)
        self.point_text = self.point_font.render(
            self.text, True, (255, 255, 255)).convert_alpha()
        self.scroll = 0
        pass

    def change_mode(self, mode_num):
        if mode_num == 1 or mode_num == 3:
            self.active = True
        else:
            self.active = False

    def draw_content(self, text):
        """Draw content in left screen"""
        self.all_content_data = text
        """point group blit"""
        point_data = []
        for key, value in self.all_content_data.items():
            point_data.append(str(key)+" : "+str(value))
        self.content_surface.fill(self.default_color)
        for text, t in zip(point_data, range(len(point_data))):
            point_text = self.point_font.render(
                text, True, (0, 0, 0)).convert_alpha()
            self.content_surface.blit(point_text, py.Vector2(
                (5 if text[:5] == "Drone" else 15), ((t*20)+5)+max(0, min(100, self.scroll))))

        """content blit"""
        self.screen_image.blit(self.content_surface, self.content_position)


class LeftSideScreen(GUI):
    """Graphical User Interface for left side of windows"""
    default_width_value, default_height_value = 0.15, 0.7
    default_x_value, default_y_value = 0, 0
    default_color = (27, 75, 113)

    def __init__(self, id, title, active=True):
        super().__init__(id, title)
        self.active = active
        self.width_value, self.height_value = self.default_width_value, self.default_height_value
        self.x_value, self.y_value = self.default_x_value, self.default_y_value
        self.content_width, self.content_height = 0.95*self.width, 0.75*self.height
        self.content_size = (self.content_width, self.content_height)
        self.content_position = py.Vector2(0, 0.12 * self.height)
        self.content_surface = py.Surface(
            self.content_size, py.SRCALPHA).convert_alpha()
        self.content_rect = self.content_surface.get_rect()
        self.content_scale = 1
        self.point_group_total = 1
        self.point_group_total_new = 1

        self.default_text = "No Data"
        self.text = self.default_text
        self.point_font = py.font.SysFont('timesnewroman', 18)
        self.point_text = self.point_font.render(
            self.text, True, (0, 0, 0)).convert_alpha()
        self.scroll = 0

        pass

    def draw_content(self, text):
        """Draw content in left screen"""
        self.all_content_data = text
        """point group blit"""
        point_data = []
        for data in self.all_content_data:
            for key, value in data.items():
                point_data.append(str(key)+" : "+str(value))
        self.content_surface.fill(self.default_color)
        for text, t in zip(point_data, range(len(point_data))):
            point_text = self.point_font.render(
                text, True, (0, 0, 0)).convert_alpha()
            self.content_surface.blit(point_text, py.Vector2(
                (5 if text[:5] == "Drone" else 15), ((t*20)+5)+max(-200, min(100, self.scroll))))
        """content blit"""
        self.screen_image.blit(self.content_surface, self.content_position)

    def change_mode(self, mode_num):
        if mode_num == 1:
            self.active = True
        else:
            self.active = False


class PlotScreen(GUI):
    """Graphical User Interface for plotting the graph"""
    default_width_value, default_height_value = 0.6, 0.7
    default_x_value, default_y_value = 0.42, 0
    default_color = (154, 217, 219)

    def __init__(self, id, title, active=True):
        super().__init__(id, title)
        self.active = active
        self.width_value, self.height_value = self.default_width_value, self.default_height_value
        self.x_value, self.y_value = self.default_x_value, self.default_y_value
        pass

    def change_mode(self, mode_num):
        if mode_num == 2:
            self.active = True
        else:
            self.active = False


class ArucoScreen(GUI):
    """Graphical User Interface for plotting the graph"""
    default_width_value, default_height_value = 0.432, 0.7
    default_x_value, default_y_value = 0.42, 0
    default_color = (154, 217, 219)

    def __init__(self, id, title, active=True):
        super().__init__(id, title)
        self.active = active
        self.width_value, self.height_value = self.default_width_value, self.default_height_value
        self.x_value, self.y_value = self.default_x_value, self.default_y_value
        pass

    def change_mode(self, mode_num):
        if mode_num == 3:
            self.active = True
        else:
            self.active = False
