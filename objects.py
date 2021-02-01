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
        self.bottom_check = 0
        self.right_check = 0
        self.volume_shape = 16
        self.update_surface = False
        self.speed = 1
        self.timer_limit = 30
        self.next_slide = 30
        self.last_slide = 0
        self.move_aside = False

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
          | after a check return the nb of lines mades
        '''
        self.next_slide = self.next_slide - self.speed
        if self.next_slide <= 0:
            self.last_slide = timer
            self.next_slide = self.timer_limit
            self.move(1)

        lines = 0 #retun the lines built
        return lines

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

    def update(self):
        self.rotation = self.next_rotation
        self.position = self.next_position
        self.move_aside = False

    def check_next_position(self):
        '''
            return True if the Tetromino can move
        '''
        pass

class Board:
    def __init__(self, data):
        self.surface_size = data['surface_size']
        self.surface_position = data['surface_position']
        self.width = data['surface_size'][0]
        self.height = data['surface_size'][1]
        self.update_surface = False

    def draw(self, surface, grid, debug=False):
        '''
            Draw the Board borders
            Draw the Board content
            Draw the Grid if debug is on
        '''
        self.draw_borders(surface, grid, 'grey')
        self.update_surface = False

        if debug == True:
            self.draw_grid(surface,grid,'red')

    def draw_borders(self, surface, grid, color):
        rectangle(surface, (0,0,grid,self.height),color)
        rectangle(surface, (grid,self.height-grid,self.width-grid,grid),color)
        rectangle(surface, (self.width-grid,0,grid,self.height-grid),color)

    def draw_grid(self, surface, grid, color):
        for x in range(0, self.width, grid):
            for y in range(0, self.height, grid):
                line(surface,(0,y), (self.width, y), color)
                line(surface,(x,0), (x, self.height), color)

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
        pass

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
