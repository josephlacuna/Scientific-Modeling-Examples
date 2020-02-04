import numpy as np
import matplotlib.pyplot as plt
from numba import jit
import matplotlib.style as sty
#parameters
maxiter = 256
#xm = 2.0
#xx = 3.0
#ym = 1.0
#yx = 2.0
xm = 0.3633
xx = 0.3933
ym = 0.2200
yx = 0.2500
itera = 100
xd = (xx - xm) / (itera*2.000001)
yd = (yx - ym) / (itera*2.000001)


'''
def mandelbrot(c,maxiter):
    c = z
    for n in range(maxiter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return 0
'''

for i in range(1, itera+1):
    xmin = xm + (xd * i)
    xmax = xx - (xd * i)
    ymin = ym + (yd * i)
    ymax = yx - (yd * i)
    xlin = np.linspace(xmin,xmax,1000)
    ylin = np.linspace(ymin,ymax,1000)
    x,y = np.meshgrid(xlin,ylin)
    z = x + y*1j
    c = z.copy()
    steps = np.zeros((len(x),len(y)))
    Z = np.zeros((len(x),len(y)))

    for n in range(maxiter):
        z = z*z + c
        mask = np.abs(z) < 2
        steps[mask] += 1

    plt.imshow(steps, extent=[min(xlin), max(xlin),min(ylin), max(ylin)])
    plt.savefig('mandelbrot_%03d.png' % i, dpi = 256)
