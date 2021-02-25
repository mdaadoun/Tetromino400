# game.py
import os
from random import randrange
from data import WIDTH, HEIGHT, GRID, LINES, COLUMNS, GSC, STATES, \
    CONTENT, COLORS, BOARD, TETROMINO, TETROMINOSHAPES, STATS, \
    ARROW, NAME, SAVES

import pygame
from pygame import freetype, gfxdraw

from api import *
import objects
from debug import *

##################
#                #
# INIT PROCESSES #
#                #
##################

def init_game():
    """
    | init_game is called once the program start and prepare the program with
    | Check and init_gamepad as an extra input device if available
    | init_screen create the main program window
    | init_objects prepare the games objects
    | init_surfaces prepare the others game surfaces
    | init_font prepare the global font
    | init_timer prepare the global clock used for timers
    | set update_screen flag at True for the first drawing of screen surface
    | set game_state flag with GSC to give code of the first game state : TITLE
    | start the game loop
    """
    global update_screen, game_state
    pygame.display.init()
    init_gamepad()
    init_screen()
    init_objects()
    init_surfaces()
    init_font()
    init_timer()
    update_screen = True
    game_state = GSC['TITLE']
    ####START DEBUG CODE####
    if DEBUG == True:
        dg = debug_game()
        game_state = dg
        init_new_game()
    #####END DEBUG CODE#####
    game_loop()

def init_screen():
    global screen
    #flags = pygame.FULLSCREEN|pygame.SCALED
    flags = pygame.NOFRAME|pygame.SCALED
    ####START DEBUG CODE####
    if DEBUG:
        flags = pygame.SCALED
    #####END DEBUG CODE#####
    #if not DEBUG:
    screen = pygame.display.set_mode((WIDTH,HEIGHT), flags)
    pygame.display.set_caption(NAME)

def init_font():
    """
    | Init the freetype pygame module
    | Retrieve the real path of the current script from __file__
    | Load the font at the same path
    """
    global font
    freetype.init()
    path = os.path.dirname(os.path.realpath(__file__))
    font = freetype.Font(f"{path}/prstartk.ttf")

def init_timer():
    global clock
    clock = pygame.time.Clock()

def init_gamepad():
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
        print("Only the first gamepad is used.")

def init_objects():
    """
    | Prepare the objects the game will use
    | 3 Objects and a list of 7 Tetromino objects :
    | Arrow, Board, Stats : main game objects
    | tetrominos : list of Tetrominos objects
    |     The Tetromino Class Variable refers alternatively
    |     to one of the object of the tetrominos list
    |     First playing Tetromino is randomly chosen from this list
    """
    global Board, Stats, Arrow
    Arrow = objects.Arrow(ARROW)
    Board = objects.Board(BOARD)
    Stats = objects.Stats(STATS)
    init_tetrominos_objects()

def init_tetrominos_objects():
    """
    | All differents tetrominos are initialized in the list
    """
    global tetrominos
    tetrominos = []
    size = TETROMINO['surface_size']
    position = TETROMINO['surface_position']
    for name in TETROMINOSHAPES:
        color = TETROMINOSHAPES[name]['color']
        shape = TETROMINOSHAPES[name]['shape']
        tetrominos.append(
            objects.Tetromino(name,size,color,shape,position,DEBUG)
        )

def init_surfaces():
    """
    | Prepare the surfaces the game will use
    | 4 Surfaces :
    | arrow_surface, board_surface, stats_surface, tetromino_surface
    | set to arrow and tetromino surfaces the pink color for transparency
    """
    global arrow_surface,board_surface,stats_surface,tetromino_surface
    arrow_surface = pygame.Surface(Arrow.surface_size)
    board_surface = pygame.Surface(Board.surface_size)
    stats_surface = pygame.Surface(Stats.surface_size)
    tetromino_surface = pygame.Surface(TETROMINO['surface_size'])
    arrow_surface.set_colorkey(COLORS['pink'])
    tetromino_surface.set_colorkey(COLORS['pink'])

