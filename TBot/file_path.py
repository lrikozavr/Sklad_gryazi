# -*- coding: utf-8 -*-
#general name
path_text = 'Texts'
path_review = 'Reviews'
path_rate = 'Rates'
path_user = 'Users'
#logs
path_text_log = f'{path_text}/logs.bin'
path_review_log = f'{path_review}/logs.bin'
path_user_log = f'{path_user}/logs.bin'
path_statistic_log = f'statistic.bin'
#delete list
path_text_del_list = f'{path_text}/del.txt'
path_review_del_list = f'{path_review}/del.txt'
path_user_del_list = f'{path_user}/del.txt'
#data
path_text_data = f'{path_text}/data'
path_review_data = f'{path_review}/data'
path_user_data = f'{path_user}/data'
path_rate_data = f'{path_rate}/data'
#text spec
text_author_comment = 'author_comment.txt'  #path_text_data/{code}/author_comment
text_data = 'data.txt'                      #path_text_data/{code}/text_data
text_reviews_code = 'reviews_code.txt'      #path_text_data/{code}/reviews_code
#review spec
review_data = 'data.txt' #path_review_data/{code}/reviews_data
#rate spec
rates_reviewer = 'rates_reviewer' #path_rate_data/{code_withoutrate}/rates_reviewer
rates_author = 'rates_author'
rates_viewer = 'rates_viewer'
#user spec
users_log_bio = 'bio.txt' #path_user_data/{code}/bio.txt
users_log_text_id = 'text_id.bin' #path_user_data/{code}/text_id.bin
users_log_review_id = 'review_id.bin' #path_user_data/{code}/review_id.bin
users_log_rate_id = 'rate_id.bin' #path_user_data/{code}/rate_id.bin