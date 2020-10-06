import itertools
import json
import random
import re

import numpy as np
import requests
from bs4 import BeautifulSoup

from text import *

URL_SSEU_M = 'http://www.sseu.ru/abitur/bachelor/#abitur_vstupitelnye-ispytania'
ID_SSEU_M_VI = 8
ID_SSEU_M_PP = 1


def parse_sseuM(url, teg):
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
def plan_priema_sseuM():
    newsList = parse_sseuM(URL_SSEU_M, ID_SSEU_M_PP)
    del newsList[:4]
    for i in range(len(newsList)):
        del newsList[i][0]
        for j in range(len(newsList[i])):
            if newsList[i][j] == '-':
                newsList[i][j] = 'Приём не ведётся'
    return newsList


# форматирование списка образовальных программ
def arrayFormatting_sseuM():
    list_super_new = []
    newsList = parse_sseuM(URL_SSEU_M, ID_SSEU_M_VI)
    del newsList[:2]
    an_iterator = itertools.groupby(newsList, lambda x: x[0])
    newL = []
    for key, group in an_iterator:
        newL.append(list(group))
    for program in newL:
        new_stroka = program[0][1:3] + program[0][-1:]
        for stroka in program:
            new_stroka += stroka[3:-1]
        list_super_new.append(new_stroka)
    for i in range(len(list_super_new)):
        for j in range(len(list_super_new[i])):
            if list_super_new[i][j] == 'Письменная':
                list_super_new[i][j + 1] = 'русский'
    return list_super_new


# сортировка по 2 элементу (алф.порядок) двоих списков и объеденение их
def mergerSortList():
    listPP = plan_priema_sseuM()
    listVI = arrayFormatting_sseuM()
    sortVI = sorted(listVI, key=lambda x: x[1])
    sortPP = sorted(listPP, key=lambda x: x[1])
    for i in range(len(sortVI)):
        if sortVI[i][1] == sortPP[i][1]:
            sortVI[i] = np.append(sortVI[i], sortPP[i][2:])
    return sortVI


# проверка на наличие всех выбранных предметов в списке строки образовательной программы
def subjectInRow_sseuM(subList, List):
    return set(subList) <= set(List)


# выделение из элемента списка образовательной программы, всех предметов и их баллах
def viewSubjectAndBall_sseuM(row):
    SubjectAndBall = []
    for i in range(2, len(row)):
        if (row[i] in SUBJECT) or (re.match(r"\d\d", row[i]) and (not re.match(r"\d\d\.", row[i]))):
            SubjectAndBall.append(row[i])
    return SubjectAndBall


# доступные абитуриенту образовательные программы СГЭУ по выбранным предметам
def availableToMe_sseuM(subject):
    array_first = mergerSortList()
    out_all = {}
    for i in range(len(array_first)):
        if len(array_first[i]) == 23 and (subjectInRow_sseuM(subject, array_first[i]) is True):
            out_all[array_first[i][0] + '_' + str(random.randint(0, MAX_INTEGER))] = {
                'code': str(array_first[i][0]),
                'program': str(array_first[i][1]),
                'level': 'magistr',
                'subject_1': str(array_first[i][4]),
                'ball_1': str(array_first[i][6]),
                'subject_2': "-",
                'ball_2': "-",
                'subject_3': "-",
                'ball_3': "-",
                'subject_4': "-",
                'ball_4': "-",
                'plan_all': str(array_first[i][9]),
                'kcp': str(array_first[i][10]),
                'special_o': str(array_first[i][11]),
                'special_z': str(array_first[i][12]),
                'special_oz': str(array_first[i][13]),
                'general_o': str(array_first[i][14]),
                'general_z': str(array_first[i][15]),
                'general_oz': str(array_first[i][16]),
                'goal_o': str(array_first[i][17]),
                'goal_oz': str(array_first[i][18]),
                'goal_z': str(array_first[i][19]),
                'pay_o': str(array_first[i][20]),
                'pay_z': str(array_first[i][21]),
                'pay_oz': str(array_first[i][22]),
            }
    return out_all


# все образовательные программы СГЭУ - магистратура
def availableToAll_sseuM():
    array_first = mergerSortList()
    out_all = {}
    for i in range(len(array_first)):
        if len(array_first[i]) == 23:
            out_all[array_first[i][0] + '_' + str(random.randint(0, MAX_INTEGER))] = {
                'code': str(array_first[i][0]),
                'program': str(array_first[i][1]),
                'level': 'magistr',
                'vuz': 'sseu',
                'subject_1': str(array_first[i][4]),
                'ball_1': str(array_first[i][6]),
                'subject_2': "-",
                'ball_2': "-",
                'subject_3': "-",
                'ball_3': "-",
                'subject_4': "-",
                'ball_4': "-",
                'plan_all': str(array_first[i][9]),
                'kcp': str(array_first[i][10]),
                'special_o': str(array_first[i][11]),
                'special_z': str(array_first[i][12]),
                'special_oz': str(array_first[i][13]),
                'general_o': str(array_first[i][14]),
                'general_z': str(array_first[i][15]),
                'general_oz': str(array_first[i][16]),
                'goal_o': str(array_first[i][17]),
                'goal_oz': str(array_first[i][18]),
                'goal_z': str(array_first[i][19]),
                'pay_o': str(array_first[i][20]),
                'pay_z': str(array_first[i][21]),
                'pay_oz': str(array_first[i][22]),
            }
    return out_all


with open('src/sseu_mag.json', 'w', encoding="utf-8") as fp:
    json.dump(availableToAll_sseuM(), fp, ensure_ascii=False)