def get_next_random_tetromino():
    """
    | Return a new object tetromino at given position
    | randomly chosen from the tetrominos list
    | with a random starting rotation
    | set Tetromino.done flag as False, to start updating
    """
    global Tetromino
    choice = randrange(0,len(tetrominos))
    try:
        Tetromino.done = False
        Tetromino = tetrominos[Tetromino.Next]
        Tetromino.Next = choice
    except NameError:
        Tetromino = tetrominos[choice]
        next_choice = randrange(0,len(tetrominos))
        Tetromino.Next = next_choice
    Stats.next_shape = tetrominos[Tetromino.Next].shape
    Stats.next_color = tetrominos[Tetromino.Next].color
    Stats.update_surface = True
    rotation = randrange(0,Tetromino.max_rotations)
    Tetromino.next_rotation = Tetromino.rotation = rotation
    Tetromino.next_position = Tetromino.position = TETROMINO['surface_position']
    Tetromino.speed_level = Stats.level

def init_new_game():
    """
    | reset the Stats data for a new game
    | get a random tetromino from list to set Tetromino object
    | set True all game object update_surface variable to draw them on the screen
    | game over is a flag for end game
    """
    global start_ticks
    start_ticks = pygame.time.get_ticks()
    reset_settings()
    get_next_random_tetromino()
    Board.update_surface = True
    Board.pattern = Board.set_pattern()
    Tetromino.update_surface = True
    Stats.update_surface = True

def reset_settings():
    """
    | reset data to 0 and take the Arrow selection (name and level)
    """
    Stats.level = Arrow.level
    Stats.name = "".join(Arrow.name)
    Stats.score = 0
    Stats.speed_points = 0
    Stats.lines = 0

def reset_arrow():
    Arrow.update_surface = True
    Arrow.update_settings = True
    Arrow.get_data(CONTENT[STATES[game_state]])

####################
#                  #
# CUSTOM PROCESSES #
#                  #
####################

def check_save_file():
    file_name = SAVES['file_name']
    options = SAVES['options']
    set_file(file_name, options)
    return file_name

def save_score():
    """
    | Retrieve save data information
    | Set the data of the last game in a tuple
    | Write the data as a tuple in a list of length 1 for the save file
    """
    s = Stats
    if s.score == 0:
        return
    file_name = check_save_file()
    time = set_time_string(s.time)
    score = str(s.score)
    save = [(s.name,score,str(s.lines),str(s.level),time)]
    write_csv(file_name, save)
    print(f'The {s.name}\'s score of {score} points is saved.')

def draw_best_score():
    """
    | Retrieve the scores from save, sort it and get data from the 1st
    """
    file_name = check_save_file()
    read = read_csv(file_name)
    sortedscore = sort_score(read[1])
    best = sortedscore[0]
    text = f"{best[0]} has made {best[1]} points !"
    x,y = 8*GRID,26*GRID
    write(font,screen,(x,y),text,"yellow")

def draw_highscores():
    """
    | Get the score list from the save file, sort it and write it all
    """
    file_name = check_save_file()
    read = read_csv(file_name)
    x, y = 2*GRID, 4*GRID
    for index, header in enumerate(read[0],start=1):
        write(font,screen,(x,y),header,'white')
        x += 7*GRID
    sortedscore = sort_score(read[1])
    x, y = 2*GRID, 6*GRID
    for index, score in enumerate(sortedscore, start=1):
        if index == 1:
            color = 'yellow'
        elif index == 2:
            color = 'lime'
        else:
            color = 'coral'
        x = 2*GRID
        for i,s in enumerate(score, start=1):
            write(font,screen,(x,y),s,color)
            x += 7*GRID
        if index == 8:
            break
        else:
            y += 3*GRID

def sort_score(scorelist):
    """
    | Sort the score list by the score integer (index 1) in reverse order
    """
    sl = scorelist
    sl.sort(key=lambda score: int(score[1]), reverse=True)
    return sl

