# def mergerJsons():
#     list_of_file = ['src/mir_bach.json', 'src/reaviz_bach.json']
#     with open('src/all.json', 'w', encoding="utf-8") as f:
#         for i in list_of_file:
#             with open(i, 'r', encoding="utf-8") as f1:
#                 templates = json.load(f1)
#                 f.write(json.dumps(templates, ensure_ascii=False))
#     print('Success!')
#
#
# mergerJsons()
with open('src/reaviz_spec.json', encoding="utf-8") as f1:
    f1data = f1.read()
with open('src/mir_bach.json', encoding="utf-8") as f2:
    f2data = f2.read()

f1data += "\n"
f1data += f2data

with open('src/all.json', 'a', encoding="utf-8") as f3:
    f3.write(f1data)
print('Success 2!')
