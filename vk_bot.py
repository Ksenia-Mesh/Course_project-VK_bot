from db_handler.user_handler import UserDb
from db_handler.candidate_handler import CandidateDB
from db_handler.photo_handler import PhotoDB

from random import randrange

from interaction_with_vk.Vk_users import VkUser
from interaction_with_vk.Vk_candidates import VkCandidate


class BotVk:
    def __init__(self, vk, vk_user_id, session):
        self.vk_user_id = vk_user_id
        self.session = session
        self.vk = vk
        self.user = self.add_user()

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
        if self.user.sex == 1:
            self.candidate_list = VkCandidate().search_candidates(2, self.user.age - 1, self.user.age + 1,
                                                                  self.user.city)
        else:
            self.candidate_list = VkCandidate().search_candidates(1, self.user.age - 1, self.user.age + 1,
                                                                  self.user.city)
        message = f'{self.candidate_list[0][1]} {self.candidate_list[0][0]}\nhttps://vk.com/id{self.candidate_list[0][2]}'
        if len(VkCandidate().get_photo(self.candidate_list[0])) == 0:
            self.vk.method('messages.send',
                           {'user_id': self.vk_user_id, 'message': message, 'random_id': randrange(10 ** 7)
                            })
            self.candidate_list.pop(0)
        elif len(VkCandidate().get_photo(self.candidate_list[0])) == 1:
            self.vk.method('messages.send',
                           {'user_id': self.vk_user_id, 'message': message, 'random_id': randrange(10 ** 7),
                            'attachment': f'{VkCandidate().get_photo(self.candidate_list[0])[0]}'})
            self.candidate_list.pop(0)
        elif len(VkCandidate().get_photo(self.candidate_list[0])) == 2:
            self.vk.method('messages.send',
                           {'user_id': self.vk_user_id, 'message': message, 'random_id': randrange(10 ** 7),
                            'attachment': f'{VkCandidate().get_photo(self.candidate_list[0])[0]},'
                                          f'{VkCandidate().get_photo(self.candidate_list[0])[1]}'})
            self.candidate_list.pop(0)
        elif len(VkCandidate().get_photo(self.candidate_list[0])) == 3:
            self.vk.method('messages.send',
                           {'user_id': self.vk_user_id, 'message': message, 'random_id': randrange(10 ** 7),
                            'attachment': f'{VkCandidate().get_photo(self.candidate_list[0])[0]},'
                                          f'{VkCandidate().get_photo(self.candidate_list[0])[1]},'
                                          f'{VkCandidate().get_photo(self.candidate_list[0])[2]}'})
            self.candidate_list.pop(0)

    @staticmethod
    def gen(can):
        for candidate in can:
            yield candidate

    def next_handler(self):
        candidate = next(self.gen(self.candidate_list))
        message = f'{candidate[1]} {candidate[0]}\nhttps://vk.com/id{candidate[2]}'
        if len(VkCandidate().get_photo(self.candidate_list[0])) == 0:
            self.vk.method('messages.send',
                           {'user_id': self.vk_user_id, 'message': message, 'random_id': randrange(10 ** 7)
                            })
            self.candidate_list.pop(0)
        elif len(VkCandidate().get_photo(self.candidate_list[0])) == 1:
            self.vk.method('messages.send',
                           {'user_id': self.vk_user_id, 'message': message, 'random_id': randrange(10 ** 7),
                            'attachment': f'{VkCandidate().get_photo(self.candidate_list[0])[0]}'})
            self.candidate_list.pop(0)
        elif len(VkCandidate().get_photo(self.candidate_list[0])) == 2:
            self.vk.method('messages.send',
                           {'user_id': self.vk_user_id, 'message': message, 'random_id': randrange(10 ** 7),
                            'attachment': f'{VkCandidate().get_photo(self.candidate_list[0])[0]},'
                                          f'{VkCandidate().get_photo(self.candidate_list[0])[1]}'})
            self.candidate_list.pop(0)
        elif len(VkCandidate().get_photo(self.candidate_list[0])) == 3:
            self.vk.method('messages.send',
                           {'user_id': self.vk_user_id, 'message': message, 'random_id': randrange(10 ** 7),
                            'attachment': f'{VkCandidate().get_photo(self.candidate_list[0])[0]},'
                                          f'{VkCandidate().get_photo(self.candidate_list[0])[1]},'
                                          f'{VkCandidate().get_photo(self.candidate_list[0])[2]}'})
            self.candidate_list.pop(0)

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
        self.vk.method('messages.send',
                       {'user_id': self.vk_user_id, 'message': message, 'random_id': randrange(10 ** 7), })

    def unknown_handler(self):
        message = 'Не понимаю вас((('
        self.vk.method('messages.send',
                       {'user_id': self.vk_user_id, 'message': message, 'random_id': randrange(10 ** 7), })
