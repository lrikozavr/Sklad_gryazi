# -*- coding: utf-8 -*-
from file_path import *

from logs import log_review_line,log_text_line,log_user_line,log_rate_line,log_users,log_statistic
global_class_value = ['text','review','rate','user']
global_class_value_short = ['t','re','ra','u'] # maybe unnecessary
#user class
user_class_value = ['reviewer','author','viewer']
user_class_value_short = ['r','a','v']

#whole file log
def read_file_log(filename):
    f = open(filename,'r')
    text = f.readline()
    f.close()
    return text

def write_file_log(filename,text):
    f = open(filename,'w')
    f.write(str(text))
    f.close()

#single line file log
def read_file_line(filename,length_line,number):
    f = open(filename,"rb")
    f.seek(length_line*number)
    text = f.read(length_line)
    f.close()
    return text

def rewrite_file_line(filename,length_line,number,text):
    f = open(filename,'r+')
    if(length_line== len(text)):
    #print(f.seekable())
    #if(f.seekable()):
        f.seek(length_line*number,0)
    #print(f.tell())
        f.write(text)
    else:
        Exception(f'length of line not compare with text, actual length ---> {len(text)}, length required ---> {length_line}')
    f.close()
#rewrite_file_line('1.txt',5,4,'00000')

def write_file_line(filename,text):
    f = open(filename,'a')
    f.write(text)
    f.close()

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

def get_object_id(id,user_class=user_class_value[0]): #?
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

# не узагальнена функція
# desired_id = id
# object by log_line_class
def binary_id_search(object,filename,desired_id):
    name = 'id'

    #write func to check object,filevalue and id class compatibility
    # напиши функцію перевірки сумісності вхідних даних

    def read_bin_value(name,fln,obj,adr):
        line = read_file_line(fln,obj.length,adr)
        object.line = line
        return object.read(name)
    # a = a_index, -//-, n = id
    # a_value = a_id, -//-
    def bin(a,b,n):
        a_value = read_bin_value(name,filename,object,a)
        b_value = read_bin_value(name,filename,object,b)
        c = (a+b)//2
        c_value = read_bin_value(name,filename,object,c)
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

class use_file:
    def add_file():
        return
    
    def del_file():
        return
    
    def edit_file():
        return
    
    def read_file():
        return

class text_file(log_text_line):
    d = ''    
    def add_text():
        stat = log_statistic()
        read_file_line(path_statistic_log,stat.length,0)
        text_id = ''
        # create text_id to text
        # make folder (check if folder already exist)
        # path_text_data/{text_id}
        # add line to path_text_log
        # create 'reviews_list_code' file
        # create 'author_comment' file
        # create 'data_text' file and add text from telegraph in
        # add text_id to user_log_text_id by path_user_data/{author_id}
        # change count in path_user_log, global statistic
        return
    
    def del_text():
        # change in file path_text_log value in 'delete_flag' column, from 0 to 1
        # add line to path_text_del_list
        # by some time delete all in loop
        return
    
    def restore_text():
        # change in file path_text_log value in 'delete_flag' column, from 1 to 0
        # del line in path_text_del_list
        return
    
    def edit_text():
        # change text in path_text_data/{text_id}/text_data
        # change in file path_text_log value in 'size' column
        return
    
    def read_text():
        # read text in path_text_data/{text_id}/text_data
        return
    
    def info_text(self):
        # return path_text_log
        self.line_format
        return
    
    def add_text_author_comment():
        return
    
    def del_text_author_comment():
        return
    
    def edit_text_author_comment():
        return
    
    def read_text_author_comment():
        return

class review_file(log_review_line):

    def add_review():
        return
    
    def del_review():
        return
    
    def edit_review():
        return
    
    def read_review():
        return

