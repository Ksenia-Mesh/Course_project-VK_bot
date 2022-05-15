from db_handler.user_handler import UserDb
from db_handler.candidate_handler import CandidateDB
from db_handler.photo_handler import PhotoDB

from random import randrange


class BotVk:
    def __init__(self, vk, vk_user_id, session):
        self.vk_user_id = vk_user_id
        self.session = session
        self.vk = vk
        self.user = self.add_user()

    def add_user(self):
        age = None
        sex = None
        city = None
        user = UserDb(self.session, self.vk_user_id, age, sex, city)
        if not user.exists():
            user.add_user()
        return user

    def message_handler(self, message=None):
        if message.lower() in ['привет']:
            self.hello_handler()
        elif message.lower() in ['начать', 'старт', 'поиск']:
            self.start_handler()
        elif message.lower() in ['добавить', 'сохранить']:
            self.add_handler()
        elif message.lower() in ['следующий', 'некст', 'скип']:
            self.next_handler()
        elif message.lower() in ['избранное', 'кандидаты']:
            self.candidate_handler()
        elif message.lower() in ['пока']:
            self.goodbye_handler()
        else:
            self.unknown_handler()

    def hello_handler(self):
        message = 'Добро пожаловать! Начните поиск прямо сейчас!!!'
        self.vk.method('messages.send',
                       {'user_id': self.vk_user_id, 'message': message, 'random_id': randrange(10 ** 7), })

    def start_handler(self):
        pass

    def add_handler(self):
        first_name = None
        last_name = None
        vk_id = None
        vk_photo_id = None
        like_count = None

        candidate = CandidateDB(self.session, first_name, last_name, vk_id)

        if not candidate.exists():
            candidate.add_candidate()
            self.user.relation(candidate.exists())
            photo = PhotoDB(self.session, candidate.get_id()[0], vk_photo_id, like_count)
            if not photo.exists():
                photo.add_photo()
        else:
            self.user.relation(candidate.exists())

    def next_handler(self):
        pass

    def candidate_handler(self):
        favorites = self.user.candidates_list(self.user)
        for item in favorites:
            if item[2].isnumeric():
                message = f'{item[0]} {item[1]} - https://vk.com/id{item[2]}'
            else:
                message = f'{item[0]} {item[1]} - https://vk.com/{item[2]}'
            self.vk.method('messages.send',
                           {'user_id': self.vk_user_id, 'message': message, 'random_id': randrange(10 ** 7), })

    def goodbye_handler(self):
        message = 'Всего хорошего!'
        self.vk.method('messages.send', {'user_id': self.vk_user_id, 'message': message, 'random_id': randrange(10 ** 7), })

    def unknown_handler(self):
        message = 'Не понимаю вас((('
        self.vk.method('messages.send', {'user_id': self.vk_user_id, 'message': message, 'random_id': randrange(10 ** 7), })
