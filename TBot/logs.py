# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

#Перевернута дія
def char_to_int(text):
    text = str(text)
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

def read_file_line(filename,length_line,number):
    f = open(filename,"r")
    f.seek(length_line*number)
    text = f.read(length_line)
    f.close()
    return text

def write_file_line(filename,text):
    f = open(filename,'a')
    f.write(text)
    f.close()

class log_line:
    def set_line(self,line):
        self.line = line

    def read_func(self,name,flag):
        match flag:
            case 1: 
                return char_to_int(read_value(self.line,self.column_index[name].iloc[1],self.column_index[name].iloc[2]))
            case 2:
                return read_value(self.line,self.column_index[name].iloc[1],self.column_index[name].iloc[2])
            case 0:
                mass = pd.DataFrame([np.zeros(len(self.column_index.columns))],columns=self.column_index.columns)
                for column in self.column_index.columns:
                    mass[column].iloc[0] = self.read(column)
                return mass
                #print(self.line)
            case _:
                raise Exception('I don`t know this column name --> ', name)

    def write_sup_func(self,name,text):
        if(len(text) < self.column_index[name].iloc[0]):
            for iii in range(len(text), self.column_index[name].iloc[0] + 1,1):
                text += chr(0)
        elif(len(text) > self.column_index[name].iloc[0]):
            print(f"{name} have value out of limit")
        return write_value(self.line,self.column_index[name].iloc[1],self.column_index[name].iloc[2],text)
    
    def write_func(self, name, text, flag):
        match flag:
            case 1:
                #можлива помилка
                if(not type(text) is int):
                    text = int(text)
                text = int_to_char(text)
                self.line = self.write_sup_func(name,text)
            case 2:
                if(not type(text) is str):
                    text = str(text)
                self.line = self.write_sup_func(name,text)
            case 0:
                for column in self.column_index.columns:
                    self.write(column,text[column].iloc[0])
            case _:
                raise Exception('I don`t know this column name --> ', name)

    def show(self):
        print(self.line)

class log_text_line(log_line):
    column_index = pd.DataFrame(np.array([[5,5,3,1,2,5,3,1,2],
                                            [0, 5, 10, 13, 14, 16, 21, 24, 25],
                                            [4, 9, 12, 13, 15, 20, 23, 24, 26]]), 
                                            columns=['text_id','author_id','size','review_m','review','rates_r','rates_a','rates_v','debates'])
    length = 27
    line = [chr(0) for i in range(length)]

    def __init__(self):
        pass

    def read(self, name):
        if(len(self.line) == self.length):
            match name:
                case 'text_id' | 'author_id' | 'size' | 'review' | 'debates':
                    return self.read_func(name,1)
                case 'review_m' | 'rates_r' | 'rates_a' | 'rates_v':
                    return self.read_func(name,2)
                case 'all':
                    return self.read_func(name,0)
                case _:
                    self.read_func(name, -1)
        else:
            raise Exception(f"Length log_text_line isn't whole, actual length ---> {len(self.line)}, when {self.length} required")

    def write(self, name, text):
            match name:
                case 'text_id' | 'author_id' | 'size' | 'review' | 'debates':
                    return self.write_func(name,text,1)
                case 'review_m' | 'rates_r' | 'rates_a' | 'rates_v':
                    return self.write_func(name,text,2)
                case 'all':
                    return self.write_func(name,text,0)
                case _:
                    self.write_func(name,text, -1)


class log_review_line(log_line):
    column_index = pd.DataFrame(np.array([[5,5,5,2,5,3,1,1],
                                            [0, 5, 10, 15, 17, 22, 25, 26],
                                            [4, 9, 14, 16, 21, 24, 25, 26]]), 
                                            columns=['text_id','review_id','author_id','size','rates_r','rates_a','rates_v','deep'])
    length = 27
    line = [chr(0) for i in range(length)] #'00000000000000000000'
    
    def __init__(self):
        pass
    
    def read(self, name):
        if(len(self.line) == self.length):
            match name:
                case 'text_id' | 'review_id' | 'author_id' | 'size' | 'deep':
                    return self.read_func(name,1)
                case 'rates_r' | 'rates_a' | 'rates_v':
                    return self.read_func(name,2)
                case 'all':
                    return self.read_func(name,0)
                #print(self.line)
                case _:
                    self.read_func(name,-1)
        else:
            raise Exception(f"Length log_review_line isn't whole, actual length ---> {len(self.line)}, when {self.length} required")

    def write(self, name, text):
        match name:
            case 'text_id' | 'review_id' | 'author_id' | 'size' | 'deep':
                self.write_func(name,text,1)
            case 'rates_r' | 'rates_a' | 'rates_v':
                self.write_func(name,text,2)
            case 'all':
                self.write_func(name,text,0)
            case _:
                self.write_func(name,text,-1)
    

