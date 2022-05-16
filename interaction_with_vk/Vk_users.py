import vk_api

from datetime import datetime
from interaction_with_vk.settings import token_group


class VkUser:
    def __init__(self):
        self.vk = vk_api.VkApi(token=token_group)
        self.vk_api = self.vk.get_api()

    def get_user_sex(self, user_id):
        return self.vk_api.users.get(user_ids=user_id, fields='sex')[0]['sex']

    def get_user_city(self, user_id):
        return self.vk_api.users.get(user_ids=user_id, fields='city')[0]['city']['title']

    def get_user_age(self, user_id):
        current_year = datetime.now().year
        bdate = self.vk_api.users.get(user_ids=user_id, fields='bdate')[0]['bdate']
        return current_year - int(bdate[-4:])
