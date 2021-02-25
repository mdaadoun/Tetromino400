from math import ceil
from api import *
from data import WIDTH, HEIGHT, GRID, LINES, COLUMNS, GSC, STATES, CONTENT, COLORS, BOARD, TETROMINOSHAPES

# DEBUG HELPER
"""
| debug_draw_grid : display a 8x8 grid on all the screen surface
"""
DEBUG = False
START_STATE = "SCORE"
DEBUG_GRID = False
DEBUG_STATS = False

def debug_draw_grid(screen):
    """
    | Draw a 8x8 red grid over all the screen
    """
    if DEBUG_GRID:
        for i in range(0, WIDTH, GRID):
            line(screen, (i,0), (i,HEIGHT), 'red')
            if i < HEIGHT:
                line(screen, (0,i), (WIDTH,i), 'red')

def debug_write_stats(font,screen,start_ticks,clock,updated_frames,frames):
    """
    | Write game states like frames per seconds, time since program launched, etc...
    """
    if DEBUG_STATS:
        time = pygame.time.get_ticks()
        timer = time - start_ticks
        fps = clock.get_fps()
        ticks = clock.get_time()
        rectangle(screen,(0,0,WIDTH,100), 'white')
        write(font,screen, (0,0), 'updated frames: '+str(updated_frames))
        write(font,screen, (0,GRID), 'frames: '+str(frames))
        write(font,screen, (0,2*GRID), 'mlsc since last frame: ' + str(ticks))
        write(font,screen, (0,3*GRID), 'mlsc since program start: ' + str(time))
        write(font,screen, (0,4*GRID), 'secondes since program start: ' + str(ceil(time/1000)))
        write(font,screen, (0,5*GRID), 'mlsc since loop start (' + str(start_ticks) + '): ' + str(timer))
        write(font,screen, (0,6*GRID), 'secondes since loop start (' + str(start_ticks) + '): ' + str(ceil(timer/1000)))
        write(font,screen, (0,7*GRID), 'fps:' + str(fps))

def debug_game():
    """
    | Return game state
    """
    return GSC[START_STATE]
