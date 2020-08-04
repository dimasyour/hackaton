import itertools
import json
import re

import requests
from bs4 import BeautifulSoup

from text import *

URL_SGSPU_B = 'http://www.pgsga.ru/abitur/bachelor/#abitur_vstupitelnye-ispytania'
ID_SGSPU_B_VI = ['class', 'table table-bordered table-condensed table-scroll-thead']
ID_SGSPU_B_PP = ['class', 'table table-bordered table-condensed table-scroll-thead table-free-cel']


def parse_sgspuB(url, teg):
    r = requests.get(url, headers=HEADERS)
    r.encoding = 'utf-8'
    html = r
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'html.parser')
        table = soup.find('table', teg)
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
def plan_priema_sgspuB():
    newsList = parse_sgspuB(URL_SGSPU_B, ID_SGSPU_B_PP)
    del newsList[:4]
    for i in range(len(newsList)):
        for j in range(len(newsList[i])):
            if newsList[i][j] == '-':
                newsList[i][j] = 'Приём не ведётся'
    return newsList


# форматирование списка образовальных программ
def arrayFormatting_sgspuB():
    list_super_new = []
    newsList = parse_sgspuB(URL_SGSPU_B, ID_SGSPU_B_VI)
    del newsList[:2]
    an_iterator = itertools.groupby(newsList, lambda x: x[0])
    newL = []
    for key, group in an_iterator:
        newL.append(list(group))
    for program in newL:
        new_stroka = program[0][1:4] + program[0][-1:]
        for stroka in program:
            new_stroka += stroka[4:-1]
        list_super_new.append(new_stroka)
    return list_super_new


# проверка на наличие всех выбранных предметов в списке строки образовательной программы
def subjectInRow_sgspuB(subList, List):
    return set(subList) <= set(List)


# выделение из элемента списка образовательной программы, всех предметов и их баллах
def viewSubjectAndBall_sgspuB(row):
    SubjectAndBall = []
    for i in range(2, len(row)):
        if (row[i] in SUBJECT) or (re.match(r"\d\d", row[i]) and (not re.match(r"\d\d\.", row[i]))):
            SubjectAndBall.append(row[i])
    return SubjectAndBall


# доступные абитуриенту образовательные программы СГСПУ по выбранным предметам
def availableToMe_sgspuB(subject):
    array_first = arrayFormatting_sgspuB()
    planList = plan_priema_sgspuB()
    out_all = []

    for i in range(len(array_first)):
        if len(array_first[i]) == 22 and (subjectInRow_sgspuB(subject, array_first[i]) is True):
            array_second = viewSubjectAndBall_sgspuB(array_first[i])
            out_all.append({
                'code': str(array_first[i][0]),
                'program': str(array_first[i][2]),
                'level': 'bachelor',
                'vuz': 'sgspu',
                'subject_1': str(array_second[0]),
                'ball_1': str(array_second[1]),
                'subject_2': str(array_second[2]),
                'ball_2': str(array_second[3]),
                'subject_3': str(array_second[4]),
                'ball_3': str(array_second[5]),
                'subject_4': "-",
                'ball_4': "-",
                'plan_all': str(planList[i][4]),
                'kcp': str(planList[i][5]),
                'special_o': str(planList[i][6]),
                'special_z': str(planList[i][7]),
                'special_oz': str(planList[i][8]),
                'general_o': str(planList[i][9]),
                'general_z': str(planList[i][10]),
                'general_oz': str(planList[i][11]),
                'goal_o': str(planList[i][12]),
                'goal_oz': str(planList[i][13]),
                'goal_z': str(planList[i][14]),
                'pay_o': str(planList[i][15]),
                'pay_z': str(planList[i][16]),
                'pay_oz': str(planList[i][17])
            })
        elif len(array_first[i]) == 28 and (subjectInRow_sgspuB(subject, array_first[i]) is True):
            array_second = viewSubjectAndBall_sgspuB(array_first[i])
            out_all.append({
                'code': str(array_first[i][0]),
                'program': str(array_first[i][2]),
                'level': 'bachelor',
                'vuz': 'sgspu',
                'subject_1': str(array_second[0]),
                'ball_1': str(array_second[1]),
                'subject_2': str(array_second[2]),
                'ball_2': str(array_second[3]),
                'subject_3': str(array_second[4]),
                'ball_3': str(array_second[5]),
                'subject_4': str(array_second[6]),
                'ball_4': str(array_second[7]),
                'plan_all': str(planList[i][4]),
                'kcp': str(planList[i][5]),
                'special_o': str(planList[i][6]),
                'special_z': str(planList[i][7]),
                'special_oz': str(planList[i][8]),
                'general_o': str(planList[i][9]),
                'general_z': str(planList[i][10]),
                'general_oz': str(planList[i][11]),
                'goal_o': str(planList[i][12]),
                'goal_oz': str(planList[i][13]),
                'goal_z': str(planList[i][14]),
                'pay_o': str(planList[i][15]),
                'pay_z': str(planList[i][16]),
                'pay_oz': str(planList[i][17])
            })
    return out_all


