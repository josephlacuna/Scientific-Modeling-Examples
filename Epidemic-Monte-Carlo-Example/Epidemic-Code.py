import numpy as np
import scipy as sc
import numba as nb
import matplotlib.pyplot as plt
import matplotlib.animation as animation

'''
This code is from a programming modeling class that is an implementation of
Markov Chain methods on an epidemic simulation for a 2-D environment. This
code creates an array with randomly assigned values representative of a type
of individual (healthy, immune, or sick) and proceeds to play out the spread of
disease between neighboring indivuals. A graph and animation are produced.
'''

# Assigning variables
# Healthy (1), Immune (2), Sick (3)
imm_count = 0              # creating immune counter
hea_count = 0              # creating healthy counter
sic_count = 0              # creating sick counter
alpha = 0.25               # probability of getting sick given an interaction
beta = 0.05                # probability of becoming immune to disease
imm_prop = 0.05            # proportion of immune
sic_prop = 0.20            # proportion of sick
immune_count = []          # creating immune counter list
healthy_count = []         # creating healthy counter list
sick_count = []            # creating sick counter list
itera = 100                # amount of iterations to run

# Generate an array with dimensions Dim X Dim with all zeros
Dim = 100                  # dimension of the grid, square
total_pop = Dim*Dim
grid = np.zeros([Dim,Dim]) # creates empty grid

# Randomly assign each grid position a value from 0 to 1 to designate status
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        grid[i,j] = np.random.rand(1)
# For example, this method has 5% immune (2), 15% sick (3), and 80% healthy (1)
        if grid[i,j] < imm_prop:
            grid[i,j] = 2
            imm_count +=1
        elif grid[i,j] < sic_prop:
            grid[i,j] = 3
            sic_count += 1
        else:
            grid[i,j] = 1
            hea_count += 1

# Creating and updating population lists
initial_pop = []                # creating initial total population list
initial_pop = healthy_count, immune_count, sick_count
sick_count.append(sic_count)
healthy_count.append(hea_count)
immune_count.append(imm_count)

#print('healthy,immune,sick')
#print(initial_pop)

# Creating stochastic, grid updating function
@nb.jit
def updategrid(grid):
# make sure the grid sizes are equal
    if grid.shape[0] == grid.shape[1]:
        x = grid.shape[0]
    else:
        raise IndexError('Bad')
    gridnew = grid.copy()
    v_size, h_size = grid.shape

    for i in range(x):
            for j in range(x):
                gridnew = grid
                # If the space is not empty, then it can move.
                # Randomly determining the direction it will move
                if grid[i,j] != 0:

                    random_num = np.random.rand(1)

                    if random_num < 0.25 and gridnew[(i+1)%x,j] == 0:
                        gridnew[(i+1)%x,j] = grid[i,j]
                        gridnew[i,j] = 0
                    else:
                        gridnew[i,j] = grid[i,j]

                    if random_num < 0.5 and gridnew[(i-1)%x,j] == 0:
                        gridnew[(i-1)%x,j] = grid[i,j]
                        gridnew[i,j] = 0
                    else:
                        gridnew[i,j] = grid[i,j]

                    if random_num < 0.75 and gridnew[i,(j+1)%x] == 0:
                        gridnew[i,(j+1)%x] = grid[i,j]
                        gridnew[i,j] = 0
                    else:
                        gridnew[i,j] = grid[i,j]

                    if random_num < 1 and gridnew[i,(j-1)%x] == 0:
                        gridnew[i,(j-1)%x] = grid[i,j]
                        gridnew[i,j] = 0
                    else:
                        gridnew[i,j] = grid[i,j]

    # If any surrounding grid point is popuated by a sick person, then spread the sickness
    # if the random number is less than the probabiliy of getting sick

                    prob = np.random.rand(1)
                    prob2 = np.random.rand(1)

                    if prob < alpha:
                        if gridnew[i,j] == 1:
                            if (gridnew[(i+1)%x,j] == 3 or gridnew[(i-1)%x,j] == 3
                            or gridnew[i,(j+1)%x] == 3 or gridnew[i,(j-1)%x] == 3):
                                gridnew[i,j] = 3

                    if prob2 < beta:
                        if gridnew[i,j] == 3:
                                gridnew[i,j] = 2

    return gridnew

# Creating grid animation
fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid()
fig.suptitle("Stochastic Epidemic Model [a = {}, b = {}]".format(alpha,beta))
grids = []
image = ax.imshow(grid, cmap='inferno')
grids.append([image])

for k in range(itera-1):
    grid = updategrid(grid)
    s_count = np.sum(grid == 3)
    h_count = np.sum(grid == 1)
    i_count = np.sum(grid == 2)
    sick_count.append(s_count)
    healthy_count.append(h_count)
    immune_count.append(i_count)
    image = ax.imshow(grid, cmap='inferno')
    grids.append([image])
    plt.close()

# Plotting Population over Steps
steps = np.linspace(0,itera-1,itera)
plt.plot(steps, immune_count, label = "Immune")
plt.plot(steps, healthy_count, label = "Healthy")
plt.plot(steps, sick_count, label = "Sick")
plt.xlabel('Steps')
plt.ylabel('Population')
plt.title("Stochastic Epidemic Model [a = {}, b = {}]".format(alpha, beta))
plt.xlim(0,itera-1)
plt.ylim(0,total_pop)
plt.text((itera/3), (total_pop/2), "{} Healthy, {} Immune, {} Sick Initially".format(hea_count,imm_count,sic_count))
plt.legend()
plt.savefig('epidemic_plot_{}_{}.png'.format(alpha,beta),format = 'png', dpi = 600, bbox_inches='tight')
plt.close()

# Animating Simulation of Grid Space
# requires ffmpeg
ani = animation.ArtistAnimation(fig, grids, blit=True)
ani.save("epidemic_animation_{}_{}.mp4".format(alpha,beta), dpi=300, fps=10, extra_args=['-vcodec', 'libx264'])
plt.close()
