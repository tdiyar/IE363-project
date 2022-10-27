from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from world_old import World

world = World(30)
world.init_turrain()
world.map[2][2].player_ID = 1
world.map[27][27].player_ID = 2
world.map[2][27].player_ID = 4
world.map[27][2].player_ID = 5
world.map[15][15].player_ID = 3


figure, ax = plt.subplots()
def animation_function(i):

    image = world.draw(return_np=True)
    world.iterate()

    ax.imshow(image, cmap='gray')
    return ax
  
animation = FuncAnimation(figure,
                          func = animation_function,
                          frames = np.arange(0, 100, 0.1), 
                          interval = 10)
plt.show()
