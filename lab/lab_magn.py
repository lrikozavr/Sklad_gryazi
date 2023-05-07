# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

def changefileconfig(filename,header,column_size):
    new_line = ''
    i = 1
    f = open(f"{filename}.csv","w")
    for line in open(filename):
        n = line.split(',')
        if(len(n) > 1):
            if(not n[1] == '\n'):
                t = n[1].split("\n")[0]
            else:
                t = 0
        else:
            n[0] = n[0].split('\n')[0]
            t = ''
        if( i % column_size == 0):
            new_line += f',{n[0]}.{t}\n'
            f.write(new_line)
            print(new_line)
            new_line = ''
        else:
            new_line += f'{n[0]}.{t}'
        i += 1
    f.close()


path = 'C:/Users/lrik/Desktop/Gorbach'
name = ['Co0,8Cu1,2Y','Co1,2Cu0,8Y','Co1,4Cu0,6Y','Co1,6Cu0,4Y','Co1Cu1Y']
'''
for i in range(len(name)):
    changefileconfig(f'{path}/{name[i]}',1,2)  
'''
import matplotlib.pyplot as plt



def grf():
  fig, ax = plt.subplots(figsize=(10, 10))
  xmin, xmax, ymin, ymax = 0, 1100, 0, 1000
  ticks_frequency = 50  

  # Set identical scales for both axes
  #ax.set(xlim=(xmin-1, xmax+1), ylim=(ymin-1, ymax+1), aspect='equal')

  # Set bottom and left spines as x and y axes of coordinate system
  ax.spines['bottom'].set_position('zero')
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
  ax.set_yticks(np.arange(ymin, ymax,10), minor=True)
  ax.grid(which='both', alpha=0.7)

  #ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
  #ax.plot(, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

  
  return fig,ax

mass_index = np.array([[13,44],[7,47],[3,46],[2,44],[13,44]])
mass_index = np.flip(mass_index,0)

from func import interp, dif_one, mean, average, local_max_dif, point_arrow
#len(name)
for i in range(5):
    fig,ax = grf()
    data = pd.read_csv(f'{path}/{name[i]}.txt.csv',header=0,sep=',',dtype=np.float64)
    data = data.sort_values(by=[f'{data.columns.values[0]}'])
    #print(name[i],data)
    mass_x,mass_y = data[data.columns.values[0]],data[data.columns.values[1]]
    #mass_y,mass_x = interp(data[data.columns.values[0]],data[data.columns.values[1]],20,1000)
    ax.scatter(mass_x,mass_y,label = name[i])
    ax.plot(mass_x,mass_y,label = name[i])
    #dif_mass_y,dif_mass_x = dif_one(mass_x,mass_y,1)
    #local_max_mass = local_max_dif(dif_mass_x,dif_mass_y,7)
    local_max_mass = mass_index[i,:]
    #print(local_max_mass) #5 - [13,44], 4 - [7,47], 3 - [3,46], 2 - [2,44], 1 - [13,44]
    #dif_mass_y_2,dif_mass_x_2 = dif_one(dif_mass_x,dif_mass_y,1)
    #dif_mass_y = average(dif_mass_x,dif_mass_y,5)
    #dif_mass_y = mean(dif_mass_x,dif_mass_y,10)
    #ax.scatter(dif_mass_x,dif_mass_y,label = f'{name[i]}_dif')
    #ax.scatter(dif_mass_x_2,dif_mass_y_2,label = f'{name[i]}_dif_2')
    mass_x = np.array(mass_x)
    mass_y = np.array(mass_y)
    ax.scatter(mass_x[local_max_mass],mass_y[local_max_mass], label = 'local max')
    point_arrow(ax,mass_x[local_max_mass[0]],mass_y[local_max_mass[0]],'температура\ спін-переорієнтаційного\ переходу')
    point_arrow(ax,mass_x[local_max_mass[1]],mass_y[local_max_mass[1]],'температура\ Кюрі')
    #dif_mass_x = np.array(dif_mass_x)
    #dif_mass_y = np.array(dif_mass_y)
    #ax.scatter(dif_mass_x[local_max_mass],dif_mass_y[local_max_mass], label = 't_1')
    ax.legend(loc = 3, fontsize='x-large')
    ax.set_xlabel('T, K',size=14, labelpad = 15)
    ax.set_ylabel('χ', size=14, labelpad=10, rotation=0)
    fig.savefig(f'c:/Users/lrik/Downloads/{name[i]}.png')


plt.show()