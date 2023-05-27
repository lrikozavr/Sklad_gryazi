# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 10))
def grf():
  #fig, ax = plt.subplots(figsize=(10, 10))
  xmin, xmax, ymin, ymax = 0, 1100, 0, 1000
  #ticks_frequency = 50  

  # Set identical scales for both axes
  #ax.set(xlim=(xmin-1, xmax+1), ylim=(ymin-1, ymax+1), aspect='equal')

  # Set bottom and left spines as x and y axes of coordinate system
  ax.spines['bottom'].set_position('zero')
  ax.spines['left'].set_position(('axes',0.))

  # Remove top and right spines
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)

  # Create 'x' and 'y' labels placed at the end of the axes
  ax.set_xlabel(r'$x, \mu m$', size=14, labelpad=24)
  ax.set_ylabel(r'$C_{Ni}$', size=14, labelpad=21, rotation=90)

  # Create custom major ticks to determine position of tick labels
  #x_ticks = np.arange(xmin-1, xmax+2, ticks_frequency)
  #y_ticks = np.arange(ymin-1, ymax+2, ticks_frequency)
  #ax.set_xticks(x_ticks[x_ticks != 0])
  #ax.set_yticks(y_ticks[y_ticks != 0])

  # Create minor ticks placed at each integer to enable drawing of minor grid
  # lines: note that this has no effect in this example with ticks_frequency=1
  ax.set_xticks(np.arange(xmin, xmax,5), minor=True)
  ax.set_yticks(np.arange(ymin, ymax,0.05), minor=True)
  ax.grid(which='both', alpha=0.7)

  #ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
  #ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

  return ax

path = 'C:/Users/lrikozavr/Downloads'
mass = pd.read_excel(f'{path}/lab_data.xlsx')
#print(mass)
name = ['x, m',r'I_{Ni}',r'C_{Ni} = I_{Ni}/I_{ет}']

def tngnt_(x,y,x0):
    from scipy import interpolate
    tck = interpolate.splrep(x,y)

    #x0 = 7.3
    y0 = interpolate.splev(x0,tck)
    dydx = interpolate.splev(x0,tck,der=1)

    tngnt = lambda x: dydx*x + (y0-dydx*x0) 
    tngnt_rev = lambda x: (x - (y0-dydx*x0)) / dydx
    return tngnt, tngnt_rev

tngnt02,tngnt02_rev = tngnt_(mass[name[0]],mass[name[2]],108) #C = 0.2
tngnt06,tngnt06_rev = tngnt_(mass[name[0]],mass[name[2]],80)  #C = 0.6

def x_cut(x,func,func_rev,a,b):
    new_x = []
    if(func_rev(b) <= x[len(x)-1] and func_rev(b) >= x[0]):
        new_x.append(func_rev(b))
    for i in range(len(x)):
        if(func(x[i]) >= a and func(x[i]) <= b):
            new_x.append(x[i])
    if(func_rev(a) <= x[len(x)-1] and func_rev(a) >= x[0]):
       new_x.append(func_rev(a))
    return new_x

x_02 = x_cut(mass[name[0]],tngnt02,tngnt02_rev,0,1)
x_06 = x_cut(mass[name[0]],tngnt06,tngnt06_rev,0,1)

#####
from func import interp

from scipy import integrate
y,x = interp(mass[name[0]],mass[name[2]],3,30)
x = np.array(x)
y = np.array(y)
l = len(x)
print(l)
index = 0
for i in range(1,len(x)-1,1):
    #print(y[0:i])
    a = integrate.simpson(y[0:i],x[0:i])
    a = abs(y[0]-y[l-1])*abs(x[i]-x[0]) - a
    b = integrate.simpson(y[i:l-1],x[i:l-1])
    #print(a,b,abs(y[0]-y[l-1])*abs(x[i]-x[0]))
    if(abs(a-b) < 0.5):
        index = i
        break
