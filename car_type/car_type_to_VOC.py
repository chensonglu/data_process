# 将车分成23种
import os
import xml.dom.minidom
from xml.dom.minidom import Document

from car_carplate import exchange_to_std as ex

root_dir = '/dataset/yz/20171214/day/1080p/Annotations'
target_dir = '/data/VALID/car_type/VOC/Annotations'

# 26 types
car_types = ['家用轿车', '家用SUV', '家用MPV', '家用房车', '家用JEEP', '出租车', '公共汽车',
             '面包车', '小型客车', '大型客车', '箱式货车', '油罐车', '垃圾车', '货运卡车', '小型货运卡车', '校车',
             '赛车', '消防车', '救护车', '邮政车', '警车', '皮卡', '教练车', '四轮车', '三轮车', '搅拌车']
car_types_en = ['car', 'suv', 'mpv', 'caravan', 'jeep', 'taxi', 'bus', 'mini_bus', 'mini_passenger_car',
                'passenger_car', 'van', 'oil_truck', 'garbage_truck', 'truck', 'mini_truck', 'school_bus',
                'race_car', 'fire_truck', 'ambulance', 'postal_car', 'police_car', 'pickup_truck', 'coach_car',
                'quadricycle', 'tricycle', 'mixer_truck']

type_ch_en = {}
for i in range(len(car_types)):
    type_ch_en[car_types[i]] = car_types_en[i]


def gen_car_and_carplate_independently(fileitem):
    num_car = 0

    dom = xml.dom.minidom.parse(os.path.join(root_dir, fileitem))
    root = dom.documentElement

    # size
    size = root.getElementsByTagName('size')[0]
    width = int(size.getElementsByTagName('width')[0].childNodes[0].nodeValue)
    height = int(size.getElementsByTagName('height')[0].childNodes[0].nodeValue)
    depth = int(size.getElementsByTagName('depth')[0].childNodes[0].nodeValue)

    # 创建dom文档
    doc = Document()
    # 创建根节点
    annotation = doc.createElement('annotation')
    # 根节点插入dom树
    doc.appendChild(annotation)
    # folder
    folder = doc.createElement('folder')
    annotation.appendChild(folder)
    folder.appendChild(doc.createTextNode('car'))
    # filename
    filename = doc.createElement('filename')
    annotation.appendChild(filename)
    filename.appendChild(doc.createTextNode(fileitem.split('.')[0] + '.jpg'))
    # source
    source = doc.createElement('source')
    annotation.appendChild(source)
    database_ = doc.createElement('database')
    database_.appendChild(doc.createTextNode('car'))
    source.appendChild(database_)
    # 创建size节点
    size = doc.createElement('size')
    annotation.appendChild(size)
    width_ = doc.createElement('width')
    width_.appendChild(doc.createTextNode(str(width)))
    height_ = doc.createElement('height')
    height_.appendChild(doc.createTextNode(str(height)))
    depth_ = doc.createElement('depth')
    depth_.appendChild(doc.createTextNode(str(depth)))
    size.appendChild(width_)
    size.appendChild(height_)
    size.appendChild(depth_)
    # segmentation
    segmented = doc.createElement('segmented')
    annotation.appendChild(segmented)
    segmented.appendChild(doc.createTextNode(str(0)))

    # notice object and obj
    objects = root.getElementsByTagName('object')
    for index, obj in enumerate(objects):
        bndbox = obj.getElementsByTagName('bndbox')[0]
        try:
            car_type = obj.getElementsByTagName('type')[0].childNodes[0].nodeValue
        except:
            continue
        else:
            num_car += 1
            car_xmin = int(bndbox.getElementsByTagName('xmin')[0].childNodes[0].nodeValue)
            car_ymin = int(bndbox.getElementsByTagName('ymin')[0].childNodes[0].nodeValue)
            car_xmax = int(bndbox.getElementsByTagName('xmax')[0].childNodes[0].nodeValue)
            car_ymax = int(bndbox.getElementsByTagName('ymax')[0].childNodes[0].nodeValue)
            # 限制不超过图片上下界
            car_xmin = ex.limit_in_bounds(car_xmin, 1, width)
            car_ymin = ex.limit_in_bounds(car_ymin, 1, height)
            car_xmax = ex.limit_in_bounds(car_xmax, 1, width)
            car_ymax = ex.limit_in_bounds(car_ymax, 1, height)

            IsOccluded = int(obj.getElementsByTagName('occlusion')[0].childNodes[0].nodeValue)
            IsTruncated = int(obj.getElementsByTagName('truncated')[0].childNodes[0].nodeValue)
            IsDifficult = int(obj.getElementsByTagName('difficult')[0].childNodes[0].nodeValue)

            # car
            object = doc.createElement('object')
            annotation.appendChild(object)
            name = doc.createElement('name')
            name.appendChild(doc.createTextNode(type_ch_en[car_type]))
            object.appendChild(name)
            # pose
            pose_ = doc.createElement('pose')
            pose_.appendChild(doc.createTextNode('Unspecified'))
            object.appendChild(pose_)
            # occluded
            occluded_ = doc.createElement('occluded')
            occluded_.appendChild(doc.createTextNode(str(IsOccluded)))
            object.appendChild(occluded_)
            # truncated
            truncated_ = doc.createElement('truncated')
            truncated_.appendChild(doc.createTextNode(str(IsTruncated)))
            object.appendChild(truncated_)
            # difficult
            difficult_ = doc.createElement('difficult')
            difficult_.appendChild(doc.createTextNode(str(IsDifficult)))
            object.appendChild(difficult_)
            # the bndbox
            bndbox = doc.createElement('bndbox')
            object.appendChild(bndbox)
            xmin_ = doc.createElement('xmin')
            xmin_.appendChild(doc.createTextNode(str(car_xmin)))
            bndbox.appendChild(xmin_)
            ymin_ = doc.createElement('ymin')
            ymin_.appendChild(doc.createTextNode(str(car_ymin)))
            bndbox.appendChild(ymin_)
            xmax_ = doc.createElement('xmax')
            xmax_.appendChild(doc.createTextNode(str(car_xmax)))
            bndbox.appendChild(xmax_)
            ymax_ = doc.createElement('ymax')
            ymax_.appendChild(doc.createTextNode(str(car_ymax)))
            bndbox.appendChild(ymax_)

    if num_car > 0:
        fp = open(os.path.join(target_dir, fileitem), 'w')
        doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")

file_list = os.listdir(root_dir)
for fileitem in file_list:
    if fileitem.endswith('xml'):
        print(fileitem)
        gen_car_and_carplate_independently(fileitem)