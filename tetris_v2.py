import sys
import pygame
from pygame import freetype, gfxdraw
import data

# DEBUG HELPER
'''
debug_draw_grid : display a 8x8 grid on all the screen surface
'''
DEBUG = False

def debug_draw_grid():
    for i in range(0, WIDTH, GRID):
        line(screen, (i,0), (i,HEIGHT))
        if i < HEIGHT:
            line(screen, (0,i), (WIDTH,i))

# GLOBAL DATA

WIDTH = data.screensizes['width']
HEIGHT = data.screensizes['height']
GRID = data.screensizes['grid']
LINES = data.screensizes['lines']
COLUMNS = data.screensizes['columns']
GSC = data.gamestatescodes # GSC = Game State Code
STATES = data.gamestates
CONTENT = data.statecontent
COLORS = data.colorslist
TETROMINOS = data.tetrominoshapes

# HELPER FUNCTIONS
'''
clear : fill screen with a color to all screen surface
write : write a text at position (x,y)
line : draw a line between position 1 (x1,y1) and position 2 (x2,y2)
'''

def clear(surface, color='black'):
    surface.fill(COLORS[color])

def write(surface, position, text, color='grey', size=GRID):
    font.render_to(surface,position,text,COLORS[color],None,0,0,size)

def line(surface, pos1, pos2, color='grey'):
    pygame.gfxdraw.line(surface,pos1[0],pos1[1],pos2[0],pos2[1],COLORS[color])

def pixel(surface, position, color='grey'):
    pygame.gfxdraw.pixel(surface,position[0],position[1],COLORS[color])

# START VARIABLES
'''
The starting variable with GSC, give code of the first game state : TITLE
updated_screen at True for the first drawing of screen surface
the others update are related to next game states and other surfaces, start false
the arrow position, 0 = first position
'''
game_state = GSC['TITLE']
updated_screen = True
updated_arrow = False
updated_tetromino = False
updated_next_tetromino = False
updated_gameboard = False
updated_gameinfos = False

# INIT PROCESS

def init_screen():
    global screen
    screen = pygame.display.set_mode((WIDTH,HEIGHT), flags=pygame.NOFRAME|pygame.SCALED)
    title = "Tetris v2"
    pygame.display.set_caption(title)

def init_font():
    global font 
    freetype.init()
    font = freetype.Font("prstartk.ttf")

def init_timer():
    global clock
    clock = pygame.time.Clock()

def init_game():
    pygame.display.init()
    init_screen()
    init_font()
    init_timer()

def init_arrow_surface():
    '''
        arrow array
        0. surface
        1. selection start as 0
    '''
    global arrow
    arrow = [pygame.Surface((8,8)), 0]

# DRAWING FUNCTIONS

def game_drawing():
    updated = False

    if updated_screen == True:
        draw_screen()
        updated = True

    if updated_arrow == True:
        draw_arrow()
        updated = True

    if updated:
        pygame.display.update()

def draw_screen():
    '''
    Clear screen, then if Debug, draw a grid.
    Draw the correct content according to game state
    '''
    global updated_screen

    clear(screen)
    
    if DEBUG == True:
        debug_draw_grid()

    draw_text_from_content(screen)

    pygame.display.update()
    updated_screen = False


def draw_text_from_content(surface):
    datas = CONTENT[STATES[game_state]]['text']
    for d in datas:
        position = d[0]
        text = d[1]
        color = d[2]
        write(surface, position, text, color)

def draw_arrow():
    '''
    first check if arrow is defined, if not, init arrow
    then load the correct shape and selection
    '''
    global updated_arrow

    try:
        arrow
    except NameError:
        init_arrow_surface()

    surface = arrow[0]
    shape = get_arrow_shape()
    color = get_arrow_selection()['color']

    clear(surface)
    x = 0
    y = 0
    for i in shape:
        for j in i:
            if j == 1:
                pixel(surface, (x,y), color)
            x += 1
        y += 1
        x = 0

    display_arrow()
    updated_arrow = False
    print('arrow draw')

def draw_game_board():
    global updated_board
    updated_board = False

def draw_current_tetromino():
    global updated_tetromino
    updated_tetromino = False

def draw_next_tetromino():
    global updated_next_tetromino
    updated_next_tetromino = False

def draw_informations():
    global updated_game_informations
    updated_game_informations = False

# ARROW FUNCTIONS

def display_arrow():
    surface = arrow[0]
    position = get_arrow_selection()['position']
    screen.blit(surface, position)

