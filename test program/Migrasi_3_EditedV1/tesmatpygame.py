from random import *
import pygame.display
import pygame
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('module://pygame_matplotlib.backend_pygame')
xtes = []
ytes = []
for x in range(5):
    xtes.append(randint(0, 50))
    ytes.append(randint(0, 500))
screen = pygame.display.set_mode((800, 600))
fig, axes = plt.subplots(1, 1,)
# Use the fig as a pygame.Surface


def plotting():
    axes.plot(xtes, ytes, color='green', label='test')
    fig.canvas.draw()
    screen.blit(fig, (0, 0))


show = True
while show:
    xtes.append(randint(0, 50))
    ytes.append(randint(0, 500))
    plotting()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Stop showing when quit
            show = False
    pygame.display.update()
