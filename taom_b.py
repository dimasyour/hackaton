import itertools
import json
import re

import requests
from bs4 import BeautifulSoup

from text import *

URL_TAOM_B = 'http://taom.academy/abitur/bachelor/#abitur_vstupitelnye-ispytania'
ID_TAOM_B_VI = ['class', 'table table-bordered table-condensed table-scroll-thead']
ID_TAOM_B_PP = ['class', 'table table-bordered table-condensed table-scroll-thead table-free-cel']


def parse_taomB(url, teg):
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
def plan_priema_taomB():
    newsList = parse_taomB(URL_TAOM_B, ID_TAOM_B_PP)
    del newsList[:4]
    for i in range(len(newsList)):
        for j in range(len(newsList[i])):
            if newsList[i][j] == '-':
                newsList[i][j] = 'Приём не ведётся'
    return newsList


# форматирование списка образовальных программ
def arrayFormatting_taomB():
    list_super_new = []
    newsList = parse_taomB(URL_TAOM_B, ID_TAOM_B_VI)
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


# доступные абитуриенту образовательные программы Тольяттинская академия управления по выбранным предметам
def subjectInRow_taomB(subList, List):
    return set(subList) <= set(List)


# выделение из элемента списка образовательной программы, всех предметов и их баллах
def viewSubjectAndBall_taomB(row):
    SubjectAndBall = []
    for i in range(2, len(row)):
        if (row[i] in SUBJECT) or (re.match(r"\d\d", row[i]) and (not re.match(r"\d\d\.", row[i]))):
            SubjectAndBall.append(row[i])
    return SubjectAndBall


# доступные абитуриенту образовательные программы Тольяттинская академия управления по выбранным предметам
def availableToMe_taomB(subject):
    array_first = arrayFormatting_taomB()
    planList = plan_priema_taomB()
    out_all = []
    for i in range(len(array_first)):
        if len(array_first[i]) == 21 and (subjectInRow_taomB(subject, array_first[i]) is True):
            array_second = viewSubjectAndBall_taomB(array_first[i])
            out_all.append({
                'code': str(array_first[i][0]),
                'program': str(array_first[i][1]),
                'level': 'bachelor',
                'vuz': 'taom',
                'subject_1': str(array_second[0]),
                'ball_1': str(array_second[1]),
                'subject_2': str(array_second[2]),
                'ball_2': str(array_second[3]),
                'subject_3': str(array_second[4]),
                'ball_3': str(array_second[5]),
                'subject_4': "-",
                'ball_4': "-",
                'plan_all': str(planList[i][3]),
                'kcp': str(planList[i][4]),
                'special_o': str(planList[i][5]),
                'special_z': str(planList[i][6]),
                'special_oz': str(planList[i][7]),
                'general_o': str(planList[i][8]),
                'general_z': str(planList[i][9]),
                'general_oz': str(planList[i][10]),
                'goal_o': str(planList[i][11]),
                'goal_oz': str(planList[i][12]),
                'goal_z': str(planList[i][13]),
                'pay_o': str(planList[i][14]),
                'pay_z': str(planList[i][15]),
                'pay_oz': str(planList[i][16])
            })
        elif len(array_first[i]) == 27 and (subjectInRow_taomB(subject, array_first[i]) is True):
            array_second = viewSubjectAndBall_taomB(array_first[i])
            out_all.append({
                'code': str(array_first[i][0]),
                'program': str(array_first[i][1]),
                'level': 'bachelor',
                'vuz': 'taom',
                'subject_1': str(array_second[0]),
                'ball_1': str(array_second[1]),
                'subject_2': str(array_second[2]),
                'ball_2': str(array_second[3]),
                'subject_3': str(array_second[4]),
                'ball_3': str(array_second[5]),
                'subject_4': str(array_second[6]),
                'ball_4': str(array_second[7]),
                'plan_all': str(planList[i][3]),
                'kcp': str(planList[i][4]),
                'special_o': str(planList[i][5]),
                'special_z': str(planList[i][6]),
                'special_oz': str(planList[i][7]),
                'general_o': str(planList[i][8]),
                'general_z': str(planList[i][9]),
                'general_oz': str(planList[i][10]),
                'goal_o': str(planList[i][11]),
                'goal_oz': str(planList[i][12]),
                'goal_z': str(planList[i][13]),
                'pay_o': str(planList[i][14]),
                'pay_z': str(planList[i][15]),
                'pay_oz': str(planList[i][16])
            })
    return out_all


# доступные абитуриенту образовательные программы Тольяттинская академия управления - бакалавриат
def availableToAll_taomB():
    array_first = arrayFormatting_taomB()
    planList = plan_priema_taomB()
    out_all = []
    for i in range(len(array_first)):
        if len(array_first[i]) == 21:
            array_second = viewSubjectAndBall_taomB(array_first[i])

            out_all.append({
                'code': str(array_first[i][0]),
                'program': str(array_first[i][1]),
                'level': 'bachelor',
                'subject_1': str(array_second[0]),
                'ball_1': str(array_second[1]),
                'subject_2': str(array_second[2]),
                'ball_2': str(array_second[3]),
                'subject_3': str(array_second[4]),
                'ball_3': str(array_second[5]),
                'subject_4': "-",
                'ball_4': "-",
                'plan_all': str(planList[i][3]),
                'kcp': str(planList[i][4]),
                'special_o': str(planList[i][5]),
                'special_z': str(planList[i][6]),
                'special_oz': str(planList[i][7]),
                'general_o': str(planList[i][8]),
                'general_z': str(planList[i][9]),
                'general_oz': str(planList[i][10]),
                'goal_o': str(planList[i][11]),
                'goal_oz': str(planList[i][12]),
                'goal_z': str(planList[i][13]),
                'pay_o': str(planList[i][14]),
                'pay_z': str(planList[i][15]),
                'pay_oz': str(planList[i][16])
            })
        elif len(array_first[i]) == 27:
            array_second = viewSubjectAndBall_taomB(array_first[i])
            out_all.append({
                'code': str(array_first[i][0]),
                'program': str(array_first[i][1]),
                'level': 'bachelor',
                'subject_1': str(array_second[0]),
                'ball_1': str(array_second[1]),
                'subject_2': str(array_second[2]),
                'ball_2': str(array_second[3]),
                'subject_3': str(array_second[4]),
                'ball_3': str(array_second[5]),
                'subject_4': str(array_second[6]),
                'ball_4': str(array_second[7]),
                'plan_all': str(planList[i][3]),
                'kcp': str(planList[i][4]),
                'special_o': str(planList[i][5]),
                'special_z': str(planList[i][6]),
                'special_oz': str(planList[i][7]),
                'general_o': str(planList[i][8]),
                'general_z': str(planList[i][9]),
                'general_oz': str(planList[i][10]),
                'goal_o': str(planList[i][11]),
                'goal_oz': str(planList[i][12]),
                'goal_z': str(planList[i][13]),
                'pay_o': str(planList[i][14]),
                'pay_z': str(planList[i][15]),
                'pay_oz': str(planList[i][16])
            })
    return out_all


with open('src/taom_bach.json', 'w', encoding="utf-8") as fp:
    json.dump(availableToAll_taomB(), fp, ensure_ascii=False)
