import numpy as np
import matplotlib as mpl

class Cell:
    player_ID_color_map = {
        1:"red",
        2:"blue",
        3:"orange",
        4:"purple",
        5:"yellow",
    }

    TERRAIN_COLOR_DICT = {
        0:"#0892d0", #blue, river
        1:"#228b22", #green forest 
        2:"#28340A", #dark forest 
        3:"#725428", #bronw mountain
    }
    
    def __init__(self, terrain) -> None:
        assert 0<=terrain
        assert terrain<len(self.TERRAIN_COLOR_DICT)
        assert type(terrain) == int
        
        self.terrain = terrain
        self.player_ID = None
        

    def __repr__(self) -> str:
        return f"terrain={self.terrain}, player = {self.player_ID}"
    
    def get_color (self):

        if self.player_ID is not None:
            color = self.player_ID_color_map[self.player_ID]
        else:
            color = self.TERRAIN_COLOR_DICT[self.terrain]

        return mpl.colors.to_rgb(color)
