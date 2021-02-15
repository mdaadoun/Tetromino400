import sys
import csv
import pygame
from data import GRID, GSC, COLORS

# HELPER FUNCTIONS

def clear(surface, color='black'):
    '''
        fill screen with a color to all screen surface
    '''
    surface.fill(COLORS[color])


def blit(surface1, surface2, position):
    '''
       draw surface2 on surface1 at position
    '''
    surface1.blit(surface2, position)

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

def read_csv(file_name):
    print(file_name)
    with open(file_name) as save_file:
        save_reader = csv.reader(save_file, delimiter=',')
        line_count = 0
        for row in save_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
            else:
                print(row)
                print(f'\t{row[0]} as a score of {row[1]}')
            line_count += 1
    print(f'Processed {line_count} lines.')

def write_csv(file_name, data):
    print(file_name, data)
    with open(file_name, mode='a') as save_file:
        save_writer = csv.writer(save_file, delimiter=',')
        save_writer.writerow([data,data,data,data,data])
    print(f'The score {data} as been saved.')

def get_dict_from_csv():
    pass

def send_dict_to_csv():
    pass
