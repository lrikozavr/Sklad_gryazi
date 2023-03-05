# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import Response
import requests

import os

from text import *
from message_manage import *
from file_manage import *

token = ""
app = Flask(__name__)



def format_date(date):
    from datetime import datetime
    print(datetime.fromtimestamp(date).strftime("%B %d, %Y %I:%M:%S"))



@app.route('/', methods=['GET', 'POST'])
def index():
    users_path = 'users'
    if request.method == 'POST':
        message = request.get_json()
        #
        chat_id, txt = parse_message(message)
        #check user bot usage
        if(not os.path.isdir(f'{users_path}/{chat_id}') and not txt.split('@')[0] == '/start'):
            tel_send_message(chat_id,group_unknown_user)


        def standart_command_line(name,text,chat_id,users_path):
            text_command,text_link,text_addition = read_main_file(chat_id,users_path)
            if(not text_command == name):
                write_main_file(chat_id,users_path,name,text_link,text_addition)

        def standart_text_line(chat_id,text_user,text_bot):
            tel_send_message(chat_id,text_bot,token)
            #print(f'user:{text_user}\nbot:{text_bot}\n')
            write_chat_file(chat_id,users_path,f'\'user\':\'{text_user}\'\n\'bot\':\'{text_bot}\'\n')

        if('entities' in list(message['message'])):   
            if(message['message']['entities'][0]['type'] == 'bot_command'): 
                match message['message']['text'].split('@')[0]:
                    case '/start':
                        if(os.path.isdir(f'{users_path}/{chat_id}')):
                            standart_command_line('/start',start_bot_text,chat_id,users_path)
                        else:
                            os.makedirs(f'{users_path}/{chat_id}')
                            write_main_file(chat_id,users_path,'/start','','')
                            write_user_bio(chat_id,users_path,message['message']['from']['first_name'],
                            message['message']['from']['last_name'],message['message']['from']['username'],'-')
                        standart_text_line(chat_id,'/start',start_bot_text)
                    case '/end':
                        standart_text_line(chat_id,'/end',end_bot_text)
                        standart_command_line('/end',end_bot_text,chat_id,users_path)
                    case '/help':
                        standart_text_line(chat_id,'/help',help_bot_text)
                        standart_command_line('/help',help_bot_text,chat_id,users_path)
                    case '/add_text':
                        standart_text_line(chat_id,'/add_text',add_text_text_start)
                        standart_command_line('/add_text',add_text_text_start,chat_id,users_path)
                    case '/add_wish':
                        standart_text_line(chat_id,'/add_wish',add_wish_text_start)
                        standart_command_line('/add_wish',add_wish_text_start,chat_id,users_path)
                    case default:
                        standart_text_line(chat_id,txt,unknown_command_text)
                return Response('ok', status = 200)
        text_command,text_link,text_addition = read_main_file(chat_id,users_path)
#       print(text_command,text_link,text_addition)
        match text_command:
            case '/add_text':
                link, addition = parse_link(txt)
                if (link==''):
                    standart_text_line(chat_id,txt,add_text_text_error_linknotfound)
                else:
                    standart_text_line(chat_id,txt,add_text_text_end)                    
                    if(text_link == ''):
                        write_main_file(chat_id,users_path,text_command,link,addition)    
                    write_main_file(chat_id,users_path,text_command,f'{text_link},{link}',f'{text_addition}///{addition}')
            case '/add_wish':
                standart_text_line(chat_id,txt,add_wish_text_end)
            case default:
                standart_text_line(chat_id,txt,unknown_text_text)
        return Response('ok', status = 200)
        
        '''
        if(txt == 'hi'):
            print(tel_send_message(chat_id,"1"))
        elif(txt == '/start'):
            print(tel_send_message(chat_id,"3"))
        else:
            print(tel_send_message(chat_id,"2"))
        #import time
        #time.sleep(3)
        '''
        return Response('ok', status = 200)
    else:
        return "<h1>Well cum</h1>"

if __name__ == '__main__':
    app.run(debug=True)