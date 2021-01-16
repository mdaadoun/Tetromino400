from random import randrange
from data import WIDTH, HEIGHT, GRID, LINES, COLUMNS, GSC, STATES, CONTENT, COLORS, BOARD, TETROMINO, TETROMINOSHAPES, STATS

import pygame
from pygame import freetype, gfxdraw

from api import *

import objects
from debug import *


# START VARIABLES
'''
  | GSC, give code of the first game state : TITLE
  | update_screen at True for the first drawing of screen surface
  | the others update are flags are game related and start False
  | new_game is a once only flag to init a new game
  | pause_game is a flag for the escape input and confirm box while playing
'''
game_state = GSC['TITLE']
update_screen = True
# update_arrow and update_play not necessary anymore with objects
update_arrow = False
update_play = False
new_game = False
pause_game = False

if DEBUG == True:
    #could come with a variable first variable = debug_game() then use it
    #avoid to call 2 time the function for no reason
    game_state = debug_game()[0]
    new_game = debug_game()[1]

# INIT PROCESS
'''
  | init_game is called once the program start and prepare the program with
  | init_screen create the main program window
  | init_font prepare the global font
  | init_timer prepare the global clock used for timers
'''
def init_screen():
    global screen
    if DEBUG:
        flags = pygame.NOFRAME|pygame.SCALED
    else:
        flags = pygame.FULLSCREEN|pygame.SCALED
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
    pygame.display.init()
    init_screen()
    init_surfaces()
    init_objects()
    init_font()
    init_timer()

def init_arrow_surface():
    #review this function, selection should come with Arrow object init
    '''
      | arrow array
      | 0. surface
      | 1. arrow selection start as 0
    '''
    global arrow_surface, arrow_selection
    arrow_surface = pygame.Surface((8,8))
    arrow_selection = 0

def init_board_surface():
    global board_surface
    board_surface = pygame.Surface(BOARD['surface_size'])

def init_statistics_surface():
    global stats_surface
    stats_surface = pygame.Surface(STATS['surface_size'])

def init_tetromino_surface():
    global tetromino_surface
    tetromino_surface = pygame.Surface(TETROMINO['surface_size'])

def init_tetrominos_objects():
    '''
      | All differents tetrominos are initianilazed in a list
      | First playing Tetromino objects are randomly defined from the Tetrominos list
    '''
    global Tetrominos, PlayingTetromino, NextTetromino
    Tetrominos = []
    for shape in TETROMINOSHAPES:
        Tetrominos.append(objects.Tetromino(shape,TETROMINOSHAPES[shape],(0,0),DEBUG))
    PlayingTetromino = get_a_random_tetromino()
    NextTetromino = get_a_random_tetromino((4,2))

def init_objects():
    '''
      | Prepare the objects the game will use
      | 5 Objects :
      | Arrow, Board, Stats, PlayingTetromino, NextTetromino
    '''
    global Board, Stats
    #Arrow init here
    Board = objects.Board(BOARD)
    Stats = objects.Stats(STATS)
    init_tetrominos_objects()

def init_surfaces():
    '''
      | Prepare the surfaces the game will use
      | 4 Surfaces :
      | arrow_surface, board_surface, stats_surface, tetromino_surface
    '''
    #init_arrow_surface()
    init_board_surface()
    init_statistics_surface()
    init_tetromino_surface()

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

# DRAWING FUNCTIONS

