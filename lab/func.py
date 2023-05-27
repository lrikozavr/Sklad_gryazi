# -*- coding: utf-8 -*-
import numpy as np

#найпростіша функція диференціювання
#n - крок диференціювання
def dif_one(mass_x,mass_y,n):
  new_mass_y = []
  new_mass_x = []
  for i in range(0,len(mass_x)-1,n):
    #print((mass[i+1][1] - mass[i][1]) / abs(mass[i+1][0] - mass[i][0]))
    new_mass_y.append(float(mass_y[i+1] - mass_y[i])*100 / abs(mass_x[i+1] - mass_x[i]))
    new_mass_x.append(mass_x[i])
  #new_mass_y.append(0)
  return new_mass_y,new_mass_x

def undif_one(mass_x,mass_y):
    new_mass_y = [0]*mass_y
    new_mass_y[0] = mass_y[0]
    for i in range(1,len(mass_x),1):
      new_mass_y[i] = mass_y[i]*(mass_x[i] - mass_x[i-1]) + new_mass_y[i-1]
    return new_mass_y

def local_max_dif(mass_x,mass_y,n):
  new_mass = []
  flag = 0
  for i in range(len(mass_x)):
    sum = [0,0]
    for j in range(n):
      index = i + j - n//2
      if(index > 0 and index < len(mass_x)):
        if(j - n//2 < 0):
          if(mass_y[index] > 0):
            sum[0] += 1
          else:
            sum[0] += -1
        if(j - n//2 > 0):
          if(mass_y[index] > 0):
            sum[1] += 1
          else:
            sum[1] += -1
    if((abs(sum[0]) == n//2 and abs(sum[1]) == n//2) and not sum[0] == sum[1]):
      #new_mass.append(i)
      
      if(flag):
        new_mass.append(i)
        flag = 0
      else:
        flag = 1
      
  return new_mass

        

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
      new_mass_y[i] = sum / count
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
      if(index >= 0 and index < len(mass_x)):
        temp_y.append(mass_y[index])
        temp_x.append(mass_x[index])
        index_temp += 1
    # Create a cubic spline interpolation function
    f = interp1d(temp_x, temp_y, kind='linear')
    # Generate some points to interpolate at
    x_interp = np.linspace(temp_x[0], temp_x[index_temp-1], extend_c)
    # Evaluate the interpolation function at the new points
    y_interp = f(x_interp)
    #хитрість 1: віднімаємо останній елемент, щоб вони не накладалися
    for j in range(len(x_interp)-1):
       new_mass_y.append(y_interp[j])
       new_mass_x.append(x_interp[j])
  return new_mass_y,new_mass_x

def point_arrow(ax,x,y,text):
    text_ = f'${text}\ ({x},{y})$'
    ax.annotate(
      text_,
      #r'\TeX\ is Number $\displaystyle\sum_{n=1}^\infty$',
      xy=(x,y), xycoords='data',
      xytext=(-100,50), textcoords='offset points',
      arrowprops=dict(arrowstyle="->")
    )