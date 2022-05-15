import vk_api
import json
import datetime
from interaction_with_vk.settings import token_group, access_token, version
from vk_api.exceptions import ApiError


class VkCandidate:
    def __init__(self):
        self.vk = vk_api.VkApi(token=token_group)
        self.vk_ = vk_api.VkApi(token=access_token)

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
        return candidates

    def get_photo(self, owner_id):
        try:
            response = self.vk_.method('photos.get',
                                  {
                                      'access_token': access_token,
                                      'version': version,
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
            top_photos.append(item[1])
        return top_photos

    def sorting_likes(self, photos):
        top_photos = []
        for photo in photos:
            if photo != ['Нет фото'] and photos != 'Нет доступа':
                top_photos.append(photo)
        return sorted(top_photos)[:3]

    def file_crietion(self, file):
        today = datetime.date.today()
        today_ = f'{today.day}.{today.month}.{today.year}'
        result = {}
        result_file = []
        for information in enumerate(file):
            result['data'] = today_
            result['first_name'] = information[0]
            result['second_name'] = information[1]
            result['link'] = information[2]
            result['id'] = information[3]
            result_file.append(result.copy())

        with open("result.json", "a", encoding='UTF-8') as write_file:
            json.dump(result_file, write_file, ensure_ascii=False)

        print(f'Записано')

