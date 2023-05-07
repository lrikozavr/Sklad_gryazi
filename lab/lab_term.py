# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
def grf():
  fig, ax = plt.subplots(figsize=(10, 10))
  xmin, xmax, ymin, ymax = 0, 1100, -20, 1000
  ticks_frequency = 50  

  # Set identical scales for both axes
  #ax.set(xlim=(xmin-1, xmax+1), ylim=(ymin-1, ymax+1), aspect='equal')

  # Set bottom and left spines as x and y axes of coordinate system
  ax.spines['bottom'].set_position(('axes',0.))
  ax.spines['left'].set_position(('axes',0.))

  # Remove top and right spines
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)

  # Create 'x' and 'y' labels placed at the end of the axes
  ax.set_xlabel('x', size=14, labelpad=-24, x=1.03)
  ax.set_ylabel('y', size=14, labelpad=-21, y=1.02, rotation=0)

  # Create custom major ticks to determine position of tick labels
  x_ticks = np.arange(xmin-1, xmax+2, ticks_frequency)
  y_ticks = np.arange(ymin-1, ymax+2, ticks_frequency)
  #ax.set_xticks(x_ticks[x_ticks != 0])
  #ax.set_yticks(y_ticks[y_ticks != 0])

  # Create minor ticks placed at each integer to enable drawing of minor grid
  # lines: note that this has no effect in this example with ticks_frequency=1
  ax.set_xticks(np.arange(xmin, xmax,10), minor=True)
  ax.set_yticks(np.arange(ymin, ymax,2), minor=True)
  ax.grid(which='both', alpha=1)

  #ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
  #ax.plot(, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)
  return fig,ax

T = [77,288,373]
ro = np.array([  [0.31894, 2.64022, 3.52753],
        [20.74801,79.28396,101.87280],
        [0.22499, 1.66855, 2.19281],
        [2.47498, 3.88186, 4.39897],
        [42.57806, 45.28265, 45.08738],
        [85.19916, 87.35189, 87.92422]])
name = ['Al','Al-Cu-Mn-Mg','Cu','Cu-Zn','Cu-Ni-Mn-Fe',r'$Fe_{80}B_{14}S_{6}$']
import math
log = np.vectorize(math.log)
#print(log(ro[1,:]))
for i in range(len(name)):
  fig,ax = grf()
  ax.scatter(T,ro[i,:])
  ax.plot(T,ro[i,:],label = name[i])
  ax.legend(loc=2)
  ax.set_xlabel('T, K',size=14, labelpad = 15)
  ax.set_ylabel('ρ, 10^-8 Ω*m', labelpad=10, rotation=90)
  fig.savefig(f'c:/Users/lrik/Downloads/{name[i]}.png')
plt.show()