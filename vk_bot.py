from db_handler.user_handler import UserDb
from db_handler.candidate_handler import CandidateDB
from db_handler.photo_handler import PhotoDB

from random import randrange, shuffle

from interaction_with_vk.Vk_users import VkUser
from interaction_with_vk.Vk_candidates import VkCandidate

from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class BotVk:
    def __init__(self, vk, vk_user_id, session):
        self.vk_user_id = vk_user_id
        self.session = session
        self.vk = vk
        self.user = self.add_user()
        self.candidate_list = None
        self.candidate = None
        self.photo = None

    def add_user(self):
        age = VkUser().get_user_age(self.vk_user_id)
        sex = VkUser().get_user_sex(self.vk_user_id)
        city = VkUser().get_user_city(self.vk_user_id)

        user = UserDb(self.session, self.vk_user_id, age, sex, city)

        if not user.exists():
            user.add_user()
        return user

    def message_handler(self, message=None):
        if message.lower() in ['привет']:
            keyboard = VkKeyboard()
            buttons = ['начать поиск', 'добавить кандидата', 'следующий кандидат', 'смотреть избранных']
            buttons_color = [VkKeyboardColor.PRIMARY, VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE,
                             VkKeyboardColor.PRIMARY]

            for btn, btn_color in zip(buttons, buttons_color):
                keyboard.add_button(btn, btn_color)
                if btn != buttons[-1]:
                    keyboard.add_line()

            self.hello_handler(keyboard)

        elif message.lower() in ['начать поиск']:
            self.start_handler()
        elif message.lower() in ['добавить кандидата']:
            self.add_handler()
        elif message.lower() in ['следующий кандидат']:
            self.next_handler()
        elif message.lower() in ['смотреть избранных']:
            self.candidate_handler()
        else:
            self.unknown_handler()

    def hello_handler(self, keyboard=None):
        message = 'Добро пожаловать! Начните поиск прямо сейчас!!!'

        values = {
            'user_id': self.vk_user_id,
            'message': message,
            'random_id': randrange(10 ** 7)
        }

        if keyboard:
            values['keyboard'] = keyboard.get_keyboard()

        self.vk.method('messages.send', values)

    def candidate_message_send(self, photos_list, message):
        try:
            photos_id = []
            for item in photos_list:
                photos_id.append(item[1])
            self.photo = {
                'photo_vk_id': [item[1] for item in photos_list],
                'like_count': [item[0] for item in photos_list],
            }
        except IndexError:
            photos_id = []

        if len(photos_id) == 0:
            self.vk.method('messages.send',
                           {'user_id': self.vk_user_id, 'message': message, 'random_id': randrange(10 ** 7)
                            })
        elif len(photos_id) == 1:
            self.vk.method('messages.send',
                           {'user_id': self.vk_user_id, 'message': message, 'random_id': randrange(10 ** 7),
                            'attachment': f'{photos_id[0]}'})
        elif len(photos_id) == 2:
            self.vk.method('messages.send',
                           {'user_id': self.vk_user_id, 'message': message, 'random_id': randrange(10 ** 7),
                            'attachment': f'{photos_id[0]},'
                                          f'{photos_id[1]}'})
        elif len(photos_id) == 3:
            self.vk.method('messages.send',
                           {'user_id': self.vk_user_id, 'message': message, 'random_id': randrange(10 ** 7),
                            'attachment': f'{photos_id[0]},'
                                          f'{photos_id[1]},'
                                          f'{photos_id[2]}'})

    def start_handler(self):
        if self.user.sex == 1:
            self.candidate_list = VkCandidate().search_candidates(2, self.user.age - 1, self.user.age + 1,
                                                                  self.user.city)
        else:
            self.candidate_list = VkCandidate().search_candidates(1, self.user.age - 1, self.user.age + 1,
                                                                  self.user.city)
        message = f'{self.candidate_list[0][1]} {self.candidate_list[0][0]}\nhttps://vk.com/id{self.candidate_list[0][2]}'
        self.candidate_message_send(VkCandidate().get_photo(self.candidate_list[0]), message)
        self.candidate = {
            'first_name': self.candidate_list[0][0],
            'last_name': self.candidate_list[0][1],
            'vk_id': self.candidate_list[0][2]
        }

    @staticmethod
    def gen(candidates):
        for candidate in candidates:
            yield candidate

    def next_handler(self):
        shuffle(self.candidate_list)
        candidate = next(self.gen(self.candidate_list))

        self.candidate = {
            'first_name': candidate[0],
            'last_name': candidate[1],
            'vk_id': candidate[2]
        }

        message = f'{candidate[1]} {candidate[0]}\nhttps://vk.com/id{candidate[2]}'
        self.candidate_message_send(VkCandidate().get_photo(self.candidate_list[0]), message)

    def add_handler(self):
        first_name = self.candidate['first_name']
        last_name = self.candidate['last_name']
        vk_id = self.candidate['vk_id']
        vk_photo_id = self.photo['photo_vk_id']
        likes = self.photo['like_count']

        candidate = CandidateDB(self.session, first_name, last_name, str(vk_id))

        if not candidate.exists():
            candidate.add_candidate()
            message = 'Добавленно...'
            self.vk.method('messages.send',
                           {'user_id': self.vk_user_id, 'message': message, 'random_id': randrange(10 ** 7)})
            self.user.relation(candidate.exists())

            for id_item, like_count in zip(vk_photo_id, likes):
                photo = PhotoDB(self.session, candidate.get_id()[0], id_item.split('_')[1], like_count)
                if not photo.exists():
                    photo.add_photo()
        else:
            self.user.relation(candidate.exists())

    def candidate_handler(self):
        favorites = self.user.candidates_list(self.user)

        for item in favorites:
            if item[2].isnumeric():
                message = f'{item[0]} {item[1]} - https://vk.com/id{item[2]}'
            else:
                message = f'{item[0]} {item[1]} - https://vk.com/{item[2]}'
            self.vk.method('messages.send',
                           {'user_id': self.vk_user_id, 'message': message, 'random_id': randrange(10 ** 7)})

    def unknown_handler(self):
        message = 'Не понимаю вас((('
        self.vk.method('messages.send',
                       {'user_id': self.vk_user_id, 'message': message, 'random_id': randrange(10 ** 7)})
