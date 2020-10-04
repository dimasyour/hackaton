import itertools
import json
import random
import re

import requests
from bs4 import BeautifulSoup

from text import *

URL_SYZRAN_SSEU_B = 'http://www.syzran.sseu.ru/abitur/bachelor/#abitur_vstupitelnye-ispytania'
ID_SYZRAN_SSEU_B_VI = ['class', 'table table-bordered table-condensed table-scroll-thead']
ID_SYZRAN_SSEU_B_PP = ['class', 'table table-bordered table-condensed table-scroll-thead table-free-cel']


def parse_syzran_sseu_B(url, teg):
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
def plan_priema_syzran_sseu_B():
    newsList = parse_syzran_sseu_B(URL_SYZRAN_SSEU_B, ID_SYZRAN_SSEU_B_PP)
    del newsList[:4]
    for i in range(len(newsList)):
        for j in range(len(newsList[i])):
            if newsList[i][j] == '-':
                newsList[i][j] = 'Приём не ведётся'
    return newsList


# форматирование списка образовальных программ
def arrayFormatting_syzran_sseu_B():
    list_super_new = []
    newsList = parse_syzran_sseu_B(URL_SYZRAN_SSEU_B, ID_SYZRAN_SSEU_B_VI)
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


# проверка на наличие всех выбранных предметов в списке строки образовательной программы
def subjectInRow_syzran_sseu_B(subList, List):
    return set(subList) <= set(List)


# выделение из элемента списка образовательной программы, всех предметов и их баллах
def viewSubjectAndBall_syzran_sseu_B(row):
    SubjectAndBall = []
    for i in range(2, len(row)):
        if (row[i] in SUBJECT) or (re.match(r"\d\d", row[i]) and (not re.match(r"\d\d\.", row[i]))):
            SubjectAndBall.append(row[i])
    return SubjectAndBall


# все образовательные программы Сызранский Филиал СГЭУ - специалитет
def availableToMe_syzran_sseu_B(subject):
    array_first = arrayFormatting_syzran_sseu_B()
    planList = plan_priema_syzran_sseu_B()
    out_all = {}
    for i in range(len(array_first)):
        if len(array_first[i]) == 21 and (subjectInRow_syzran_sseu_B(subject, array_first[i]) is True):
            array_second = viewSubjectAndBall_syzran_sseu_B(array_first[i])
            out_all[array_first[i][0] + '_' + str(random.randint(0, MAX_INTEGER))] = {
                'code': str(array_first[i][0]),
                'program': str(array_first[i][1]),
                'level': 'bachelor',
                'vuz': 'syzran_sseu',
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
                'goal_o': 'Приём не ведётся',
                'goal_oz': 'Приём не ведётся',
                'goal_z': 'Приём не ведётся',
                'pay_o': str(planList[i][11]),
                'pay_z': str(planList[i][12]),
                'pay_oz': str(planList[i][13])
            }
        elif len(array_first[i]) == 26 and (subjectInRow_syzran_sseu_B(subject, array_first[i]) is True):
            array_second = viewSubjectAndBall_syzran_sseu_B(array_first[i])
            out_all[array_first[i][0] + '_' + str(random.randint(0, MAX_INTEGER))] = {
                'code': str(array_first[i][0]),
                'program': str(array_first[i][1]),
                'level': 'bachelor',
                'vuz': 'syzran_sseu',
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
                'goal_o': 'Приём не ведётся',
                'goal_oz': 'Приём не ведётся',
                'goal_z': 'Приём не ведётся',
                'pay_o': str(planList[i][11]),
                'pay_z': str(planList[i][12]),
                'pay_oz': str(planList[i][13])
            }
    return out_all


# доступные абитуриенту образовательные программы Cызранский Филиал СГЭУ - бакалавриат
def availableToAll_syzran_sseu_B():
    array_first = arrayFormatting_syzran_sseu_B()
    planList = plan_priema_syzran_sseu_B()
    out_all = {}
    for i in range(len(array_first)):
        if len(array_first[i]) == 21:
            array_second = viewSubjectAndBall_syzran_sseu_B(array_first[i])
            out_all[array_first[i][0] + '_' + str(random.randint(0, MAX_INTEGER))] = {
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
                'goal_o': 'Приём не ведётся',
                'goal_oz': 'Приём не ведётся',
                'goal_z': 'Приём не ведётся',
                'pay_o': str(planList[i][11]),
                'pay_z': str(planList[i][12]),
                'pay_oz': str(planList[i][13])
            }
        elif len(array_first[i]) == 26:
            array_second = viewSubjectAndBall_syzran_sseu_B(array_first[i])
            out_all[array_first[i][0] + '_' + str(random.randint(0, MAX_INTEGER))] = {
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
                'goal_o': 'Приём не ведётся',
                'goal_oz': 'Приём не ведётся',
                'goal_z': 'Приём не ведётся',
                'pay_o': str(planList[i][11]),
                'pay_z': str(planList[i][12]),
                'pay_oz': str(planList[i][13])
            }
    return out_all


with open('src/syzran_sseu_bach.json', 'w', encoding="utf-8") as fp:
    json.dump(availableToAll_syzran_sseu_B(), fp, ensure_ascii=False)
