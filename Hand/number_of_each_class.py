# 统计手势数据中每类的数量


from pathlib import Path
import os
import xml.dom.minidom
from xml.dom.minidom import Document
import sys
sys.path.append(".")


ZHhands_path = '/dataset/ZHhands/labels'
name_dic = {}
for i in range(9):
    name_dic[i] = 0


p = Path(ZHhands_path)
xmls_per_scene = list(p.glob('*.xml'))
xmls_per_scene.sort()
for i, xml_path in enumerate(xmls_per_scene):
    print(str(xml_path))
    dom = xml.dom.minidom.parse(str(xml_path))
    root = dom.documentElement

    # if xml dont have any object, continue
    objects = root.getElementsByTagName('object')
    if len(objects) == 0:
        continue
    
    for index, obj in enumerate(objects):
        name = int(obj.getElementsByTagName('name')[0].childNodes[0].nodeValue)
        name_dic[name] = name_dic[name] + 1

print(name_dic)