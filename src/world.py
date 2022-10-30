import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

import copy
import random

from cell import Cell

class World:
    N_PLAYER = len(Cell.player_ID_color_map)
    
    def get_terrain(self, value):    
        if value <self.terrain_borders[0]:
            return 0
        if value <self.terrain_borders[1]:
            return 1
        if value <self.terrain_borders[2]:
            return 2
        return 3
    
    
    def __init__(self, N, terrain_borders = None) -> None:
        self.N = N

        if terrain_borders is not None:
            self.terrain_borders = terrain_borders
        else:
            self.terrain_borders = (95, 135, 155)

        self.map = None
        self.iteration = 0

    
    def init_turrain (self, octaves = 5, seed = 0):
        self.map = [ [ None for x in range(self.N)] for y in range(self.N) ]
        noise = PerlinNoise(octaves=octaves, seed=seed)

        for y in range(self.N):
            for x in range(self.N):
                
                value = (noise([x/self.N, y/self.N])+1)*127
                value = int(value)
                value = max(value, 0)
                value = min(value, 255)
                
                terrain = self.get_terrain(value)
                
                self.map[y][x] = Cell( terrain )

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

    def add_player (self, player_ID):
        while (True):
            x = random.randrange(self.N)
            y = random.randrange(self.N)
            if self.map[y][x].player_ID is None:
                if self.map[y][x].terrain == 1:
                    self.map[y][x].player_ID = player_ID
                    return 


    @classmethod
    def state_transition (cls, cell: Cell, neighbors_)-> Cell:
        new_cell = copy.deepcopy(cell)
        
        new_cell.player_ID = cls.get_new_player_ID(cell, neighbors_)
        
        return new_cell


    @classmethod
    def get_new_player_ID(cls, cell: Cell, neighbors_)->int:
        '''
        return value:
            a new player ID of the cell. Might be stochastic in nature
        '''
        if cell.terrain == 0:
            return None
        if cell.terrain == 3:
            return None

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
            if count_dict[i]>4:
                IDs_list.append(i)
        
        if cell.terrain==2:
            IDs_list.extend( [0,0,0] )
        
        new_ID = random.choice(IDs_list)
        
        if cell.terrain==2:
            if new_ID == 0:
                return None
            return new_ID
        
        if cell.player_ID is not None:
            if new_ID == 0:
                # if new value is None, preserve it
                return cell.player_ID
        if new_ID == 0:
            return None
        return new_ID
