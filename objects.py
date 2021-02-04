from api import *

class Tetromino:
    def __init__(self, name, size, color, shape, position, debug=False):
        '''
            get a random current rotation at object creation with max rotation
            volume_shape : pixel number in one shape
        '''
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
        self.speed = 1
        self.timer_limit = 30
        self.next_slide = 30
        self.move_aside = False
        self.update = False
        self.done = False

        if debug == True:
            pass
            #self.debug_draw_all()

    def set_tuple(self, data):
        '''
            prepare a single tupple with the shape data and return it
        '''
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
        '''
            draw all shapes in text from the tuple
        '''
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
        print(self.name)
        print(self.color)
        print('position : ' + str(self.rotation))
        self.start = self.current_rotation*self.volume_shape
        for pixel in range(self.volume_shape):
            print(self.shape[self.start+pixel], end='')
            if pixel%4 == 3:
                print('')

    def draw(self, surface, grid, debug=False, clear=False):
        '''
            draw the shape on the given surface with the given rotation
            loop the self.shape built tupple using an offset with self.start
            if clear flag is True, draw the previous rotation for clearing
        '''
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
        self.update_surface = False

        if debug == True:
            pass
            #self.debug_draw()

    def slide(self, timer):
        '''
          | Use frames per seconds and speed to keep down
          | when using move 1 is the key for down
          | after a check return the nb of lines with self.move or 0
        '''
        if self.done is not True:
            self.next_slide = self.next_slide - self.speed
            if self.next_slide <= 0:
                self.next_slide = self.timer_limit
                return self.move(1)

    def move(self, direction):
        '''
          | check if next position is possible
          | if yes :
          | * save previous position
          | * uptade position
          | * play movement sound
          | * else play the blocked sound
          | 1 : DOWN = GO FASTER
          | 2 : LEFT = GO LEFT
          | 3 : RIGHT = GO RIGHT
          | 4 : SPACE & RETURN = JUMP DOWN
          | * the flag move_aside is to give priority moving aside over going down
        '''
        if self.done is not True:
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
            if direction == 4 and not self.move_aside:
                print("jump")
            self.update_surface = True

    def rotate(self):
        '''
          | check if next rotation is possible
          | if yes :
          | * save previous rotation
          | * get the next rotation
          | * play rotating sound
          | * else play the blocked sound
        '''
        self.next_rotation = (self.rotation + 1)%self.max_rotations
        self.update_surface = True

    def set_update(self):
        '''
          | if the tetromino can move, update to next position and/or rotation
          | if not, reset next datas to current datas
        '''
        if self.update == True:
            self.rotation = self.next_rotation
            self.position = self.next_position
        else:
            self.next_rotation = self.rotation
            self.next_position = self.position
        self.move_aside = False

    def check_update(self, Board):
        '''
          | check if tetromino can move and rotate, raise flag if yes
          | return nb of lines made (0 to 4) if the Tetromino can move
          | return data to Board object to update if the position is the last
          | self.update=True when tetromino can move aside or down
          | self.update=False when tetromino can't move aside
          | self.update=False and self.done=True
          |     when the tetromino can't move down, tetromion data passed
          |     to board for updating the pattern. Then get the next Tetromino.
        '''
        lt = Board.surface_position[0] #limit left
        lr = Board.surface_position[0] + Board.width #limit right
        side_collision = self.check_side_collision(lt, lr)
        board_collision = self.check_board_collision(Board)
        if board_collision[0] == True:
            self.update = False
            self.done = True
        elif side_collision == True:
            self.update = False
        else:
            self.update = True
        return board_collision[1]

    def get_side_limits(self):
        '''
          | Return left & right x coordinate of tetromino
          | c : nb of column the Tetromino size got
          | size : (c*8) : nb of column * nb of pixel by column
          | left : value of x coordinate
          | right : value of left coordinate + size of Tetromino
        '''
        c = 4
        self.offset = self.rotation*self.volume_shape
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
        '''
          | Check sides of the tetromino with board limits
          | board limits : left (lt) & right (lr)
          | ts : Tetromino size, to get collision limits
          | xl : Check the x coordinate of the tetromino left side
          | xr : Check the x coordinate of the tetromino right side
          | c : Collision flag
        '''
        ts = self.get_side_limits()
        xl, xr = ts[0], ts[1]
        c = False
        if xl <= lt or xr >= lr:
            c = True
        return c

    def check_board_collision(self,Board):
        '''
          | First we gather all the datas needed to check
          | We work with square grid of 8 pixel.
          | For the pattern :
          |   The pattern tupple, with 0 for empty square, 1 for occuped
          |   The pattern size that we store as colums and lines (in squares not pixels)
          |     The 1 added to lines is for representing the pattern floor
          |   It's top/left coordinates that we store as px_start & py_start
          |   The total of squares in the pattern (lines*columns)
          | For the tetromino we want to test :
          |   We store the correct shape using index in a variable shape
          | With those data, we build one lists :
          |   All the coordinates of the Tetromino occupied square
          | First we check if there is no square out of the pattern bottom limit
          | Then we compare those two lists with each other :
          |   If there is an identical pair, there is collision, return True
          |     The board get the coordinates of the Tetromino to update the pattern
          |     The game get the next Tetromino
          |   Else, we return False and keep going.
        '''
        collision = False
        grid = 8
        pattern = Board.pattern
        size = Board.pattern_size
        surface_position = Board.surface_position
        position = Board.pattern_position
        px_start = surface_position[0]+position[0]
        py_start = surface_position[1]+position[1]
        tx1_start = self.position[0]
        ty1_start = self.position[1]
        tx2_start = self.next_position[0]
        ty2_start = self.next_position[1]
        columns,lines = size[0],size[1]+1
        squares = lines*columns
        index1 = self.next_rotation*self.volume_shape
        index2 = self.rotation*self.volume_shape
        shape1 = self.shape[index1:index1+self.volume_shape]
        shape2 = self.shape[index2:index2+self.volume_shape]
        c = 0
        x1,y1,x2,y2 = tx1_start,ty1_start,tx2_start,ty2_start
        t1_coords = []
        t2_coords = []
        while c < len(shape1):
            if shape1[c] == 1:
                t1_coords.append((x1,y1))
            if shape2[c] == 1:
                t2_coords.append((x2,y2))
            x1 += grid
            x2 += grid
            #print(shape[c],end="")
            if (c+1)%4==0:
                #print("")
                x1 = tx1_start
                x2 = tx2_start
                y1 += grid
                y2 += grid
            c+=1
        #print("\n")
        #print(t1_coords)
        #print(t2_coords)
        #draw the pattern
        #print("\n")
        c = 0
        x,y = px_start,py_start
        new_pattern = []
        while c < squares:
            if ((x,y) in t2_coords) and pattern[c] == 1:
                #print("x",end="")
                collision = True
            if (x,y) in t1_coords:
                #print(1,end="")
                new_pattern.append(1)
            else:
                new_pattern.append(pattern[c])
                #print(pattern[c],end="")
            x += grid
            if (c+1)%columns==0:
                #print("")
                x = px_start
                y += grid
            c+=1
        #print("\n")
        #draw the pattern and tetrominos squares positions
        #print(new_pattern)
        #print("Tetromino next position:",self.next_position)
        #print("pattern lines, columns, square, x, y")
        #print(lines,columns, squares, px_start, py_start)
        if collision == True:
            return (True,tuple(new_pattern))
        else:
            return (False,None)

