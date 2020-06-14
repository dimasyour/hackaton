import json
import requests
from bs4 import BeautifulSoup
from text import *
import re
import itertools
import numpy as np

URL = 'https://www.imi-samara.ru/abitur/bachelor/'
ID_VI = 0
ID_PP = 1


def parse(url, teg):
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
def plan_priema(teg):
    newsList = parse(URL, teg)
    del newsList[:3]
    for i in range(len(newsList)):
        for j in range(len(newsList[i])):
            if newsList[i][j] == '':
                newsList[i][j] = 'Приём не ведётся'
    return newsList


# форматирование списка образовальных программ
def arrayFormatting():
    newsList = parse(URL, ID_VI)
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


# проверка на наличие всех выбранных предметов в списке строки образовательной программы
def subjectInRow(subList, List):
    return set(subList) <= set(List)


# выделение из элемента списка образовательной программы, всех предметов и их баллах
def viewSubjectAndBall(row):
    SubjectAndBall = []
    for i in range(2, len(row)):
        if (row[i] in SUBJECT) or (re.match(r"\d\d", row[i]) and (not re.match(r"\d\d\.", row[i]))):
            SubjectAndBall.append(row[i])
    return SubjectAndBall


# доступные студенту образовательные программы по выбранным предметам
def availableToMe(subject):
    array_first = arrayFormatting()
    planList = plan_priema(ID_PP)
    out_all = []
    summaArray = []  # список содерждащий кол-во выделенных мест под платников для каждого НП
    var_kcp = 0  # КЦП не рассчитан в этой таблице, считаем сами (КЦП = Всего - Платники)
    for u in range(len(planList)):
        summa = 0
        for k in range(10, len(planList[u])):
            if re.match(r"\d\d", planList[u][k]) and not (re.match(r"\d\d\.", planList[u][k])):
                summa += int(planList[u][k])
        summaArray.append(summa)
    for i in range(len(array_first)):
        if len(array_first[i]) == 9 and (subjectInRow(subject, array_first[i]) is True):
            array_second = viewSubjectAndBall(array_first[i])
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
                'plan_all': str(planList[i][2]),
                'kcp': str(int(planList[i][2]) - int(summaArray[i])),
                'special_o': str(planList[i][3]),
                'special_z': str(planList[i][4]),
                'special_oz': str(planList[i][5]),
                'general_o': str(planList[i][7]),
                'general_z': str(planList[i][8]),
                'general_oz': str(planList[i][9]),
                'goal_o': str(planList[i][6]),
                'goal_oz': str(planList[i][6]),
                'goal_z': str(planList[i][6]),
                'pay_o': str(planList[i][10]),
                'pay_z': str(planList[i][11]),
                'pay_oz': str(planList[i][12])
            })
    return out_all


test = ['Математика']

with open('src/mir_bach.json', 'w', encoding="utf-8") as fp:
    json.dump(availableToMe(test), fp, ensure_ascii=False)
