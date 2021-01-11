from api import *

class Tetromino:

    def __init__(self, name, data, debug=False):
        '''
            get a random current rotation at object creation with max rotation
            volume_shape : pixel number in one shape
        '''
        self.name = name
        self.color = data['color']
        self.shape = self.prepare_shape_data_as_one_tuple(data['shape'])
        self.max_rotations = len(data['shape'])
        self.current_rotation = 0
        self.current_top_left_position = (0,0)
        self.bottom_check = 0
        self.right_check = 0
        self.volume_shape = 16
        self.update_surface = True
        self.position = (0,0)

        if debug == True:
            self.debug_draw_all()

    def prepare_shape_data_as_one_tuple(self, data):
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
        print('position : ' + str(self.current_rotation))
        self.start = self.current_rotation*self.volume_shape
        for pixel in range(self.volume_shape):
            print(self.shape[self.start+pixel], end='')
            if pixel%4 == 3:
                print('')

    def draw(self, surface, grid, debug=False):
        '''
            draw the shape of the current rotation
        '''
        if debug == True:
            self.debug_draw()

    def move(self, key):
        '''
            movement
            play movement sound
        '''
        pass

    def rotate(self, rotation):
        '''
            rotation clockwise(cw) or anticlockwise(acw), get the correct
            play rotating sound
        '''
        if rotation == 'cw':
            self.current_rotation = (self.current_rotation + 1)%self.max_rotations
        elif rotation == 'acw':
            self.current_rotation = (self.current_rotation - 1)%self.max_rotations
        else:
            print('can only be clockwise(cw) or anticlockwise(acw).')

    def check_next_position(self, next_position):
        '''
            return True if the Tetromino can move
        '''
        pass

class Board:
    def __init__(self, data):
        self.width = data['surface_size'][0]
        self.height = data['surface_size'][1]
        self.update_surface = True

    def draw(self, surface, grid, color='grey', debug=False):
        '''
            Draw the Board borders
            Draw the Board content
            Draw the Grid if debug is on
        '''
        self.draw_borders(surface, grid, color='grey')

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
        self.update_surface = True
        self.next_box = (data['position_next'],data['size_next'])
        self.stats = data['stats']

    def draw(self, surface, grid, next_tetromino, font, debug=False):
        '''
            Draw the next tetromino box
            Draw the next tetromino in the box
            Draw the stats titles
            Draw the stats data
            Draw the grid if debug is on
        '''
        self.draw_next_box(surface, grid, self.next_box)
        self.draw_next_tetromino(surface, grid, next_tetromino)
        self.draw_stats(font, surface, grid, self.stats)

        if debug == True:
            self.debug_draw_grid(surface, grid, color='red')

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

    def draw_next_tetromino(self, surface, grid, tetromino):
        print('next tetromino:', tetromino)

    def debug_draw_grid(self, surface, grid, color):
        print('draw stats debug grid', surface, grid, color)
