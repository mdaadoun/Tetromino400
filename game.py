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
  | pause_game is a flag for the escape input and confirm box while playing
'''
game_state = GSC['TITLE']
update_screen = True
pause_game = False

####DEBUG CODE####
if DEBUG == True:
    global new_game
    dg = debug_game()
    game_state = dg[0]
    new_game = dg[1]

##################
#                #
# INIT PROCESSES #
#                #
##################

def init_screen():
    global screen
    #flags = pygame.NOFRAME|pygame.SCALED
    flags = pygame.FULLSCREEN|pygame.SCALED
    ###DEBUG CODE###
    if DEBUG:
        flags = pygame.NOFRAME|pygame.SCALED
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
    init_gamepad()
    init_screen()
    init_objects()
    init_surfaces()
    init_font()
    init_timer()

def init_gamepad():
    '''
      | Check and init connected gamepad
    '''
    global gamepad
    gamepad = []
    pygame.joystick.init()
    gamepad_count = pygame.joystick.get_count()
    for i in range(gamepad_count):
        gp = pygame.joystick.Joystick(i)
        gp.init()
        gamepad.append(gp)
    if (len(gamepad) == 0):
        print("No Gamepad Connected")
    else:
        for i, gp in enumerate(gamepad):
            name = gp.get_name()
            print(f"The gamepad {i+1} is named: {name}")
        print(f"Only the first gamepad is used.")

def init_objects():
    '''
      | Prepare the objects the game will use
      | 4 Objects :
      | Arrow, Board, Stats, Tetromino
    '''
    global Board, Stats, Arrow
    Arrow = objects.Arrow(ARROW)
    Board = objects.Board(BOARD)
    Stats = objects.Stats(STATS)
    init_tetrominos_objects()
    get_a_random_tetromino()

def init_tetrominos_objects():
    '''
      | All differents tetrominos are initianilazed in a list
      | First playing Tetromino objects are randomly defined from the Tetrominos list
    '''
    global Tetrominos
    Tetrominos = []
    size = TETROMINO['surface_size']
    position = TETROMINO['surface_position']
    for name in TETROMINOSHAPES:
        color = TETROMINOSHAPES[name]['color']
        shape = TETROMINOSHAPES[name]['shape']
        Tetrominos.append(objects.Tetromino(name,size,color,shape,position,DEBUG))
    #NextTetromino = get_a_random_tetromino((4,2))
    #Need an other way to get next tetromino as a fixed shape in stats without object

def init_surfaces():
    '''
      | Prepare the surfaces the game will use
      | 4 Surfaces :
      | arrow_surface, board_surface, stats_surface, tetromino_surface
      | set to arrow and tetromino surfaces the pink color for transparency
    '''
    global arrow_surface, arrow_selection, board_surface,stats_surface, tetromino_surface
    arrow_surface = pygame.Surface(Arrow.surface_size)
    board_surface = pygame.Surface(Board.surface_size)
    stats_surface = pygame.Surface(Stats.surface_size)
    tetromino_surface = pygame.Surface(TETROMINO['surface_size'])
    arrow_surface.set_colorkey(COLORS['pink'])
    tetromino_surface.set_colorkey(COLORS['pink'])

def get_a_random_tetromino():
    '''
      | Return a new object tetromino at given position
      | randomly chosen from the Tetrominos list
      | with a random starting rotation
    '''
    global Tetromino
    choice = randrange(0,len(Tetrominos))
    Tetromino = Tetrominos[choice]
    rotation = randrange(0,Tetromino.max_rotations)
    Tetromino.next_rotation = Tetromino.rotation = rotation
    Tetromino.next_position = Tetromino.position = TETROMINO['surface_position']

def init_new_game():
    get_a_random_tetromino()
    Board.update_surface = True
    Tetromino.update_surface = True
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
        ####DEBUG CODE####
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
        print("update stats and next tetro surface")
        Stats.draw(stats_surface, GRID, font, DEBUG)
        #NextTetromino.draw(stats_surface, GRID, DEBUG)
        blit(screen, stats_surface, Stats.surface_position)
        updated = True
    if Tetromino.update_surface == True:
        Stats.update_score(Tetromino.check_update(Board))
        Tetromino.draw(tetromino_surface, GRID, DEBUG, True)
        blit(screen, tetromino_surface, Tetromino.position)
        Tetromino.set_update()
        Tetromino.draw(tetromino_surface, GRID, DEBUG)
        blit(screen, tetromino_surface, Tetromino.position)
        updated = True
    if Arrow.update_surface == True:
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
    write(font,screen,position,text,color)

def draw_confirm_box():
    '''
      | Draw a centered box with a message
    '''
    datas = [CONTENT['CONFIRM']['confirm'], CONTENT['CONFIRM']['info'], CONTENT['CONFIRM']['continue']]
    box = CONTENT['CONFIRM']['box']
    rectangle(screen,(box[0],box[1],box[2],box[3]),'white')
    rectangle(screen,(box[0],box[1],box[2],box[3]),'red',False)
    for d in datas:
        position = d[0]
        text = d[1]
        color = d[2]
        write(font,screen,position,text,color)

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
    global game_state, update_screen, pause_game
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
        init_new_game()
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
        Tetromino.update_surface = True
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
      | The Stats score is updated if a Tetromino return completed lines
    '''
    if game_state == GSC['MENU'] or game_state == GSC['NEW']:
        Arrow.move(key, game_state)
        reset_arrow()
    elif game_state == GSC['PLAY']:
        if key == 0:
            Tetromino.rotate()
        else:
            Tetromino.move(key)

