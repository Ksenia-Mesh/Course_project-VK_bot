from models.photos import Photos


class PhotoDB:
    def __init__(self, session, candidate_id, vk_id, like_count):
        self.session = session
        self.vk_id = vk_id
        self.like_count = like_count
        self.candidate_id = candidate_id

    def exists(self):
        """Метод проверки наличия фотографии в бд."""

        return self.session.query(Photos).filter(Photos.vk_id == self.vk_id).first()

    def add_photo(self):
        """Метод добавления фотографии в бд."""

        photo = Photos(
            vk_id=self.vk_id,
            like_count=self.like_count,
            candidate_id=self.candidate_id

        )

        self.session.add(photo)
        self.session.commit()
