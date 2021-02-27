# game.py
import os
from random import randrange, randint
from data import WIDTH, HEIGHT, GRID, LINES, COLUMNS, GSC, STATES, \
    CONTENT, COLORS, BOARD, TETROMINO, TETROMINOSHAPES, STATS, \
    ARROW, NAME, SAVES

import pygame
from pygame import freetype, gfxdraw

from api import *
import objects
from debug import *

fullscreen = False
music = True

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
    | init_sound load music and sound for the game
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
    init_sound()
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

def set_fullscreen():
    """
    | Switch fullscreen
    """
    global screen, fullscreen, update_screen
    if fullscreen is True:
        flags = pygame.FULLSCREEN|pygame.SCALED
        fullscreen = False
    else:
        flags = pygame.NOFRAME|pygame.SCALED
        fullscreen = True
    ####START DEBUG CODE####
    if DEBUG:
        flags = pygame.SCALED
    #####END DEBUG CODE#####
    screen = pygame.display.set_mode((WIDTH,HEIGHT), flags)
    update_screen = True

def set_sound():
    """
    | Stop music stream, start it if it have been stopped
    """
    global music
    if music is True:
        music = False
        pygame.mixer.music.stop()
    else:
        music = True
        pygame.mixer.music.play()

def init_screen():
    set_fullscreen()
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

def init_sound():
    """
    | Init the mixer module
    | Retrieve the file path of the currebt script from __file__
    | Load the music and play it
    | Load the different sounds and store them in global variable
    | SOUNDS for later access
    """
    global SOUNDS
    path = os.path.dirname(os.path.realpath(__file__))
    pygame.mixer.init()
    pygame.mixer.music.load(f'{path}/chord-128.mp3')
    pygame.mixer.music.play()
    SOUNDS = {}
    Arrowmove = pygame.mixer.Sound(f'{path}/sounds/Arrowmove.ogg')
    SOUNDS['arrowmove'] = Arrowmove
    Arrowselect = pygame.mixer.Sound(f'{path}/sounds/Arrowselect.ogg')
    SOUNDS['arrowselect'] = Arrowselect
    Blocked = pygame.mixer.Sound(f'{path}/sounds/Blocked.ogg')
    SOUNDS['blocked'] = Blocked
    Done = pygame.mixer.Sound(f'{path}/sounds/Done.ogg')
    SOUNDS['done'] = Done
    Rotate = pygame.mixer.Sound(f'{path}/sounds/Rotate.ogg')
    SOUNDS['rotate'] = Rotate
    Move = pygame.mixer.Sound(f'{path}/sounds/Move.ogg')
    SOUNDS['move'] = Move
    GameOver = pygame.mixer.Sound(f'{path}/sounds/GameOver.ogg')
    SOUNDS['gameover'] = GameOver
    GameStart = pygame.mixer.Sound(f'{path}/sounds/GameStart.ogg')
    SOUNDS['gamestart'] = GameStart
    LevelUp = pygame.mixer.Sound(f'{path}/sounds/LevelUp.ogg')
    SOUNDS['levelup'] = LevelUp
    Line1 = pygame.mixer.Sound(f'{path}/sounds/Line1.ogg')
    SOUNDS['line1'] = Line1
    Line2 = pygame.mixer.Sound(f'{path}/sounds/Line2.ogg')
    SOUNDS['line2'] = Line2
    Line3 = pygame.mixer.Sound(f'{path}/sounds/Line3.ogg')
    SOUNDS['line3'] = Line3
    lines4 = []
    Line4_1 = pygame.mixer.Sound(f'{path}/sounds/Line4_1.ogg')
    lines4.append(Line4_1)
    Line4_2 = pygame.mixer.Sound(f'{path}/sounds/Line4_2.ogg')
    lines4.append(Line4_2)
    Line4_3 = pygame.mixer.Sound(f'{path}/sounds/Line4_3.ogg')
    lines4.append(Line4_3)
    SOUNDS['lines4'] = lines4

