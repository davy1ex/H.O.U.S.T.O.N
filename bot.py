import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random

# try:
from settings import token
# except



def main():
    def reply_to(key, text, user_id=None, chat_id=None, message_id=None):
        if user_id:        
            vk.messages.send(
                user_id = user_id,
                message = text,
                random_id = random.randint(100000000, 9999999999)
            )

            if message_id:
                vk.messages.markAsRead(
                    peer_id = user_id,
                    messages_ids = message_id
                )
        
        elif chat_id:        
            vk.messages.send(
                peer_id = 2000000000 + chat_id,
                message = text,
                random_id = random.randint(100000000, 9999999999)
            )

            # if message_id:
            #     vk.messages.markAsRead(
            #         peer_id = 2000000000 + chat_id,
            #         messages_ids = message_id
            #     )

    vk_session = vk_api.VkApi(token=token)

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
                reply_to("test", "тестнул", user_id=event.user_id, message_id=event.message_id)
            
            if event.from_chat:
                reply_to("test", "тестнул", chat_id=event.chat_id)

        # elif event.type == VkEventType.MESSAGE_NEW and event.text and event.from_user:
        #         print(event.user_id, 'в беседе', event.chat_i      

        else:
            print(event.type, event.raw[1:])




    


if __name__ == '__main__':
    main()