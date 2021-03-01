#: 1 GRID PIXEL (PX) = SIZE GRID = 8 pixel
PX = GRID = 8
NAME = 'Tetromino400'

#: SAVE
saves = {
    'file_name':'save.csv',
    'options':('name','score','lines','level','time'),
    'file_start':
                [
                 ('EGO','112','42','4','00:04:24'),
                 ('EGO','91','42','2','00:05:51'),
                 ('EGO','12','10','1','00:03:46'),
                 ('EGO','32','19','2','00:03:03'),
                 ('EGO','1','0','1','01:01:01')
                ]
}

#: SCREEN SIZE
screensizes = {
    'width':320,
    'height':240,
    'grid':GRID,
    'columns':40,
    'lines':30
}

#: COLORS DATA - PAX-24 colors
colorslist = {
    'black':(25, 16, 35), #191023
    'white':(244,245,239), #f4f5ef
    'steel':(94, 106, 130), #5e6a82
    'iron':(160, 171, 177), #a0abb1
    'silver':(200, 219, 223), #c8dbdf
    'coral':(248, 199, 164), #f8c7a4
    'pink':(231, 132, 168), #e784a8
    'magenta':(161, 70, 170), #a146aa
    'purple':(71, 67, 148), #474394
    'berry':(50, 45, 77), #322d4d
    'cyan':(133, 223, 235), #85dfeb
    'teal':(51, 156, 163), #339ca3
    'ocean':(27, 76, 90), #1b4c5a
    'blue':(114, 173, 238), #72adee
    'royal':(67, 94, 219), #435edb
    'lime':(143, 203, 98), #8fcb62
    'green':(53, 136, 78), #35884e 
    'yellow':(246, 228, 85), #f6e455
    'olive':(187, 154, 62), #bb9a3e
    'orange':(235, 157, 69), #eb9d45
    'brown':(166, 93, 53), #a65d35
    'red':(215, 77, 76), #d74d4c
    'crimson':(150, 47, 44), #962f2c
    'maroon':(104, 45, 44) #682d2c
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
            [(10*PX,4*PX),"Pax Fabrica presents", 'white'],
            [(14*PX,8*PX),"Tetromino400", 'cyan'],
            [(14*PX,10*PX),"Tetromino400", 'blue'],
            [(14*PX,12*PX),"Tetromino400", 'magenta'],
            [(14*PX,14*PX),"Tetromino400", 'lime'],
            [(14*PX,16*PX),"Tetromino400", 'orange'],
            [(14*PX,18*PX),"Tetromino400", 'yellow'],
            [(14*PX,20*PX),"Tetromino400", 'red'],
            [(18*PX,27*PX),"1983", 'iron']
        ]
    },
    'INTRO': {
        'text':[
            [(4*PX,2*PX),"WIN POINTS, GET THE BEST SCORE!", 'yellow'],
            [(2*PX,5*PX),"1 line  =  1xlvl pts  &  9 speed pts", 'purple'],
            [(2*PX,7*PX),"2 lines =  3xlvl pts  &  5 speed pts", 'magenta'],
            [(2*PX,9*PX),"3 lines =  5xlvl pts  &  3 speed pts", 'pink'],
            [(2*PX,11*PX),"4 lines =  9xlvl pts  &  1 speed pt.", 'coral'],
            [(2*PX,15*PX),"Every 100 speed points :", 'red'],
            [(3*PX,17*PX),"Jump 1 level, the speed increase !", 'orange'],
            [(8*PX,19*PX),"There is 9 speed levels.", 'orange'],
            [(14*PX,21*PX),"Playtime max is 1 hour.", 'orange'],
            [(2*PX,24*PX),"Current best Score :", 'white'],
            [(8*PX,27*PX),"*************************", 'red'],
        ]
    },
    'INPUTS': {
       'text':[
            [(3*PX,2*PX),"HOW TO PLAY, KEYBOARD and GAMEPAD", 'yellow'],
            [(15*PX,5*PX),"KEY", 'coral'],
            [(15*PX,5*PX),"   BOARD", 'pink'],
            [(2*PX,7*PX),"Use      and       keys to move.", 'white'],
            [(2*PX,7*PX),"    LEFT     RIGHT", 'lime'],
            [(2*PX,9*PX),"Use    key to rotate tetromino.", 'white'],
            [(2*PX,9*PX),"    UP", 'lime'],
            [(2*PX,11*PX),"Use       and       to go faster.", 'white'],
            [(2*PX,11*PX),"    SPACE     ENTER", 'lime'],
            [(2*PX,13*PX),"Use        to quit the game.", 'white'],
            [(2*PX,13*PX),"    ESCAPE", 'red'],
            [(15*PX,15*PX),"GAME", 'pink'],
            [(15*PX,15*PX),"    PAD", 'coral'],
            [(2*PX,17*PX),"Use      and       of D-Pad to move.", 'white'],
            [(2*PX,17*PX),"    LEFT     RIGHT", 'lime'],
            [(2*PX,19*PX),"Use    of D-Pad to rotate tetromino.", 'white'],
            [(2*PX,19*PX),"    UP", 'lime'],
            [(2*PX,21*PX),"Use         to go faster and rotate.", 'white'],
            [(2*PX,21*PX),"    BUTTONS", 'lime'],
            [(2*PX,23*PX),"Use        button to quit the game.", 'white'],
            [(2*PX,23*PX),"    SELECT", 'red'],
            [(10*PX,26*PX),"Have a good game!", 'yellow'],
            [(10*PX,27*PX),"*****************", 'red'],
       ]
    },
    'MENU': {
        'text':[
            [(14*PX,6*PX),"T",'coral'],
            [(14*PX,6*PX)," et",'pink'],
            [(14*PX,6*PX),"   ro",'magenta'],
            [(14*PX,6*PX),"     mi",'purple'],
            [(14*PX,6*PX),"       no",'magenta'],
            [(14*PX,6*PX),"         40",'pink'],
            [(14*PX,6*PX),"           0",'coral'],
            [(12*PX,12*PX),"Start a New Game",'lime'],
            [(12*PX,14*PX),"View Instructions",'white'],
            [(12*PX,16*PX),"View Highscores",'white'],
            [(12*PX,18*PX),"Exit Game",'red']
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
            [(10*PX,12*PX),'lime',GSC['NEW']],
            [(10*PX,14*PX),'white',GSC['INTRO']],
            [(10*PX,16*PX),'white',GSC['SCORE']],
            [(10*PX,18*PX),'red',GSC['EXIT']]
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
            [(2*PX,1*PX),"************************************",'yellow'],
            [(15*PX,2*PX),"HIGHSCORES",'red']
        ]
    },
    'CONFIRM': {
        'confirm': [(7*PX,12*PX),"You really want to leave ?", 'red'],
        'info': [(7*PX,14*PX),"The score will be saved.", 'iron'],
        'continue': [(7*PX,16*PX),"Press space to leave.", 'black'],
        'box': (4*GRID, 10*GRID, 32*GRID, 9*GRID)
    },
    'OVER': {
        'confirm': [(14*PX,12*PX),"GAME OVER !", 'red'],
        'info': [(4*PX,14*PX),"The score is saved.", 'iron'],
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
SAVES = saves
'''
    GLOBAL DATA
    | Prepare all the datas to use in game
'''
