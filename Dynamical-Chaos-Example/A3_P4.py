from numpy import *
from scipy import *
from matplotlib.pyplot import *

from random import randrange

# steps to run simulation for (generally only needs a few
# to sketch full limit cycles)

N = 150
np.random.seed(1)
K = 0.5

def stdmap(x, p):
    pn = mod(p + K*sin(x), 2*pi)
    xn = mod(x + pn, 2*pi)
    return (xn, pn)

 # make the mesh for phase space
x0 = linspace(0, 2*pi, 7)
p0 = linspace(0, 2*pi, 8)
mesh = list()
for i in range(len(x0)):
    for j in range(len(p0)):
        mesh.append((x0[i], p0[j]))

Kvals = linspace(.1,2*pi,10)

for val in Kvals:
    K = val
    fig = figure(figsize=(5, 5))
    for item in mesh:
        traj = [item]
        for i in range(N):
            for j in range(N):
                traj.append(stdmap(x0[i], p0[j]))
        plot(array(traj).T[0], array(traj).T[1],'.')
        hold(True)

    xlim([0, 2*pi])
    ylim([0, 2*pi])
    xlabel('Position (rad)')
    ylabel('Momentum')
    show()
#   savefig('stdmap_'+ str(round(K, 5))+'.png')

def func(K, npoints, x0, p0):
    x = x0
    p = p0
    X = []
    P = []
    for n in range(npoints):
        X.append(x)
        P.append(p)
        xnew, pnew = std(x,p)

        x,p = xnew, pnew

    plt.scatter(X, P, s=.2)

for k in np.linspace(0,5,100):
    for i in np.random.rand(30) * 2 * np.pi:
        for in np.random.rand(30) * np.pi:
            func (k, 100, i, j)
    plt.xlabel('$\Theta$')
    plt.ylabel('$Angular Momentum$')
    plt.title('K = {}'.format(round(K, 2)))
    plt.savefig('StandardMapping_K_{}'.format(round(K,2)))
    plt.close()