#####################
#                   #
# DRAWING FUNCTIONS #
#                   #
#####################

def game_drawing():
    """
    | Using differents flags
    | Draw screen
    | Draw objects
    | Update display
    """
    global update_screen
    screen_updated = False
    if update_screen == True:
        draw_screen()
        screen_updated = True
        update_screen = False
    objects_updated = draw_objects()
    if screen_updated or objects_updated:
        pygame.display.update()
        ####START DEBUG CODE####
        if DEBUG:
            global updated_frames
            updated_frames +=1
        #####END DEBUG CODE#####

def reset_screen(color):
    """
    | Clear screen, draw the program 1 px border
    """
    clear(screen)
    rectangle(screen, (0,0,WIDTH,HEIGHT), color, False)

def draw_screen():
    """
    | Draw the correct content according to game state
    | For PLAY game state, clear the screen for object only
    | For CONFIRM, no clearing, draw confirm box over the game
    | For others game states, clear the screen then draw the text content
    """
    if game_state == GSC['PLAY']:
        reset_screen('iron')
        write(font,screen,Stats.name_position,Stats.name+Stats.suffix,'white')
    elif game_state == GSC['CONFIRM'] or game_state == GSC['OVER']:
        draw_confirm_box()
    else:
        reset_screen('white')
        draw_text_from_content()
        draw_global_message()

def draw_objects():
    """
    | Draw the correct surface when flag of related object is up
    | Is the Game State is a playing state :
    |     Draw game board
    |     Check the speed points and draw game stats
    |     Check score game and draw tetromino new position
    | For Arrow object:
    |     Clear the surface before drawing
    |     Draw the arrow to new position
    """
    updated = False
    if game_state == GSC['PLAY']:
        if Board.update_surface == True:
            Board.draw(board_surface, GRID, DEBUG)
            blit(screen, board_surface, Board.surface_position)
            updated = True
        if Stats.update_surface == True:
            Stats.check_level()
            Stats.draw(stats_surface, GRID, font, DEBUG)
            blit(screen, stats_surface, Stats.surface_position)
            updated = True
        if Tetromino.update_surface == True:
            Stats.update_score(Board.update_pattern(Tetromino.check_update(Board)))
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
    if Arrow.update_settings == True and game_state == GSC['NEW']:
        Arrow.draw_settings(screen, GRID, font)
        updated = True
    return updated

def draw_text_from_content():
    """
    | Get all text content from data and write it on the surface
    """
    datas = CONTENT[STATES[game_state]]['text']
    for d in datas:
        position = d[0]
        text = d[1]
        color = d[2]
        write(font, screen, position, text, color)
    if game_state == GSC['SCORE']:
        draw_highscores()
    if game_state == GSC['INTRO']:
        draw_best_score()

def draw_global_message():
    """
    | Draw a message in a rectangle at the bottom of the screen
    """
    if game_state == GSC['MENU']:
        datas = CONTENT['GLOBAL']['menu_continue']
    elif game_state == GSC['NEW']:
        datas = CONTENT['GLOBAL']['new_continue']
    else:
        datas = CONTENT['GLOBAL']['continue']
    position = datas[0]
    text = datas[1]
    color = datas[2]
    rectangle(screen,(0,29*GRID-1,WIDTH,GRID+1),'white')
    write(font,screen,position,text,color)

def draw_confirm_box():
    """
    | Draw a centered box with a message
    """
    state = STATES[game_state]
    datas = [CONTENT[state]['confirm'], CONTENT[state]['info'], CONTENT[state]['continue']]
    box = CONTENT[state]['box']
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

def game_over():
    """
    | Update the flags that define a game over state
    """
    global game_state, update_screen
    game_state = GSC['OVER']
    Tetromino.game_over = False
    Stats.game_over = False
    update_screen = True

