# 这个数据集错误太多,暂时不用 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from xml.dom.minidom import Document
import cv2
from car_carplate import exchange_to_std as ex
import os
import csv

csv_file = csv.reader(open('/dataset/Udacity/labels.csv'))
img_path = '/dataset/Udacity/object-dataset'
target_dir = '/data/Udacity/Dataset2/Annotations'

Car_num = 0
Truck_num = 0
Pedestrian_num = 0
Biker_num = 0
TrafficLight_num = 0

# 是否需要车
need_car = True
# 是否需要卡车
need_truck = True
# 是否需要行人
need_pedestrian = True
# 是否需要自行车
need_biker = True
# 是否需要交通灯
need_trafficlight = False


# 将图片中车和车牌的信息读到字典中
def read_to_dic():
    dic = {}

    for line in csv_file:
        line = line[0]  # 注意这里是list
        line_part = line.strip().split()
        img_name = line_part[0]
        if img_name in dic.keys():
            # 这句话意味着dic是深拷贝，不需要额外读取dic的值
            dic[img_name].append(line)
        else:
            dic[img_name] = [line]

    return dic


# 将上面得到的字典进一步处理,提取出其中有用的信息,得到进一步的字典
def pars_dic(key, values):
    dic = {}

    img_name = key
    img = cv2.imread(os.path.join(img_path, img_name))
    height, width, channel = img.shape
    dic['img_name'] = img_name
    dic['height'] = height
    dic['width'] = width
    dic['channel'] = channel
    dic['objs'] = []

    for value in values:
        tmp_dic = {}
        value_part = value.strip().split()
        tmp_dic['Label'] = value_part[6].strip('"')
        tmp_dic['xmin'] = value_part[1]
        tmp_dic['xmax'] = value_part[3]
        tmp_dic['ymin'] = value_part[2]
        tmp_dic['ymax'] = value_part[4]
        tmp_dic['IsOccluded'] = value_part[5]

        dic['objs'].append(tmp_dic)

    return dic


