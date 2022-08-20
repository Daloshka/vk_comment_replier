from random import randint

# Ссылка для получения токена VK https://oauth.vk.com/authorize?client_id=8129750&scope=wall,groups,offline&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1
# Скопировать между [access_token=]   df32b9dc3fd95ff6f8c8e3377b1b313f8daa84a3c39fc95803ea6b03f3421eda1425bcacc29f390f9cd40   [&expires_in]  (FAKE TOKEN)


token_vk = ""

# Сюда нужно встаить id группы от лица, которой будут отправляться сообщение (токен вк должен иметь доступ админа в этой группе)
# Можно получить тут https://regvk.com/id/

your_group_id = 

# Задержка между ответом на комментарии в диапозоне от 30 до 50 секунд
delay_for_message = randint(30, 50)

# text =  ["Текст1", "Текст2"]   добавляете разный текст через запятую в подобном формате  , "Текст3"
text = ["Го к нам, давай к нам"]


comments_under_each_post = 5
posts_each_group = 5