from random import randrange
from data import WIDTH, HEIGHT, GRID, LINES, COLUMNS, GSC, STATES, CONTENT, COLORS, BOARD, TETROMINO, TETROMINOSHAPES, STATS, ARROW

import pygame
from pygame import freetype, gfxdraw

from api import *

import objects
from debug import *

###################
#                 #
# START VARIABLES #
#                 #
###################

'''
  | GSC, give code of the first game state : TITLE
  | update_screen at True for the first drawing of screen surface
  | the others update are flags are game related and start False
  | new_game is a once only flag to init a new game
  | pause_game is a flag for the escape input and confirm box while playing
'''

game_state = GSC['TITLE']
update_screen = True
# update_arrow not necessary anymore with objects
update_arrow = False
new_game = False
pause_game = False

if DEBUG == True:
    #could come with a variable first variable = debug_game() then use it
    #avoid to call 2 time the function for no reason
    game_state = debug_game()[0]
    new_game = debug_game()[1]

##################
#                #
# INIT PROCESSES #
#                #
##################

def init_screen():
    global screen
    if DEBUG:
        flags = pygame.NOFRAME|pygame.SCALED
    else:
        flags = pygame.NOFRAME|pygame.SCALED
        #flags = pygame.FULLSCREEN|pygame.SCALED
    screen = pygame.display.set_mode((WIDTH,HEIGHT), flags)
    pygame.display.set_caption("Tetris")

def init_font():
    global font
    freetype.init()
    font = freetype.Font("prstartk.ttf")

def init_timer():
    global clock
    clock = pygame.time.Clock()

def init_game():
    '''
      | init_game is called once the program start and prepare the program with
      | init_screen create the main program window
      | init_surfaces prepare the others game surfaces
      | init_objects prepare the games objects
      | init_font prepare the global font
      | init_timer prepare the global clock used for timers
    '''
    pygame.display.init()
    init_screen()
    init_objects()
    init_surfaces()
    init_font()
    init_timer()

def init_tetrominos_objects():
    '''
      | All differents tetrominos are initianilazed in a list
      | First playing Tetromino objects are randomly defined from the Tetrominos list
    '''
    global Tetrominos, PlayingTetromino, NextTetromino
    Tetrominos = []
    size = TETROMINO['surface_size']
    for name in TETROMINOSHAPES:
        color = TETROMINOSHAPES[name]['color']
        shape = TETROMINOSHAPES[name]['shape']
        Tetrominos.append(objects.Tetromino(name,size,color,shape,(0,0),DEBUG))
    PlayingTetromino = get_a_random_tetromino()
    NextTetromino = get_a_random_tetromino((4,2))

def init_objects():
    '''
      | Prepare the objects the game will use
      | 5 Objects :
      | Arrow, Board, Stats, PlayingTetromino, NextTetromino
    '''
    global Board, Stats, Arrow
    Arrow = objects.Arrow(ARROW)
    Board = objects.Board(BOARD)
    Stats = objects.Stats(STATS)
    init_tetrominos_objects()

def init_surfaces():
    '''
      | Prepare the surfaces the game will use
      | 4 Surfaces :
      | arrow_surface, board_surface, stats_surface, tetromino_surface
      | set to arrow and tetromino surfaces the black color for transparency
    '''
    global arrow_surface, arrow_selection, board_surface,stats_surface, tetromino_surface
    arrow_surface = pygame.Surface(Arrow.surface_size)
    board_surface = pygame.Surface(Board.surface_size)
    stats_surface = pygame.Surface(Stats.surface_size)
    tetromino_surface = pygame.Surface(TETROMINO['surface_size'])
    arrow_surface.set_colorkey(COLORS['pink'])
    tetromino_surface.set_colorkey(COLORS['black'])

def get_a_random_tetromino(position=(0,0)):
    '''
      | Return a new object tetromino at given position
      | randomly chosen from the Tetrominos list
      | with a random starting rotation
    '''
    choice = randrange(0,len(Tetrominos))
    tetromino = Tetrominos[choice]
    rotation = randrange(0,tetromino.max_rotations)
    tetromino.current_rotation = rotation
    tetromino.position = position
    return tetromino

def init_new_game():
    Board.update_surface = True
    PlayingTetromino.update_surface = True
    Stats.update_surface = True

def reset_arrow():
    Arrow.update_surface = True
    Arrow.get_data(CONTENT[STATES[game_state]])

