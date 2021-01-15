import sys
import pygame
from data import WIDTH, HEIGHT, GRID, LINES, COLUMNS, GSC, STATES, CONTENT, COLORS, BOARD, TETROMINOSHAPES

# HELPER FUNCTIONS

def clear(surface, color='black'):
    '''
        fill screen with a color to all screen surface
    '''
    surface.fill(COLORS[color])

def write(font, surface, position, text, color='grey', size=GRID):
    '''
        write a text at position (x,y)
    '''
    font.render_to(surface,position,text,COLORS[color],None,0,0,size)

def line(surface, pos1, pos2, color='grey'):
    '''
        draw a line between position 1 (x1,y1) and position 2 (x2,y2)
    '''
    pygame.gfxdraw.line(surface,pos1[0],pos1[1],pos2[0],pos2[1],COLORS[color])

def rectangle(surface, rect, color='grey',fill=True):
    '''
        draw a rectangle with position top left and width and height (x,y,width,height)
    '''
    if fill:
        pygame.gfxdraw.box(surface,rect,COLORS[color])
    else:
        pygame.gfxdraw.rectangle(surface,rect,COLORS[color])

def pixel(surface, position, color='grey'):
    '''
        draw a pixel at position x and y on the given surface
    '''
    pygame.gfxdraw.pixel(surface,position[0],position[1],COLORS[color])

def check_exit(game_state):
    '''
        check if the game state is exit, and return False to stop program loop
    '''
    global update_screen
    if game_state == GSC['EXIT']:
        update_screen = False
        return False
    else:
        return True

def quit():
    pygame.quit()
    sys.exit()
