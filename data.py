# 1 GRID PIXEL (PX) = SIZE GRID = 8 pixel
PX = GRID = 8

# SCREEN SIZE
screensizes = {
    'width':320,
    'height':240,
    'grid':GRID,
    'columns':40,
    'lines':30
}

# GAME STATES
'''
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

GSC = gamestatescodes = {
    'TITLE':0,
    'INTRO':1,
    'MENU':2,
    'SCORE':3,
    'NEW':4,
    'PLAY':5,
    'OVER':6,
    'EXIT':7
}

gamestates = ['TITLE', 'INTRO', 'MENU', 'SCORE', 'NEW', 'PLAY', 'OVER', 'EXIT']

# GAME DATA CONTENT
'''
text to write: position, text, color
arrow selection : position, game state number
'''
statecontent = {
    'GLOBAL': {
        'continue': [(8*PX,24*PX),"Press Space Bar to continue", 'white'],
        'confirm': [(8*PX,12*PX),"Are you sure you want to leave ?", 'white'],
        'info': [(8*PX,14*PX),"The score will be saved.", 'white'] 
    },
    'TITLE': {
        'text': [
            [(16*PX,15*PX),"TETRIS", 'white']
        ]
    },
    'INTRO': {
        'text':[
            [(10*PX,1*PX),"GET THE BEST SCORE!", 'yellow'],
            [(4*PX,4*PX),"1 line  :  10 score  & 10 speed", 'white'],
            [(4*PX,6*PX),"2 lines :  25 score  &  5 speed", 'white'],
            [(4*PX,8*PX),"3 lines :  50 score  &  2 speed", 'white'],
            [(4*PX,10*PX),"4 lines : 100 score  &  1 speed", 'white'],
            [(2*PX,14*PX),"Every 100 speed point :", 'cyan'],
            [(4*PX,16*PX),"Jump 1 level, the speed increase !", 'cyan'],
            [(4*PX,20*PX),"Current best Score :", 'white'],
        ]
    },
    'MENU': {
        'text':[
            [(12*PX,10*PX),"Start a New Game",'green'],
            [(12*PX,12*PX),"View Introduction",'white'],
            [(12*PX,14*PX),"View Highscores",'white'],
            [(12*PX,16*PX),"Exit Game",'red']
        ],
        'arrowshape':[
            (0,0,0,0,1,0,0,0),
            (0,0,0,0,1,1,0,0),
            (0,1,1,1,1,1,1,0),
            (0,1,1,1,1,1,1,1),
            (0,1,1,1,1,1,1,0),
            (0,0,0,0,1,1,0,0),
            (0,0,0,0,1,0,0,0),
            (0,0,0,0,0,0,0,0)
        ],
        'arrowselect':[
            [(10*PX,10*PX),'green',GSC['NEW']],
            [(10*PX,12*PX),'white',GSC['INTRO']],
            [(10*PX,14*PX),'white',GSC['SCORE']],
            [(10*PX,16*PX),'red',GSC['EXIT']]
        ]
    },
    'NEW': {
        'text':[
            [(6*PX,4*PX),"NAME",'blue'],
            [(6*PX,6*PX),"SPEED",'white']
        ],
        'arrowshape':[
            (0,0,0,0,1,0,0,0),
            (0,0,0,1,1,1,0,0),
            (0,0,1,1,1,1,1,0),
            (0,1,1,1,1,1,1,1),
            (0,0,0,1,1,1,0,0),
            (0,0,0,1,1,1,0,0),
            (0,0,0,1,1,1,0,0),
            (0,0,0,1,1,1,0,0)
        ],
        'arrowselect':[
            [(4*PX,4*PX),'LETTER_1'],
            [(4*PX,6*PX),'LETTER_2'],
            [(4*PX,8*PX),'LETTER_3'],
            [(4*PX,10*PX),'SPEED LEVEL']
        ]
    },
}

# COLORS DATA

colorslist = {
    'black':(0,0,0),
    'white':(255,255,255),
    'grey':(128,128,128),
    'cyan':(0,255,255),
    'blue':(0,0,255),
    'orange':(255,165,0),
    'yellow':(255,255,0),
    'red':(255,0,0),
    'green':(0,255,0),
    'purple':(255,0,255)
}

# TETROMINO SHAPES

shapes_I = []

shapes_J = []

shapes_L = []

shapes_O = []

shapes_Z = []

shapes_S = []

shapes_T = []

tetrominoshapes = {
    'I': {
        'shape': shapes_I,
        'color': 'cyan'
    },
    'J': {
        'shape': shapes_J,
        'color': 'blue'
    },
    'L': {
        'shape': shapes_L,
        'color': 'orange'
    },
    'O': {
        'shape': shapes_O,
        'color': 'yellow'
    },
    'Z': {
        'shape': shapes_Z,
        'color': 'red'
    },
    'S': {
        'shape': shapes_S,
        'color': 'green'
    },
    'T': {
        'shape': shapes_T,
        'color': 'purple'
    }
}