def init_timer():
    global clock
    clock = pygame.time.Clock()

def init_gamepad():
    """
    | Init the joystick module
    | Quit the module if no joystick connected
    | The different gamepads are listed and the first
    | is stored for later access
    """
    global gamepad
    gamepad = []
    pygame.joystick.init()
    gamepad_count = pygame.joystick.get_count()
    for i in range(gamepad_count):
        gp = pygame.joystick.Joystick(i)
        gp.init()
        gamepad.append(gp)
    if (len(gamepad) == 0):
        pygame.joystick.quit()
        print("No Gamepad Connected")
    else:
        for i, gp in enumerate(gamepad):
            name = gp.get_name()
            print(f"The gamepad {i+1} is named: {name}")
        print("Only the first gamepad is used.")
        gamepad = gamepad[0]

def init_objects():
    """
    | Prepare the objects the game will use
    | 3 Objects and a list of 7 Tetromino objects :
    | Arrow, Board, Stats : main game objects
    | the tetrominos are set in the init fonction
    """
    global Board, Stats, Arrow
    Arrow = objects.Arrow(ARROW)
    Board = objects.Board(BOARD)
    Stats = objects.Stats(STATS)
    init_tetrominos_objects()

def init_tetrominos_objects():
    """
    | All differents tetrominos are initialized in the list
    | Each 7 tetromino types are stored in a global variable tetrominos
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
    | Prepare the surfaces the game will use in global variables
    | 4 Surfaces :
    | arrow_surface, board_surface, stats_surface, tetromino_surface
    | set to arrow and tetromino surfaces a color for transparency
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
    | Set the Tetromino main object with a reference to 1 of the 7 tetrominos
    | by chosing it randomly from the tetrominos list in the global variable
    | with a random starting rotation
    | set Tetromino.done flag as False
    | get the next tetromino in the current Tetromino object
    | select a random next tetromino and send it to Stats to draw it
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
    | set True all game surfaces update flags to draw them on the screen
    | Play the new game sound
    """
    global start_ticks
    start_ticks = pygame.time.get_ticks()
    reset_settings()
    get_next_random_tetromino()
    Board.update_surface = True
    Board.pattern = Board.set_pattern()
    Tetromino.update_surface = True
    Stats.update_surface = True
    pygame.mixer.Sound.play(SOUNDS['gamestart'])

def reset_settings():
    """
    | reset data to 0 and take the Arrow selection (name and level)
    | to pass it to Stats for updating the stats surface
    """
    Stats.level = Arrow.level
    Stats.name = "".join(Arrow.name)
    Stats.score = 0
    Stats.speed_points = 0
    Stats.lines = 0

def reset_arrow():
    """
    | Set flags of arrow to reset config, give the default data to Arrow object
    """
    Arrow.update_surface = True
    Arrow.update_settings = True
    Arrow.get_data(CONTENT[STATES[game_state]])

####################
#                  #
# CUSTOM PROCESSES #
#                  #
####################

def check_save_file():
    """
    | get file name and default datas for the file
    | set_file : Check if save file exist, create it if not
    """
    file_name = SAVES['file_name']
    options = SAVES['options']
    set_file(file_name, options)
    return file_name

def save_score():
    """
    | Retrieve save data information
    | Set the data of the last game in a tuple if score > 0
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
    | Get the score list from the save file, sort it and write the 8 best
    | Restart the music if the stream was stopped, play a random sound
    """
    rndsnd = randint(0, 2)
    pygame.mixer.Sound.play(SOUNDS['lines4'][rndsnd])
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()
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
    | Using differents flags to redirect with the drawing function needed
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
    | For PLAY game state, clear the screen for object only, write player name
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

def draw_tetromino():
    Tetromino.draw(tetromino_surface, GRID, DEBUG, True)
    blit(screen, tetromino_surface, Tetromino.position)
    Tetromino.set_update()
    Tetromino.draw(tetromino_surface, GRID, DEBUG)
    blit(screen, tetromino_surface, Tetromino.position)

