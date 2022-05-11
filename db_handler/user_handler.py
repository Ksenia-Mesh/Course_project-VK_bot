from models.users import Users


class UserDb:
    def __init__(self, session, vk_user_id, age, sex, city):
        self.session = session
        self.vk_user_id = vk_user_id
        self.age = age
        self.sex = sex
        self.city = city

    def exists(self):
        """Метод проверки наличия пользователя в бд. Если пользователь есть в бд,
        проверяются данные на актуальность. Если возраст или город устарели,
        происходит обновление данных."""

        if self.session.query(Users).filter(Users.vk_id == self.vk_user_id).first():
            if self.session.query(Users.age).filter(
                    Users.vk_id == self.vk_user_id).first() == self.age and self.session.query(Users.city).filter(
                    Users.vk_id == self.vk_user_id).first() == self.city:
                return True
            else:
                self.update_user()
                return True
        else:
            return False

    def add_user(self):
        """Метод добавления пользователя в бд."""

        user = Users(
            vk_id=self.vk_user_id,
            sex=self.sex,
            age=self.age,
            city=self.city
        )

        self.session.add(user)
        self.session.commit()

    def update_user(self):
        """Метод обновления возраста и города в бд."""

        user = self.session.query(Users).filter(Users.vk_id == self.vk_user_id).first()

        user.age = self.age
        user.city = self.city

        self.session.add(user)
        self.session.commit()

    def relation(self, candidate):
        """Медот добавления связей между пользователем и кандидатом."""

        user = self.session.query(Users).filter(Users.vk_id == self.vk_user_id).first()

        user.candidates.append(candidate)
        self.session.commit()