class log_user_line(log_line):
    column_index = pd.DataFrame(np.array([[5,1,2,2,2,3,5,3,1,2],
                                          [0, 5, 6, 8, 10, 12, 15, 20, 23, 24],
                                          [4, 5, 7, 9, 11, 14, 19, 22, 23, 25]]), 
                                            columns=['id','class','age','count_t','count_r','count_rate','rates_r','rates_a','rates_v','rep'])
    length = 26
    line = [chr(0) for i in range(length)]
    
    def __init__(self):
        pass
    
    def read(self, name):
        if(len(self.line) == self.length):
            match name:
                case 'id' | 'age' | 'count_t' | 'count_r' | 'count_rate' | 'rep':
                    return self.read_func(name,1)
                case 'class' | 'rates_r' | 'rates_a' | 'rates_v':
                    return self.read_func(name,2)
                case 'all':
                    return self.read_func(name,0)
                #print(self.line)
                case _:
                    self.read_func(name,-1)
        else:
            raise Exception(f"Length log_review_line isn't whole, actual length ---> {len(self.line)}, when {self.length} required")
            

    def write(self, name, text):
        match name:
            case 'id' | 'age' | 'count_t' | 'count_r' | 'count_rate' | 'rep':
                self.write_func(name,text,1)
            case 'class' | 'rates_r' | 'rates_a' | 'rates_v':
                self.write_func(name,text,2)
            case 'all':
                self.write_func(name,text,0)
            case _:
                self.write_func(name,text,-1)

import json

def read_file_log(filename):
    f = open(filename,'r')
    text = f.readline()
    f.close()
    return text

def write_file_log(filename,text):
    f = open(filename,'w')
    f.write(str(text))
    f.close()

class log_users:
    
    bio = {
        "name": "",
        "number": "",
        "command": "",
        "status": "",
        "bio": "",
    }
    data = {
        "text_id": "",
        "review_id": "",
    }

    def __init__(self):
        pass

    def give(self,text,flag):
        if(flag == 'data'):
            self.data = json.loads(text)
        elif(flag == 'bio'):
            self.bio = json.loads(text)
        else:
            raise Exception(f"log_users don't have [{flag}] atribute")
        
    def get(self,flag):
        if(flag == 'data'):
            return json.dumps(self.data)
        elif(flag == 'bio'):
            return json.dumps(self.bio)
        else:
            raise Exception(f"log_users don't have [{flag}] atribute")

    def read(self,name):
        if name in self.data:
            return self.data[name]
        elif name in self.bio:
            return self.bio[name]
        else:
            raise Exception(f"log_users don't have [{name}] atribute")
    
    def write(self,name,text):
        if name in self.data:
            self.data[name] = text
        elif name in self.bio:
            self.bio[name] = text
        else:
            raise Exception(f"log_users don't have [{name}] atribute")



def index_column(mass):
    #mass = [3,5,2,5,3,1,1]
    index = 0
    index_m_1, index_m_2 = [], []
    for i in range(len(mass)):
        index_m_1.append(index)
        index_m_2.append(index+mass[i]-1)#index+mass[i]-1])
        index += mass[i]
    print(index_m_1)
    print(index_m_2)
    print(index_m_2[len(mass)-1]+1)
    '''
    line = ''
    for i in range(index_m_2[len(mass)-1]):
        line += chr(0)
    print(len(line))
    print(f'/{line}/')
    #return index_m
    '''

#index_column([5,5,5,2,5,3,1,1])
'''
g = log_users()
g.write('text_id',100101010)
g.write('review_id',100101010)
g.write('name',1)
print(g.read('text_id'))
print(g.get('bio'))
write_file_log('1.txt',g.get('data'))
h = log_users()
h.give(read_file_log('1.txt'),'data')
print(h.get('data'))
print(h.read('text_id'))
'''
#print(f.read('text_i'))
'''
#print(len(int_to_char(0)))
f = log_text_line()
data = pd.DataFrame(np.array([[45,'aaaaaaaaaaa',8000000000,90000,'R',20000,12345,123,1,20000]]), columns=['number','name','author_id','size','review_m','review','rates_r','rates_a','rates_v','debates'])
f.write('all',data)
print(f.read('all'))
f.write('size','0')
print(f.read('all'))
#print(f.read('name'))
#f.show()

g = log_review_line()
data = pd.DataFrame(np.array([[1111,1145,800000000,7000,12040,123,1,20]]), columns=['text_id','review_id','author_id','size','rates_r','rates_a','rates_v','deep'])
g.write('all',data)
print(g.read('all'))
g.write('all',g.read('all'))

write_file_line('2.txt',g.line)

print(read_file_line('2.txt',27,1))

g.line = read_file_line('2.txt',27,1)
print(g.read('all'))
'''