def clear_arrow():
    surface = arrow[0]
    clear(surface)
    display_arrow()

def get_arrow_shape():
    return CONTENT[STATES[game_state]]['arrowshape']

def get_arrow_selection():
    '''
        get the content and return a dictionnary with position, color and target of the arrow
    '''
    selection = arrow[1]
    content = CONTENT[STATES[game_state]]['arrowselect'][selection]
    data = {
        'position': content[0],
        'color': content[1],
        'target': content [2]
    }
    return data

def update_arrow_selection(direction):
    global arrow
    index_max = len(CONTENT[STATES[game_state]]['arrowselect']) - 1
    arrow[1] += direction
    if arrow[1] < 0:
        arrow[1] = index_max
    elif arrow[1] > index_max:
        arrow[1] = 0

def update_arrow(key):
    '''
        change position of the key
        At game state Menu, arrows used to select an other game state
        At game state New Game, arrows used to change settings  (name, speed)
        keys :
        0 : UP
        1 : DOWN
        2 : LEFT
        3 : RIGHT
    '''
    if game_state == GSC['MENU']:
        if key == 0:
           update_arrow_selection(-1) 
        elif key == 1:
           update_arrow_selection(1)
    elif game_state == GSC['NEW']:
        if key == 0:
           #change setting function
           pass
        elif key == 1:
           #change setting function
           pass
        elif key == 2:
           update_arrow_selection(1) 
        elif key == 3:
           update_arrow_selection(-1)

# INPUTS

def validation_key():
    '''
    Most game state, move to an other game state
    but in Menu state, select the arrow choice
    and in Play state, move tetromino directly down
    STATES :
    0 : TITLE : Title screen
    1 : INTRO : Introduction screen
    2 : MENU : Menu screen
    3 : SCORE : Highscores screen
    4 : NEW : New Game screen / Start Settings
    5 : PLAY : Game Playing screen
    6 : OVER : Game Over screen
    7 : EXIT : Flag to Exit the Game
    '''
    global game_state, updated_screen, updated_arrow
    if game_state == GSC['TITLE']:
        game_state = GSC['INTRO']
        updated_screen = True
    elif game_state == GSC['INTRO']:
        game_state = GSC['MENU']
        updated_screen = True
        updated_arrow = True
    elif game_state == GSC['MENU']:
        # depend the arrow selection
        pass

def escape_key():
    global game_state, updated_screen, updated_arrow
    '''
    Most game states return to menu, 
    but Playing state return to menu after confirmation
    and Menu leave the game, return false for loop
    '''
    if game_state == GSC['PLAY']:
        # If state is PLAYING, verify if user really want to quit, if yes, return to menu
        return True
    elif game_state == GSC['MENU']:
        return False
    else:
        game_state = GSC['MENU']
        updated_screen = True
        updated_arrow = True
        return True

def move_key(key):
    global updated_arrow, updated_tetromino
    '''
        At all states except Playing, inputs used to move arrow
        At game state Playing, inputs used to move tetromino
    '''
    if game_state == GSC['MENU'] or game_state == GSC['NEW']:
        clear_arrow()
        update_arrow(key)
        updated_arrow = True
    elif game_state == GSC['PLAY']:
        move_tetromino(key)
        updated_tetromino = True

# TETROMINO FUNCTIONS

def move_tetromino(key):
    pass

# CHECK EVENTS

def check_inputs():
    '''
    check player possible inputs
    * the exit window
    * the escape input
    * the space input
    * the 4 arrows input
    if no exit input, return True to keep game running
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return escape_key()
            if event.key == pygame.K_SPACE:
                validation_key()
            if event.key == pygame.K_UP:
                move_key(0)
            if event.key == pygame.K_DOWN:
                move_key(1)
            if event.key == pygame.K_LEFT:
                move_key(2)
            if event.key == pygame.K_RIGHT:
                move_key(3)
    return True

# CHECK UPDATES


# MAIN GAME LOOP

def game_loop():
    '''
    At each loop
    * Check events input
    * Move the arrow for animation
    * Move the tetromino and update time if game state is Playing
    * Check the tetromino & board after each tetromino movement or user input
    * Update screen display if asked
    * Update surfaces display (arrows, tetromino, informations) if asked
    '''
    game_running = True
    while game_running:
        game_running = check_inputs()

        if game_state == GSC['PLAY']:
            pass
            #draw board, tetromino, infos
            #tetromino moving
            #play_game()
            #check board
            #update datas

        game_drawing()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # INIT & START LOOP
    init_game()
    game_loop()