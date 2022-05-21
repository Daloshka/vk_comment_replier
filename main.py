import vk_api
import random
import info  # bot_token
from random import randint
import datetime
import time

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
    list_owner_id = []
    list_post_id = []
    owner_id = id
    for i in range(count):
        list_post_id.append(session.method('wall.get', {'owner_id':id,'count':info.posts_each_group, 'random_id' : random.randint(1000, 99999)})['items'][i]['id'])
    #print(owner_id, post_id)
    return owner_id, list_post_id

# получаем id 5 комментариев под постом
def get_comments_id_under_post(post_owner_id, post_id):
    session = vk_api.VkApi(token= info.token_vk)
    comment_ids = []
    comments = session.method('wall.getComments', {'owner_id':post_owner_id,'post_id':post_id,'count':info.comments_under_each_post,'random_id' : random.randint(1000, 99999)})['items']
    for comment in comments:
        comment_ids.append(comment['id'])
    #print(comment_ids)
    return comment_ids

def create_comment(owner_id, post_id, reply_to_comment, from_group = 0):
    session = vk_api.VkApi(token= info.token_vk)
    message = info.text[randint(0, len(info.text)-1)]
    print(owner_id, post_id, reply_to_comment, from_group)
    session.method('wall.createComment', {'owner_id':owner_id,'post_id':post_id, 'reply_to_comment':reply_to_comment, 'message':message, 'from_group':from_group,'random_id' : random.randint(1000, 99999)})
    


def main():
    list_links = read_lines_from_txt()
    for link in list_links:
        # получаем id группы
        group_id = get_id_by_link(link)
        # получаем id на последний пост
        post_owner_id, list_post_id = get_owner_id_and_post_id_five_posts(group_id)
        for i in range(len(list_post_id)):
            post_id = list_post_id[i]
            # пишем коммент под последнии 5 комментов от лица вашего сообщества пользователям под их comment id 
            comment_ids = get_comments_id_under_post(post_owner_id, post_id)
            print(f"Comment_ids {comment_ids}")
            for reply_to_comment in comment_ids:
                print(reply_to_comment)
                print(type(info.your_group_id), info.your_group_id)
                create_comment(post_owner_id, post_id, reply_to_comment, info.your_group_id)
                print(f"Ответ на комментарий отправлен")
                time.sleep(3)


#post_id_id, post_id = get_owner_id_and_post_id_last_post(-213025701)

#print(get_owner_id_and_post_id_five_posts(-213025701))

#print(get_comments_id_under_post(-213025701, 2))



main()

# session = vk_api.VkApi(token= info.token_vk)
# session.method('wall.createComment', {'owner_id' :user_id, 'post_id':,'from_group':0,'message':info.text[randint(0, len(info.text)-1)], 'random_id' : random.randint(1000, 99999)})


