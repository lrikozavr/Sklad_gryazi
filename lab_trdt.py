# -*- coding: utf-8 -*-

path = 'c:/Users/lrik/Downloads'

dta = open(f'{path}/DTA.dat','r')
tg = open(f'{path}/TG.dat','r')

def write_file(f):
    mass = []
    for line in f:
        n = line.split(' ')
        mass.append([float(n[0]),float(n[1].split('\n')[0])])
    return mass

dta_mass = write_file(dta)
tg_mass = write_file(tg)
dm_mass = [100*((tg_mass[i-1][1]) - (tg_mass[i][1])) for i in range(1,len(tg_mass),1)]
#print(dta_mass)
import matplotlib.pyplot as plt
import numpy as np

tg_mass = np.array(tg_mass)
dta_mass = np.array(dta_mass)
dm_mass = np.array(dm_mass)

#print(dta_mass)
#print(tg_mass[:,1])
fig, ax = plt.subplots(figsize=(10, 10))
def grf():
  xmin, xmax, ymin, ymax = -50, 1000, -100, 100
  ticks_frequency = 50  

  # Set identical scales for both axes
  #ax.set(xlim=(xmin-1, xmax+1), ylim=(ymin-1, ymax+1), aspect='equal')

  # Set bottom and left spines as x and y axes of coordinate system
  ax.spines['bottom'].set_position('zero')
  ax.spines['left'].set_position('zero')

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
  ax.set_xticks(np.arange(xmin, xmax,25), minor=True)
  ax.set_yticks(np.arange(ymin, ymax,5), minor=True)
  ax.grid(which='both', alpha=1)

  return ax

print(tg_mass[:,0])
print(dta_mass[:,0])
ax = grf()
ax.plot(tg_mass[:,0],tg_mass[:,1]+100,label='tg')
ax.plot(dta_mass[:,0],dta_mass[:,1],label='dta')
ax.plot((-26.6584 - (dm_mass[:])*(174.19/100.09))*100/(-26.6584),(dm_mass[:])*(174.19/100.09))
ax.legend()
plt.show()