def game_drawing():
    global update_screen, update_arrow, update_play
    updated = False

    if update_screen == True:
        draw_screen()
        updated = True
        update_screen = False

    draw_objects()

    # should be removed, arrow drawing move to draw_screen
    if update_arrow == True:
        draw_arrow()
        updated = True
        update_arrow = False

    # still useful with draw_objects() ?
    if update_play == True:
        updated = True
        update_play = False

    if updated:
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
    '''
    if game_state == GSC['PLAY']:
        pass
    elif game_state == GSC['CONFIRM']:
        draw_confirm_box()
    else:
        reset_screen()
        draw_text_from_content()
        draw_global_message()
        #Draw arrow object here
        #if Arrow.update_surface == True:
        #    Arrow.draw(screen)

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

def draw_arrow():
    #to remove when Arrow.draw() is set
    '''
      | first check if arrow surface is defined, if not, init arrow
      | then load the correct shape and selection
    '''
    try:
        arrow_surface
    except NameError:
        init_arrow_surface()

    shape = CONTENT[STATES[game_state]]['arrowshape']
    color = get_arrow_selection()['color']

    clear(arrow_surface)
    x = 0
    y = 0
    for i in shape:
        for j in i:
            if j == 1:
                pixel(arrow_surface, (x,y), color)
            x += 1
        y += 1
        x = 0

    display_arrow_surface()

def draw_objects():
    '''
      | Draw the playing game surface when flag update for each is up
      | Draw game board, game stats+next tetromino, game current tetromino
    '''
    if Board.update_surface == True:
        print("update board surface")
        position = BOARD['surface_position']
        #the position should be an object internal variable
        Board.draw(board_surface, GRID, DEBUG)
        #screen blit could be added to API ?
        screen.blit(board_surface, position)
        #Could be internal to object ?
        #Board.update_surface = False

    if Stats.update_surface == True:
        print("update stats surface")
        position = STATS['surface_position']
        #the position should be an object internal variable
        Stats.draw(stats_surface, GRID, font, DEBUG)
        NextTetromino.draw(stats_surface, GRID, DEBUG)
        #screen blit could be added to API ?
        screen.blit(stats_surface, position)
        #Could be internal to object ?
        #Stats.update_surface = False

    if PlayingTetromino.update_surface == True:
        print("update tetromino surface")
        #the position should be an object internal variable
        position = TETROMINO['surface_position']
        PlayingTetromino.draw(tetromino_surface, GRID, DEBUG)
        #screen blit could be added to API ?
        screen.blit(tetromino_surface, position)
        #Could be internal to object ?
        #PlayingTetromino.update_surface = False

    #if Arrow.update_surface == True:
        #print("update arrow surface")
        #Arrow.draw()
        #screen.blit(arrow_surface, Arrow.position)

    print('draw objects done')

# ARROW FUNCTIONS

def clear_arrow():
    #to remove when object ready
    clear(arrow_surface)
    display_arrow_surface()

def display_arrow_surface():
    #to remove when Arrow.update_surface and Arrow.draw set
    position = get_arrow_selection()['position']
    screen.blit(arrow_surface, position)

def get_arrow_selection():
    #to remove when Arrow init set
    '''
      | get the content and return a dictionnary with position, color and target of the arrow
    '''
    selection = arrow_selection
    content = CONTENT[STATES[game_state]]['arrowselect'][selection]
    data = {
        'position': content[0],
        'color': content[1],
        'target': content[2]
    }
    return data

def update_arrow_selection(direction):
    #to remove when object move and variable Arrow.selection set
    global arrow_selection
    index_max = len(CONTENT[STATES[game_state]]['arrowselect']) - 1
    arrow_selection += direction
    if arrow_selection < 0:
        arrow_selection = index_max
    elif arrow_selection > index_max:
        arrow_selection = 0

def move_arrow(key):
    #to remove when function Arrow.move() set
    '''
      | change position of the key
      | At game state Menu, arrows used to select an other game state
      | At game state New Game, arrows used to change settings  (name, speed)
      | keys :
      | 0 : UP
      | 1 : DOWN
      | 2 : LEFT
      | 3 : RIGHT
    '''
    print(key)
    if game_state == GSC['MENU']:
        if key == 0:
            update_arrow_selection(-1)
        elif key == 1:
            update_arrow_selection(1)
    elif game_state == GSC['NEW']:
        if key == 0:
            #change setting function
            print("change setting")
        elif key == 1:
            #change setting function
            print("change setting")
        elif key == 2:
            update_arrow_selection(-1)
        elif key == 3:
            update_arrow_selection(1)

def goto_menu():
    '''
      | reset stats
    '''
    global game_state, update_screen, update_arrow
    game_state = GSC['MENU']
    update_screen = True
    #Arrow.update_surface = True
    update_arrow = True


# INPUTS

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
        #game_state = Arrow.get_selection()
        game_state = get_arrow_selection()['target']
        if not game_state == GSC['EXIT']:
            update_screen = True
        if game_state == GSC['NEW']:
            #Arrow.update_surface = True
            update_arrow = True

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
        # Arrow.clear()
        # Arrow.move(key)
        # Arrow.update_surface = True
        clear_arrow()
        move_arrow(key)
        update_arrow = True
    elif game_state == GSC['PLAY']:
        if key == 0:
            PlayingTetromino.rotate('cw')
        elif key == 1:
            print("go down faster")
            #accelerate game speed ?
        elif key == 2:
            PlayingTetromino.move('left')
        elif key == 3:
            PlayingTetromino.move('right')
        elif key == 4:
            PlayingTetromino.move('jump')
        PlayingTetromino.update_surface = True

# CHECK EVENTS

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


# CHECK UPDATES

def check_play():
    '''
      | Where the game is playing data change
      | new_game flag is checked before to initialize a new game
      | update_play is a flag telling to draw the game
      | Check the tetromino & board after each tetromino movement or user input
    '''
    global new_game, update_play

    # remove update_play flag, draw_objects() is enough
    if new_game == True:
        #a function to reinitialize to zero the objects ? 
        print('A new game :', new_game)
        new_game = False
        update_play = True

    # clean here, define in variable each then should be "if B or S or P == True:"
    # probably not necessary in fact with draw_objects()
    if Board.update_surface == True or Stats.update_surface == True or PlayingTetromino.update_surface == True:
        update_play = True
    #tetromino moving
    #check and update board, tetromino, infos
    #update datas


# MAIN GAME LOOP

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
    # INIT & START LOOP
    init_game()
    game_loop()
