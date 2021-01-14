import sys
import pygame
from pygame.locals import *
import data

colors = data.colorslist

pygame.init()

fps = 30
fpsClock = pygame.time.Clock()

width,height = 640,480
screen = pygame.display.set_mode((width,height), pygame.SCALED)

line_width = width/24 

while True:
    x=0
    for color in colors:
        pygame.draw.rect(screen, colors[color],(x,0,x+line_width,height)) 
        x += line_width 

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    fpsClock.tick(fps)


