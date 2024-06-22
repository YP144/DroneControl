from turtle import color
from sympy import rotations
import matplotlib.pyplot as plt
import pygame as py
import matplotlib
# matplotlib.use('module://pygame_matplotlib.backend_pygame')


class CustomPlot:
    def __init__(self):
        self.font = py.font.SysFont('timesnewroman', 20)
        self.figure, self.axes = plt.subplots()
        self.screen = py.Surface(
            (384, 350), py.SRCALPHA).convert_alpha()
        self.x, self.y = 0, 0
        self.axes.clear()
        self.axes.plot(self.x, self.y, color='green', label='test')
        # self.axes.grid()
        self.figure.canvas.draw()
        plt.autoscale()

    def update(self, data):
        self.screen.fill((255, 255, 255))
        self.x, self.y1, self.y2 = data
        self.fig = py.transform.rotozoom(self.figure, 0, 0.6).convert_alpha()
        self.fig.get_size()
        title_image = self.font.render(
            'Velocity over time', True, (0, 0, 0)).convert_alpha()

        self.screen.blit(title_image, (120, 10))
        self.screen.blit(self.fig, (0, 45))

    def run(self):
        self.axes.clear()
        self.axes.plot(self.x, self.y1, color='green', label='Vx')
        self.axes.plot(self.x, self.y2, color='red', label='Vy')
        # self.axes.set_ylabel("Position", fontweight='bold',
        #                      fontsize='10')
        # self.axes.set_xlabel("Time", fontweight='bold',
        #                      fontsize='10')
        self.figure.canvas.draw()
        # self.figure.set_dpi(80)
