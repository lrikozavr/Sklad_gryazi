# -*- coding: utf-8 -*-

sudoku = [[9, 1, 6, 8, 2, 5, 7, 3, 4], [2, 4, 8, 6, 7, 3, 1, 9, 5], [5, 7, 3, 4, 1, 9, 6, 8, 2], [6, 2, 7, 3, 8, 4, 9, 5, 1], [4, 3, 9, 1, 5, 7, 8, 2, 6], [1, 8, 5, 9, 6, 2, 4, 7, 3], [8, 5, 1, 2, 9, 6, 3, 4, 7], [3, 9, 2, 
7, 4, 1, 5, 6, 8], [7, 6, 4, 5, 3, 8, 2, 1, 9]]

def g(x,y):
    if(x == y):
        return 1
    else:
        return 0

def check(x,mass,ai,aj):
    sum=0
    for i in range(9):
        if(not i == ai):
            sum += g(x,mass[i][aj])
    if(sum == 1):
        return 0
    sum=0
    for j in range(9):
        if(not j == aj):
            sum += g(x,mass[ai][j])
    if(sum == 1):
        return 0
    sum=0
    for i in range(3*(ai // 3),3*(ai // 3) + 3,1):
        for j in range(3*(aj // 3),3*(aj // 3) + 3,1):
            if(not i==ai and not j==aj):
                sum += g(x,mass[i][j])   
    if(sum == 1):
        return 0
    return 1

def temp(x,mass,i):
    sum_ch = 0
    t_m = []
    for n in range(9):
        if (mass[i][n] == 0):
            ch = check(x,mass,i,n)
            sum_ch += ch
            if(ch == 1):
                t_m.append(n)
    return sum_ch,t_m

def farvision(x,mass,i):
    e_m = []
    sum_ch, t_m = temp(x,mass,i)    
    if (len(t_m) == 0):
        #print("something wrong")
        return 0, 0
    if(i==8):
        mass[i][t_m[0]] = x
        return 1, t_m
    for m in t_m:
        mass[i][m] = x
        rez, r_m = farvision(x,mass,i+1)
        if(rez == 0):
            mass[i][m] = 0
            continue
        else:
            e_m.append(m)
            for g in r_m:
                e_m.append(g)
            return rez, e_m
    return 0, 0
    

import random

mass = [[0]*9 for i in range(9)]
k=4
for x in range(1,k,1):
    #print(mmm,mass)
    for i in range(9):
        sum_ch,t_m = temp(x,mass,i)
        if(len(t_m) == 0):
            print("something wrong")
            exit()
        
        mass_index = []
        if(i!=8):
            for m in t_m:
                mass[i][m] = x
                sum_ch1, t_m1 = temp(x,mass,i+1)
                if(sum_ch1 > 0):
                    mass_index.append(m)
                mass[i][m] = 0

            if(len(mass_index)==0):
                print(2 // 3)
                print("not ok")
                exit()
            
            #min = 100
            max_index = 0
            sub_mass_index = []
            for m in mass_index:
                sum_weight = 0
                for jj in range(3*(m // 3),3*(m // 3) + 3,1):
                    if(mass[i][jj] == 0):
                        sum_weight += 1
                sub_mass_index.append(sum_weight)
            
            temp_sub_mass_index = []
            s_sum = 0
            for s in sub_mass_index:
                s_sum += s
            s_avr = s_sum / len(sub_mass_index)
            for s in range(len(sub_mass_index)):
                if(sub_mass_index[s] >= s_avr):
                    temp_sub_mass_index.append(mass_index[s])
            
            j = temp_sub_mass_index[int(random.random()*(len(temp_sub_mass_index)))]
            #j = mass_index[int(random.random()*(len(mass_index)))]
            #j = max_index
            mass[i][j] = x           
        else:
            j = t_m[int(random.random()*(len(t_m)))]
            mass[i][j] = x
        #j = t_m[len(t_m)-1]
        #print(x,sum_ch,t_m,mass_index,j,sub_mass_index)
for x in range(k,10,1):
    rez, mmm = farvision(x,mass,0)   
#sum = 0
for i in range(9):
    for j in range(9):
        #if(check(sudoku[i][j],sudoku,i,j) == 0):
        #    print('not_working')
        #sum += sudoku[i][j]
        if(check(mass[i][j],mass,i,j) == 0):
            print("not working")
#print(sum)
print(mass)
for i in range(9):
    print(mass[i])

