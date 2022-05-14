import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from models import Users
from interaction_with_vk.settings import token_group
from random import randrange
from sqlalchemy.exc import IntegrityError, InvalidRequestError

# Для работы с вк_апи
vk = vk_api.VkApi(token=token_group)
longpoll = VkLongPoll(vk)
# Для работы с БД
session = Session()
connection = engine.connect()

# Регистрация пользователя
def register_user(vk_id):
    try:
        new_user = Users(
            vk_id=vk_id
        )
        session.add(new_user)
        session.commit()
        return True
    except (IntegrityError, InvalidRequestError):
        return False

# Пишет сообщение пользователю
def write_msg(user_id, message, attachment=None):
    vk.method('messages.send',
              {'user_id': user_id,
               'message': message,
               'random_id': randrange(10 ** 7),
               'attachment': attachment})

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")


def menu_bot(id):
    write_msg(id,
              f"Вас приветствует бот\n"
              f"Для регистрации введите - Да.\n"
              f"Если вы уже зарегистрированы: удачи в поиске!\n"
              f"Перейти в избранное нажмите - 0\n")


def show_info(user_id):
    write_msg(user_id, f'Это была последняя анкета.'
                       f'Перейти в избранное - 0'
                       f'Меню бота')


def reg_new_user(id):
    write_msg(id, 'Вы прошли регистрацию')
    write_msg(id,
              f"Нажмите для активации бота\n")
    register_user(id)