# все образовательные программы СГСПУ - бакалавриат
def availableToAll_sgspuB():
    array_first = arrayFormatting_sgspuB()
    planList = plan_priema_sgspuB()
    out_all = []

    for i in range(len(array_first)):
        if len(array_first[i]) == 22:
            array_second = viewSubjectAndBall_sgspuB(array_first[i])
            out_all.append({
                'code': str(array_first[i][0]),
                'program': str(array_first[i][2]),
                'level': 'bachelor',
                'subject_1': str(array_second[0]),
                'ball_1': str(array_second[1]),
                'subject_2': str(array_second[2]),
                'ball_2': str(array_second[3]),
                'subject_3': str(array_second[4]),
                'ball_3': str(array_second[5]),
                'subject_4': "-",
                'ball_4': "-",
                'plan_all': str(planList[i][4]),
                'kcp': str(planList[i][5]),
                'special_o': str(planList[i][6]),
                'special_z': str(planList[i][7]),
                'special_oz': str(planList[i][8]),
                'general_o': str(planList[i][9]),
                'general_z': str(planList[i][10]),
                'general_oz': str(planList[i][11]),
                'goal_o': str(planList[i][12]),
                'goal_oz': str(planList[i][13]),
                'goal_z': str(planList[i][14]),
                'pay_o': str(planList[i][15]),
                'pay_z': str(planList[i][16]),
                'pay_oz': str(planList[i][17])
            })
        elif len(array_first[i]) == 28:
            array_second = viewSubjectAndBall_sgspuB(array_first[i])
            out_all.append({
                'code': str(array_first[i][0]),
                'program': str(array_first[i][2]),
                'level': 'bachelor',
                'subject_1': str(array_second[0]),
                'ball_1': str(array_second[1]),
                'subject_2': str(array_second[2]),
                'ball_2': str(array_second[3]),
                'subject_3': str(array_second[4]),
                'ball_3': str(array_second[5]),
                'subject_4': str(array_second[6]),
                'ball_4': str(array_second[7]),
                'plan_all': str(planList[i][4]),
                'kcp': str(planList[i][5]),
                'special_o': str(planList[i][6]),
                'special_z': str(planList[i][7]),
                'special_oz': str(planList[i][8]),
                'general_o': str(planList[i][9]),
                'general_z': str(planList[i][10]),
                'general_oz': str(planList[i][11]),
                'goal_o': str(planList[i][12]),
                'goal_oz': str(planList[i][13]),
                'goal_z': str(planList[i][14]),
                'pay_o': str(planList[i][15]),
                'pay_z': str(planList[i][16]),
                'pay_oz': str(planList[i][17])
            })
    return out_all


with open('src/sgspu_bach.json', 'w', encoding="utf-8") as fp:
    json.dump(availableToAll_sgspuB(), fp, ensure_ascii=False)
