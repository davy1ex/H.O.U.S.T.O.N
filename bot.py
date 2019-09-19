import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import os
import requests
from bs4 import BeautifulSoup

import settings


def google_image_search(for_search):
    print("ass")
    word = ""
    
    for w in for_search:
        word += w + " "


    url = "https://www.google.com/search?q=" + word + "&tbm=isch"
    page = requests.get(url).text
    soup = BeautifulSoup(page, "html.parser")
    
    # url_imgs = []
    
    for raw_img in soup.find_all("img"):
        
        try:
            os.mkdir(settings.IMAGES_DIR)
        except FileExistsError:
            pass

        print("качаю")
        link = raw_img.get("src")
        # проверка на ссылку
        if "http" in link:
            
            os.system("wget -O " + settings.IMAGES_DIR + "/" + str(random.randint(1, 1000000)) + ".jpeg " + link)
            # os.rename(os.listdir(settings.IMAGES_DIR)[-1], settings.IMAGES_DIR + "/" + link + ".jpeg")
            print("скачал")
        
        # скачать всего 10 штук
        if len(os.listdir(settings.IMAGES_DIR)) == 10:
            break


def main():
    def reply_to(text, user_id=None, chat_id=None, message_id=None, attachment=None):
        if user_id:        
            vk.messages.send(
                user_id = user_id,
                attachment = attachment,
                message = text,
                random_id = random.randint(100000000, 9999999999)
            )
        
        elif chat_id:        
            vk.messages.send(
                peer_id = 2000000000 + chat_id,
                message = text,
                random_id = random.randint(100000000, 9999999999)
            )

    vk_session = vk_api.VkApi(token=settings.TOKEN)

    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.text and event.to_me:
            print('Новое сообщение:')

            if event.from_me:
                print('От меня для: ', end='')
            elif event.to_me:
                print('Для меня от: ', end='')                
            
            if event.from_user:
                # ex: "хью г apple"
                if "г" in event.text and len(event.text) >= 2 and event.text.split()[1] == "г":
                    for_search = event.text.split()[2:] # слово для поиска
                    photos = google_image_search(for_search) # страница с результатами
                    
                    upload = vk_api.VkUpload(vk_session)
                    
                    vk_photo_urls = []

                    for photo_name in os.listdir(settings.IMAGES_DIR):                        
                        print(photo_name, "\n")
                        photo = upload.photo(  # Подставьте свои данные
                            settings.IMAGES_DIR + "/" + photo_name,
                            album_id = 263864981,
                            group_id = 183407860
                        )

                        vk_photo_url = 'photo{}_{}'.format(
                            photo[0]['owner_id'], photo[0]['id']
                        )

                        vk_photo_urls.append(vk_photo_url)
                    
                    text = "Картинки по запросу: "
                    
                    for word in for_search:
                         text += word + " "
                    
                    print(vk_photo_urls)
                    reply_to(attachment=vk_photo_urls, text=text, user_id=event.user_id)
                    os.system("rm -rf " + settings.IMAGES_DIR + "/")

                #reply_to("test", "тестнул", user_id=event.user_id, message_id=event.message_id)
            
            if event.from_chat:
                reply_to("test", "тестнул", chat_id=event.chat_id)




    


if __name__ == '__main__':
    main()