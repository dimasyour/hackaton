import itertools
import json
import random
import re

import numpy as np
import requests
from bs4 import BeautifulSoup

from text import *

URL_MIR_B = 'https://www.imi-samara.ru/abitur/bachelor/'
ID_MIR_B_VI = 0
ID_MIR_B_PP = 1


def parse_mirB(url, teg):
    r = requests.get(url, headers=HEADERS)
    r.encoding = 'utf-8'
    html = r
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'html.parser')
        tablici = soup.find_all('table')
        table = tablici[teg]
        table_rows = table.find_all('tr')
        newsList = []
        for tr in table_rows:
            td = tr.find_all('td')
            row = [i.get_text(strip=True) for i in td]
            newsList.append(row)
        return newsList
    else:
        print('Error parse()')


# форматирование списка образовальных программ
def plan_priema_mirB(teg):
    newsList = parse_mirB(URL_MIR_B, teg)
    del newsList[:3]
    for i in range(len(newsList)):
        for j in range(len(newsList[i])):
            if newsList[i][j] == '':
                newsList[i][j] = 'Приём не ведётся'
    return newsList


# форматирование списка образовальных программ
def arrayFormatting_mirB():
    newsList = parse_mirB(URL_MIR_B, ID_MIR_B_VI)
    count = 0  # сколько направлений подготовки
    del newsList[:2]
    newsList2 = list(itertools.chain.from_iterable(newsList))
    for i in range(len(newsList2)):
        if re.match(r"\d\d\.", newsList2[i]):
            count += 1
    num_columns = 9
    data = np.array(newsList2)
    arr = data.reshape(-1, num_columns)
    return arr


# сортировка по 2 элементу (алф.порядок) двоих списков и объеденение их
def mergerSortList():
    listPP = plan_priema_mirB(ID_MIR_B_PP)
    listVI = arrayFormatting_mirB()
    sortVI = sorted(listVI, key=lambda x: x[1])
    sortPP = sorted(listPP, key=lambda x: x[1])
    for i in range(len(sortVI)):
        if sortVI[i][1] == sortPP[i][1]:
            sortVI[i] = np.append(sortVI[i], sortPP[i][2:])
    return sortVI


# проверка на наличие всех выбранных предметов в списке строки образовательной программы
def subjectInRow_mirB(subList, List):
    return set(subList) <= set(List)


# выделение из элемента списка образовательной программы, всех предметов и их баллах
def viewSubjectAndBall_mirB(row):
    SubjectAndBall = []
    for i in range(2, len(row)):
        if (row[i] in SUBJECT) or (re.match(r"\d\d", row[i]) and (not re.match(r"\d\d\.", row[i]))):
            SubjectAndBall.append(row[i])
    return SubjectAndBall


# считаем платников
def valuePay(lst):
    sumPay = 0
    for i in range(16, len(lst)):
        if re.match(r"\d\d", lst[i]):
            sumPay += int(lst[i])
    return sumPay


# доступные абитуриенту образовательные программы МИР по выбранным предметам
def availableToMe_mirB(subject):
    array_first = mergerSortList()
    out_all = {}
    for i in range(len(array_first)):
        if len(array_first[i]) == 20 and (subjectInRow_mirB(subject, array_first[i]) is True):
            kcp_int = int(array_first[i][9]) - (valuePay(array_first[i]))
            out_all[array_first[i][0] + '_' + str(random.randint(0, MAX_INTEGER))] = {
                'code': str(array_first[i][0]),
                'program': str(array_first[i][1]),
                'level': 'bachelor',
                'vuz': 'mir',
                'subject_1': str(array_first[i][2]),
                'ball_1': str(array_first[i][3]),
                'subject_2': str(array_first[i][5]),
                'ball_2': str(array_first[i][6]),
                'subject_3': str(array_first[i][7]),
                'ball_3': str(array_first[i][8]),
                'subject_4': "-",
                'ball_4': "-",
                'plan_all': str(array_first[i][9]),
                'kcp': str(kcp_int),
                'special_o': str(array_first[i][10]),
                'special_z': str(array_first[i][11]),
                'special_oz': str(array_first[i][12]),
                'general_o': str(array_first[i][14]),
                'general_z': str(array_first[i][15]),
                'general_oz': str(array_first[i][16]),
                'goal_o': str(array_first[i][13]),
                'goal_oz': str(array_first[i][13]),
                'goal_z': str(array_first[i][13]),
                'pay_o': str(array_first[i][17]),
                'pay_z': str(array_first[i][18]),
                'pay_oz': str(array_first[i][19])
            }
    return out_all


# доступные абитуриенту образовательные программы МИР - бакалавриат
def availableToAll_mirB():
    array_first = mergerSortList()
    out_all = {}
    for i in range(len(array_first)):
        if len(array_first[i]) == 20:
            kcp_int = int(array_first[i][9]) - (valuePay(array_first[i]))
            out_all[array_first[i][0] + '_' + str(random.randint(0, MAX_INTEGER))] = {
                'code': str(array_first[i][0]),
                'program': str(array_first[i][1]),
                'level': 'bachelor',
                'vuz': 'mir',
                'subject_1': str(array_first[i][2]),
                'ball_1': str(array_first[i][3]),
                'subject_2': str(array_first[i][5]),
                'ball_2': str(array_first[i][6]),
                'subject_3': str(array_first[i][7]),
                'ball_3': str(array_first[i][8]),
                'subject_4': "-",
                'ball_4': "-",
                'plan_all': str(array_first[i][9]),
                'kcp': str(kcp_int),
                'special_o': str(array_first[i][10]),
                'special_z': str(array_first[i][11]),
                'special_oz': str(array_first[i][12]),
                'general_o': str(array_first[i][14]),
                'general_z': str(array_first[i][15]),
                'general_oz': str(array_first[i][16]),
                'goal_o': str(array_first[i][13]),
                'goal_oz': str(array_first[i][13]),
                'goal_z': str(array_first[i][13]),
                'pay_o': str(array_first[i][17]),
                'pay_z': str(array_first[i][18]),
                'pay_oz': str(array_first[i][19])
            }
    return out_all


with open('src/mir_bach.json', 'w', encoding="utf-8") as fp:
    json.dump(availableToAll_mirB(), fp, ensure_ascii=False)