def goto_menu():
    """
    | reset settings and go to MENU game state
    """
    global game_state, update_screen
    game_state = GSC['MENU']
    update_screen = True
    reset_arrow()

def validation_key():
    """
    | Most game state, move to an other game state
    | but in Menu state, move to the arrow selected choice
    | and in Play state, is it a game input that move the Tetromino
    | STATES :
    | * TITLE : Title screen
    | * INTRO : Introduction screen
    | * MENU : Menu screen
    | * SCORE : Highscores screen
    | * NEW : New Game screen / Start Settings
    | * PLAY : Game Playing screen
    | * OVER : Game Over screen
    | * EXIT : Flag to Exit the Game
    """
    global game_state, update_screen
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
        game_state = GSC['NEW']
        update_screen = True
    elif game_state == GSC['CONFIRM']:
        save_score()
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
    """
    | Most game states return to MENU state,
    | but in PLAY state ask a confirmation before
    | in CONFIRM state which pause the game, cancel the confirm state
    | in MENU state leave the game
    | if DEBUG, leave program immediatly
    """
    global game_state, update_screen
    if game_state == GSC['PLAY']:
        game_state = GSC['CONFIRM']
        update_screen = True
    elif game_state == GSC['CONFIRM']:
        game_state = GSC['PLAY']
        Stats.update_surface = True
        Tetromino.update_surface = True
        Board.update_surface = True
        update_screen = True
    elif game_state == GSC['MENU']:
        game_state = GSC['EXIT']
    else:
        goto_menu()

def move_key(key):
    """
    | At all states except PLAY, inputs used to move arrows
    | At game state PLAY, inputs used to interact with the tetromino
    | 0 : UP = ROTATE TETROMINO (cw=clockwise)
    | 1 : DOWN = GO FASTER
    | 2 : LEFT = GO LEFT
    | 3 : RIGHT = GO RIGHT
    | 4 : SPACE & RETURN = JUMP DOWN
    | The Stats score is updated if a Tetromino return completed lines
    """
    if game_state == GSC['MENU'] or game_state == GSC['NEW']:
        Arrow.move(key, game_state)
        reset_arrow()
    elif game_state == GSC['PLAY']:
        if key == 0:
            Tetromino.rotate()
        else:
            Tetromino.move(key)

def check_inputs():
    """
    | check player possible inputs
    | * the exit window
    | * the escape input
    | * the space & return input
    | * the 4 arrows input
    | * the gamepad inputs
    | check game_state to return True or False to loop running
    """
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
    """
    | Check the used input of the gamepad
    """
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
    """
    | At each loop
    | 1. Check events input and change datas if game is playing
    | 2. Check game over from the Tetromino or from the Stats:
    |    1. If over, score saved, game over.
    |    2. If done, get next tetromino.
    | 3. Update clock, keep tetromino moving down and update timer
    | 4. Update screen & surfaces drawing if related flag raised True
    | 5. Keep the FPS clock at 60
    """
    game_running = True
    ####START DEBUG CODE####
    if DEBUG == True:
        global updated_frames, frames
        updated_frames = 0
        frames = 0
    #####END DEBUG CODE#####
    while game_running:
        game_running = check_inputs() #1
        if game_state == GSC['PLAY']: #2
            if Tetromino.game_over == True or Stats.game_over == True: #2.1
                save_score()
                game_over()
            elif Tetromino.done: #2.2
                get_next_random_tetromino()
            else: #3
                game_ticks = pygame.time.get_ticks()
                Tetromino.slide(game_ticks)
                Stats.update_time(game_ticks - start_ticks)
        game_drawing() #4
        clock.tick(60) #5
        ####START DEBUG CODE####
        if DEBUG == True:
            frames += 1
            debug_draw_grid(screen)
            debug_write_stats(font,screen,start_ticks,clock,updated_frames,frames)
            pygame.display.update()
        #####END DEBUG CODE#####
    quit()

##############
#            #
# START GAME #
#            #
##############

if __name__ == "__main__":
    init_game()
