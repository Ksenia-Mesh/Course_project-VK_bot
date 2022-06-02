import vk_api

from random import shuffle

from vk_api.exceptions import ApiError
import configparser


config = configparser.ConfigParser()
config.read('settings.ini')


class VkCandidate:
    def __init__(self):
        self.vk = vk_api.VkApi(token=config["Params"]["token_group"])
        self.vk_ = vk_api.VkApi(token=config["Params"]["access_token"])

    def search_candidates(self, sex, age_from, age_to, city):
        candidates = []
        response = self.vk_.method('users.search',
                                   {'sort': 1,
                                    'sex': sex,
                                    'status': 1,
                                    'age_from': age_from,
                                    'age_to': age_to,
                                    'has_photo': 1,
                                    'count': 1000,
                                    'hometown': city
                                    })
        for element in response['items']:
            candidate = [
                element['first_name'],
                element['last_name'],
                element['id']
            ]

            candidates.append(candidate)
            shuffle(candidates)

        return candidates

    def get_photo(self, owner_id):
        try:
            response = self.vk_.method('photos.get',
                                       {
                                           'access_token': config["Params"]["access_token"],
                                           'version': config["Params"]["version"],
                                           'owner_id': owner_id,
                                           'album_id': 'profile',
                                           'count': 10,
                                           'extended': 1,
                                           'photo_sizes': 1,
                                       })
        except ApiError:
            return 'Нет доступа'

        photos_candidate = []

        for i in range(10):
            try:
                photos_candidate.append(
                    [response['items'][i]['likes']['count'],
                     'photo' + str(response['items'][i]['owner_id']) + '_' + str(response['items'][i]['id'])])
            except IndexError:
                photos_candidate.append(['Нет фото'])

        top_photos = []

        for item in self.sorting_likes(photos_candidate):
            top_photos.append(item)
        return top_photos

    @staticmethod
    def sorting_likes(photos):
        top_photos = []
        for photo in photos:
            if photo != ['Нет фото'] and photos != 'Нет доступа':
                top_photos.append(photo)
        return sorted(top_photos, reverse=True)[:3]