#####################
#                   #
# DRAWING FUNCTIONS #
#                   #
#####################

def game_drawing():
    '''
      | Using differents flags
      | Draw screen
      | Draw objects
      | Update display
    '''
    global update_screen
    screen_updated = False
    if update_screen == True:
        draw_screen()
        screen_updated = True
        update_screen = False
    objects_updated = draw_objects()
    if screen_updated or objects_updated:
        pygame.display.update()
        if DEBUG:
            global updated_frames
            updated_frames +=1

def reset_screen():
    '''
      | Clear screen, draw the program 1 px border
    '''
    clear(screen)
    rectangle(screen, (0,0,WIDTH,HEIGHT),'silver', False)

def draw_screen():
    '''
      | Draw the correct content according to game state
      | For PLAY game state, clear the screen for object only
      | For CONFIRM, no clearing, draw confirm box over the game
      | For others game states, clear the screen then draw the text content
    '''
    if game_state == GSC['PLAY']:
        reset_screen()
    elif game_state == GSC['CONFIRM']:
        draw_confirm_box()
    else:
        reset_screen()
        draw_text_from_content()
        draw_global_message()

def draw_objects():
    '''
      | Draw the correct surface when flag of related object is up
      | Draw game board, game stats+next tetromino, game current tetromino
      | For Arrow object, clear the surface before drawing
    '''
    updated = False
    if Board.update_surface == True:
        print("update board surface")
        Board.draw(board_surface, GRID, DEBUG)
        blit(screen, board_surface, Board.surface_position)
        updated = True
    if Stats.update_surface == True:
        print("update stats surface")
        Stats.draw(stats_surface, GRID, font, DEBUG)
        NextTetromino.draw(stats_surface, GRID, DEBUG)
        blit(screen, stats_surface, Stats.surface_position)
        updated = True
    if PlayingTetromino.update_surface == True:
        print("update tetromino surface")
        PlayingTetromino.draw(tetromino_surface, GRID, DEBUG)
        blit(screen, tetromino_surface, PlayingTetromino.surface_position)
        updated = True
    if Arrow.update_surface == True:
        print("update arrow surface")
        clear(arrow_surface)
        blit(screen,arrow_surface,Arrow.previous_position)
        Arrow.draw(arrow_surface)
        blit(screen,arrow_surface,Arrow.position)
        updated = True
    return updated

def draw_text_from_content():
    datas = CONTENT[STATES[game_state]]['text']
    for d in datas:
        position = d[0]
        text = d[1]
        color = d[2]
        write(font, screen, position, text, color)

def draw_global_message():
    '''
      | Draw a message in a rectangle at the bottom of the screen
    '''
    if game_state == GSC['MENU']:
        datas = CONTENT['GLOBAL']['menu_continue']
    elif game_state == GSC['NEW']:
        datas = CONTENT['GLOBAL']['new_continue']
    else:
        datas = CONTENT['GLOBAL']['continue']
    position = datas[0]
    text = datas[1]
    color = datas[2]
    rectangle(screen,(0,29*GRID-1,WIDTH,GRID+1),'silver')
    write(font, screen, position, text, color)

def draw_confirm_box():
    '''
      | Draw a centered box with a message
    '''
    datas = [CONTENT['CONFIRM']['confirm'], CONTENT['CONFIRM']['info'], CONTENT['CONFIRM']['continue']]
    box = CONTENT['CONFIRM']['box']
    rectangle(screen, (box[0], box[1], box[2], box[3]), 'white')
    rectangle(screen, (box[0], box[1], box[2], box[3]), 'red', False)
    for d in datas:
        position = d[0]
        text = d[1]
        color = d[2]
        write(font, screen, position, text, color)

#################
#               #
# INPUT CONTROL #
#               #
#################

def goto_menu():
    '''
      | reset settings and go to MENU game state
    '''
    global game_state, update_screen
    game_state = GSC['MENU']
    update_screen = True
    reset_arrow()

