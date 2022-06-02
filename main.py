from models.base import Base
from models.user_candidate import UserCandidate
from models.photos import Photos
from models.users import Users
from models.candidates import Candidates

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType

from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker

from vk_bot import BotVk

import configparser


def main(bots):
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


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')

    vk = VkApi(token=config["Params"]["token_group"])
    longpoll = VkLongPoll(vk)

    engine = create_engine(
        f'postgresql+psycopg2://{config["Params"]["USERNAME"]}:{config["Params"]["PASSWORD"]}@localhost'
        f':{config["Params"]["PORT"]}/{config["Params"]["DATABASE"]}')

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    bots = {}

    main(bots)
