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
            [(14*PX,8*PX),"PiTetromino", 'cyan'],
            [(14*PX,10*PX),"PiTetromino", 'blue'],
            [(14*PX,12*PX),"PiTetromino", 'orange'],
            [(14*PX,14*PX),"PiTetromino", 'yellow'],
            [(14*PX,16*PX),"PiTetromino", 'red'],
            [(14*PX,18*PX),"PiTetromino", 'lime'],
            [(14*PX,20*PX),"PiTetromino", 'magenta']
        ]
    },
    'INTRO': {
        'text':[
            [(4*PX,2*PX),"WIN POINTS, GET THE BEST SCORE!", 'yellow'],
            [(2*PX,5*PX),"1 line  =  1xlvl pts  & 10 speed pts", 'white'],
            [(2*PX,7*PX),"2 lines =  2xlvl pts  &  5 speed pts", 'white'],
            [(2*PX,9*PX),"3 lines =  3xlvl pts  &  2 speed pts", 'white'],
            [(2*PX,11*PX),"4 lines =  4xlvl pts  &  1 speed pts", 'white'],
            [(2*PX,15*PX),"Every 100 speed points :", 'cyan'],
            [(3*PX,17*PX),"Jump 1 level, the speed increase !", 'cyan'],
            [(8*PX,19*PX),"There is 9 speed levels.", 'cyan'],
            [(14*PX,21*PX),"Playtime max is 1 hour.", 'cyan'],
            [(2*PX,24*PX),"Current best Score :", 'white'],
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
            [(12*PX,12*PX),"View Instructions",'white'],
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
            [(8*PX,8*PX),"Get Ready for a New Game !", 'white'],
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
            [(8*PX,19*PX),'blue',None],
            [(10*PX,19*PX),'blue',None],
            [(12*PX,19*PX),'blue',None],
            [(20*PX,19*PX),'yellow',None]
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
    },
    'OVER': {
        'confirm': [(14*PX,12*PX),"GAME OVER !", 'red'],
        'info': [(4*PX,14*PX),"The score is saved.", 'grey'],
        'continue': [(4*PX,16*PX),"Press space to replay or escape.", 'black'],
        'box': (2*GRID, 10*GRID, 36*GRID, 9*GRID)
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
        (1,0,0),
        (1,1,0),
        (0,1,0)
    ],
    [
        (0,1,1),
        (1,1,0),
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
    'surface_position':(5*PX,6*PX),
    'pattern_position':(1*PX,0),
    'pattern_size':(10,20)
}

#: Stats & Next Tetromino Box sizes and positions + Stats titles positions and content
stats = {
    'surface_size':(12*PX, 24*PX),
    'surface_position':(23*PX,3*PX),
    'position_next':(2*PX,0*PX),
    'size_next':(8*PX, 8*PX),
    'name_position':(6*PX, 3*PX),
    'name_suffix':' PLAY !',
    'stats': (
        ('NEXT',(4*PX,0)),
        ('LINES',(2*PX,10*PX)),
        ('SCORE',(2*PX,13*PX)),
        ('SPEED',(2*PX,16*PX)),
        ('LEVEL',(2*PX,19*PX)),
        ('TIME',(2*PX,22*PX))
    )
}

#: Tetromino
tetromino = {
    'surface_size':(4*PX, 4*PX),
    'surface_position':(10*PX, 4*PX)
}

arrow = {
    'surface_size':(PX,PX),
    'player_name':['A','A','A'],
    'settings_position':(8*PX, 17*PX),
    'level':1,
    'alpha_color':'pink',
    'start_position':(1,1)
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
