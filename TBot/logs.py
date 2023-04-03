# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

from file_path import path_review_log,path_statistic_log,path_text_log,path_user_log,path_rate_log


# виводить назву класу до якого належить це id
# не узагальнена функція
def check_class_id(id):
    n = str(id)
    match n[0]:
        case '1':
            return 'rate'
        case '9':
            return 'user'
        case '8':
            return 'review'
        case '7':
            return 'text'
        case _:
            Exception('unknown id number --> ', id)
# виводить номер об'єкту класу виходячи зі значення id
# не узагальнена функція
def get_number_id(id):
    match check_class_id(id):
        case 'rate':
            return id - 1e+10
        case 'user':
            return id - 9e+9
        case 'review':
            return id - 8e+9
        case 'text':
            return id - 7e+9

def get_object_id(id,user_class='reviewer'): #?
    match check_class_id(id):
        case 'rate':
            value = log_rate_line(user_class=user_class)
            return value
        case 'user':
            value = log_user_line()
            return value
        case 'review':
            value = log_review_line()
            return value
        case 'text':
            value = log_text_line()
            return value
# виводить індекс класу, який використовується в id
def get_class_index(name_class):
    match name_class:
        case 'rate':
            return 10
        case 'user':
            return 9
        case 'review':
            return 8
        case 'text':
            return 7
        case _:
            raise Exception('unknown class name --> ', name_class)


# Convert chat to int
def char_to_int(text):
    text = str(text)
    number = 0
    for i in range(len(text)):
        number += ord(text[i])*pow(256,i)
    return number

# Convert int to char
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

# read text from line by [a,b] range
def read_value(line,a,b):
    text = ''
    for i in range(a,b+1,1):
        text += line[i]
    return text

# write text in line by [a,b] range
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

class log_file:
    def __init__(self):
        pass
    
    # filename ще можна задавати автоматично, якщо знати назву класу об'єкту
    def __init__(self,filename):
        #filename = globals()[f'path_{class_name}_log']
        self.filename = filename
    
    #single line file log
    def read_file_line(self,number):
        f = open(self.filename,"rb")
        f.seek(self.length*number)
        self.line = f.read(self.length)
        f.close()

    def rewrite_file_line(self,number):
        f = open(self.filename,'r+')
        if(self.length == len(self.line)):
        #print(f.seekable())
        #if(f.seekable()):
            f.seek(self.length*number,0)
            f.write(self.line)
        else:
            Exception(f'length of line not compare with text, actual length ---> {len(self.line)}, length required ---> {self.length}')
        f.close()
    #rewrite_file_line('1.txt',5,4,'00000')

    def write_file_line(self):
        f = open(self.filename,'a')
        f.write(self.line)
        f.close()
    
    def read_file_line_value(self,name,number_line):
        f = open(self.filename,'rb')
        f.seek(self.length*number_line,0)
        f.seek(self.column_index[name].iloc[1],1)
        text = f.read(self.column_index[name].iloc[0])
        f.close()
        if(name in self.bin_value_name_mass):
            text = char_to_int(text)
        return text
    # додати конвертер значень, бо воно просто видає у бінарному вигляді і нормально не інтерпретується
    # він до цього вже був, я ж не настільки далекий від реальності
    def rewrite_file_line_value(self,name,number_line,text):
        f = open(self.filename,'r+')
        f.seek(self.length*number_line,0)
        f.seek(self.column_index[name].iloc[1],1)
        if(name in self.bin_value_name_mass):
            text = int_to_char(text)
        if(len(text) < self.column_index[name].iloc[0]):
            for iii in range(len(text), self.column_index[name].iloc[0] + 1,1):
                text += chr(0)
        f.write(text)
        f.close()

    def binary_id_search(self,desired_id):
        name = 'id'

        #write func to check object,filevalue and id class compatibility
        # напиши функцію перевірки сумісності вхідних даних

        # a = a_index, -//-, n = id
        # a_value = a_id, -//-
        def bin(a,b,n):
            a_value = self.read_file_line_value(name, a) #read_bin_value(name,filename,object,a)
            b_value = self.read_file_line_value(name, b) #read_bin_value(name,filename,object,b)
            c = (a+b)//2
            c_value = self.read_file_line_value(name, c)
            if(a_value < n and c_value >= n):
                return bin(a,c,n)
            elif(c_value < n and b_value > n):
                return bin(c,b,n)
            elif(n == a_value or n == b_value):
                if(n == a_value):
                    return a
                if(n == b_value):
                    return b

        return bin(0,get_number_id(desired_id),desired_id)

