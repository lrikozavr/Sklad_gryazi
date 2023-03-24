# -*- coding: utf-8 -*-

path_text = 'Texts'
path_review = 'Reviews'
path_rate = 'Rates'
path_user = 'Users'

path_text_log = f'{path_text}/logs.bin'
path_review_log = f'{path_review}/logs.bin'
path_user_log = f'{path_user}/logs.bin'

path_text_data = f'{path_text}/data'
path_review_data = f'{path_review}/data'
path_user_data = f'{path_user}/data'

text_author_comment = 'author_comment.txt'  #path_text_data/{code}/author_comment
text_data = 'data.txt'                      #path_text_data/{code}/text_data
text_reviews_code = 'reviews_code.txt'      #path_text_data/{code}/reviews_code

review_data = 'data.txt' #path_review_data/{code}/reviews_data

rates_reviewer = 'rates_reviewer' #path_rate/{code_withoutrate}/rates_reviewer
rates_author = 'rates_author'
rates_viewer = 'rates_viewer'

users_log_data = 'data.txt' #path_user_data/{code}/logs.txt
users_log_bio = 'bio.txt' #path_user_data/{code}/logs.txt


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
