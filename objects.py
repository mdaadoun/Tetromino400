# objects.py
from string import ascii_uppercase as alphabet
from api import *
import math
from random import randint

class Tetromino:
    def __init__(self, name, size, color, shape, position, debug=False):
        """
        | Next : The next tetromino object
        | surface_size : Size of the tetromino surface
        | name : Tetromino name (I, L, J, T, O, I, S, Z)
        | color : Tetromino color
        | alpha : The alpha color for transparency
        | max_rotations : the number of rotation this tetromino have
        | next_rotation : the rotation to check
        | rotation : the current tetromino rotation
        | next_position : the position to check
        | position : the current position
        | volume_shape : pixel number in one shape
        | update_surface : drawing the surface flag
        | speed_level : the level to use with speed
        | timer_limit : max time reference
        | next_slide_timer : counter before next tetromino move down
        | move_aside : Flag to signal tetromino is moving aside from input
        |    which is priority over moving down
        | update : Flag that need to be True for next_position and next_rotation
        |    to become the current position and rotation
        | done : The tetromino is on the board floor, cannot move anymore
        | game_over : global flag to signal the game is finished
        | last_input : the last user input used
        | jumping : flag to control speed of the tetromino
        """
        self.Next = None
        self.surface_size = size
        self.name = name
        self.color = color
        self.alpha = 'pink'
        self.shape = self.set_tuple(shape)
        self.max_rotations = len(shape)
        self.next_rotation = 0
        self.rotation = 0
        self.next_position = position
        self.position = position
        self.volume_shape = 16
        self.update_surface = False
        self.speed_level = 0
        self.timer_limit = 30
        self.next_slide_timer = 30
        self.move_aside = False
        self.update = False
        self.done = False
        self.game_over = False
        self.last_input = None
        self.jumping = False

        if debug == True:
            pass
            #self.debug_draw_all()

    def set_tuple(self, data):
        """
        | prepare a single tupple with the shape data and return it
        """
        shapelist = []
        for shape in data:
            for line in range(4):
                for pixel in range(4):
                    try:
                        if shape[line][pixel] == 1:
                            shapelist.append(1)
                        else:
                            shapelist.append(0)
                    except IndexError:
                        shapelist.append(0)
        shapetuple = tuple(shapelist)
        return shapetuple

    def debug_draw_all(self):
        """
        | DEBUG : draw all shapes in text console from the tuple
        """
        print(self.name)
        print(self.color)
        for rotation in range(self.max_rotations):
            self.start = rotation*self.volume_shape
            for pixel in range(self.volume_shape):
                print(self.shape[self.start+pixel], end='')
                if pixel%4 == 3:
                    print('')
            print('****')

    def debug_draw(self):
        """
        | DEBUG : draw the current tetromino shape in text console
        """
        print(self.name)
        print(self.color)
        print('position : ' + str(self.rotation))
        self.start = self.current_rotation*self.volume_shape
        for pixel in range(self.volume_shape):
            print(self.shape[self.start+pixel], end='')
            if pixel%4 == 3:
                print('')

    def draw(self, surface, grid, debug=False, clear=False):
        """
        | draw the shape on the given surface with the given rotation
        | loop the self.shape built tupple using an offset with self.start
        | if clear flag is True, draw the previous rotation for clearing
        """
        if self.done is not True:
            if clear:
                color='black'
            else:
                color = self.color
            self.start = self.rotation*self.volume_shape
            x, y = 0,0
            for pixel in range(self.volume_shape):
                if self.shape[self.start+pixel] == 1:
                    rectangle(surface,(x*grid,y*grid,grid,grid),color)
                else:
                    rectangle(surface,(x*grid,y*grid,grid,grid),self.alpha)
                x += 1
                if pixel%4 == 3:
                    y += 1
                    x = 0

        if debug == True:
            pass
            #self.debug_draw()

    def slide(self, timer):
        """
        | Use frames per seconds and speed level to decrease timer
        | when timer is 0
        |   reset the slide timer
        |   return move with input 1 to move down
        """
        if self.done is not True:
            self.next_slide_timer = self.next_slide_timer - self.speed_level
            if self.next_slide_timer <= 0 or self.jumping == True:
                self.next_slide_timer = self.timer_limit
                return self.move(1)

    def move(self, direction):
        """
        | uptade next_position for checking
        | 1 : DOWN = GO FASTER
        | 2 : LEFT = GO LEFT
        | 3 : RIGHT = GO RIGHT
        """
        if self.done is not True and self.last_input == None:
            p = self.position
            x,y = p[0],p[1]
            grid = 8
            if direction == 1 and not self.move_aside:
                self.next_position = (x, y+grid)
            if direction == 2:
                self.move_aside = True
                self.next_position = (x-grid, y)
            if direction == 3:
                self.move_aside = True
                self.next_position = (x+grid, y)
            self.last_input = direction
            self.update_surface = True

    def rotate(self):
        """
        | get the next rotation to check
        """
        if self.done is not True and self.last_input == None:
            self.next_rotation = (self.rotation + 1)%self.max_rotations
            self.last_input = 0
            self.update_surface = True

    def jump(self):
        """
        | switch flag to remove slide timer
        """
        if self.done is not True and self.last_input == None:
            self.jumping = True

    def set_update(self):
        """
        | if update flag is True
        |   update current position/rotation with  next position and rotation
        | if not, reset next datas to current datas
        | the reset to False of move_aside is to give back control to sliding down
        """
        if self.update == True:
            self.rotation = self.next_rotation
            self.position = self.next_position
        else:
            self.next_rotation = self.rotation
            self.next_position = self.position
        self.move_aside = False

    def check_update(self, Board, SOUNDS):
        """
        | prepare data for collision checking :
        |   lt & lr : are the limit left and right of the board
        | Check side collision, if true, the tetromino position is not updated
        | Check pattern collision to check contact aside or bottom of the tetromino
        | the self.position[1] <= 32 is to check if the tetromino
        | is not going out of board, if yes, it is game over
        | Play sound related to player input and result
        | return the new pattern for updating the game
        """
        lt = Board.surface_position[0]
        lr = Board.surface_position[0] + Board.width
        side_collision = self.check_side_collision(lt, lr)
        results = self.check_pattern_collision(Board)
        new_pattern = results[1]
        ltinput = self.last_input
        if side_collision == True or results[0] == True:
            if ltinput in [2,3]:
                pygame.mixer.Sound.play(SOUNDS['blocked'])
            self.update = False
        elif new_pattern is not None:
            pygame.mixer.Sound.play(SOUNDS['done'])
            self.update = False
            self.done = True
            self.jumping = False
            if self.position[1] <= 32:
                self.game_over = True
        else:
            if ltinput in [2,3]:
                pygame.mixer.Sound.play(SOUNDS['move'])
            if ltinput == 0:
                pygame.mixer.Sound.play(SOUNDS['rotate'])
            self.update = True
        self.last_input = None
        self.update_surface = False
        return new_pattern

    def get_side_limits(self):
        """
        | Return left & right x coordinate of tetromino
        | c : index to count the column number Tetromino size got
        | size : (c*8) : nb of column * nb of pixel by column
        | left : value of x coordinate
        | right : value of left coordinate + size of Tetromino
        """
        c = 4
        self.offset = self.next_rotation*self.volume_shape
        check = True
        while check == True:
            for block in range(c-1,self.volume_shape,4):
                if self.shape[self.offset+block] == 1:
                    check = False
            if check == True:
                c -= 1
                if c == 0:
                    check = False
        size = c*8
        left = self.next_position[0]
        right = left + size
        return (left,right)

    def check_side_collision(self,lt,lr):
        """
        | Check sides of the tetromino with board limits
        | board limits : left (lt) & right (lr)
        | ts : Tetromino size, to get collision limits
        | xl : Check the x coordinate of the tetromino left side
        | xr : Check the x coordinate of the tetromino right side
        | c : Collision flag
        | In the special case of the I Tetromino, the rotation is made
        |  possible when close to the right limit by moving its left coordinates
        """
        ts = self.get_side_limits()
        xl, xr = ts[0], ts[1]
        c = False
        if xl <= lt or xr >= lr:
            c = True
            if self.name == 'I':
                if (xl == 104 or xl == 112):
                    self.next_position = (96,self.next_position[1])
                    c = False
        return c

    def get_pattern_data(self,Board):
        """
        | Build a dictionnary with the pattern data necessary for checking
        | Shape : The pattern tupple, with 0 for empty square, 1 for occuped
        | Size :  The pattern size that we store (in squares not pixels)
        | Columns and lines is equal to sizes length and height
        | Squares numbers :  The total of squares in the pattern (lines*columns)
        | Lines :  The 1 added to lines is for representing the pattern floor
        | The top/left coordinates that we store as position x & y
        """
        pattern = {}
        pattern['shape'] = Board.pattern
        pattern['size'] = ps  = Board.pattern_size
        columns, lines = ps[0], ps[1]+1
        pattern['squares_number'] = lines*columns
        pattern_surface_position = Board.surface_position
        pattern_position = Board.pattern_position
        pattern['position_x'] = pattern_surface_position[0]+pattern_position[0]
        pattern['position_y'] = pattern_surface_position[1]+pattern_position[1]
        return pattern

    def get_tetrominos_data(self):
        """
        | Build a dictionnary of two dictionnaries with
        | the current & next tetrominos data necessary for checking
        | We store the positions top/left of the surface as x & y
        | We store the correct shape using rotation index as an offset
        """
        tetromino = {'current':{},'next':{}}
        tetromino['current']['position_x'] = self.position[0]
        tetromino['current']['position_y'] = self.position[1]
        tetromino['next']['position_x'] = self.next_position[0]
        tetromino['next']['position_y'] = self.next_position[1]
        index1 = self.next_rotation*self.volume_shape
        index2 = self.rotation*self.volume_shape
        tetromino['next']['shape'] = self.shape[index1:index1+self.volume_shape]
        tetromino['current']['shape'] = self.shape[index2:index2+self.volume_shape]
        return tetromino

    def get_tetromino_squares_coordinates(self, tetromino):
        """
        | Get the coordinates of all the occupied squares
        | of a given tetromino.
        """
        grid = 8
        x = xstart = tetromino['position_x']
        y = tetromino['position_y']
        squares_coordinates = []
        for i, square in enumerate(tetromino['shape'], 1):
            if square == 1:
                squares_coordinates.append((x,y))
            x += grid
            if i % 4 == 0:
                x = xstart
                y += grid
        return squares_coordinates

    def get_squares_collision(self, pattern, next_positions):
        """
        | Check if square of tetromino and pattern collide
        |    if collide to the bottom, input(1,4) return 1
        |    if collide to the side or in rotation, input(0,2,3) return 2
        |    else return None
        """
        grid = 8
        columns = pattern['size'][0]
        x = xstart = pattern['position_x']
        y = pattern['position_y']
        collide = None
        for i in range(pattern['squares_number']):
            if pattern['shape'][i] == 1 and (x,y) in next_positions:
                if self.last_input in [1, 4]:
                    collide = 1
                else:
                    collide = 2
            x += grid
            if (i+1)%columns == 0:
                x = xstart
                y += grid
        return collide

    def build_new_pattern(self, pattern, current_positions):
        """
        | Build a new pattern by adding the current tetromino
        | To the current pattern.
        """
        grid = 8
        columns = pattern['size'][0]
        x = xstart = pattern['position_x']
        y = pattern['position_y']
        new_pattern = []
        for i in range(pattern['squares_number']):
            if (x,y) in current_positions:
                new_pattern.append(1)
            else:
                new_pattern.append(pattern['shape'][i])
            x += grid
            if (i+1)%columns == 0:
                x = xstart
                y += grid
        return tuple(new_pattern)

    def debug_draw_tetrominos_and_pattern(self, pattern, next_positions):
        print("debug")

    def check_pattern_collision(self,Board):
        """
        | First we gather all the datas needed to check
        |    get_pattern_datas for the pattern
        |    get_tetrominos_datas for the tetrominos
        | We then get the coordinates of all the squares from current and next tetromino
        | We use the next coordinates to check collision
        | In the case of a collision, we use the current coordinates to update the pattern
        | Return a first flag True if there is a side collision without pattern update
        | Return a second flag None if there is no collision (no pattern to update)
        """
        pattern = self.get_pattern_data(Board)
        tetrominos = self.get_tetrominos_data()
        coordinates = []
        for i, t in enumerate(tetrominos):
            coordinates.append(self.get_tetromino_squares_coordinates(tetrominos[t]))
        current_coordinates = coordinates[0]
        next_coordinates = coordinates[1]
        collision = self.get_squares_collision(pattern, next_coordinates)
        #self.debug_draw_tetrominos_and_pattern(pattern, next_coordinates)
        if collision == 1:
            new_pattern = self.build_new_pattern(pattern, current_coordinates)
            return [False, new_pattern]
        elif collision == 2:
            return [True, None]
        else:
            return [False, None]

