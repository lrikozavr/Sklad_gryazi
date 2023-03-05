# -*- coding: utf-8 -*-
import requests

def parse_message(message):
    print("message-->", message)
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    print("chat_id-->", chat_id)
    print("txt-->", txt)
    type = message['message']['chat']['type']
    '''
    id = user_chat_id = message['message']['from']['id']
    f_n = user_first_name = message['message']['from']['first_name']
    l_n = user_last_name = message['message']['from']['last_name']
    u_n = user_username = message['message']['from']['username']
    bi = bio_text
    '''
    '''
    if(not chat_id == '-850841161'):
        first_name = message['message']['chat']['first_name']
        last_name = message['message']['chat']['last_name']
        username = message['message']['chat']['username']
        date = message['message']['date']
        print("first_name-->", first_name)
        print("last_name-->", last_name)
        print("username-->", username)
        print("date-->", date)
        format_date(date)
    '''
    return chat_id,txt,type

def parse_link(text):
    split_text = 'https://telegra.ph/'
    sym_arr = [' ',',','\t']
    text_1 = text.split('\n')
    link = ''
    addition = ''
    for line_1 in text_1:
        if(len(line_1.split(split_text)) >= 2):
            addition = line_1.split(split_text)[0]
            for i in range(1,len(line_1.split(split_text)),1):
                line_2 = line_1.split(split_text)[i]
                for sym in sym_arr:
                    if(not len(line_2.split(sym)) == 1):
                        line_2 = line_2.split(sym)[0]
                addition += str(i) + line_1.split(split_text)[i].split(line_2)[1]
                if(not link == ''):
                    link += ',' + split_text + line_2
                else:
                    link = split_text + line_2
    return link, addition

def tel_send_message(chat_id, text, token):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    r = requests.post(url,json=payload)
    return r

def tel_send_message_reply(chat_id, text, message_id, token):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'reply_to_message_id': message_id
    }
    r = requests.post(url,json=payload)
    return r