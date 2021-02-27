import sys
import csv
import pygame
from data import GRID, GSC, COLORS, SAVES

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

def write(font, surface, position, text, color='iron', size=GRID):
    '''
        write a text at position (x,y)
    '''
    font.render_to(surface,position,text,COLORS[color],None,0,0,size)

def line(surface, pos1, pos2, color='iron'):
    '''
        draw a line between position 1 (x1,y1) and position 2 (x2,y2)
    '''
    pygame.gfxdraw.line(surface,pos1[0],pos1[1],pos2[0],pos2[1],COLORS[color])

def rectangle(surface, rect, color='iron',fill=True):
    '''
        draw a rectangle with position top left and width and height
        (x,y,width,height)
    '''
    if fill:
        pygame.gfxdraw.box(surface,rect,COLORS[color])
    else:
        pygame.gfxdraw.rectangle(surface,rect,COLORS[color])

def pixel(surface, position, color='iron'):
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

#######
# CSV #
#######

def read_csv(file_name):
    rows = []
    titles = ()
    with open(file_name) as save_file:
        save_reader = csv.reader(save_file, delimiter=',')
        line_count = 0
        for row in save_reader:
            if line_count == 0:
                titles = tuple(row)
            else:
                rows.append(tuple(row))
            line_count += 1
    return (titles, rows)

def erase_file(file_name):
    open(file_name, 'w').close()

def set_file(file_name, headers):
    """
    | Check if file exist, if not recreate the csv file with the headers header
    """
    data = [None]
    try:
        data = read_csv(file_name)
    except FileNotFoundError:
        open(file_name,'w')
    if headers != data[0]:
        print('The save file got a problem, rebuilding.')
        erase_file(file_name)
        newdata = SAVES['file_start']
        newdata.insert(0,headers)
        write_csv(file_name,newdata)

def write_csv(file_name, data):
    with open(file_name, mode='a') as save_file:
        save_writer = csv.writer(save_file, delimiter=',')
        if len(data) == 1:
            save_writer.writerow(data[0])
        else:
            save_writer.writerows(data)

#def get_dict_from_csv(file_name):
#    csv_dict = []
#    with open(file_name, mode='r') as save_file:
#        csv_dict = csv.DictReader(save_file)
#        for row in csv_dict:
#            print(row)
#    return csv_dict

#def send_dict_to_csv(file_name, data_dict):
#    print(file_name, data_dict)
#    print("Score is saved in the file", file_name, ".")

###########
#         # 
# STRINGS #
#         # 
###########

def set_time_string(time):
    """
    | Format the given secondes
    """
    time_text = ['00','00','00']
    secondes = time
    time_text[2] = str(secondes%60)
    minutes = secondes//60
    time_text[1] = str(minutes%60)
    time_text[0] = str(minutes//60)
    for i,txt in enumerate(time_text):
        if len(txt) == 1:
            time_text[i] = '0'+txt
    time_text = ':'.join(time_text)
    return time_text