class rate_file(log_rate_line):

    def add_rate():
        return
    
    def del_rate():
        return
    
    def edit_rate():
        return
    
    def read_rate():
        return
    
    # need to debug
    def count_rate_average(id):
        
        # calculate average value for define user_class and return mass
        # path_rate/{id}/rates_{user_class}
        def culc(id,user_class):
            f = open(f'path_rate/{id}/rates_{user_class}','r')
            rate_line_obj = log_rate_line(user_class) 
            
            count = (f.seek(-1,2) + 1) // rate_line_obj.length #?
            
            column_count = rate_line_obj.column_index['rate'].iloc[0]
            sum = [0]*(column_count)
            #
            #mass = [[0]*(rate_line_obj.length-10) for i in range(count)]
            for i in range(count):
                f.seek(i*rate_line_obj.length,0)
                rate_line_obj.line = f.read(rate_line_obj.length)
                rate_value = rate_line_obj.read('rate')
                for j in range(column_count):
                    sum[j] += int(rate_value[j])
                #
                    #Може бути використано у функціях які будуть рахувати статистику
                    #mass[i][j] = rate_value[j]
                #
            import math                        
            for j in range(column_count):
                sum[j] = math.ceil(sum[j] / count)
            #ідея зберігати дробні варіанти середнього поки вважається непотрібною
            return sum
        
        # check id class
        object_id = get_object_id(id)
        filename = globals()[f'path_{check_class_id(id)}_log']
        # find line in path_{class}_log by binary_id_search
        number = binary_id_search(object_id,filename,id)
        
        object_id.line = read_file_line(filename,object_id.length,number)
        
        # write calculated average value for 'review_r', 'review_a', 'review_v'
        for class_name,class_name_short in user_class_value,user_class_value_short:
            mass_rate = culc(id,class_name)
            rate_text = ''
            for i in range(len(mass_rate)):
                rate_text += str(mass_rate[i])
            object_id.write(f'rates_{class_name_short}',rate_text)
         
        rewrite_file_line(filename,object_id.length,number,object_id.line)
        
        # count average for each class
        rate_dict = {
            'reviewer': '',
            'author': '',
            'viewer': '',
        }
        for class_name,class_name_short in user_class_value,user_class_value_short:
            rate_text = object_id.read(f'rates_{class_name_short}')
            sum = 0
            for j in range(len(rate_text)):
                sum += int(rate_text[j])
            avrg = round(sum / len(rate_text),2)
            rate_dict[class_name] = avrg

        return rate_dict

#class user_file():
    
####################################################

def read_main_file(chat_id,save_path):
    dirname = chat_id
    path = f'{save_path}/{dirname}'
    for line in open(f'{path}/main.txt',encoding="utf-8"):
        n_line = line.split(':')
        match n_line[0]:
            case "command":
                text_command = n_line[1].split('\n')[0]
            case "link":
                text_link = n_line[1].split('\n')[0]
                for i in range(2,len(n_line),1):
                    text_link += ':' + n_line[i].split('\n')[0]
            case "addition":
                text_addition = n_line[1].split('\n')[0]
    '''
    text_chat = []
    for line in open(f'{path}/chat.txt'):
        text_chat.append(line)
    
    return text_command,text_link,text_addition,text_chat
    '''
    return text_command,text_link,text_addition

def read_user_bio(chat_id,save_path):
    file_text = ''
    for line in open(f'{save_path}/{chat_id}/bio.txt'):
        file_text += line
    f_n = file_text['first_name']
    l_n = file_text['last_name']
    u_n = file_text['username']
    bi = file_text['bio']
    return  f_n,l_n,u_n,bi
'''
def read_chat(chat_id,save_path):
    file_main = open(f'{save_path}/{chat_id}/chat.txt','r')
    return
'''
#def write_file(chat_id,save_path,text_command,text_link,text_addition,text_chat):
def write_main_file(chat_id,save_path,text_command,text_link,text_addition):
    file_main = open(f'{save_path}/{chat_id}/main.txt','w',encoding="utf-8")
    #file_chat = open(f'{save_path}/{chat_id}/chat.txt','w')
    text_main = '\'command\':\'' + text_command + '\',' +'\'link\':[' + text_link + '],' +'\'addition\':[' + text_addition + ']'
    file_main.write(str(text_main))
    '''
    for line in text_chat:
        file_chat.write(line)
    '''
def write_chat_file(chat_id,save_path,text):
    file_chat = open(f'{save_path}/{chat_id}/chat.txt','a',encoding="utf-8")
    file_chat.write(text)

def write_user_bio(chat_id,save_path,f_n,l_n,u_n,bi):
    f = open(f'{save_path}/{chat_id}/bio.txt','w')
    line = f'\'id\': {chat_id}, \'first_name\': \'{f_n}\', \'last_name\': \'{l_n}\', \'username\': \'{u_n}\', \'bio\':\'{bio_text}\''
    f.write(f'{{line}}')
