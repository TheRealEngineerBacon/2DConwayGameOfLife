import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import matplotlib.animation as animation
from numba import njit

sim_steps = 200
dimensions = 150
border = 10

#SETUP STAGE
#Create array which includes a 3rd dimensions to save each tick.
array_0 = np.ndarray((dimensions, dimensions, sim_steps), dtype=np.int8)

#Create random allocation of 0 and 1 states across first tick of simulation.
for y in range(border, dimensions-border):
    for x in range(border, dimensions-border):
        array_0[y, x, 0] = np.random.randint(0, 2)

@njit
def summation(y, x, i):
    alive_count = 0
    if (x > 0 and x < dimensions-1) and (y > 0 and y < dimensions-1):
        # sum = (array_0[y-1, x-1, i] + array_0[y-1, x, i] + array_0[y-1, x+1, i]
        #         + array_0[y, x-1, i] + array_0[y, x+1, i] + array_0[y+1, x-1, i]
        #         + array_0[y+1, x, i] + array_0[y+1, x+1, i])
        alive_count = np.sum(array_0[y-1:y+2, x-1:x+2, i])
        if array_0[y, x, i] == 1:
            return alive_count-1
        else:
            return alive_count
        
    elif y == 0 and x == 0:
        alive_count = (array_0[y, x+1, i] + array_0[y+1, x, i] + array_0[y+1, x+1, i]
                + array_0[dimensions-1, dimensions-1, i] + array_0[dimensions-1, x, i]
                + array_0[dimensions-1, x+1, i] + array_0[y, dimensions-1, i]
                + array_0[y+1, dimensions-1, i])
        return alive_count
    elif y == 0 and (x > 0 and x < dimensions-1):
        alive_count = (array_0[y, x-1, i] + array_0[y, x+1, i] + array_0[y+1, x-1, i] 
                + array_0[y+1, x, i] + array_0[y+1, x+1, i]
                + array_0[dimensions-1, x-1, i] + array_0[dimensions-1, x, i]
                + array_0[dimensions-1, x+1, i])
        return alive_count
    elif y == 0 and x == dimensions-1:
        alive_count = (array_0[y, x-1, i] + array_0[y+1, x-1, i] + array_0[y+1, x, i]
               + array_0[dimensions-1, 0, i] + array_0[dimensions-1, dimensions-1, i]
               + array_0[dimensions-1, dimensions-2, i] + array_0[y, 0, i]
               + array_0[y+1, 0, i])
        return alive_count
    elif (y > 0 and y < dimensions-1) and x == dimensions-1:
        alive_count = (array_0[y-1, x-1, i] + array_0[y-1, x, i] + array_0[y, x-1, i]
                + array_0[y+1, x-1, i] + array_0[y+1, x, i] + array_0[y-1, 0, i]
                + array_0[y, 0, i] + array_0[y+1, 0, i])
        return alive_count
    elif y == dimensions-1 and x == dimensions-1:
        alive_count = (array_0[y-1, x-1, i] + array_0[y-1, x, i] + array_0[y, x-1, i]
               + array_0[0, 0, i] + array_0[y-1, 0, i] + array_0[y, 0, i]
               + array_0[0, x-1, i] + array_0[0, x, i])
        return alive_count
    elif y == dimensions-1 and (x > 0 and x < dimensions-1):
        alive_count = (array_0[y-1, x-1, i] + array_0[y-1, x, i] + array_0[y-1, x+1, i]
                + array_0[y, x-1, i] + array_0[y, x+1, i] + array_0[0, x-1, i]
                + array_0[0, x, i] + array_0[0, x+1, i])
        return alive_count
    elif y == dimensions-1 and x == 0:
        alive_count = (array_0[y-1, x, i] + array_0[y-1, x+1, i] + array_0[y, x+1, i]
               + array_0[0, dimensions-1, i] + array_0[y, dimensions-1, i]
               + array_0[y-1, dimensions-1, i] + array_0[0, x, i]
               + array_0[0, x+1, i])
        return alive_count
    elif (y > 0 and y < dimensions-1) and x == 0:
        alive_count = (array_0[y-1, x, i] + array_0[y-1, x+1, i] + array_0[y, x+1, i]
                + array_0[y+1, x, i] + array_0[y+1, x+1, i] + array_0[y-1, dimensions-1, i]
                + array_0[y, dimensions-1, i] + array_0[y+1, dimensions-1, i])
        return alive_count
    
entropylist = [0]
for i in range(1, sim_steps):
    entropy = 0
    for y in range(0, dimensions):
        for x in range(0, dimensions):
            if array_0[y, x, i-1] == 0:
                if summation(y, x, i-1) == 3:
                    array_0[y, x, i] = 1
                    entropy += 1
                else:
                    array_0[y, x, i] = 0
            elif array_0[y, x, i-1] == 1:
                if summation(y, x, i-1) < 2 or summation(y, x, i-1) > 3:
                    array_0[y, x, i] = 0
                    entropy += 1
                elif summation(y, x, i-1) == 2 or summation(y, x, i-1) == 3:
                    array_0[y, x, i] = 1
            else:
                print(f"Error in computation[{y, x, i}]: Review conditions.")
    entropylist.append(entropy)
    print(i, entropy)


# for frames in range(0, sim_steps):
#     # fig1 = plt.figure()
#     # fig1.tight_layout()
#     # ax1 = plt.subplot(111)
#     # ax1.set_title('Particles')
#     # ax1.set_axis_off()
#     plt.imsave(rf'C:/Users/DellPC/Desktop/MAPRENDERS/Conway/test_{frames}.png', array_0[:, :, frames], cmap=cm.Greys, format='png')

fig, ax = plt.subplots()
ims = []
for frames in range(0, sim_steps):
    im = ax.imshow(array_0[:, :, frames], animated=True, cmap=cm.Greys)
    if i == 0:
        ax.imshow(array_0[:, :, frames])  # show an initial one first
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                repeat_delay=0)

# To save the animation, use e.g.
#
# ani.save("movie.mp4")
#
# or
#
# writer = animation.FFMpegWriter(
#     fps=15, metadata=dict(artist='Me'), bitrate=1800)
# ani.save("movie.mp4", writer=writer)

plt.show()
