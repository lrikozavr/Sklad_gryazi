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
#dm_mass = [((tg_mass[i-1][1]) - (tg_mass[i][1])) + tg_mass[i-1][1] for i in range(1,len(tg_mass),1)]
#dm_mass.append(0)
#print(dta_mass)
import matplotlib.pyplot as plt
import numpy as np

tg_mass = np.array(tg_mass)
dta_mass = np.array(dta_mass)
#dm_mass = np.array(dm_mass)

#print(dta_mass)
#print(tg_mass[:,1])
fig, ax = plt.subplots(figsize=(10, 10))
def grf():
  xmin, xmax, ymin, ymax = -50, 1000, -30, 80
  ticks_frequency = 5  

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
  ax.grid(which='both', alpha=0.7)
  
  ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
  ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

  return ax

from func import *

def dta_temperature(mass_x,mass_y):
    new_mass_y = [0]*mass_y
    for i in range(len(mass_x)):
      new_mass_y[i] = mass_y[i] + mass_x[i]
    return new_mass_y

def percent_of_mass(mass_y):
  m1 = 0.3241 # 4.1415 - 3.8174
  new_mass_y = [0]*len(mass_y)
  for i in range(len(mass_y)):
    new_mass_y[i] = 1 - (m1 + mass_y[i]/1000.0)/m1
    new_mass_y[i] *= 100
  return new_mass_y

ax = grf()
'''
print(tg_mass[:,0])
print(dta_mass[:,0])

#dif_tg_mass = average(tg_mass[:,0],tg_mass[:,1]+100,5)
#ax.plot(tg_mass[:,0],dif_tg_mass,label='tg_mass')
print(len(tg_mass[:,0]))
dif_tg_mass,dif_tg_mass_x = interp(tg_mass[:,0],tg_mass[:,1],10,100)
#ax.scatter(dif_tg_mass_x,dif_tg_mass,label='tg_not_dif')
print(len(dif_tg_mass))
print(len(dif_tg_mass_x))
dif_tg_mass,dif_tg_mass_x = dif_one(dif_tg_mass_x,dif_tg_mass,1)
dif_tg_mass = average(dif_tg_mass_x,dif_tg_mass,10)
dif_tg_mass = mean(dif_tg_mass_x,dif_tg_mass,10)

dif_2_tg_mass,dif_2_tg_mass_x = dif_one(dif_tg_mass_x,dif_tg_mass,1)
dif_2_tg_mass = average(dif_2_tg_mass_x,dif_2_tg_mass,500)
dif_2_tg_mass = mean(dif_2_tg_mass_x,dif_2_tg_mass,20)
'''
#ax.plot(dif_tg_mass_x,dif_tg_mass,label='tg_dif')
#ax.plot(dif_2_tg_mass_x,dif_2_tg_mass,label='tg_dif_2')
#print(dta_t)
#print(dif_dta_t)
#dta_mass_undif = undif_one(dta_mass[:,0],dta_mass[:,1])
#ax.plot(tg_mass[:,0],tg_mass[:,1],label='tg')
#ax.plot(dta_mass[:,0],dta_mass[:,1],label='dta')


#dta_t = dta_temperature(dta_mass[:,0],dta_mass[:,1])
#dif_dta_t,dif_dta_t_x = dif_one(dta_mass[:,0],dta_t,10)

#ax.plot(dta_mass[:,0],dta_t,label='dta_t')
#ax.plot(dif_dta_t_x,dif_dta_t,label='dta_t_dif')

#ax.plot(dta_mass[:,0],dta_mass_undif,label='dta_undif')

#ax.plot(tg_mass[:,0],(-26.6584 - (dm_mass[:])*(174.19/100.09))*100/(-26.6584))

def fond(mass,number,dim):
    index_mass = []
    index = 0
    for i in mass:
        if(i < number+dim and i > number-dim):
            index_mass.append(index)
        index+=1
    return index_mass
#
#a_value = fond(tg_mass[:,0],537,0.5)
a_value = fond(dta_mass[:,0],537,0.5)
print(a_value)
#tg_mass_p = percent_of_mass(tg_mass[:,1])
#ax.plot(tg_mass[:,0],tg_mass_p,label='tg_percent')

ax.plot(dta_mass[:,0],dta_mass[:,1],label='dta')
ax.set_xlabel(' T, °C', size=14, labelpad=-24, x=1.05)
ax.set_ylabel(r'$T_{проби} - T_{інертної_ речовини}, °C$', size=14, labelpad=-21, y=1.02, rotation=0)
ax.legend(loc = 9, fontsize='x-large')

#
ax.annotate(
   '$Ca(OH)_2$',
   size=20,
   #xy=(537,tg_mass_p[a_value[0]]), xycoords='data',
   xy=(537,dta_mass[a_value[0],1]), xycoords='data',
   xytext=(-120,-50), textcoords='offset points',
   arrowprops=dict(arrowstyle="->")
)
ax.annotate(
   '$CaCO_3$',
   size=20,
   #xy=(840,tg_mass_p[fond(tg_mass[:,0],840,0.5)[0]]), xycoords='data',
   xy=(840,dta_mass[fond(dta_mass[:,0],840,0.5)[0],1]), xycoords='data',
   xytext=(-120,-50), textcoords='offset points',
   arrowprops=dict(arrowstyle="->")
)
#plt.rcParams['text.usetex'] = True
def point_arrow(ax,x,y,text):
    text_ = f'${text} ({x},{y})$'
    ax.annotate(
      text_,
      #r'\TeX\ is Number $\displaystyle\sum_{n=1}^\infty$',
      xy=(x,y), xycoords='data',
      xytext=(-100,50), textcoords='offset points',
      arrowprops=dict(arrowstyle="->")
    )

T = 537
#x_1,y_1 = T,tg_mass_p[fond(tg_mass[:,0],T,0.5)[0]]
x_1,y_1 = T,dta_mass[fond(dta_mass[:,0],T,0.5)[0],1]
point_arrow(ax,x_1,y_1, 'm_2')
T = 450
#x_1,y_1 = T,tg_mass_p[fond(tg_mass[:,0],T,0.5)[0]]
x_1,y_1 = T,dta_mass[fond(dta_mass[:,0],T,0.5)[0],1]
point_arrow(ax,x_1,y_1, 'm_1')

T = 840
#x_1,y_1 = T,tg_mass_p[fond(tg_mass[:,0],T,0.5)[0]]
x_1,y_1 = T,dta_mass[fond(dta_mass[:,0],T,0.5)[0],1]
point_arrow(ax,x_1,y_1, 'm_3')

fig.savefig(r'c:/Users/lrik/Downloads/dta.png')

plt.show()