class Board:
    def __init__(self, data):
        """
        | surface_size : size of the board surface
        | surface_position : position of the board surface
        | pattern_position : position of the pattern
        | width : width of the surface
        | height : height of the surface
        | pattern_size : size of the pattern
        | pattern : tuple with all the squares
        | update_surface : flag to draw the board
        """
        self.surface_size = data['surface_size']
        self.surface_position = data['surface_position']
        self.pattern_position = data['pattern_position']
        self.width = data['surface_size'][0]
        self.height = data['surface_size'][1]
        self.pattern_size = data['pattern_size']
        self.pattern = self.set_pattern()
        self.update_surface = False

    def draw(self, surface, grid, debug=False):
        """
        | Draw the Board borders
        | Draw the Board content (pattern)
        | Draw the Grid if debug is on
        """
        self.draw_borders(surface, grid, 'iron')
        self.draw_pattern(surface, grid, 'white')
        self.update_surface = False

        if debug == True:
            self.debug_draw_grid(surface,grid,'red')

    def draw_borders(self, surface, grid, color):
        """
        | draw the Board surface borders
        """
        rectangle(surface, (0,0,grid,self.height),color)
        rectangle(surface, (grid,self.height-grid,self.width-grid,grid),color)
        rectangle(surface, (self.width-grid,0,grid,self.height-grid),color)

    def draw_pattern(self, surface, grid, color):
        """
        | Draw the game pattern on the Board surface
        """
        x_start = x = self.pattern_position[0]
        y = self.pattern_position[1]
        columns = self.pattern_size[0]
        lines = self.pattern_size[1]
        squares = lines*columns
        s = 0
        while s < squares:
            if self.pattern[s] == 1:
                rectangle(surface,(x,y,grid,grid),color)
            else:
                rectangle(surface,(x,y,grid,grid),'black')
            x += grid
            if (s+1) % columns == 0:
                x = x_start
                y += grid
            s += 1

    def debug_draw_grid(self, surface, grid, color):
        for x in range(0, self.width, grid):
            for y in range(0, self.height, grid):
                line(surface,(0,y), (self.width, y), color)
                line(surface,(x,0), (x, self.height), color)

    def set_pattern(self):
        """
        | Set an empty (0) pattern using the board size minus its borders
        | Add the last line for the floor as occupied (1)
        | Return a tuple from the list
        """
        x = self.pattern_size[0]
        y = self.pattern_size[1]
        pattern = [0,]*(x*y)
        pattern += ([1,]*x)
        return tuple(pattern)

    def update_pattern(self, new_pattern):
        """
        | Check if there is lines complete
        | Update Board pattern
        | Raise flag for Board update
        """
        lines = 0
        if new_pattern is not None:
            check = self.check_pattern(new_pattern)
            lines = check[0]
            self.pattern = check[1]
            self.update_surface = True
        return lines

    def check_pattern(self,pattern):
        """
        | check from bottom up if line are completed (full line of 1)
        | Lines start at -1 to take into account the floor line of the pattern
        | if yes, increments lines numbers and return it
        | Add removed lines as new lines of 0 at the top of pattern
        | return the new pattern removed from the completed lines
        """
        lines = -1
        line_length = self.pattern_size[0]
        new_pattern = []
        check_line = []
        index = len(pattern) - 1
        while index >= 0:
            check_line.append(pattern[index])
            if (index) % line_length == 0:
                if check_line[0] == 1 and len(set(check_line)) == 1:
                    lines += 1
                else:
                    new_pattern = check_line[::-1] + new_pattern
                check_line = []
            index -= 1
        c = lines
        while c > 0:
            c -= 1
            new_pattern = [0,]*line_length + new_pattern
        new_pattern += ([1,]*line_length)
        return [lines,tuple(new_pattern)]