class log_line:
    def set_line(self,line):
        self.line = line

    def read_line(self,name):
        if(len(self.line) == self.length):
            if(name in self.bin_value_name_mass):
                    return char_to_int(read_value(self.line,self.column_index[name].iloc[1],self.column_index[name].iloc[2]))
            elif(name in self.str_value_name_mass):
                    return read_value(self.line,self.column_index[name].iloc[1],self.column_index[name].iloc[2])
            elif(name == 'all'):
                mass = pd.DataFrame([np.zeros(len(self.column_index.columns))],columns=self.column_index.columns)
                for column in self.column_index.columns:
                    mass[column].iloc[0] = self.read(column)
                return mass
            else:
                raise Exception('I don`t know this column name --> ', name)
        else:
            raise Exception(f"Length log_text_line isn't whole, actual length ---> {len(self.line)}, when {self.length} required")


    def write_sup_func(self,name,text):
        if(len(text) < self.column_index[name].iloc[0]):
            for iii in range(len(text), self.column_index[name].iloc[0] + 1,1):
                text += chr(0)
        elif(len(text) > self.column_index[name].iloc[0]):
            print(f"{name} have value out of limit")
        return write_value(self.line,self.column_index[name].iloc[1],self.column_index[name].iloc[2],text)
    
    def write_line(self, name, text):
        if(name in self.bin_value_name_mass):
            if(not type(text) is int):
                text = int(text)
            text = int_to_char(text)
            self.line = self.write_sup_func(name,text)
        elif(name in self.str_value_name_mass):
            if(not type(text) is str):
                text = str(text)
            self.line = self.write_sup_func(name,text)
        elif(name == 'all'):
            for column in self.column_index.columns:
                self.write(column,text[column].iloc[0])
        else:
            raise Exception('I don`t know this column name --> ', name)

    def line_format(self):
        output_line = 'column\tsize\tplace\n'
        for column in self.column_index.columns:
            output_line += f'{column}\t{self.column_index[column].iloc[0]}\t{self.column_index[column].iloc[1]}{self.column_index[column].iloc[2]}\t'
            output_line += self.read_line(column)
            output_line += '\n'
        #print(output_line)
        return output_line

    def show(self):
        print(self.line)

class log_text_line(log_line,log_file):
    # 7000000000
    index_value = 7e+9
    filename = path_text_log
    class_name = 'text'
    # line struct
    column_index = pd.DataFrame(np.array([[1,5,5,3,1,2,5,3,1,2],
                                            [0, 1, 6, 11, 14, 15, 17, 22, 25, 26],
                                            [0, 5, 10, 13, 14, 16, 21, 24, 25, 27]]), 
                                            columns=['delete_flag','id','author_id','size','review_m','review','rates_r','rates_a','rates_v','debates'])
    bin_value_name_mass = ['id','author_id','size','review','debates']
    str_value_name_mass = ['delete_flag','review_m','rates_r','rates_a','rates_v']
    
    length = column_index[column_index.columns[len(column_index.columns)-1]].iloc[2] + 1
    line = [chr(0) for i in range(length)]

    def __init__(self):
        pass


class log_review_line(log_line,log_file):
    # 8000000000
    index_value = 8e+9
    filename = path_review_log
    class_name = 'review'
    # line struct
    column_index = pd.DataFrame(np.array([[1,5,5,5,2,5,3,1,1],
                                            [0, 1, 6, 11, 16, 18, 23, 26, 27],
                                            [0, 5, 10, 15, 17, 22, 25, 26, 27]]), 
                                            columns=['delete_flag','text_id','id','author_id','size','rates_r','rates_a','rates_v','deep'])
    bin_value_name_mass = ['text_id','id','author_id','size','deep']
    str_value_name_mass = ['delete_flag','rates_r','rates_a','rates_v']
    
    length = column_index[column_index.columns[len(column_index.columns)-1]].iloc[2] + 1
    line = [chr(0) for i in range(length)]
    
    def __init__(self):
        pass

class log_rate_line(log_line,log_file):
    # 10000000000
    index_value = 1e+10
    filename = path_rate_log
    class_name = 'rate'
    # line struct
    column_index = pd.DataFrame(np.array([[1,5,5,5,1],
                                          [0, 1, 6, 11, 16],
                                          [0, 5, 10, 15, 16]]), 
                                            columns=['delete_flag','text_id','id','author_id','user_class'])
    bin_value_name_mass = ['text_id','id','author_id']
    str_value_name_mass = ['delete_flag','user_class']

    length = column_index[column_index.columns[len(column_index.columns)-1]].iloc[2] + 1
    line = [chr(0) for i in range(length)]

    def __init__(self):
        pass