print(index,x[index])
'''
from func import interp
y,x = interp(mass[name[0]],mass[name[2]],3,30)
x = np.array(x)
y = np.array(y)
l = len(x)
index = 96
print(x[index])
'''

Matano_x,Matano_y = [x[index],x[index]],[y[0],y[l-1]]
#####
#print(abs(x_06[len(x_06) - 1] - x_06[0]),abs(tngnt06(x_06[len(x_06) - 1]) - tngnt06(x_06[0])))
#print(x_06[len(x_06) - 1],x_06[0],tngnt06(x_06[len(x_06) - 1]),tngnt06(x_06[0]))
#print(abs(x_02[len(x_02) - 1] - x_02[0]),abs(tngnt02(x_02[len(x_02) - 1]) - tngnt02(x_02[0])))
#print(x_02[len(x_02) - 1],x_02[0],tngnt02(x_02[len(x_02) - 1]),tngnt02(x_02[0]))

tng06 = abs(x_06[len(x_06) - 1] - x_06[0])/abs(tngnt06(x_06[len(x_06) - 1]) - tngnt06(x_06[0]))
tng02 = abs(x_02[len(x_02) - 1] - x_02[0])/abs(tngnt02(x_02[len(x_02) - 1]) - tngnt02(x_02[0]))
#####

#####
x_02_b,y_02_b = [],[]
for i in range(index,l,1):
    if(y[i] > 0.2):
        y_02_b.append(0.2)
    else:
        y_02_b.append(y[i])
    x_02_b.append(x[i])
x_06_u,y_06_u = [],[]
for i in range(0,index+1,1):
    x_06_u.append(x[i])
    if(y[i] < 0.6):
        y_06_u.append(0.6)
    else:
        y_06_u.append(y[i])
from scipy import integrate
integ_02_b = integrate.simpson(y_02_b,x_02_b)
integ_06_u = integrate.simpson(y_06_u,x_06_u)
integ_06_u = abs(y[0]-y[l-1])*abs(x[index]-x[0]) - integ_06_u
print('S- - S1:',integ_06_u,'\tS+ - S2:',integ_02_b)

integ_m_1 = integrate.simpson(y[0:index],x[0:index])
integ_m_1 = abs(y[0]-y[l-1])*abs(x[index]-x[0]) - integ_m_1
integ_m_2 = integrate.simpson(y[index:l-1],x[index:l-1])
print('S-:',integ_m_1,'\tS+:',integ_m_2)

print('S1:',integ_m_1 - integ_06_u,'\tS2:',integ_m_2 - integ_02_b)
#####
ax = grf()

ax.text(5,0.6,f"$tan(φ_2) = {round(tng02,4)}$", rotation = 310, fontsize = 10)
ax.text(50,0.7,f"$tan(φ_6) = {round(tng06,4)}$", rotation = 285, fontsize = 10)
ax.text(95,0.6,f'Matano plane',rotation = 90, fontsize=20)
ax.fill_between(x_02_b,0,y_02_b, facecolor = 'orange', alpha=0.7)
ax.text(100,0.1,r'$S_{0.2}$',fontsize=20)
ax.fill_between(x_06_u,y_06_u,1, facecolor = 'blue', alpha=0.7)
ax.text(70,0.9,r'$S_{0.6}$', fontsize = 20)
ax.plot(Matano_x,Matano_y, label = "Matano plane")
#ax.plot(x,y,label = 'interpol')
ax.scatter(x,y,label = 'linear_interpolation')
ax.plot(mass[name[0]],mass[name[2]], label = r'$C_{Ni}(x)$')
#ax.scatter(mass[name[0]],mass[name[2]])
ax.plot(x_06,tngnt06(x_06), label = r'$tan(\varphi_{C_{Ni}=0.6})$')
ax.plot(x_02,tngnt02(x_02), label = r'$tan(\varphi_{C_{Ni}=0.2})$')
ax.legend()
fig.savefig(r'C:\Users\lrikozavr\Downloads\teor_dif_lab.png')
plt.show()
