
#: 1 GRID PIXEL (PX) = SIZE GRID = 8 pixel
PX = GRID = 8

#: SCREEN SIZE
screensizes = {
    'width':320,
    'height':240,
    'grid':GRID,
    'columns':40,
    'lines':30
}

#: COLORS DATA - 4 + 20 colors
colorslist = {
    'black':(0,0,0),
    'grey':(128,128,128),
    'silver':(192,192,192),
    'white':(255,255,255),
    'cyan':(0,255,255),
    'teal':(0,128,128),
    'sky':(0,191,255),
    'royal':(65,105,225),
    'blue':(0,0,255),
    'navy':(0,0,128),
    'lime':(0,255,0),
    'green':(0,128,0),
    'yellow':(255,255,0),
    'olive':(128,128,0),
    'orange':(255,140,0),
    'chocolate':(179,98,0),
    'magenta':(255,0,255),
    'purple':(128,0,128),
    'pink':(255,20,147),
    'violet':(102,0,51),
    'red':(255,0,0),
    'maroon':(128,0,0),
    'brown':(139,69,19),
    'earth':(69,27,4)
}

#: GAME STATES CODE NUMBERS
GSC = gamestatescodes = {
    'TITLE':0,
    'INTRO':1,
    'INPUTS':2,
    'MENU':3,
    'SCORE':4,
    'NEW':5,
    'PLAY':6,
    'CONFIRM':7,
    'OVER':8,
    'EXIT':9
}

gamestates = [
    'TITLE',
    'INTRO',
    'INPUTS',
    'MENU',
    'SCORE',
    'NEW',
    'PLAY',
    'CONFIRM',
    'OVER',
    'EXIT'
]
'''
    STATES :
    | 0 : TITLE : Title screen
    | 1 : INTRO : Introduction screen
    | 2 : INPUTS : Introduction inputs
    | 3 : MENU : Menu screen
    | 4 : SCORE : Highscores screen
    | 5 : NEW : New Game screen / Start Settings
    | 6 : PLAY : Game Playing screen
    | 7 : CONFIRM : Confirm end game
    | 8 : OVER : Game Over screen
    | 9 : EXIT : Flag to Exit the Game
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
            [(16*PX,18*PX),"TETRIS", 'lime'],
            [(16*PX,20*PX),"TETRIS", 'magenta']
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
    'INPUTS': {
       'text':[
            [(10*PX,1*PX),"HOW TO PLAY, KEYBOARD and GAMEPAD", 'yellow']
       ]
    },
    'MENU': {
        'text':[
            [(12*PX,10*PX),"Start a New Game",'lime'],
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
            [(10*PX,10*PX),'lime',GSC['NEW']],
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
            [(20*PX,14*PX),"LEVEL",'yellow'],
            [(20*PX,18*PX),"_",'yellow']
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
            [(20*PX,19*PX),'yellow', 1]
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
'''
    GAME DATA CONTENT
    | text to write: position, text, color
    | arrow selection : position, game state number (in menu) or setting (in new game)
    | arrow shapes in differents menus
    | the confirm box size to draw
'''

#: I TETROMINO SHAPES
shapes_I = [
    [
        (1,0,0,0),
        (1,0,0,0),
        (1,0,0,0),
        (1,0,0,0)
    ],
    [
        (0,0,0,0),
        (0,0,0,0),
        (1,1,1,1),
        (0,0,0,0)
    ]
]

#: J TETROMINO SHAPES
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
        (1,1,0),
        (1,0,0),
        (1,0,0)
    ],
    [
        (0,0,0),
        (1,1,1),
        (0,0,1)
    ]
]

#: L TETROMINO SHAPES
shapes_L = [
    [
        (1,0,0),
        (1,0,0),
        (1,1,0)
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

#: O TETROMINO SHAPE
shapes_O = [
    [
        (1,1),
        (1,1)
    ]
]

#: Z TETROMINO SHAPES
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

#: S TETROMINO SHAPES
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

#: T TETROMINO SHAPES
shapes_T = [
    [
        (1,0,0),
        (1,1,0),
        (1,0,0)
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
        'color': 'lime'
    },
    'T': {
        'shape': shapes_T,
        'color': 'magenta'
    }
}
'''
    Variable that gather all Tetromino Shapes with the related colors
'''

#: Board size and position
board = {
    'surface_size':(12*PX, 21*PX),
    'surface_position':(5*PX,6*PX)
}

#: Stats & Next Tetromino Box sizes and positions + Stats titles positions and content
stats = {
    'surface_size':(12*PX, 24*PX),
    'surface_position':(23*PX,3*PX),
    'position_next':(2*PX,0*PX),
    'size_next':(8*PX, 8*PX),
    'stats': (
        ('NEXT',(4*PX,0),None),
        ('LINES',(2*PX,10*PX),'0'),
        ('SCORE',(2*PX,13*PX),'0000'),
        ('SPEED',(2*PX,16*PX),'0000'),
        ('LEVEL',(2*PX,19*PX),'0'),
        ('TIME',(2*PX,22*PX),'00:00:00')
    )
}

#: Tetromino
tetromino = {
    'surface_size':(4*PX, 4*PX),
    'surface_position':(10*PX, 2*PX)
}

arrow = {
    'surface_size':(PX,PX)
}

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
STATS = stats
ARROW = arrow
TETROMINO = tetromino
TETROMINOSHAPES = tetrominoshapes
'''
    GLOBAL DATA
    | Prepare all the datas to use in game
'''