class Board:
    def __init__(self, data):
        self.surface_size = data['surface_size']
        self.surface_position = data['surface_position']
        self.pattern_position = data['pattern_position']
        self.width = data['surface_size'][0]
        self.height = data['surface_size'][1]
        self.pattern_size = data['pattern_size']
        self.pattern = self.set_pattern()
        self.update_surface = False

    def draw(self, surface, grid, debug=False):
        '''
            Draw the Board borders
            Draw the Board content
            Draw the Grid if debug is on
        '''
        self.draw_borders(surface, grid, 'grey')
        self.draw_pattern(surface, grid, 'white')
        self.update_surface = False

        if debug == True:
            self.draw_grid(surface,grid,'red')

    def draw_borders(self, surface, grid, color):
        rectangle(surface, (0,0,grid,self.height),color)
        rectangle(surface, (grid,self.height-grid,self.width-grid,grid),color)
        rectangle(surface, (self.width-grid,0,grid,self.height-grid),color)

    def draw_pattern(self, surface, grid, color):
        x_start = x = self.pattern_position[0]
        y = self.pattern_position[1]
        columns = self.pattern_size[0]
        lines = self.pattern_size[1]
        squares = lines*columns
        s = 0
        while s < squares:
            if self.pattern[s] == 1:
                rectangle(surface,(x,y,grid,grid),color)
            x += grid
            if (s+1) % columns == 0:
                x = x_start
                y += grid
            s += 1

    def draw_grid(self, surface, grid, color):
        for x in range(0, self.width, grid):
            for y in range(0, self.height, grid):
                line(surface,(0,y), (self.width, y), color)
                line(surface,(x,0), (x, self.height), color)

    def set_pattern(self):
        '''
          | Set an empty (0) pattern using the board size minus its borders
          | Add the last line for the floor as occupied (1)
          | Return a tuple from the list
        '''
        x = self.pattern_size[0]
        y = self.pattern_size[1]
        pattern = [0,]*(x*y)
        pattern += ([1,]*x)
        return tuple(pattern)

    def update_pattern(self, new_pattern):
        '''
          | Check if there is lines complete
          | Update Board pattern
          | Raise flag for Board update
        '''
        lines = 0
        if new_pattern is not None:
            print("update the pattern and surface update")
            self.pattern = new_pattern
            self.update_surface = True
        return lines

