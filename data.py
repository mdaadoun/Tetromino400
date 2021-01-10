
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

# GAME STATES
'''
STATES :
0 : TITLE : Title screen
1 : INTRO : Introduction screen
2 : MENU : Menu screen
3 : SCORE : Highscores screen
4 : NEW : New Game screen / Start Settings
5 : PLAY : Game Playing screen
6 : CONFIRM : Confirm end game
7 : OVER : Game Over screen
8 : EXIT : Flag to Exit the Game
'''

GSC = gamestatescodes = {
    'TITLE':0,
    'INTRO':1,
    'MENU':2,
    'SCORE':3,
    'NEW':4,
    'PLAY':5,
    'CONFIRM':6,
    'OVER':7,
    'EXIT':8
}

gamestates = ['TITLE', 'INTRO', 'MENU', 'SCORE', 'NEW', 'PLAY', 'CONFIRM', 'OVER', 'EXIT']

# GAME DATA CONTENT
'''
text to write: position, text, color
arrow selection : position, game state number
'''
statecontent = {
    'GLOBAL': {
        'continue': [(8*PX,29*PX),"Press Space to continue", 'black'],
        'menu_continue': [(4*PX,29*PX),"Select An Option and Press Space", 'black'],
        'new_continue': [(4*PX,29*PX),"Change Settings and Press Space", 'black']
    },
    'TITLE': {
        'text': [
            [(16*PX,8*PX),"TETRIS", 'cyan'],
            [(16*PX,10*PX),"TETRIS", 'blue'],
            [(16*PX,12*PX),"TETRIS", 'orange'],
            [(16*PX,14*PX),"TETRIS", 'yellow'],
            [(16*PX,16*PX),"TETRIS", 'red'],
            [(16*PX,18*PX),"TETRIS", 'green'],
            [(16*PX,20*PX),"TETRIS", 'purple']
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
            [(8*PX,14*PX),"NAME",'blue'],
            [(8*PX,18*PX),"_",'blue'],
            [(10*PX,18*PX),"_",'blue'],
            [(12*PX,18*PX),"_",'blue'],
            [(26*PX,14*PX),"SPEED",'yellow'],
            [(26*PX,18*PX),"_",'yellow']
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
            [(8*PX,19*PX),'blue', 'A'],
            [(10*PX,19*PX),'blue', 'A'],
            [(12*PX,19*PX),'blue', 'A'],
            [(26*PX,19*PX),'yellow', 1]
        ]
    },
    'SCORE': {
        'text':[
            [(15*PX,1*PX),"HIGHSCORES",'yellow']
        ]
    },
    'CONFIRM': {
        'confirm': [(7*PX,12*PX),"You really want to leave ?", 'red'],
        'info': [(7*PX,14*PX),"The score will be saved.", 'grey'],
        'continue': [(7*PX,16*PX),"Press space to leave.", 'black'],
        'box': (4*GRID, 10*GRID, 32*GRID, 9*GRID)
    }
}

# TETROMINO SHAPES
shapes_I = [
    [
        (0,0,1,0),
        (0,0,1,0),
        (0,0,1,0),
        (0,0,1,0)
    ],
    [
        (0,0,0,0),
        (0,0,0,0),
        (1,1,1,1),
        (0,0,0,0)
    ]
]

shapes_J = [
    [
        (0,1,0),
        (0,1,0),
        (1,1,0)
    ],
    [
        (1,0,0),
        (1,1,1),
        (0,0,0)
    ],
    [
        (0,1,1),
        (0,1,0),
        (0,1,0)
    ],
    [
        (0,0,0),
        (1,1,1),
        (0,0,1)
    ]
]

shapes_L = [
    [
        (0,1,0),
        (0,1,0),
        (0,1,1)
    ],
    [
        (0,0,0),
        (1,1,1),
        (1,0,0)
    ],
    [
        (1,1,0),
        (0,1,0),
        (0,1,0)
    ],
    [
        (0,0,1),
        (1,1,1),
        (0,0,0)
    ]
]

shapes_O = [
    [
        (1,1),
        (1,1)
    ]
]

shapes_Z = [
    [
        (0,1,0),
        (1,1,0),
        (1,0,0)
    ],
    [
        (1,1,0),
        (0,1,1),
        (0,0,0)
    ]
]

shapes_S = [
    [
        (0,1,0),
        (1,1,0),
        (1,0,0)
    ],
    [
        (1,1,0),
        (0,1,1),
        (0,0,0)
    ]
]

shapes_T = [
    [
        (0,1,0),
        (0,1,1),
        (0,1,0)
    ],
    [
        (0,0,0),
        (1,1,1),
        (0,1,0)
    ],
    [
        (0,1,0),
        (1,1,0),
        (0,1,0)
    ],
    [
        (0,1,0),
        (1,1,1),
        (0,0,0)
    ]
]

tetrominoshapes = {
    'I': {
        'shape': shapes_I,
        'color': colorslist['cyan']
    },
    'J': {
        'shape': shapes_J,
        'color': colorslist['blue']
    },
    'L': {
        'shape': shapes_L,
        'color': colorslist['orange']
    },
    'O': {
        'shape': shapes_O,
        'color': colorslist['yellow']
    },
    'Z': {
        'shape': shapes_Z,
        'color': colorslist['red']
    },
    'S': {
        'shape': shapes_S,
        'color': colorslist['green']
    },
    'T': {
        'shape': shapes_T,
        'color': colorslist['purple']
    }
}

board = {
    'position':(6*PX,6*PX),
    'size':(12*PX, 21*PX)
}

infos = {
    'position':(20*PX,6*PX),
    'size':(12*PX, 21*PX),
    'position_next':(4*PX,2*PX),
    'size_next':(8*PX, 8*PX),
    'texts': (
        ('NEXT',(2*PX,0)),
        ('LINES',(2*PX,12*PX)),
        ('SCORE',(2*PX,14*PX)),
        ('LEVEL',(2*PX,16*PX)),
        ('TIME',(2*PX,18*PX))
    )
}

# GLOBAL DATA
'''
    Prepare the datas for import
'''
WIDTH = screensizes['width']
HEIGHT = screensizes['height']
GRID = screensizes['grid']
LINES = screensizes['lines']
COLUMNS = screensizes['columns']
GSC = gamestatescodes # GSC = Game State Code
STATES = gamestates
CONTENT = statecontent
COLORS = colorslist
BOARD = board
TETROMINOS = tetrominoshapes
