# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

#Перевернута дія
def char_to_int(text):
    number = 0
    for i in range(len(text)):
        number += ord(text[i])*pow(256,i)
    return number

def int_to_char(number):
    number = int(number)
    text = ''
    while True:
        sym = number % 256
        text += chr(sym)
        number = number // 256
        if(number == 0):
            break
    return text

def read_value(line,a,b):
    text = ''
    for i in range(a,b+1,1):
        text += line[i]
    return text

def write_value(line,a,b,text):
    ii = 0
    new_line = ''
    for i in range(len(line)):
        if(i < a or i > b):
            new_line += line[i] 
        else:
            new_line += text[ii]
            ii += 1
    if(not len(new_line) == len(line)):
        print(f"Length log_text_line isn't whole, actual length ---> {len(new_line)}, when {len(line)} required")
    return new_line

class log_text_line:
    column_index = pd.DataFrame(np.array([[2,32,5,3,1,2,5,3,1,2],
                                            [0, 2, 34, 39, 42, 43, 45, 50, 53, 54],
                                            [1, 33, 38, 41, 42, 44, 49, 52, 53, 55]]), 
                                            columns=['number','name','author_id','size','review_m','review','rates_r','rates_a','rates_v','debates'])
    length = 56
    line = '00000000000000000000000000000000000000000000000000000000'

    def __init__(self):
        pass

    def read(self, name):
        if(len(self.line) == self.length):
            if(name == 'number' or name == 'author_id' or name == 'size' or name == 'review' or name == 'debates'):
                #binary
                return char_to_int(read_value(self.line,self.column_index[name].iloc[1],self.column_index[name].iloc[2]))
            elif(name == 'name' or name == 'size' or name == 'review_m' or name == 'rates_r' or name == 'rates_a' or name == 'rates_v'):
                return read_value(self.line,self.column_index[name].iloc[1],self.column_index[name].iloc[2])
            elif(name == 'all'):
                mass = pd.DataFrame([np.zeros(len(self.column_index.columns))],columns=self.column_index.columns)
                for column in self.column_index.columns:
                     mass[column].iloc[0] = self.read(column)
                return mass
                #print(self.line)
            else:
                print('I don`t know this column name --> ', name)
                exit()
        else:
            print(f"Length log_text_line isn't whole, actual length ---> {len(self.line)}, when {self.length} required")
            exit()

    def write(self, name, text):
        if(name == 'number' or name == 'author_id' or name == 'size' or name == 'review' or name == 'debates'):
            #binary
            if(len(int_to_char(text)) < self.column_index[name].iloc[0]):
                text = int_to_char(text)
                for iii in range(len(text), self.column_index[name].iloc[0] + 1,1):
                    text += chr(0)
                return write_value(self.line,self.column_index[name].iloc[1],self.column_index[name].iloc[2],text)
            return write_value(self.line,self.column_index[name].iloc[1],self.column_index[name].iloc[2],int_to_char(text))
        elif(name == 'name' or name == 'size' or name == 'review_m' or name == 'rates_r' or name == 'rates_a' or name == 'rates_v'):
            if(len(text) < self.column_index[name].iloc[0]):
                for iii in range(len(text), self.column_index[name].iloc[0] + 1,1):
                    text += chr(0)
            return write_value(self.line,self.column_index[name].iloc[1],self.column_index[name].iloc[2],text)
        elif(name == 'all'):
            for column in self.column_index.columns:
                self.line = self.write(column,text[column].iloc[0])
                #print(self.line)
        else:
            print('I don`t know this column name --> ', name)
            exit()
    
    def show(self):
        print(self.line)               
            
def index_column():
    mass = [2,32,5,3,1,2,5,3,1,2]
    index = 0
    index_m = []
    for i in range(len(mass)):
        index_m.append(index)#index+mass[i]-1])
        index += mass[i]
    print(index_m)
    return index_m

class log_rate_file:
    column_index = pd.DataFrame(np.array([[2,32,5,3,1,2,5,3,1,2],
                                            [0, 2, 34, 39, 42, 43, 45, 50, 53, 54],
                                            [1, 33, 38, 41, 42, 44, 49, 52, 53, 55]]), 
                                            columns=['number','name','author_id','size','review_m','review','rates_r','rates_a','rates_v','debates'])
    length = 56
    line = '00000000000000000000000000000000000000000000000000000000'
    
    def __init__(self):
        pass


#index_column()
#print(len(int_to_char(0)))
f = log_text_line()
data = pd.DataFrame(np.array([[45,'aaaaaaaaaaaaaaaaaaaaaaaaaa',8000000000,90000,'R',20000,12345,123,1,20000]]), columns=['number','name','author_id','size','review_m','review','rates_r','rates_a','rates_v','debates'])
f.write('all',data)
print(f.read('all'))
#print(f.read('name'))
#f.show()