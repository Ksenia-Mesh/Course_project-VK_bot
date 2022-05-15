from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from interaction_with_vk.settings import token_group

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from vk_bot import BotVk


vk = VkApi(token=token_group)
longpoll = VkLongPoll(vk)

engine = create_engine('postgresql+psycopg2://alexd:12345@localhost:5432/vkinder')
Session = sessionmaker(bind=engine)
session = Session()

bots = {}

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            if event.user_id in bots:
                bot = bots[event.user_id]
            else:
                bot = BotVk(vk=vk, vk_user_id=str(event.user_id), session=session)
                bots[event.user_id] = bot

            request = event.text
            bot.message_handler(request)

