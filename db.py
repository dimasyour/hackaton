import sqlite3
import colorama
from datetime import datetime
from text import *

conn = sqlite3.connect("src/base.db")
c = conn.cursor()
print(colorama.Fore.LIGHTGREEN_EX + SUCCESS_DB_CONNECTION)


# проверяет есть ли пользователь с таким ID в БД
def check_if_exists(user_id):
    c.execute("SELECT * FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()
    if result is None:
        return False
    return True


# добавляет нового пользователя
def register_new_user(UserID):
    new_user_param = (UserID, 1, 0, 0, 0)
    c.execute("INSERT INTO users (user_id, user_reg, user_admin, user_ball, user_group) VALUES (?,?,?,?)",
              new_user_param)
    conn.commit()

    new_user_ball_param = (UserID, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    c.execute(
        "INSERT INTO user_ball (user_id, user_choose, math_p, russ, obsh, biol, phys, isto, info, himi, lite, geog, lang_e) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
        new_user_ball_param)
    conn.commit()


# проверяет есть ли хотя бы один предмет с добавленными баллами
def get_status_ball(user_id):
    c.execute(
        "SELECT math_p, russ, obsh, biol, phys, isto, info, himi, lite, geog, lang_e FROM user_ball WHERE user_id = %d" % user_id)
    result = c.fetchone()
    res = 0
    for i in range(0, 11):
        if result[i] != 0:
            res = res + 1
    if res > 0:
        return True
    else:
        return False


# показать баллы абитуриента
def get_my_ball(user_id):
    c.execute(
        "SELECT math_p, russ, obsh, biol, phys, isto, info, himi, lite, geog, lang_e FROM user_ball WHERE user_id = %d" % user_id)
    result = c.fetchone()
    i = 0
    myballs = []
    for i in range(11):
        if result[i] != 0:
            myballs.append(SUBJECTS_LIST[i] + ": " + str(result[i]))
            myballsString = '\n'.join(myballs)
    return myballsString


# получает значение из столбца статуса баллов (1 - добавил баллы, 0 - не добавил)
def get_user_ball_status(user_id):
    c.execute("SELECT user_ball FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()
    return result[0]


# записывает, какой предмет абитуриент, хочет выбрать, чтобы добавить баллы к нему (0 - выйти из добавления)
def set_user_choose_subject(user_id, subject_id):
    c.execute("UPDATE user_ball SET user_choose = %d WHERE user_id = %d" % (subject_id, user_id))
    conn.commit()


# изменяет баллы по выбранному предмету
def set_user_ball(user_id, subject, ball):
    if subject == 1:
        c.execute("UPDATE user_ball SET math_p = %s WHERE user_id = %d" % (ball, user_id))
        conn.commit()
    elif subject == 2:
        c.execute("UPDATE user_ball SET russ = %s WHERE user_id = %d" % (ball, user_id))
        conn.commit()
    elif subject == 3:
        c.execute("UPDATE user_ball SET obsh = %s WHERE user_id = %d" % (ball, user_id))
        conn.commit()
    elif subject == 4:
        c.execute("UPDATE user_ball SET biol = %s WHERE user_id = %d" % (ball, user_id))
        conn.commit()
    elif subject == 5:
        c.execute("UPDATE user_ball SET phys = %s WHERE user_id = %d" % (ball, user_id))
        conn.commit()
    elif subject == 6:
        c.execute("UPDATE user_ball SET isto = %s WHERE user_id = %d" % (ball, user_id))
        conn.commit()
    elif subject == 7:
        c.execute("UPDATE user_ball SET info = %s WHERE user_id = %d" % (ball, user_id))
        conn.commit()
    elif subject == 8:
        c.execute("UPDATE user_ball SET himi = %s WHERE user_id = %d" % (ball, user_id))
        conn.commit()
    elif subject == 9:
        c.execute("UPDATE user_ball SET lite = %s WHERE user_id = %d" % (ball, user_id))
        conn.commit()
    elif subject == 10:
        c.execute("UPDATE user_ball SET geog = %s WHERE user_id = %d" % (ball, user_id))
        conn.commit()
    elif subject == 11:
        c.execute("UPDATE user_ball SET lang_e = %s WHERE user_id = %d" % (ball, user_id))
        conn.commit()


# узнает к какому предмету хочет добавить студент баллы
def get_user_choose_subject(user_id):
    c.execute("SELECT user_choose FROM user_ball WHERE user_id = %d" % user_id)
    result = c.fetchone()
    return result[0]