class Stats:
    def __init__(self, data):
        """
        | update_surface : the flag to draw the Stats surface
        | surface_size : the size of the Stats surface
        | width : widht of the Stats surface
        | height : height of the Stats surface
        | surface_position : position of the Stats surface
        | next_box : position and size to draw next tetromino on Stats surface
        | next_shape : shape of the next tetromino
        | next_color : color of the next tetromino
        | stats_titles : the differents heades of the Stats to display
        | stats : the game stats as a dictionnary
        | score : score point of current game
        | speed_points : speed points of current game
        | level : the level of the current game
        | lines : numbers of lines completed on the current game
        | time : timer of the current game
        | name_position : position to where to display player name
        | suffix : text to add after the name
        | name : player name of the current game
        | game_over : flag to signal if the game is completed
        """
        self.update_surface = False
        self.surface_size = data['surface_size']
        self.width = data['surface_size'][0]
        self.height = data['surface_size'][1]
        self.surface_position = data['surface_position']
        self.next_box = (data['position_next'],data['size_next'])
        self.next_shape = None
        self.next_color = None
        self.stats_titles = data['stats']
        self.stats = {}
        self.score = 0
        self.speed_points = 0
        self.level = 1
        self.lines = 0
        self.time = 0
        self.name_position = data['name_position']
        self.suffix = data['name_suffix']
        self.name = 'AAA'
        self.game_over = False

    def draw(self, surface, grid, font, debug=False):
        """
        | Draw the next tetromino box
        | Draw the stats headers and datas
        | Draw the grid if debug is on
        """
        clear(surface,'black')
        self.draw_next_tetromino(surface, grid, self.next_box)
        self.draw_stats(font, surface, grid, self.stats_titles)
        self.update_surface = False

        if debug == True:
            self.debug_draw_grid(surface,grid,'red')

    def draw_next_tetromino(self, surface, grid, box):
        """
        | draw the borders of the next tetromino box
        | draw the tetromino inside it, square by square
        """
        x = box[0][0]
        y = box[0][1]
        width = box[1][0]
        height = box[1][1]
        rectangle(surface,(x,y,grid,height))
        rectangle(surface,(x,height-grid,width,grid))
        rectangle(surface,(x+width-grid,y,grid,height))
        x_start = x = x + 3*grid
        y = y + 2*grid
        squares = 4*4
        c = 0
        while c < squares:
            if self.next_shape[c] == 1:
                rectangle(surface,(x,y,grid,grid),self.next_color)
            x += grid
            if (c+1)%4 == 0:
                y += grid
                x = x_start
            c+=1

    def draw_stats(self, font, surface, grid, titles):
        """
        | first get the global stats in a dictionnary
        | then draw each stat according to it's header
        """
        stats = self.prepare_stats()
        for data in titles:
            title = data[0]
            x = data[1][0]
            y = data[1][1]
            write(font, surface, (x,y), title)
            if stats[title] is not None:
                write(font, surface, (x,y+grid), stats[title], 'white')

    def prepare_stats(self):
        """
        | prepare dictionnary with the correct stats converted as string
        """
        self.stats['NEXT'] = None
        self.stats['LINES'] = str(self.lines)
        self.stats['SCORE'] = str(self.score)
        self.stats['SPEED'] = str(self.speed_points) + "/100"
        self.stats['LEVEL'] = str(self.level)
        self.stats['TIME'] = set_time_string(self.time)
        return self.stats

    def debug_draw_grid(self, surface, grid, color):
        for x in range(0, self.width, grid):
            for y in range(0, self.height, grid):
                line(surface,(0,y), (self.width, y), color)
                line(surface,(x,0), (x, self.height), color)

    def update_time(self,timer):
        """
        | Get the seconds from game ticks and up timer every 1 sec
        """
        t = math.ceil(timer/1000)
        t = t-1
        if t  != self.time:
            self.check_time(t)
            self.time = t
            self.update_surface = True

    def update_score(self,lines, SOUNDS):
        """
        | Calculate the correct score according to the number of line completed
        | Play the related sound (random sound for line4)
        """
        self.lines += lines
        if lines == 1:
            pygame.mixer.Sound.play(SOUNDS['line1'])
            self.score += 1 * self.level
            self.speed_points += 10
        if lines == 2:
            pygame.mixer.Sound.play(SOUNDS['line2'])
            self.score += 3 * self.level
            self.speed_points += 5
        if lines == 3:
            pygame.mixer.Sound.play(SOUNDS['line3'])
            self.score += 5 * self.level
            self.speed_points += 3
        if lines == 4:
            rndsnd = randint(0, 2)
            pygame.mixer.Sound.play(SOUNDS['lines4'][rndsnd])
            self.score += 10 * self.level
            self.speed_points += 1

    def check_level(self,SOUNDS):
        """
        | Check if the level reach 100, if yes
        | Check if the level is not the last (level 9 + >100 speed points)
        | jump to next level, set speed points with remaining points
        """
        sp = self.speed_points
        if sp//100 >= 1:
            if self.level == 9 and sp >= 100:
                self.game_over = True
                self.speed_points = 100
            else:
                pygame.mixer.Sound.play(SOUNDS['levelup'])
                pygame.mixer.music.play()
                self.level += 1
                r = sp%100
                self.speed_points = r

    def check_time(self,secondes):
        """
        | check if time is not 1hour, 1min and 1sec else, game over
        """
        if secondes == 3661:
            self.game_over = True

