# 根据VOC的xml统计车辆和车牌的数量，包括被遮挡和截断的数量


import os
import xml.dom.minidom

root_dir = r'C:\Users\chens\Desktop\20171214_20180203\720p\Annotations'
xml_file = r'C:\Users\chens\Desktop\20171214\720p\ImageSets\Main\trainval.txt'

car_num = 0
car_occluded = 0
car_truncated = 0
carplate_num = 0
carplate_occluded = 0
carplate_truncated = 0


def gen_car_and_carplate_independently(fileitem):
    dom = xml.dom.minidom.parse(os.path.join(root_dir, fileitem))
    root = dom.documentElement

    global car_num
    global car_occluded
    global car_truncated
    global carplate_num
    global carplate_occluded
    global carplate_truncated

    # notice object and obj
    objects = root.getElementsByTagName('object')
    for index, obj in enumerate(objects):
        name = obj.getElementsByTagName('name')[0].childNodes[0].nodeValue
        if name == 'car':
            car_num += 1
            try:
                occluded = obj.getElementsByTagName('occluded')[0].childNodes[0].nodeValue
                if int(occluded):
                    car_occluded += 1
            except:
                pass
            try:
                truncated = obj.getElementsByTagName('truncated')[0].childNodes[0].nodeValue
                if int(truncated):
                    car_truncated += 1
            except:
                pass
        if name == 'carplate':
            carplate_num += 1
            try:
                occluded = obj.getElementsByTagName('occluded')[0].childNodes[0].nodeValue
                if int(occluded):
                    carplate_occluded += 1
            except:
                pass
            try:
                truncated = obj.getElementsByTagName('truncated')[0].childNodes[0].nodeValue
                if int(truncated):
                    carplate_truncated += 1
            except:
                pass

fo = open(xml_file)
lines = fo.readlines()
for fileitem in lines:
    print(fileitem)
    gen_car_and_carplate_independently(fileitem.strip() + '.xml')


print("car_num")
print(car_num)
print("car_occluded")
print(car_occluded)
print("car_truncated")
print(car_truncated)
print("carplate_num")
print(carplate_num)
print("carplate_occluded")
print(carplate_occluded)
print("carplate_truncated")
print(carplate_truncated)