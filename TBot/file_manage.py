# -*- coding: utf-8 -*-
from file_path import *
import pandas as pd
import numpy as np

from logs import log_review_line,log_text_line,log_user_line,log_user_file,log_rate_line,log_rate_file,log_statistic
from logs import get_object_id,get_number_id,check_class_id,get_class_index
#class
global_class_value_short = {
    'text': 't',
    'review': 're',
    'rate': 'ra',
    'user': 'u'
}
#user class
global_user_class_value_short = {
    'reviewer': 'r',
    'author': 'a',
    'viewer': 'v'
}


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

################################################################
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

# не узагальнена функція
# desired_id = id
# object by log_line_class
def binary_id_search(object,filename,desired_id):
    name = 'id'
    # не дає вийти значенню номеру за межі файлу
    f = open(filename,'r')
    f.seek(-0,2) #f.seek(-self.length,2)
    border = f.tell() // object.length
    if(get_number_id(desired_id) < border):
        border = get_number_id(desired_id)
    f.close()
    #write func to check object,filevalue and id class compatibility
    # напиши функцію перевірки сумісності вхідних даних
    def read_bin_value(name,fln,obj,adr):
        line = read_file_line(fln,obj.length,adr)
        object.line = line
        return object.read(name)
    # a = a_index, -//-, n = id
    # a_value = a_id, -//-
    def bin(a,b,n):
        if(a == b):
            return -1        
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

    return bin(0,border,desired_id)
################################################################

import os
from file_path import user_log_bio,user_log_rate_id,user_log_review_id,user_log_text_id
from file_path import path_text_del_list,path_review_del_list,path_user_del_list,path_rate_del_list
class use_file:
    def create_id(self):
        stat = log_statistic()
        all_count_class_name = stat.read_file_line_value(f'all_count_{self.class_name}',0)
        index = str(get_class_index(self.class_name))
        null_line = [chr(0) for i in range(9 - len(str(all_count_class_name)))]
        id = index + null_line + str(all_count_class_name)
        return id
    
    def create_directory(self,name):
        save_path = globals()[f'path_{self.class_name}_data']
        dir_name = f"{save_path}/{name}"
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)

    def stat_increment(self):
        stat = log_statistic()
        all_count_class_name = stat.read_file_line_value(f'all_count_{self.class_name}',0)
        now_count_class_name = stat.read_file_line_value(f'now_count_{self.class_name}',0)
        stat.rewrite_file_line_value(f'all_count_{self.class_name}',0,int(all_count_class_name)+1)
        stat.rewrite_file_line_value(f'now_count_{self.class_name}',0,int(now_count_class_name)+1)
    
    def add_delete(self,id):
        path_delete = globals()[f'path_{self.class_name}_del_list']
        filename = path_delete
        self.write_file_line_value(filename,'id',id)
    
    def change_average_once(self,average,new_rate,n,flag):
        def increment(average,new,n):
            if(n > 0):
                return average + (new - average)/(n+1)
            else:
                raise Exception('division by zero')
        def decrement(average,old,n):
            if(n > 1):
                return average - (old - average)/(n-1)
            else:
                raise Exception('division by zero')
        new_average = [0]*len(average)
        if(flag):
            for i in range(len(average)):
                new_average[i] = increment(int(average[i]),int(new_rate[i]),n)
        else:
            for i in range(len(average)):
                new_average[i] = decrement(int(average[i]),int(new_rate[i]),n)
        new_str_average = ''
        for i in range(len(average)):
            new_str_average += new_average[i]
        return new_str_average

    def add_file(self,users_tg_id,text,reviewed_id=10000000001,user_class='viewer'):
        #create id
        id = self.create_id()
        # Додай перевірку існування для текстів та рев'ю
        match self.class_name:
            case 'user':
                # path
                path_data = globals()[f'path_{self.class_name}_data'] + '/' + str(users_tg_id)
                #
                self.create_directory(users_tg_id)
                #open(f'{path_data}/{user_log_bio}','w').close()
                open(f'{path_data}/{user_log_text_id}','w').close()
                open(f'{path_data}/{user_log_review_id}','w').close()
                open(f'{path_data}/{user_log_rate_id}','w').close()
                #
                line = pd.DataFrame(np.array([0,id,users_tg_id,global_user_class_value_short[user_class],0,0,0,0,00000,000,0,0,0,0,0]), columns=self.column_index.columns)
                self.write_line('all',line)
                self.write_file_line()                
                del line
                #
                user_file = log_user_file('bio',users_tg_id)
                user_file.write_line('all',text)
                user_file.write_file_line()
                del user_file
            case 'text' | 'review' | 'rate':
                # get user_id
                user = log_user_file('bio',users_tg_id)
                user_id = user.read_file_line_value('id',0)
                del user
                # make folder (check if folder already exist) path_{class_names}_data/{id}/{class_names}_data
                match self.class_name:
                    case 'text' | 'rate':
                        # path
                        path_data = globals()[f'path_{self.class_name}_data'] + '/' + str(id)
                        #
                        self.create_directory(id)
                        # create data_file and fill by text
                        filename_data = globals()[f'{self.class_name}_data']
                        f = open(f'{path_data}/{filename_data}','w')
                        f.write(text)
                        f.close()
                    case 'rate':
                        self.create_directory(reviewed_id)
                        #Додай перевірку чи робив це юзер до цього
                        rate_object = log_rate_file(user_class,reviewed_id)
                        if(os.path.isfile(self.filename)):
                            if(rate_object.binary_id_search(reviewed_id) != -1):
                                del rate_object
