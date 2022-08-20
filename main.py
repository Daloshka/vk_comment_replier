import vk_api
import random
import info  # bot_token
from random import randint
import datetime
import time

captcha_sid = None
captcha_key = None
captcha_url = 'Ссылка пуста'

# Чтение ссылок из текстового документа
def read_lines_from_txt():
    with open("group_links.txt") as file:
        list_links = []
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        for line in lines:
            list_links.append(line)
        # print(list_links)
        return list_links

# return negative ID for group from URL
def get_id_by_link(url):
    session = vk_api.VkApi(token= info.token_vk)
    short_url = url.split('/')[-1]
    #print(short_url)
    group_id = session.method('groups.getById', {'group_ids':short_url, 'random_id' : random.randint(1000, 99999)})[0]['id']
    group_id *= -1
    print(group_id)
    return group_id

def get_owner_id_and_post_id_last_post(id):
    session = vk_api.VkApi(token= info.token_vk)
    owner_id = session.method('wall.get', {'owner_id':id,'count':1, 'random_id' : random.randint(1000, 99999)})['items'][0]['owner_id']
    post_id = session.method('wall.get', {'owner_id':id,'count':1, 'random_id' : random.randint(1000, 99999)})['items'][0]['id']
    #print(owner_id, post_id)
    return owner_id, post_id

def get_owner_id_and_post_id_five_posts(id):
    session = vk_api.VkApi(token= info.token_vk)
    # сколько постов комментить в каждой группе
    list_post_id = []
    owner_id = id
    for i in range(info.posts_each_group):
        try:
            list_post_id.append(session.method('wall.get', {'owner_id':owner_id, 'random_id' : random.randint(1000, 99999)})['items'][i]['id'])
        except:
            print(f"Комментарии под постом закончились")
    #print(owner_id, post_id)
    return owner_id, list_post_id

def leave_comment_under_post(owner_id, post_id):
    message = info.text[randint(0, len(info.text)-1)]
    session = vk_api.VkApi(token= info.token_vk)
    session.method('wall.createComment', {'owner_id':owner_id,'post_id':post_id, 'message':message, 'from_group':info.your_group_id,'random_id' : random.randint(1000, 99999)})
    print(f"Был оставлен комментарий")

# получаем id 5 комментариев под постом
def get_comments_id_under_post(post_owner_id, post_id):
    session = vk_api.VkApi(token= info.token_vk)
    comment_ids = []
    comments = session.method('wall.getComments', {'owner_id':post_owner_id,'post_id':post_id,'count':info.comments_under_each_post,'random_id' : random.randint(1000, 99999)})['items']
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
    try:
        if (captcha_sid is not None):
            session = vk_api.VkApi(token= info.token_vk)
            message = info.text[randint(0, len(info.text)-1)]
            print(owner_id, post_id, reply_to_comment, from_group)
            session.method('wall.createComment', {'owner_id':owner_id,'post_id':post_id, 'reply_to_comment':reply_to_comment, 'message':message, 'from_group':from_group, 'captcha_sid':captcha_sid, 'captcha_key':input(f'Введите капчу указаную в ссылке: {captcha_url}\n')})
        else:
            session = vk_api.VkApi(token= info.token_vk)
            message = info.text[randint(0, len(info.text)-1)]
            print(owner_id, post_id, reply_to_comment, from_group)
            session.method('wall.createComment', {'owner_id':owner_id,'post_id':post_id, 'reply_to_comment':reply_to_comment, 'message':message, 'from_group':from_group})
    except vk_api.exceptions.Captcha as captcha:
        captcha_sid = captcha.sid
        #print(captcha.sid) # Получение sid
        captcha_url = captcha.get_url()
        print(captcha.get_url()) # Получить ссылку на изображение капчи
        #print(captcha.get_image()) # Получить изображение капчи (jpg)
    


def main():
    list_links = read_lines_from_txt()
    for link in list_links:
        try:
            # получаем id группы
            group_id = get_id_by_link(link)
            # получаем id на последний пост
            post_owner_id, list_post_id = get_owner_id_and_post_id_five_posts(group_id)
            for i in range(len(list_post_id)):
                try:
                    post_id = list_post_id[i]
                    # пишем коммент под последнии 5 комментов от лица вашего сообщества пользователям под их comment id 
                    comment_ids = get_comments_id_under_post(post_owner_id, post_id)
                    print(f"Comment_ids {comment_ids}")
                    for reply_to_comment in comment_ids:
                        #print(reply_to_comment)
                        #print(type(info.your_group_id), info.your_group_id)
                        create_comment(post_owner_id, post_id, reply_to_comment, info.your_group_id)
                        print(f"Ответ на комментарий {post_owner_id} отправлен")
                        time.sleep(info.delay_for_message)
                except Exception as ex:
                    print(f"!!!!!!!")
                    print(post_owner_id, list_post_id[i])
                    print(f"Error in list_post_id {ex}")
        except Exception as ex:
            print(f"Error in list_links {ex}")

# print(get_owner_id_and_post_id_last_post(-213025701))
# owner_id, post_id = get_owner_id_and_post_id_last_post(-213025701)
# leave_comment_under_post(owner_id, post_id)

main()
time.sleep(20)


#post_id_id, post_id = get_owner_id_and_post_id_last_post(-213025701)

#print(get_owner_id_and_post_id_five_posts(-213025701))

#print(get_comments_id_under_post(-213025701, 2))

# session = vk_api.VkApi(token= info.token_vk)
# session.method('wall.createComment', {'owner_id' :user_id, 'post_id':,'from_group':0,'message':info.text[randint(0, len(info.text)-1)], 'random_id' : random.randint(1000, 99999)})


