import pygame
from pygame import freetype, gfxdraw
import sys

# DATA

WIDTH = 320
HEIGHT = 240
STATES = ['INTRO1', 'INTRO2', 'MENU', 'SCORE', 'GAME']
game_state = STATES[0]
black = (0,0,0)
white = (255,255,255)
grey = (128,128,128)

# INIT PROCESS

def screen_init():
    global screen, update_screen
    title = "Tetris v1"
    pygame.display.set_caption(title)
    screen = pygame.display.set_mode((WIDTH,HEIGHT), flags=pygame.NOFRAME|pygame.SCALED)
    update_screen = True

def font_init():
    global font 
    freetype.init()
    font = freetype.Font("prstartk.ttf")

def init_timer():
    global clock
    clock = pygame.time.Clock()

def game_init():
    pygame.display.init()
    screen_init()
    font_init()
    init_timer()
    # LOOP
    game_loop()
    print('OK')


# DRAWING GAME

def draw_screen():
    global update_screen
    # STATE INTRODUCTION 1
    if game_state == STATES[0]:
        screen.fill(white)
        font.render_to(screen,(WIDTH/2, HEIGHT/2), "Super Tetris", black,None,0,0,8)

    # STATE INTRODUCTION 2
    elif game_state == STATES[1]:
        screen.fill(white)
        font.render_to(screen,(WIDTH/2, HEIGHT/2), "Score", black,None,0,0,8)
        for i in range(8, WIDTH, 8):
            pygame.gfxdraw.line(screen,i,0,i,HEIGHT,grey)
            if i < HEIGHT:
                pygame.gfxdraw.line(screen,0,i,WIDTH,i,grey) 
    
    pygame.display.update()
    update_screen = False


# UPDATE

def change_game_state():
    global game_state, update_screen
    if game_state == STATES[0]:
        game_state = STATES[1]
        update_screen = True
    elif game_state == STATES[1]:
        game_state = STATES[0]
        update_screen = True

# CHECK EVENTS

def check_inputs():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if event.key == pygame.K_SPACE:
                change_game_state()
    
    # game still running
    return True


# MAIN GAME LOOP

def game_loop():
    game_running = True
    while game_running:
        game_running = check_inputs()
        if update_screen == True:
            draw_screen()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_init()