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

#найпростіша функція диференціювання
def dif_one(mass_x,mass_y,n):
  new_mass_y = []
  new_mass_x = []
  for i in range(0,len(mass_x)-1,n):
    #print((mass[i+1][1] - mass[i][1]) / abs(mass[i+1][0] - mass[i][0]))
    new_mass_y.append(float(mass_y[i+1] - mass_y[i])*100 / abs(mass_x[i+1] - mass_x[i]))
    new_mass_x.append(mass_x[i+1])
  #new_mass_y.append(0)
  return new_mass_y,new_mass_x

#виводить медіанне значення
def mean(mass_x,mass_y,n):
  new_mass_y = [0]*len(mass_x)
  for i in range(len(mass_x)):
      temp = [0]*n
      for j in range(n):
        index = i + j - n//2
        if(index > 0 and index < len(mass_x)):
          temp[j] = mass_y[index]
      temp = np.sort(temp)
      new_mass_y[i] = temp[n//2]
  return new_mass_y

#рахує середнє значення з вікном n
def average(mass_x,mass_y,n):
  new_mass_y = [0]*len(mass_x)
  for i in range(len(mass_x)):
      sum = 0
      count = 0
      for j in range(n):
        index = i + j - n//2
        if(index > 0 and index < len(mass_x)):
          count+=1
          sum += mass_y[index]
      new_mass_y[i] = sum // count
  return new_mass_y

#за допомогою кубічного сплайну додає точки
#extend_c - кількість точок які бажаємо отримати
#n - діапазон точок для котрих бажаємо отримати
#extend_c/n - ступінь збільшення точності
def interp(mass_x,mass_y,n,extend_c):
  from scipy.interpolate import interp1d
  new_mass_y = []
  new_mass_x = []
  for i in range(0,len(mass_x),n):
    temp_y = []
    temp_x = []
    index_temp = 0
    #хитрість 1: додаємо точку з наступного шматку
    for j in range(n+1):
      index = i + j - n//2
      if(index > 0 and index < len(mass_x)):
        temp_y.append(mass_y[index])
        temp_x.append(mass_x[index])
        index_temp += 1
    # Create a cubic spline interpolation function
    f = interp1d(temp_x, temp_y, kind='cubic')
    # Generate some points to interpolate at
    x_interp = np.linspace(temp_x[0], temp_x[index_temp-1], extend_c)
    # Evaluate the interpolation function at the new points
    y_interp = f(x_interp)
    #хитрість 1: віднімаємо останній елемент, щоб вони не накладалися
    for j in range(len(x_interp)-1):
       new_mass_y.append(y_interp[j])
       new_mass_x.append(x_interp[j])
  return new_mass_y,new_mass_x

print(tg_mass[:,0])
print(dta_mass[:,0])
ax = grf()
#dif_tg_mass = average(tg_mass[:,0],tg_mass[:,1]+100,5)
#ax.plot(tg_mass[:,0],dif_tg_mass,label='tg_mass')
print(len(tg_mass[:,0]))
dif_tg_mass,dif_tg_mass_x = interp(tg_mass[:,0],tg_mass[:,1],10,100)
ax.scatter(dif_tg_mass_x,dif_tg_mass,label='tg_not_dif')
print(len(dif_tg_mass))
print(len(dif_tg_mass_x))
dif_tg_mass,dif_tg_mass_x = dif_one(dif_tg_mass_x,dif_tg_mass,1)
dif_tg_mass = average(dif_tg_mass_x,dif_tg_mass,10)
dif_tg_mass = mean(dif_tg_mass_x,dif_tg_mass,10)

dif_2_tg_mass,dif_2_tg_mass_x = dif_one(dif_tg_mass_x,dif_tg_mass,1)
dif_2_tg_mass = average(dif_2_tg_mass_x,dif_2_tg_mass,500)
dif_2_tg_mass = mean(dif_2_tg_mass_x,dif_2_tg_mass,20)

ax.plot(dif_tg_mass_x,dif_tg_mass,label='tg_dif')
ax.plot(dif_2_tg_mass_x,dif_2_tg_mass,label='tg_dif_2')

ax.plot(tg_mass[:,0],tg_mass[:,1],label='tg')
ax.plot(dta_mass[:,0],dta_mass[:,1],label='dta')
#ax.plot(tg_mass[:,0],(-26.6584 - (dm_mass[:])*(174.19/100.09))*100/(-26.6584))
ax.legend()
plt.show()


