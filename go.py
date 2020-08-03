from mir_b import *
from mir_m import *
from reaviz_b import *
from reaviz_s import *
from samgups_b import *
from samgups_s import *
from sgspu_b import *
from sgspu_s import *
from sgspu_m import *
from sseu_b import *
from sseu_s import *
from sseu_m import *
from syzran_sseu_b import *
from taom_b import *
from taom_m import *
from tolgas_b import *
from json import loads
from json import dump

from jsonmerge import merge

def main_parse():
    with open('src/mir_bach.json', 'w', encoding="utf-8") as fp:
        json.dump(availableToAll_mirB(), fp, ensure_ascii=False)
    print('Complite!')

json_files = ['src/mir_bach.json', 'src/reaviz_bach.json', 'src/reaviz_spec.json']
with open('src/merged.json', 'w') as json_out:
    data = {}
    for file in json_files:
        with open(file, 'rb') as json_file:
            json_data = loads(json_file.read())
            data.update(merge(data, json_data))
    dump(data, json_out, indent=4)
