import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import copy
import random
from matplotlib.animation import FuncAnimation

def colorFader(c1,c2,mix=0): #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)

class Cell:
    player_ID_color_map = {
        1:"red",
        2:"blue",
        3:"orange",
        4:"purple",
        5:"yellow",
    }
    
    def __init__(self, h) -> None:
        assert 0<=h
        assert h<256
        assert type(h) == int
        self.h = h
        self.player_ID = None

    def __repr__(self) -> str:
        return f"h={self.h}, player = {self.player_ID}"
    
    
    def get_color (self):

        if self.player_ID is not None:
            color = self.player_ID_color_map[self.player_ID]
        else:
            c1 = '#579C79'
            c2='#362419' #brown
            n=255
            color=colorFader(c1,c2,self.h/n)

        return mpl.colors.to_rgb(color)

class World:
    N_PLAYER = len(Cell.player_ID_color_map)
    
    def __init__(self, N) -> None:
        self.N = N
        self.map = None
        self.iteration = 0
    
    def init_turrain (self, seed = 0):
        self.map = [ [ None for x in range(self.N)] for y in range(self.N) ]
        noise = PerlinNoise(octaves=3, seed=seed)

        for y in range(self.N):
            for x in range(self.N):
                
                value = (noise([x/self.N, y/self.N])+1)*127
                value = int(value)
                value = max(value, 0)
                value = min(value, 255)
                
                self.map[y][x] = Cell( value )

    def draw(self, return_np = False):
        if self.map is None:
            assert False, "initialize turrain first using `init_turrain`"

        image = [ [ None for j in range(self.N)] for i in range(self.N) ]
        for y in range(self.N):
            for x in range(self.N):
                image[y][x] = self.map[y][x].get_color()
        
        image_np = np.stack(image)
        if return_np:
            return image_np
        fig, ax = plt.subplots(  )
        ax.imshow (image_np)
        ax.set_title(f'World at iteration: {self.iteration}')
        fig.set_size_inches(5,5)
        fig.show()
        
    
    def get_neighbors(self, x, y, use_neibors = 1):
        grid_n  = 2*use_neibors+1
        neighbors_ = [ [None for _ in range(grid_n)] for _ in range(grid_n) ]
        N = self.N
        for yn in range(y-use_neibors, y+use_neibors+1):
            for xn in range(x-use_neibors, x+use_neibors+1):
                if yn<0 or yn>=N:
                    neighbors_[yn-y+use_neibors][xn-x+use_neibors] = None
                    continue
                if xn<0 or xn>=N:
                    neighbors_[yn-y+use_neibors][xn-x+use_neibors] = None
                    continue

                neighbors_[yn-y+use_neibors][xn-x+use_neibors] = self.map[yn][xn]

        return neighbors_

    def iterate(self ):
        self.iteration+=1

        new_map = [[ None for x in range(self.N)] for y in range(self.N)]

        for y in range(self.N):
            for x in range(self.N):
                
                neighbors_ = self.get_neighbors (x, y)
                new_map[y][x] = self.state_transition(self.map[y][x], neighbors_)
        self.map = new_map


    @classmethod
    def state_transition (cls, cell: Cell, neighbors_)-> Cell:
        new_cell = copy.deepcopy(cell)
        
        # new_cell.h = cls.get_new_h(cell, neighbors_)

        new_cell.player_ID = cls.get_new_player_ID(cell, neighbors_)
        return new_cell

    @classmethod
    def get_new_h(cls, cell: Cell, neighbors_)->int:
        new_h = 0
        n = 0
        use_neibors = len(neighbors_)
        for yn in range(use_neibors):
            for nx in range(use_neibors):
                temp = neighbors_[yn][nx]
                if temp is not None:
                    new_h +=temp.h
                    n+=1
        
        return new_h//n


    @classmethod
    def get_new_player_ID(cls, cell: Cell, neighbors_)->int:
        '''
        return value:
            a new player ID of the cell. Might be stochastic in nature
        '''
        count_dict = { i+1:0 for i in range(cls.N_PLAYER)}
        count_dict[0] = 0
        IDs_list = []
        use_neibors = len(neighbors_)
        for yn in range(use_neibors):
            for nx in range(use_neibors):
                temp = neighbors_[yn][nx]
                if temp is not None:
                    id = temp.player_ID
                    if id is not None:
                        IDs_list.append(id)
                        count_dict[id] +=1
                    else: 
                        IDs_list.append(0)
                        count_dict[0] +=1
        
        for i in range(1, cls.N_PLAYER+1):
            if count_dict[i]>5:
                IDs_list.append(i)
                IDs_list.append(i)
            if count_dict[i]>4:
                IDs_list.append(i)
            if count_dict[i]>3:
                IDs_list.append(i)
        
        new_ID = random.choice(IDs_list)

        if cell.player_ID is not None:
            if new_ID == 0:
                # if new value is None, preserve it
                return cell.player_ID
        if new_ID == 0:
            return None
        return new_ID