def gen_car_and_carplate_independently(dic):
    num_car = 0
    num_truck = 0
    num_pedestrian = 0
    num_biker = 0
    num_trafficlight = 0

    img_name = dic['img_name']
    height = dic['height']
    width = dic['width']
    channel = dic['channel']
    objs = dic['objs']

    # 创建dom文档
    doc = Document()
    # 创建根节点
    annotation = doc.createElement('annotation')
    # 根节点插入dom树
    doc.appendChild(annotation)
    # folder
    folder = doc.createElement('folder')
    annotation.appendChild(folder)
    folder.appendChild(doc.createTextNode('Udacity'))
    # filename
    filename = doc.createElement('filename')
    annotation.appendChild(filename)
    filename.appendChild(doc.createTextNode(img_name))
    # source
    source = doc.createElement('source')
    annotation.appendChild(source)
    database_ = doc.createElement('database')
    database_.appendChild(doc.createTextNode('Udacity objects'))
    source.appendChild(database_)
    # 创建size节点
    size = doc.createElement('size')
    annotation.appendChild(size)
    width_ = doc.createElement('width')
    width_.appendChild(doc.createTextNode(str(width)))
    height_ = doc.createElement('height')
    height_.appendChild(doc.createTextNode(str(height)))
    depth_ = doc.createElement('depth')
    depth_.appendChild(doc.createTextNode(str(channel)))
    size.appendChild(width_)
    size.appendChild(height_)
    size.appendChild(depth_)
    # segmentation
    segmented = doc.createElement('segmented')
    annotation.appendChild(segmented)
    segmented.appendChild(doc.createTextNode(str(0)))

    for obj in objs:
        obj_class = obj['Label']
        xmin = round(float(obj['xmin']))
        xmax = round(float(obj['xmax']))
        ymin = round(float(obj['ymin']))
        ymax = round(float(obj['ymax']))
        IsOccluded = int(obj['IsOccluded'])

        if need_car and obj_class == 'car':
            num_car += 1
            global Car_num
            Car_num += 1
            # 限制不超过图片上下界
            car_xmin = ex.limit_in_bounds(xmin, 1, width)
            car_ymin = ex.limit_in_bounds(ymin, 1, height)
            car_xmax = ex.limit_in_bounds(xmax, 1, width)
            car_ymax = ex.limit_in_bounds(ymax, 1, height)

            # car
            object = doc.createElement('object')
            annotation.appendChild(object)
            name = doc.createElement('name')
            name.appendChild(doc.createTextNode('car'))
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
            truncated_.appendChild(doc.createTextNode(str(0)))
            object.appendChild(truncated_)
            # difficult
            difficult_ = doc.createElement('difficult')
            difficult_.appendChild(doc.createTextNode(str(0)))
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

        if need_truck and obj_class == 'truck':
            num_truck += 1
            global Truck_num
            Truck_num += 1
            # 限制不超过图片上下界
            truck_xmin = ex.limit_in_bounds(xmin, 1, width)
            truck_ymin = ex.limit_in_bounds(ymin, 1, height)
            truck_xmax = ex.limit_in_bounds(xmax, 1, width)
            truck_ymax = ex.limit_in_bounds(ymax, 1, height)

            # truck
            object = doc.createElement('object')
            annotation.appendChild(object)
            name = doc.createElement('name')
            name.appendChild(doc.createTextNode("truck"))
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
            truncated_.appendChild(doc.createTextNode(str(0)))
            object.appendChild(truncated_)
            # difficult
            difficult_ = doc.createElement('difficult')
            difficult_.appendChild(doc.createTextNode(str(0)))
            object.appendChild(difficult_)
            # the bndbox
            bndbox = doc.createElement('bndbox')
            object.appendChild(bndbox)
            xmin_ = doc.createElement('xmin')
            xmin_.appendChild(doc.createTextNode(str(truck_xmin)))
            bndbox.appendChild(xmin_)
            ymin_ = doc.createElement('ymin')
            ymin_.appendChild(doc.createTextNode(str(truck_ymin)))
            bndbox.appendChild(ymin_)
            xmax_ = doc.createElement('xmax')
            xmax_.appendChild(doc.createTextNode(str(truck_xmax)))
            bndbox.appendChild(xmax_)
            ymax_ = doc.createElement('ymax')
            ymax_.appendChild(doc.createTextNode(str(truck_ymax)))
            bndbox.appendChild(ymax_)

        if need_pedestrian and obj_class == 'pedestrian':
            num_pedestrian += 1
            global Pedestrian_num
            Pedestrian_num += 1
            # 限制不超过图片上下界
            pedestrian_xmin = ex.limit_in_bounds(xmin, 1, width)
            pedestrian_ymin = ex.limit_in_bounds(ymin, 1, height)
            pedestrian_xmax = ex.limit_in_bounds(xmax, 1, width)
            pedestrian_ymax = ex.limit_in_bounds(ymax, 1, height)

            # pedestrian
            object = doc.createElement('object')
            annotation.appendChild(object)
            name = doc.createElement('name')
            name.appendChild(doc.createTextNode("pedestrian"))
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
            truncated_.appendChild(doc.createTextNode(str(0)))
            object.appendChild(truncated_)
            # difficult
            difficult_ = doc.createElement('difficult')
            difficult_.appendChild(doc.createTextNode(str(0)))
            object.appendChild(difficult_)
            # the bndbox
            bndbox = doc.createElement('bndbox')
            object.appendChild(bndbox)
            xmin_ = doc.createElement('xmin')
            xmin_.appendChild(doc.createTextNode(str(pedestrian_xmin)))
            bndbox.appendChild(xmin_)
            ymin_ = doc.createElement('ymin')
            ymin_.appendChild(doc.createTextNode(str(pedestrian_ymin)))
            bndbox.appendChild(ymin_)
            xmax_ = doc.createElement('xmax')
            xmax_.appendChild(doc.createTextNode(str(pedestrian_xmax)))
            bndbox.appendChild(xmax_)
            ymax_ = doc.createElement('ymax')
            ymax_.appendChild(doc.createTextNode(str(pedestrian_ymax)))
            bndbox.appendChild(ymax_)

        if need_biker and obj_class == 'biker':
            num_biker += 1
            global Biker_num
            Biker_num += 1
            # 限制不超过图片上下界
            biker_xmin = ex.limit_in_bounds(xmin, 1, width)
            biker_ymin = ex.limit_in_bounds(ymin, 1, height)
            biker_xmax = ex.limit_in_bounds(xmax, 1, width)
            biker_ymax = ex.limit_in_bounds(ymax, 1, height)

            # biker
            object = doc.createElement('object')
            annotation.appendChild(object)
            name = doc.createElement('name')
            name.appendChild(doc.createTextNode("biker"))
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
            truncated_.appendChild(doc.createTextNode(str(0)))
            object.appendChild(truncated_)
            # difficult
            difficult_ = doc.createElement('difficult')
            difficult_.appendChild(doc.createTextNode(str(0)))
            object.appendChild(difficult_)
            # the bndbox
            bndbox = doc.createElement('bndbox')
            object.appendChild(bndbox)
            xmin_ = doc.createElement('xmin')
            xmin_.appendChild(doc.createTextNode(str(biker_xmin)))
            bndbox.appendChild(xmin_)
            ymin_ = doc.createElement('ymin')
            ymin_.appendChild(doc.createTextNode(str(biker_ymin)))
            bndbox.appendChild(ymin_)
            xmax_ = doc.createElement('xmax')
            xmax_.appendChild(doc.createTextNode(str(biker_xmax)))
            bndbox.appendChild(xmax_)
            ymax_ = doc.createElement('ymax')
            ymax_.appendChild(doc.createTextNode(str(biker_ymax)))
            bndbox.appendChild(ymax_)

        if need_trafficlight and obj_class == 'trafficLight':
            num_trafficlight += 1
            global TrafficLight_num
            TrafficLight_num += 1
            # 限制不超过图片上下界
            trafficlight_xmin = ex.limit_in_bounds(xmin, 1, width)
            trafficlight_ymin = ex.limit_in_bounds(ymin, 1, height)
            trafficlight_xmax = ex.limit_in_bounds(xmax, 1, width)
            trafficlight_ymax = ex.limit_in_bounds(ymax, 1, height)

            # trafficlight
            object = doc.createElement('object')
            annotation.appendChild(object)
            name = doc.createElement('name')
            name.appendChild(doc.createTextNode("trafficlight"))
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
            truncated_.appendChild(doc.createTextNode(str(0)))
            object.appendChild(truncated_)
            # difficult
            difficult_ = doc.createElement('difficult')
            difficult_.appendChild(doc.createTextNode(str(0)))
            object.appendChild(difficult_)
            # the bndbox
            bndbox = doc.createElement('bndbox')
            object.appendChild(bndbox)
            xmin_ = doc.createElement('xmin')
            xmin_.appendChild(doc.createTextNode(str(trafficlight_xmin)))
            bndbox.appendChild(xmin_)
            ymin_ = doc.createElement('ymin')
            ymin_.appendChild(doc.createTextNode(str(trafficlight_ymin)))
            bndbox.appendChild(ymin_)
            xmax_ = doc.createElement('xmax')
            xmax_.appendChild(doc.createTextNode(str(trafficlight_xmax)))
            bndbox.appendChild(xmax_)
            ymax_ = doc.createElement('ymax')
            ymax_.appendChild(doc.createTextNode(str(trafficlight_ymax)))
            bndbox.appendChild(ymax_)

    # 如果车辆,卡车或行人数量大于0，才写入文件 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if (need_car and num_car > 0) or (need_truck and num_truck > 0) or (need_pedestrian and num_pedestrian > 0)\
            or (need_biker and num_biker > 0) or (need_trafficlight and num_trafficlight > 0):
        fp = open(os.path.join(target_dir, img_name.split('.')[0] + '.xml'), 'w')
        doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")

dics = read_to_dic()
for key, values in dics.items():
    dic = pars_dic(key, values)
    gen_car_and_carplate_independently(dic)

print(Car_num)
print(Truck_num)
print(Pedestrian_num)
print(Biker_num)
print(TrafficLight_num)
