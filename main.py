import datetime
import vk_api
from vk_api import Captcha
import random
from random import randint
import info  # bot_token
from info import ANTICAPTCHA_KEY
import time
from time import sleep
import re
import onnxruntime as rt
import requests
import base64

def get_responce_captcha(_id):
    print('Ожидание выполнения капчи.')
    isGet = False
    text = None
    while (isGet == False):
        print('Попытка получить капчу')
        r = requests.get(f'https://rucaptcha.com/res.php?key={ANTICAPTCHA_KEY}&action=get&id={_id}')
        text = r.text.split('|')[-1]
        if (text != 'ERROR_WRONG_CAPTCHA_ID' and text != 'CAPCHA_NOT_READY' and r.status_code == 200):
            isGet = True
    print(f"Капча получена: {text}\n5 секунд до ввода")
    time.sleep(5)
    return text

def captcha_handler(captcha: Captcha):
    """
    Хендлер для обработки капчи из VK
    """
    print('Обнаружена капча!')
    captcha_url = captcha.get_url()
    base_64_link = base64.b64encode(requests.get(captcha_url).content).decode("utf-8")
    data = {
        'key': ANTICAPTCHA_KEY,
        'method': 'base64',
        'body': base_64_link,
        'soft_id': 788289
    }
    r = requests.post('http://rucaptcha.com/in.php', data=data)
    #print(r.status_code)
    _id = r.text.split('|')[-1]
    #print(_id)
    key = get_responce_captcha(_id)
    #key = input("\n\n[!] Чтобы продолжить, введи сюда капчу с картинки {0}:\n> ".format(captcha.get_url())).strip()
    return captcha.try_again(key)

# Чтение ссылок из текстового документа
def read_lines_from_txt():
    with open("group_links.txt") as file:
        list_links = []
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        for line in lines:
            list_links.append(line)
        return list_links

# return negative ID for group from URL
def get_id_by_link(url):
    short_url = url.split('/')[-1]
    session = vk_api.VkApi(token= info.token_vk, captcha_handler=captcha_handler)
    group_id = session.method('groups.getById', {'group_ids':short_url})[0]['id']
    group_id *= -1
    #print(group_id)
    return group_id

def get_owner_id_and_post_id_last_post(id):
    session = vk_api.VkApi(token= info.token_vk, captcha_handler=captcha_handler)
    owner_id = session.method('wall.get', {'owner_id':id,'count':1})['items'][0]['owner_id']
    post_id = session.method('wall.get', {'owner_id':id,'count':1})['items'][0]['id']
    return owner_id, post_id

def get_owner_id_and_post_id_five_posts(id):
    # сколько постов комментить в каждой группе
    session = vk_api.VkApi(token= info.token_vk, captcha_handler=captcha_handler)
    list_post_id = []
    owner_id = id
    for i in range(info.posts_each_group):
        try:
            list_post_id.append(session.method('wall.get', {'owner_id':owner_id})['items'][i]['id'])
        except:
            print(f"Комментарии под постом закончились")
    return owner_id, list_post_id

def leave_comment_under_post(owner_id, post_id):
    session = vk_api.VkApi(token= info.token_vk, captcha_handler=captcha_handler)
    message = info.text[randint(0, len(info.text)-1)]
    session.method('wall.createComment', {'owner_id':owner_id,'post_id':post_id, 'message':message, 'from_group':info.your_group_id})
    print(f"Был оставлен комментарий")

# получаем id 5 комментариев под постом
def get_comments_id_under_post(post_owner_id, post_id):
    comment_ids = []
    session = vk_api.VkApi(token= info.token_vk, captcha_handler=captcha_handler)
    comments = session.method('wall.getComments', {'owner_id':post_owner_id,'post_id':post_id,'count':info.comments_under_each_post})['items']
    for comment in comments:
        try:
            if (comment['from_id'] != -info.your_group_id):
                comment_ids.append(comment['id'])
            else:
                pass
        except Exception as ex:
            print(f"Error in get_comments_id_under_post {ex}")
    #print(comment_ids)
    if (len(comment_ids) == 0):
        leave_comment_under_post(post_owner_id, post_id)
    return comment_ids

def create_comment(owner_id, post_id, reply_to_comment, from_group = 0):
    session = vk_api.VkApi(token= info.token_vk, captcha_handler=captcha_handler)
    message = info.text[randint(0, len(info.text)-1)]
    #print(owner_id, post_id, reply_to_comment, from_group)
    session.method('wall.createComment', {'owner_id':owner_id,'post_id':post_id, 'reply_to_comment':reply_to_comment, 'message':message, 'from_group':from_group})


def main():
    session = vk_api.VkApi(token= info.token_vk, captcha_handler=captcha_handler)
    list_links = read_lines_from_txt()
    for link in list_links:
        try:
            # получаем id группы
            group_id = get_id_by_link(link)
            # получаем id на последний пост
            post_owner_id, list_post_id = get_owner_id_and_post_id_five_posts(group_id)
            for i in range(len(list_post_id)):
                post_id = list_post_id[i]
                # пишем коммент под последнии 5 комментов от лица вашего сообщества пользователям под их comment id 
                comment_ids = get_comments_id_under_post(post_owner_id, post_id)
                #print(f"Comment_ids {comment_ids}")
                for reply_to_comment in comment_ids:
                    create_comment(post_owner_id, post_id, reply_to_comment, info.your_group_id)
                    print(f"Ответ на комментарий {post_owner_id} отправлен")
                    time.sleep(info.delay_for_message)
        except Exception as ex:
            print(f"Error in list_links {ex}")


main()
time.sleep(20)