def check_inputs():
    '''
      | check player possible inputs
      | * the exit window
      | * the escape input
      | * the space & return input
      | * the 4 arrows input
      | * the gamepad inputs
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
        if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYAXISMOTION:
            get_gamepad_input()
    return check_exit(game_state)

def get_gamepad_input():
    '''
      | Check the used input of the gamepad
    '''
    gp = gamepad[0]
    ax_up_dn = gp.get_axis(1)
    ax_lf_rg = gp.get_axis(0)
    btnA = gp.get_button(0)
    btnB = gp.get_button(1)
    if ax_up_dn < 0:
        move_key(0)
    elif ax_up_dn > 0:
        move_key(1)
    elif ax_lf_rg > 0:
        move_key(3)
    elif ax_lf_rg < 0:
        move_key(2)
    if btnB == True:
        validation_key()
    if btnA == True:
        escape_key()

#############
#           #
# GAME LOOP #
#           #
#############

def game_loop():
    '''
      | At each loop
      | 1. Check events input and change datas if game is playing
      | 2. Update timers if game is playing to keep tetromino moving and stats up
      | 3. Update screen & surfaces drawing if related flag raised True
      | 4. Keep the FPS at 30 with clock
    '''
    start_ticks = pygame.time.get_ticks()
    game_running = True
    ###DEBUG CODE###
    if DEBUG == True:
        global updated_frames, frames
        updated_frames = 0
        frames = 0
    while game_running:
        game_running = check_inputs()
        if game_state == GSC['PLAY'] and pause_game == False:
            game_ticks = pygame.time.get_ticks()
            Tetromino.slide(game_ticks)
            Stats.update_time(game_ticks - start_ticks)
        game_drawing()
        clock.tick(30)
        ####DEBUG CODE####
        if DEBUG == True:
            global new_game
            if new_game == True:
                init_new_game()
                new_game = False
            frames += 1
            debug_draw_grid(screen)
            debug_write_stats(font,screen,start_ticks,clock,updated_frames,frames)
            pygame.display.update()
    quit()

if __name__ == "__main__":
    # INIT GAME & START LOOP
    init_game()
    game_loop()
