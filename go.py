from mir_b import *
from mir_m import *
from reaviz_b import *
from reaviz_s import *
from samgups_b import *
from samgups_s import *
from sgspu_b import *
from sgspu_m import *
from sgspu_s import *
from sseu_b import *
from sseu_m import *
from sseu_s import *
from syzran_sseu_b import *
from taom_b import *
from taom_m import *
from tolgas_b import *


def updateMainDict():
    mirB = availableToAll_mirB()
    mirM = availableToAll_mirM()
    reavizB = availableToAll_reavizB()
    reavizS = availableToAll_reavizS()
    samgupsB = availableToAll_samgupsB()
    samgupsS = availableToAll_samgupsS()
    sgspuB = arrayFormatting_sgspuB()
    sgspuS = availableToAll_sgspuS()
    sgspuM = arrayFormatting_sgspuM()
    sseuB = arrayFormatting_sseuB()
    sseuS = availableToAll_sseuS()
    sseuM = availableToAll_sseuM()
    syzran_sseuB = arrayFormatting_syzran_sseu_B()
    taomB = arrayFormatting_taomB()
    taomM = arrayFormatting_taomM()
    tolgasB = viewExcel_tolgas_b()

    alls = {}
    listDicts = [sgspuM]
    for i in range(len(listDicts)):

        alls.update(listDicts[i])
    return alls


def mainDictToJson():
    mainDict = updateMainDict()
    with open('src/all.json', "w", encoding="utf-8") as file:
        json.dump(mainDict, file, indent=4, sort_keys=False, ensure_ascii=False)


mainDictToJson()
