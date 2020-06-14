import json
import requests
from bs4 import BeautifulSoup
from text import *
import re
import itertools

URL_SGSPU = 'http://taom.academy/abitur/bachelor/#abitur_vstupitelnye-ispytania'
ID_SGSPU_VI = ['class', 'table table-bordered table-condensed table-scroll-thead']
ID_SGSPU_PP = ['class', 'table table-bordered table-condensed table-scroll-thead table-free-cel']


def parse(url, teg):
    r = requests.get(url, headers=HEADERS)
    r.encoding = 'utf-8'
    html = r
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'html.parser')
        tablici = soup.find_all('table', teg)
        table_spec = tablici[1]
        table_rows = table_spec.find_all('tr')
        newsList = []
        for tr in table_rows:
            td = tr.find_all('td')
            row = [i.get_text(strip=True) for i in td]
            newsList.append(row)
        return newsList
    else:
        print('Error parse()')


# форматирование списка образовальных программ
def plan_priema():
    newsList = parse(URL_SGSPU, ID_SGSPU_PP)
    del newsList[:4]
    for i in range(len(newsList)):
        for j in range(len(newsList[i])):
            if newsList[i][j] == '-':
                newsList[i][j] = 'Приём не ведётся'
    return newsList


# форматирование списка образовальных программ
def arrayFormatting():
    list_super_new = []
    newsList = parse(URL_SGSPU, ID_SGSPU_VI)
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
                list_super_new[i][j+1] = 'русский'
    return list_super_new


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
    planList = plan_priema()
    out_all = []
    for i in range(len(array_first)):
        if len(array_first[i]) == 9 and (subjectInRow(subject, array_first[i]) is True):
            array_second = viewSubjectAndBall(array_first[i])
            out_all.append({
                'code': str(array_first[i][0]),
                'program': str(array_first[i][1]),
                'level': 'magistr',
                'subject_1': str(array_second[0]),
                'ball_1': str(array_second[1]),
                'subject_2': "-",
                'ball_2': "-",
                'subject_3': "-",
                'ball_3': "-",
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
    return out_all


test = ['Междисциплинарный экзамен']

with open('src/taom_mag.json', 'w', encoding="utf-8") as fp:
    json.dump(availableToMe(test), fp, ensure_ascii=False)