#########################################################################################################################################
                                return 'Rate for this text already exist'
#########################################################################################################################################
                        #Додав
                #additional file
                match self.class_name:
                    case 'text':
                        line = pd.DataFrame(np.array([0,id,user_id,len(text),'W',0,00000,000,0,0,0,0,0]), columns=self.column_index.columns)
                        self.write_line('all',line)
                        self.write_file_line()
                        # create 'reviews_list_code' file
                        open(f'{path_data}/{text_reviews_code}','w').close()
                        # create 'author_comment' file
                        open(f'{path_data}/{text_author_comment}','w').close()
                        del line
                    case 'review':
                        line = pd.DataFrame(np.array([0,reviewed_id,id,user_id,len(text),00000,000,0,0,0,0,0]), columns=self.column_index.columns)
                        self.write_line('all',line)
                        self.write_file_line()
                        del line
                        # Додай збільшення count в логу тексту і може ще десь
                        text_object = log_text_line()
                        number_line = text_object.binary_id_search(reviewed_id)
                        review_count = text_object.read_file_line_value('review_count',number_line)
                        text_object.rewrite_file_line_value('review_count',number_line,review_count + 1)
                        del text_object
                        # Додав
                    case 'rate':
                        # Додай зміну середнього значення
                        reviewed_object = get_object_id(reviewed_id)
                        number_line = reviewed_object.binary_id_search(reviewed_id)
                        average_rate = reviewed_object.read_file_line_value(f'rates_{global_user_class_value_short[user_class]}',number_line)
                        count_rate = reviewed_object.read_file_line_value(f'rates_{global_user_class_value_short[user_class]}_count',number_line)
                        new_average_rate = self.change_average_once(average_rate,text,count_rate,1)
                        reviewed_object.rewrite_file_line_value(f'rates_{global_user_class_value_short[user_class]}',number_line,new_average_rate)
                        reviewed_object.rewrite_file_line_value(f'rates_{global_user_class_value_short[user_class]}_count',number_line,count_rate+1)
                        del reviewed_object
                        # Додав
                        line = pd.DataFrame(np.array([0,reviewed_id,id,user_id,user_class]), columns=self.column_index.columns)
                        self.write_line('all',line)
                        self.write_file_line()
                        del line
                        #
                        rate_file = log_rate_file(user_class,reviewed_id)
                        line = pd.DataFrame(np.array([text,id,user_id,0]), columns=rate_file.column_index.columns)
                        rate_file.write_line('all',line)
                        rate_file.write_file_line()                                                
                        del rate_file

                # add line to users class_name_id
                user = log_user_file(f'{self.class_name}_id',users_tg_id)
                user.write_line('id',id)
                user.write_file_line()
                del user
                # change count in path_user_log
                user = log_user_line()
                number_line = user.binary_id_search(user_id)
                count_text = user.read_file_line_value(f'çount_{global_class_value_short[self.class_name]}',number_line)
                user.rewrite_file_line_value(f'çount_{global_class_value_short[self.class_name]}',number_line,count_text + 1)
                del user
        # change count in global_statistic
        self.stat_increment()
        #return  'ok'
    
    def delete_file(self,id,user_class = 'viewer'):
        number_line = self.binary_id_search(id)
        self.rewrite_file_line_value('delete_flag',number_line,1)
        self.add_delete(id)
        if(self.class_name == 'rate'):
            rated_id = self.read_file_line_value('text_id')
            rate_data = log_rate_file(user_class,rated_id)
            number_line = rate_data.binary_id_search(id)
            rate_data.rewrite_file_line_value('delete_flag',number_line,1)
            del rate_data
        #return 'ok'
    
    def restore_file(self,id,user_class = 'viewer'):
        number_line = self.binary_id_search(id)
        self.rewrite_file_line_value('delete_flag',number_line,0)        
        if(self.class_name == 'rate'):
            rated_id = self.read_file_line_value('text_id')
            rate_data = log_rate_file(user_class,rated_id)
            number_line = rate_data.binary_id_search(id)
            rate_data.rewrite_file_line_value('delete_flag',number_line,0)
            del rate_data
        #return 'ok'
    # Для кожного різне
    #def edit_file(self):
    #    return
    # Для кожного різне
    #def read_file():
    #    return

