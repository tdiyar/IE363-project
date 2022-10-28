import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

import copy
import random
from matplotlib.animation import FuncAnimation

from world import World

def main():
    world = World(100, terrain_borders = (100, 155, 185))
    world.init_turrain(octaves = 10, seed = 11)

    world.add_player(1)
    world.add_player(2)
    world.add_player(3)
    world.add_player(4)
    world.add_player(5)


    figure, ax = plt.subplots()

    # image = self.draw(return_np=True)
    # ax.imshow(image, cmap='gray')

    def animation_function(i):

        image = world.draw(return_np=True)
        world.iterate()
        ax.clear()
        ax.imshow(image, cmap='gray')
        ax.set_title(f'World at iteration: {world.iteration}')
        return ax

    animation = FuncAnimation(figure,
                            func = animation_function,
                            frames = np.arange(0, 100, 0.1), 
                            interval = 1)
    plt.show()


if __name__ == "__main__":
    main()