class Arrow:
    def __init__(self, data):
        """
        | update_surface : flag to draw the arrow surface
        | surface_size : the size of the arrow surface
        | selection : the current arrow selected option
        | target : the game_state the arrow have selected
        | index_max : the maximum of options arrow can select
        | shape : the shape of the arrow as a binary tuple
        | color : the arrow color
        | alpha : the transparent color chosen
        | previous_position : previous surface position used for cleaning
        | position : current surface position of arrow
        | update_settings : flag to signal an option have been modified
        | settings_position : the options data position for drawing
        | level : the data for the level setting
        | name : the data for the name setting
        """
        self.update_surface = False
        self.surface_size = data['surface_size']
        self.selection = 0
        self.target = 0
        self.index_max = 0
        self.shape = None
        self.color = None
        self.alpha = data['alpha_color']
        self.previous_position = data['start_position']
        self.position = data['start_position']
        self.update_settings = True
        self.settings_position = data['settings_position']
        self.level = data['level']
        self.name = data['player_name']

    def draw(self, surface):
        """
        | Draw arrow on the surface
        """
        x,y = 0,0
        for i in self.shape:
            for j in i:
                if j == 1:
                    pixel(surface, (x,y), self.color)
                else:
                    pixel(surface, (x,y), self.alpha)
                x += 1
            y += 1
            x = 0
        self.update_surface = False

    def draw_settings(self, surface, grid, font):
        """
        | Draw the settings, erase with a black rectangle, write text
        """
        x = self.settings_position[0]
        y = self.settings_position[1]
        lvl = str(self.level)
        for l in self.name:
            rectangle(surface,(x,y,grid,grid),'black')
            write(font, surface, (x,y), l, 'white')
            x += 2*grid
        x += 6*grid
        rectangle(surface,(x,y,grid,grid),'black')
        write(font, surface, (x,y), lvl, 'white')
        self.update_settings = False

    def update_selection(self, direction):
        """
        | Change arrow selection inside a range between 0 and index_max
        """
        self.selection += direction
        if self.selection < 0:
            self.selection = self.index_max
        elif self.selection > self.index_max:
            self.selection = 0
        self.previous_position = self.position

    def move(self, key, state):
        """
        | change position or behavior depending the game state and input key
        | At game state Menu (3), arrows used to select an other game state
        | At game state New Game (4), arrows used to change settings  (name, speed)
        | keys :
        | 0 : UP
        | 1 : DOWN
        | 2 : LEFT
        | 3 : RIGHT
        | Add a update_surface when noted a bug with gamepad in moving arrow
        """
        if self.update_surface == False:
            if state == 3:
                if key == 0:
                    self.update_selection(-1)
                elif key == 1:
                    self.update_selection(1)
            elif state == 5:
                if key == 0:
                    self.update_setting(1)
                elif key == 1:
                    self.update_setting(-1)
                elif key == 2:
                    self.update_selection(-1)
                elif key == 3:
                    self.update_selection(1)

    def update_setting(self, direction):
        """
        | Check if the input is up or down
        | if the selection is level : up/down of 1 the level
        | if the selection is a letter from the name : get next letter from alphabet
        | raise the flag to draw settings on main surface
        """
        if direction == 1:
            if self.selection == 3:
                if self.level < 9:
                    self.level += 1
                else:
                    self.level = 1
            else:
                letter = self.name[self.selection]
                next_letter = self.get_next_letter(letter, direction)
                self.name[self.selection] = next_letter
        elif direction == -1:
            if self.selection == 3:
                if self.level > 1:
                    self.level -= 1
                else:
                    self.level = 9
            else:
                letter = self.name[self.selection]
                next_letter = self.get_next_letter(letter, direction)
                self.name[self.selection] = next_letter
        self.update_settings = True

    def get_next_letter(self, letter, direction):
        """
        | Get a letter_list from the python string alphabet = ascii_uppercase
        | Retrieve the list index of the current letter
        | Change the index with the direction and check for limits
        | modify the index to retrieve the corresponding letter if selection outbounds
        | Return the new letter
        """
        letter_list = list(alphabet)
        index = letter_list.index(letter)
        index = index + direction
        max_index = len(letter_list) - 1
        if index < 0:
            index = max_index
        elif index > max_index:
            index = 0
        return letter_list[index]

    def get_data(self, content):
        """
        | get the arrow data from current selection
        | position, color and target
        """
        self.index_max = len(content['arrowselect']) - 1
        self.shape = content['arrowshape']
        options = content['arrowselect'][self.selection]
        self.position = options[0]
        self.color = options[1]
        self.target = options[2]