def validation_key():
    '''
      | Most game state, move to an other game state
      | but in Menu state, select the arrow choice
      | and in Play state, move tetromino directly down
      | STATES :
      | * TITLE : Title screen
      | * INTRO : Introduction screen
      | * MENU : Menu screen
      | * SCORE : Highscores screen
      | * NEW : New Game screen / Start Settings
      | * PLAY : Game Playing screen
      | * OVER : Game Over screen
      | * EXIT : Flag to Exit the Game
    '''
    global game_state, update_screen, update_arrow, pause_game, new_game
    if game_state == GSC['PLAY']:
        move_key(4)
    elif game_state == GSC['TITLE']:
        game_state = GSC['INTRO']
        update_screen = True
    elif game_state == GSC['INTRO']:
        goto_menu()
    elif game_state == GSC['SCORE']:
        goto_menu()
    elif game_state == GSC['OVER']:
        goto_menu()
    elif game_state == GSC['CONFIRM']:
        goto_menu()
    elif game_state == GSC['NEW']:
        game_state = GSC['PLAY']
        update_screen = True
        pause_game = False
        new_game = True
    elif game_state == GSC['MENU']:
        game_state = Arrow.target
        if not game_state == GSC['EXIT']:
            update_screen = True
        if game_state == GSC['NEW']:
            reset_arrow()

def escape_key():
    '''
      | Most game states return to MENU state,
      | but in PLAY state ask a confirmation before
      | in CONFIRM state which pause the game, cancel the confirm state
      | in MENU state leave the game
      | if DEBUG, leave program immediatly
    '''
    global game_state, update_screen, pause_game
    if DEBUG:
        game_state = GSC['EXIT']
    elif game_state == GSC['PLAY']:
        game_state = GSC['CONFIRM']
        update_screen = True
        pause_game = True
    elif game_state == GSC['CONFIRM']:
        game_state = GSC['PLAY']
        Stats.update_surface = True
        PlayingTetromino.update_surface = True
        Board.update_surface = True
        update_screen = True
        pause_game = False
    elif game_state == GSC['MENU']:
        game_state = GSC['EXIT']
    else:
        goto_menu()

def move_key(key):
    '''
      | At all states except PLAY, inputs used to move arrows
      | At game state PLAY, inputs used to interact with the tetromino
      | 0 : UP = ROTATE TETROMINO (cw=clockwise)
      | 1 : DOWN = GO FASTER
      | 2 : LEFT = GO LEFT
      | 3 : RIGHT = GO RIGHT
      | 4 : SPACE & RETURN = JUMP DOWN
    '''
    global update_arrow
    if game_state == GSC['MENU'] or game_state == GSC['NEW']:
        Arrow.move(key, game_state)
        reset_arrow()
    elif game_state == GSC['PLAY']:
        if key == 0:
            PlayingTetromino.rotate()
        elif key == 1:
            print("go down faster")
            #accelerate game speed ?
        elif key == 2:
            PlayingTetromino.move('left')
        elif key == 3:
            PlayingTetromino.move('right')
        elif key == 4:
            PlayingTetromino.move('jump')

def check_inputs():
    '''
      | check player possible inputs
      | * the exit window
      | * the escape input
      | * the space & return input
      | * the 4 arrows input
      | check game_state to return True or False to loop running
    '''
    global game_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = GSC['EXIT']
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                escape_key()
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                validation_key()
            if event.key == pygame.K_UP:
                move_key(0)
            if event.key == pygame.K_DOWN:
                move_key(1)
            if event.key == pygame.K_LEFT:
                move_key(2)
            if event.key == pygame.K_RIGHT:
                move_key(3)
    return check_exit(game_state)

################
#              #
# GAME UPDATES #
#              #
################

def check_play():
    '''
      | Where the game is playing data change
      | new_game flag is checked before to initialize a new game
      | Check the tetromino & board after each tetromino movement or user input
    '''
    global new_game

    if new_game == True:
        init_new_game()
        new_game = False

    #update game timer
    #tetromino moving
    #check and update board, tetromino, infos
    #update datas

#############
#           #
# GAME LOOP #
#           #
#############

def game_loop():
    '''
      | At each loop
      | 1. Check events input and change datas if game is playing
      | 2. Update timers if game is playing
      | 3. Update screen & surfaces drawing if related flag raised True
    '''
    game_running = True
    if DEBUG == True:
        global updated_frames, frames, start_ticks
        frames = 0
        updated_frames = 0
        start_ticks = pygame.time.get_ticks()
    while game_running:
        game_running = check_inputs()
        if game_state == GSC['PLAY'] and pause_game == False:
            check_play()
        game_drawing()
        if DEBUG == True:
            frames += 1
            debug_draw_grid(screen)
            debug_write_stats(font,screen,start_ticks,clock,updated_frames,frames)
            pygame.display.update()
        clock.tick(30)
    quit()

if __name__ == "__main__":
    # INIT GAME & START LOOP
    init_game()
    game_loop()
