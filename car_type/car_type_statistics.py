# 从珠海标注中统计每种车辆type的数量


import os
import xml.dom.minidom

root_dir = r'C:\Users\chens\Desktop\20171214\720p\Annotations'

# 26 types
car_types = ['家用轿车', '家用SUV', '家用MPV', '家用房车', '家用JEEP', '出租车', '公共汽车',
             '面包车', '小型客车', '大型客车', '箱式货车', '油罐车', '垃圾车', '货运卡车', '小型货运卡车', '校车',
             '赛车', '消防车', '救护车', '邮政车', '警车', '皮卡', '教练车', '四轮车', '三轮车', '搅拌车']
car_types_en = ['car', 'suv', 'mpv', 'caravan', 'jeep', 'taxi', 'bus', 'mini_bus', 'mini_passenger_car',
                'passenger_car', 'van', 'oil_truck', 'garbage_truck', 'truck', 'mini_truck', 'school_bus',
                'race_car', 'fire_truck', 'ambulance', 'postal_car', 'police_car', 'pickup_truck', 'coach_car',
                'quadricycle', 'tricycle', 'mixer_truck']

# 16 types
easy_types = ['公共汽车', '小型客车', '大型客车', '箱式货车', '油罐车', '垃圾车', '校车', '赛车', '消防车',
              '救护车', '邮政车', '四轮车', '三轮车', '搅拌车', '货运卡车', '小型货运卡车']

type_count = {}
for i in range(len(car_types)):
    type_count[car_types[i]] = 0

type_ch_en = {}
for i in range(len(car_types)):
    type_ch_en[car_types[i]] = car_types_en[i]


def count_types(root_path, fileitem):
    dom = xml.dom.minidom.parse(os.path.join(root_path, fileitem))
    root = dom.documentElement
    objects = root.getElementsByTagName('object')

    for index, obj in enumerate(objects):
        try:
            type = obj.getElementsByTagName('type')[0].childNodes[0].nodeValue
        except:
            continue

        if type in car_types:
            type_count[type] += 1
        else:
            print(os.path.join(root_path, fileitem))
            print("不合法车型!!!!!!!!!!!!!")

file_list = os.listdir(root_dir)
for fileitem in file_list:
    if fileitem.endswith('xml'):
        count_types(root_dir, fileitem)

print(sorted(type_count.items(), key=lambda x: x[1], reverse=True))
print(len(type_count))
