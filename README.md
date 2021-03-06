# Чат-бот Вконтакте «VKinder» 

Разработка программы-бота для взаимодействия с базами данных социальной сети. Бот предлагает различные варианты людей для знакомств в социальной сети Вконтакте в виде диалога с пользователем.

- [x] Поиск людей ведется по критериям: пол, возраст, город.
- [x] У подошедших выбираются самые популярные фотографии.
- [x] Информация в чате выводится в формате:
```text
Имя Фамилия
Ссылка на профиль
Три фотографии в виде attachment
```
- [x] Управление осуществляется с помощью кнопок.
- [x] Существует возможность добавлять в список избранных.
- [x] Возможен просмотр избранных людей.

## Используемые библиотеки и СУБД

- vk_api
- SQLAlchemy
- PostgreSQL

## Настройка БД

Для корректной работы программы вам необходимо установить PostgreSQL на свой компьютер. Для настройки базы данных используйте следующие команды

```bash
psql -U postgres

create database <db_name>;

create user <user_name> with password <password>;

alter database <db_name> owner to <user_name>;
```
## Токены

### Токен группы
Необходимо создать группа во Вконтакте, от имени которой будет общаться бот. Инструкцию по настройке и получению токена можно посмотреть [здесь](https://github.com/netology-code/adpy-team-diplom/blob/main/group_settings.md).

### Токен пользователя
Для получения токена можно воспользоваться [ссылкой](https://api.vk.com/oauth%C2%AD/token?grant_type=password%E2%80%8B&client_id=2274003%E2%80%8B&client_secret=hHbZxrka2uZ6jB1inYsH%E2%80%8B&username=НОМЕРТЕЛФОНА%E2%80%8B&password=ПАРОЛЬ). Вместо ***username*** необходимо вставить номер телефона, ***password*** необходимо вставить пароль.

## Структура БД
| Пользователь                 |
| -----------------------------|
| ID Пользователя: Serial, PK  |
| ВК ID Пользователя: Varchar  |
| Возраст: Integer             |
| Пол: Integer                 |
| Город: Varchar               |

| Кандидат                     |
| -----------------------------|
| ID Кандидата: Serial, PK     |
| Имя: Varchar                 |
| Фамилия: Varchar             | 
| ВК ID: Varchar               | 

| Фотографии                                      |
| ------------------------------------------------|
| ID Фотографии: Serial, PK                       |
| ID Кандидата: Integer, FK(Кандидат.ID Кандидата)|
| ВК ID Фотографии: Varchar                       | 
| Количество лайков: Integer                      | 

| Пользователь-Кандидат                                     |
| ----------------------------------------------------------|
| ID Кандидата: Integer, FK(Кандидат.ID Кандидата)          |
| ID Пользователя: Integer, FK(Пользователь.ID Пользователя)|

## Логика работы чат-бота
 - В файле *main.py* необходимо заполнить **USERNAME**, **PASSWORD**, **PORT**, **DATABASE**. В файле *interaction_with_vk\settings.py* заполните **token_group**, **access_token**.
 - Бот получает информацию от пользователя с помощь *get_user_sex*, *get_user_city*, *get_user_age* в классе **VkUser** (пакет interaction_with_vk  модуль Vk_users.py)
 - С помощью модуля *vk_api* осуществляем поиск кандидатов по критериям, используется метод *search_candidates* в классе **VkCandidate** (пакет interaction_with_vk модуль Vk_candidates.py)
 - Для нахождения фото людей используется метод *get_photo* (пакет interaction_with_vk модуль Vk_candidates.py)
**ВАЖНО!** Для получения фото используется токен **пользователя**
 - После нахождения всех кандидатов они сортируются по количеству лайков методом *sorting_likes* (пакет interaction_with_vk модуль Vk_candidates.py)
 - Подключение к базе данных реализовано в пакете *models* в модуле **base.py**
 - Создание пользователя бота ВК реализуется методом *Users(Base)* (пакет models в модуле users.py)
 - Затем осуществляется проверка наличия кандидата в БД, наличия фотографий в БД, а также осуществляется добавление его в черный список или в избранное, данная реализация представлена в пакете ***db_handler**
 - Метод *candidates_list* (класса UserDb) пакета db_handler модуля user_handler.py – формирование листа кандидатов
 - В модуле *.gitignore* представлены файлы, которые программа будет игнорировать 
 - В модуле *BotVk* отображена логика работы бота с выводимыми сообщениями и настроенными кнопками
 - Для работы бота необходимо запустить файл **main.py**

## Установка и запуск проекта
Используйте следующие команды для установки и запуска проекта:

 - клонирование проекта:
```bash
git clone https://github.com/Ksenia-Mesh/Course_project-VK_bot.git
```
 - Установка и активация виртуального окружения:
 ```bash
python -m venv venv
.\venv\Scripts\activate
```
 - Подключение зависимостей:
```bash
pip install -r requirements.txt
```

В файле *main.py* заполните **USERNAME**, **PASSWORD**, **PORT**, **DATABASE**.
В файле interaction_with_vk\settings.py заполните **token_group**, **access_token**.

Запустите файл *main.py*.

Для начала работы с ботом напишите в чате "Привет".

Удачи!!!