from file_path import rates_author,rates_reviewer,rates_viewer,path_rate_data
class log_rate_file(log_line,log_file):

    def __init__(self,user_class,reted_id):
        self.bin_value_name_mass = ['id','author_id']
        self.str_value_name_mass = ['rate']
        match user_class:
            case 'reviewer':
                self.column_index = pd.DataFrame(np.array([[5,5,5],
                                          [0, 5, 10],
                                          [4, 9, 14]]), 
                                            columns=['rate','id','author_id'])
                self.filename = f'{path_rate_data}/{reted_id}/{rates_reviewer}'
            case 'author':
                self.column_index = pd.DataFrame(np.array([[3,5,5],
                                          [0, 3, 8],
                                          [2, 7, 12]]), 
                                            columns=['rate','id','author_id'])
                self.filename = f'{path_rate_data}/{reted_id}/{rates_author}'
            case 'viewer':
                self.column_index = pd.DataFrame(np.array([[1,5,5],
                                          [0, 1, 6],
                                          [0, 5, 10]]), 
                                            columns=['rate','id','author_id'])
                self.filename = f'{path_rate_data}/{reted_id}/{rates_viewer}'
            case _:
                Exception('go fuck yourself')
        self.length = self.column_index[self.column_index.columns[len(self.column_index.columns)-1]].iloc[2] + 1
        self.line = [chr(0) for i in range(self.length)]


class log_user_line(log_line,log_file):
    # 9000000000
    index_value = 9e+9
    filename = path_user_log
    class_name = 'user'
    # line struct
    column_index = pd.DataFrame(np.array([[1,5,5,1,2,2,2,3,5,3,1,2],
                                          [0, 1, 6, 11, 12, 14, 16, 18, 21, 26, 29, 30],
                                          [0, 5, 10, 11, 13, 15, 17, 20, 25, 28, 29, 31]]), 
                                            columns=['delete_flag','id','tg_id','class','age','count_t','count_re','count_ra','rates_r','rates_a','rates_v','rep'])
    bin_value_name_mass = ['id','tg_id','age','count_t','count_re','count_ra','rep']
    str_value_name_mass = ['delete_flag','class','rates_r','rates_a','rates_v']
    
    length = column_index[column_index.columns[len(column_index.columns)-1]].iloc[2] + 1
    line = [chr(0) for i in range(length)]
    
    def __init__(self):
        pass
    

import json
from file_path import path_user_data,users_log_bio,users_log_rate_id,users_log_review_id,users_log_text_id
class log_user_file(log_line,log_file):
    
    def __init__(self, name, tg_id):
        match name:
            case 'bio':    
                self.column_index = pd.DataFrame(np.array([[128,5,5,128,128,1024],
                                                            [0, 128, 133, 138, 266, 394],
                                                            [127, 132, 137, 265, 393, 1417]]), 
                                                            columns=['name','id','tg_id','command','status','bio'])
                self.filename = f'{path_user_data}/{tg_id}/{users_log_bio}'
                self.bin_value_name_mass = ['id','tg_id']
                self.str_value_name_mass = ['name','command','status','bio']

            case 'text_id' | 'review_id' | 'rate_id':
                # for review_id and text_id at once
                self.column_index = pd.DataFrame(np.array([[5],
                                                            [0],
                                                            [4]]), 
                                                            columns=['id'])
                name_log = globals()[f'users_log_{name}']
                self.filename = f'{path_user_data}/{tg_id}/{name_log}'
                self.bin_value_name_mass = ['id']
                self.str_value_name_mass = []

        self.length = self.column_index[self.column_index.columns[len(self.column_index.columns)-1]].iloc[2] + 1
        self.line = [chr(0) for i in range(self.length)]


class log_statistic(log_line,log_file):
    filename = path_statistic_log
    class_name = 'statistic'
    column_index = pd.DataFrame(np.array([[5,5,5,5,5,5,5,5],
                                          [0, 5, 10, 15, 20, 25, 30, 35],
                                          [4, 9, 14, 19, 24, 29, 34, 39]]), 
                                            columns=['now_count_text','now_count_review','now_count_rate','now_count_user','all_count_text','all_count_review','all_count_rate','all_count_user'])
    bin_value_name_mass = ['now_count_text','now_count_review','now_count_rate','now_count_user','all_count_text','all_count_review','all_count_rate','all_count_user']
    str_value_name_mass = []
    length = column_index[column_index.columns[len(column_index.columns)-1]].iloc[2] + 1
    line = [chr(0) for i in range(length)]
    
    def __init__(self):
        pass

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

index_column([1,5,5,5,1])
#index_column([5,5,5])
#index_column([3,5,5])
#index_column([1,5,5])

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
data = pd.DataFrame(np.array([[0,7000000045,9000000001,90000,'R',20000,12345,123,1,20000]]), columns=['delete_flag','id','author_id','size','review_m','review','rates_r','rates_a','rates_v','debates'])
f.write('all',data)
print(f.read('all'))
f.write('size','90')
print(f.read('all'))
print(f.read('id'))
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