def draw_objects():
    """
    | Draw the correct surface when flag of related object is up
    | Is the Game State is a playing state :
    |     Board : Draw game board
    |     Stats : Check the speed points to change level before to draw game stats
    |     Tetromino : Check score game and draw tetromino new position
    | For Arrow object:
    |     Clear the surface before drawing (no transparency needed)
    |     Draw the arrow to new position
    """
    updated = False
    if game_state == GSC['PLAY']:
        if Board.update_surface == True:
            Board.draw(board_surface, GRID, DEBUG)
            blit(screen, board_surface, Board.surface_position)
            updated = True
        if Stats.update_surface == True:
            Stats.check_level(SOUNDS)
            Stats.draw(stats_surface, GRID, font, DEBUG)
            blit(screen, stats_surface, Stats.surface_position)
            updated = True
        if Tetromino.update_surface == True:
            Stats.update_score(
                Board.update_pattern(
                Tetromino.check_update(Board, SOUNDS)
                ), SOUNDS
            )
            draw_tetromino()
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
    pygame.mixer.Sound.play(SOUNDS['gameover'])

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
    | * INPUTS : Gameplay instructions
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
        game_state = GSC['INPUTS']
        update_screen = True
    elif game_state == GSC['INPUTS']:
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
        pygame.mixer.Sound.play(SOUNDS['arrowselect'])
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
    | 0 : UP = ROTATE TETROMINO (clockwise)
    | 1 : DOWN = GO FASTER ONCE
    | 2 : LEFT = GO LEFT
    | 3 : RIGHT = GO RIGHT
    | 4 : SPACE & RETURN = GO FASTER (jump)
    """
    if game_state == GSC['MENU'] or game_state == GSC['NEW']:
        pygame.mixer.Sound.play(SOUNDS['arrowmove'])
        Arrow.move(key, game_state)
        reset_arrow()
    elif game_state == GSC['PLAY']:
        if key == 0:
            Tetromino.rotate()
        elif key == 4:
            Tetromino.jump()
        else:
            Tetromino.move(key)

def check_inputs():
    """
    | check player possible inputs
    | * the exit window
    | * the escape input
    | * the space & return input
    | * the 4 arrows input
    | * F for fullscreen switch, S for music switch
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
            if event.key == pygame.K_f:
                set_fullscreen()
            if event.key == pygame.K_s:
                set_sound()
        if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYAXISMOTION:
            get_gamepad_input()
    return check_exit(game_state)

def get_gamepad_input():
    """
    | Check the used input of the gamepad
    """
    gp = gamepad
    #axes = gp.get_numaxes()
    #print("Number of axes: {}".format(axes))

    #buttons = gp.get_numbuttons()
    #print("Number of buttons: {}".format(buttons))

    ax_up_dn = gp.get_axis(1)
    ax_lf_rg = gp.get_axis(0)
    btnA = gp.get_button(0)
    btnB = gp.get_button(1)
    btnUnk = gp.get_button(2)
    btnX = gp.get_button(3)
    btnY = gp.get_button(4)
    btnRe = gp.get_button(10)
    btnSt = gp.get_button(11)

    #for i in range(axes):
    #    axis = gp.get_axis(i)
    #    print("Axis {} value: {:>6.3f}".format(i, axis))
    #for i in range(buttons):
    #    button = gp.get_button(i)
    #    print("Button {:>2} value: {}".format(i, button))

    if ax_up_dn < 0 or btnA == True or btnY == True:
        move_key(0)
    elif ax_up_dn > 0:
        move_key(1)
    elif ax_lf_rg > 0:
        move_key(3)
    elif ax_lf_rg < 0:
        move_key(2)
    if btnSt == True or btnUnk == True or btnB == True:
        validation_key()
    if btnRe == True or btnX == True:
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