class user_file(log_user_line,use_file):
    
    def __init__(self):
        pass

    def __init__(self,tg_id):
        self._users_bio = log_user_file('bio',tg_id)
        self._users_text_id = log_user_file('text_id',tg_id)
        self._users_review_id = log_user_file('review_id',tg_id)
        self._users_rate_id = log_user_file('rate_id',tg_id)

    def edit_user():
        #edit users files
        return
    
    def show_first_n_line(self,class_name):
        
        match class_name:
            case 'text':
                class_object_users = self._users_text_id
                class_object = log_text_line()
            case 'rate':
                class_object_users = self._users_rate_id
                class_object = log_rate_line()
            case 'review':
                class_object_users = self._users_review_id
                class_object = log_review_line()
        number_line = 0
        #for
        class_name_id_value = class_object_users.read_file_line_value('id',number_line*class_object_users.length)
        number_line = class_object.binary_id_search(class_name_id_value)
        match class_name:
            case 'text' | 'review':
                
            case 'rate':
                    

    def info():
        #write 'bio', and log
        return

class text_file(log_text_line,use_file):
    
    def edit_text(self,text_id,text):
        # change text in path_text_data/{text_id}/text_data
        path_data = globals()[f'path_{self.class_name}_data'] + '/' + str(text_id)
        f = open(f'{path_data}/{text_data}','w')
        f.write(text)
        f.close()
        # change in file path_text_log value in 'size' column
        size = len(text)
        #
        number_line = self.binary_id_search(text_id)
        self.rewrite_file_line_value('size',number_line,size)
        #return
    
    def read_text(self,text_id):
        # read text in path_text_data/{text_id}/text_data
        number_line = self.binary_id_search(text_id)
        size = self.read_file_line_value('size',number_line)
        path_data = globals()[f'path_{self.class_name}_data'] + '/' + str(text_id)
        f = open(f'{path_data}/{text_data}','r')
        text = f.read(size)
        return text
    
    def info_text(self,text_id):
        # return path_text_log
        number_line = self.binary_id_search(text_id)
        self.read_file_line(number_line)
        return self.line_format()
    
    def add_text_author_comment():
        #create file
        #add text
        return
    
    def del_text_author_comment():
        #delete text file
        return
    
    def edit_text_author_comment():
        #edit text file
        return
    
    def read_text_author_comment():
        #read text file 
        return

class review_file(log_review_line,use_file):
    
    def edit_review():
        #change text in path_review_data/{review_id}/review_data
        #change in file path_text_log value in 'size' colum
        return
    
    def read_review():
        #read text in path_text_data/{review_id}/review_data
        return

class rate_file(log_rate_line,use_file):
    
    def edit_rate():
        #chage 'rate' in path_rate_data/{class_id}/{user_class_file}
        return
    
    def read_rate():
        #read 'rate' in path_rate_data/{class_id}/{user_class_file}
        return
    

    
    # Зважаючи на останні зміни треба повністю передивитись
    # need to debug but theoretical complite
    def count_rate_average(id):
        # calculate changes from database

        # calculate average value for define user_class and return mass
        # path_rate/{id}/rates_{user_class}
        def culc(id,user_class):
            filename = globals()[f'rates_{user_class}']
            f = open(f'{path_rate_data}/{id}/{filename}','r')
            rate_file_obj = log_rate_file(user_class,id) 
            
            count = (f.seek(-1,2) + 1) // rate_file_obj.length #?
            
            column_count = rate_file_obj.column_index['rate'].iloc[0]
            sum = [0]*column_count
            #
            #mass = [[0]*(rate_line_obj.length-10) for i in range(count)]
            for i in range(count):
                f.seek(i*rate_file_obj.length,0)
                rate_file_obj.line = f.read(rate_file_obj.length)
                rate_value = rate_file_obj.read_line('rate')
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
        #filename = globals()[f'path_{check_class_id(id)}_log']
        # find line in path_{class}_log by binary_id_search
        number_line = object_id.binary_id_search(id) #binary_id_search(object_id,filename,id)
        
        object_id.read_file_line(number_line)
        
        # write calculated average value for 'review_r', 'review_a', 'review_v'
        for class_name,class_name_short in global_user_class_value_short.keys(),global_user_class_value_short.values():
            mass_rate = culc(id,class_name)
            rate_text = ''
            for i in range(len(mass_rate)):
                rate_text += str(mass_rate[i])
            object_id.write_line(f'rates_{class_name_short}',rate_text)

        # push changes to database
        object_id.rewrite_file_line(number_line)
        
        # count average for each class
        rate_dict = {
            'reviewer': '',
            'author': '',
            'viewer': '',
        }

        for class_name,class_name_short in global_user_class_value_short.keys(),global_user_class_value_short.values():
            rate_text = object_id.read_line(f'rates_{class_name_short}')
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
