import sys
import pygame
from data import WIDTH, HEIGHT, GRID, LINES, COLUMNS, GSC, STATES, CONTENT, COLORS, BOARD, TETROMINOSHAPES

# HELPER FUNCTIONS
'''
    clear : fill screen with a color to all screen surface
    write : write a text at position (x,y)
    line : draw a line between position 1 (x1,y1) and position 2 (x2,y2)
    rectangle : draw a rectangle with position top left and width and height (x,y,width,height)
'''

def clear(surface, color='black'):
    surface.fill(COLORS[color])

def write(font, surface, position, text, color='grey', size=GRID):
    font.render_to(surface,position,text,COLORS[color],None,0,0,size)

def line(surface, pos1, pos2, color='grey'):
    pygame.gfxdraw.line(surface,pos1[0],pos1[1],pos2[0],pos2[1],COLORS[color])

def rectangle(surface, rect, color='grey',fill=True):
    if fill:
        pygame.gfxdraw.box(surface,rect,COLORS[color])
    else:
        pygame.gfxdraw.rectangle(surface,rect,COLORS[color])

def pixel(surface, position, color='grey'):
    pygame.gfxdraw.pixel(surface,position[0],position[1],COLORS[color])

def exit(game_state):
    global update_screen
    if game_state == GSC['EXIT']:
        update_screen = False
        return False
    else:
        return True


def quit():
    pygame.quit()
    sys.exit()