class Stats:
    def __init__(self, data):
        self.update_surface = False
        self.surface_size = data['surface_size']
        self.width = data['surface_size'][0]
        self.height = data['surface_size'][1]
        self.surface_position = data['surface_position']
        self.next_box = (data['position_next'],data['size_next'])
        self.stats = data['stats']

    def draw(self, surface, grid, font, debug=False):
        '''
            Draw the next tetromino box
            Draw the stats titles
            Draw the stats data
            Draw the grid if debug is on
        '''
        self.draw_next_box(surface, grid, self.next_box)
        self.draw_stats(font, surface, grid, self.stats)
        self.update_surface = False

        if debug == True:
            self.draw_grid(surface,grid,'red')

    def draw_next_box(self, surface, grid, box):
        x = box[0][0]
        y = box[0][1]
        width = box[1][0]
        height = box[1][1]
        rectangle(surface,(x,y,grid,height))
        rectangle(surface,(x,height-grid,width,grid))
        rectangle(surface,(x+width-grid,y,grid,height))

    def draw_stats(self, font, surface, grid, stats):
        for stat in stats:
            title = stat[0]
            x = stat[1][0]
            y = stat[1][1]
            write(font, surface, (x,y), title)
            variable = stat[2]
            if variable is not None:
                write(font, surface, (x,y+grid), variable, 'white')

    def draw_grid(self, surface, grid, color):
        for x in range(0, self.width, grid):
            for y in range(0, self.height, grid):
                line(surface,(0,y), (self.width, y), color)
                line(surface,(x,0), (x, self.height), color)

    def update_time(self,timer):
        pass

    def update_score(self,lines):
        if lines != 0:
            print('lines:',lines)

class Arrow:
    def __init__(self, data):
        '''
          | update surface flag
        '''
        self.update_surface = False
        self.surface_size = data['surface_size']
        self.selection = 0
        self.target = 0
        self.shape = None
        self.color = None
        self.transparent_color = 'pink'
        self.previous_position = (1,1)
        self.position = (1,1)
        self.index_max = 0

    def draw(self, surface):
        x,y = 0,0
        for i in self.shape:
            for j in i:
                if j == 1:
                    pixel(surface, (x,y), self.color)
                else:
                    pixel(surface, (x,y), self.transparent_color)
                x += 1
            y += 1
            x = 0
        self.update_surface = False

    def update_selection(self, direction):
        self.selection += direction
        if self.selection < 0:
            self.selection = self.index_max
        elif self.selection > self.index_max:
            self.selection = 0
        self.previous_position = self.position

    def move(self, key, state):
        '''
          | change position of the key
          | At game state Menu (3), arrows used to select an other game state
          | At game state New Game (4), arrows used to change settings  (name, speed)
          | keys :
          | 0 : UP
          | 1 : DOWN
          | 2 : LEFT
          | 3 : RIGHT
        '''
        if state == 3:
            if key == 0:
                self.update_selection(-1)
            elif key == 1:
                self.update_selection(1)
        elif state == 5:
            if key == 0:
                #change setting function
                print("change setting")
            elif key == 1:
                #change setting function
                print("change setting")
            elif key == 2:
                self.update_selection(-1)
            elif key == 3:
                self.update_selection(1)

    def get_data(self, content):
        '''
          | get the arrow data from current selection
          | position, color and target
        '''
        self.index_max = len(content['arrowselect']) - 1
        self.shape = content['arrowshape']
        options = content['arrowselect'][self.selection]
        self.position = options[0]
        self.color = options[1]
        self.target = options[2]
