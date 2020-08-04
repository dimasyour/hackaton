#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
import logging
import os
import random
import re
import time

import apiai
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from command import *
from db import *
from keyboard import *

logging.basicConfig(filename=FILE_NAME_LOG, level=logging.INFO)
logging.info(STARTING_BOT_LOG + str(datetime.now()))

token = os.environ.get(TOKEN)
vk_session = vk_api.VkApi(token=token)

global Random


def random_chat_id():
    chat_id = 0
    chat_id += random.randint(0, 1000000000)
    return chat_id


def dialogFlow(msg):
    request = apiai.ApiAI(CLIENT_TOKEN_DIALOGFLOW).text_request()
    request.lang = 'ru'
    request.query = msg
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']
    return response


def main():
    while True:
        try:
            longpoll = VkLongPoll(vk_session)
            vk = vk_session.get_api()
            print(colorama.Fore.LIGHTGREEN_EX + SUCCESS_CONNECTION)
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    msg = event.text.lower()
                    if dialogFlow(msg) is None:
                        print(dialogFlow(msg))
                    else:
                        if not check_if_exists(event.user_id):
                            register_new_user(event.user_id)
                        if msg in START:
                            vk.messages.send(
                                user_id=event.user_id,
                                message=WELCOME_MESSAGE,
                                keyboard=keyboard_start(),
                                random_id=random_chat_id()
                            )
                        elif msg in ('/my_ball', '📖 мои баллы'):
                            if get_status_ball(event.user_id):
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="✅ Все ваши баллы указанны ниже: \n\n" + get_my_ball(event.user_id),
                                    keyboard=keyboard_subject_1(),
                                    random_id=random_chat_id()
                                )
                            else:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="⚠ Вы не добавили баллы!",
                                    keyboard=keyboard_add_ball(),
                                    random_id=random_chat_id()
                                )
                        elif msg in ('/add_ball', '📖 добавить баллы', 'показать предыдущие предметы'):
                            if get_status_ball(event.user_id):
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="✅ Все ваши баллы указанны ниже: \n\n" + get_my_ball(event.user_id),
                                    keyboard=keyboard_start(),
                                    random_id=random_chat_id()
                                )
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🔰Выберите предмет, который хотите добавить!",
                                    keyboard=keyboard_add_ball(),
                                    random_id=random_chat_id()
                                )
                            else:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🔰Выберите предмет, который хотите добавить!",
                                    keyboard=keyboard_subject_1(),
                                    random_id=random_chat_id()
                                )
                        elif msg in ('/add_ball_2', '📖 добавить баллы 2', 'показать следующие предметы'):
                            if get_user_ball_status(event.user_id) == 1:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Ваши баллы: ",
                                    keyboard=keyboard_start(),
                                    random_id=random_chat_id()
                                )
                            else:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🔰Выберите предмет, который хотите добавить!",
                                    keyboard=keyboard_subject_2(),
                                    random_id=random_chat_id()
                                )
                        elif event.text in (
                                '🧮 Профильная математика', '🇷🇺 Русский язык', '🏘 Обществознание', '🧬 Биология',
                                '⚛ Физика',
                                '🏰 История', '💻 Информатика', '🧪 Химия', '📝 Литература', '🗺 География'):
                            if event.text == '🧮 Профильная математика':
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🧮 Введите количество баллов по Профильной математике: ",
                                    keyboard=keyboard_insert_ball(),
                                    random_id=random_chat_id()
                                )
                                set_user_choose_subject(event.user_id, 1)
                            elif event.text == '🇷🇺 Русский язык':
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🇷🇺 Введите количество баллов по Русскому языку: ",
                                    keyboard=keyboard_insert_ball(),
                                    random_id=random_chat_id()
                                )
                                set_user_choose_subject(event.user_id, 2)
                            elif event.text == '🏘 Обществознание':
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🏘 Введите количество баллов по Обществознанию: ",
                                    keyboard=keyboard_insert_ball(),
                                    random_id=random_chat_id()
                                )
                                set_user_choose_subject(event.user_id, 3)
                            elif event.text == '🧬 Биология':
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🧬 Введите количество баллов по Биологии: ",
                                    keyboard=keyboard_insert_ball(),
                                    random_id=random_chat_id()
                                )
                                set_user_choose_subject(event.user_id, 4)
                            elif event.text == '⚛ Физика':
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="⚛ Введите количество баллов по Физике: ",
                                    keyboard=keyboard_insert_ball(),
                                    random_id=random_chat_id()
                                )
                                set_user_choose_subject(event.user_id, 5)
                            elif event.text == '🏰 История':
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🏰 Введите количество баллов по Истории: ",
                                    keyboard=keyboard_insert_ball(),
                                    random_id=random_chat_id()
                                )
                                set_user_choose_subject(event.user_id, 6)
                            elif event.text == '💻 Информатика':
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="💻 Введите количество баллов по Информатике: ",
                                    keyboard=keyboard_insert_ball(),
                                    random_id=random_chat_id()
                                )
                                set_user_choose_subject(event.user_id, 7)
                            elif event.text == '🧪 Химия':
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🧪 Введите количество баллов по Химии: ",
                                    keyboard=keyboard_insert_ball(),
                                    random_id=random_chat_id()
                                )
                                set_user_choose_subject(event.user_id, 8)
                            elif event.text == '📝 Литература':
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="📝 Введите количество баллов по Литературе: ",
                                    keyboard=keyboard_insert_ball(),
                                    random_id=random_chat_id()
                                )
                                set_user_choose_subject(event.user_id, 9)
                            elif event.text == '🗺 География':
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🗺 Введите количество баллов по Географии: ",
                                    keyboard=keyboard_insert_ball(),
                                    random_id=random_chat_id()
                                )
                                set_user_choose_subject(event.user_id, 10)
                        elif msg in ('/back_to_add_ball', '📖 назад к выбору предмета', 'отмена добавления балла'):
                            set_user_choose_subject(event.user_id, 0)
                            if get_user_ball_status(event.user_id) == 1:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Ваши баллы: ",
                                    keyboard=keyboard_start(),
                                    random_id=random_chat_id()
                                )
                            else:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🔰Выберите предмет, который хотите добавить!",
                                    keyboard=keyboard_subject_1(),
                                    random_id=random_chat_id()
                                )
                        elif (re.match(r"\d\d", event.text)) or (re.match(r"\d\d\d", event.text)):
                            set_user_ball(event.user_id, get_user_choose_subject(event.user_id), event.text)
                            vk.messages.send(
                                user_id=event.user_id,
                                message="🔰Вы ввели: " + event.text + "\n✔Баллы по предмету обновлены!",
                                keyboard=keyboard_start(),
                                random_id=random_chat_id()
                            )
                            set_user_choose_subject(event.user_id, 0)
                        elif msg in ('/remove_ball_to_choose_subject', '📖 удалить баллы по этому предмету'):
                            set_user_ball(event.user_id, get_user_choose_subject(event.user_id), 0)
                            if get_status_ball(event.user_id):
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="✔Баллы у предмета удалены! \n\n" + get_my_ball(event.user_id),
                                    keyboard=keyboard_start(),
                                    random_id=random_chat_id()
                                )
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🔰Выберите предмет, который хотите добавить!",
                                    keyboard=keyboard_subject_1(),
                                    random_id=random_chat_id()
                                )
                            else:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="✔Баллы у предмета удалены!\nБольше баллов нет. Добавьте их!",
                                    keyboard=keyboard_subject_1(),
                                    random_id=random_chat_id()
                                )

                        else:
                            vk.messages.send(
                                user_id=event.user_id,
                                message=dialogFlow(msg),
                                keyboard=keyboard_start(),
                                random_id=random_chat_id()
                            )

        except Exception as e:
            logging.error(str(datetime.now()) + " " + str(e))
            time.sleep(10)


if __name__ == '__main__':
    main()
