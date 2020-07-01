# 注意csv中ImageID的第一位可能显示不出来,sublime text可以显示出来
from xml.dom.minidom import Document
import cv2
from car_carplate import exchange_to_std as ex
import os
import csv

# 需要分别对validation和test进行处理
csv_file = csv.DictReader(open('/dataset/OID/test_car_carplate.csv'))
img_path = '/dataset/OID/test_with_carplate'
target_dir = '/data/OID/OID_carplate/VOC/Annotations'

# 是否需要车
need_car = False
# 是否需要车牌
need_carplate = True


# 将图片中车和车牌的信息读到字典中
def read_to_dic():
    dic = {}

    for line in csv_file:
        img_name = line['ImageID'].strip()
        if img_name in dic.keys():
            # 这句话意味着dic是深拷贝，不需要额外读取dic的值
            dic[img_name].append(line)
        else:
            dic[img_name] = [line]

    return dic


# 将上面得到的字典进一步处理,提取出其中有用的信息,得到进一步的字典
def pars_dic(key, values):
    dic = {}

    img_name = key + '.jpg'
    img = cv2.imread(os.path.join(img_path, img_name))
    height, width, channel = img.shape
    dic['img_name'] = img_name
    dic['height'] = height
    dic['width'] = width
    dic['channel'] = channel
    dic['url'] = values[0]['URL'].strip()
    dic['objs'] = []

    for value in values:
        tmp_dic = {}
        tmp_dic['LabelName'] = value['LabelName']
        tmp_dic['XMin'] = value['XMin']
        tmp_dic['XMax'] = value['XMax']
        tmp_dic['YMin'] = value['YMin']
        tmp_dic['YMax'] = value['YMax']
        tmp_dic['IsOccluded'] = value['IsOccluded']
        tmp_dic['IsTruncated'] = value['IsTruncated']

        dic['objs'].append(tmp_dic)

    return dic


def gen_car_and_carplate_independently(dic):
    num_car = 0
    num_carplate = 0

    img_name = dic['img_name']
    url = dic['url']
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
    folder.appendChild(doc.createTextNode('OID'))
    # filename
    filename = doc.createElement('filename')
    annotation.appendChild(filename)
    filename.appendChild(doc.createTextNode(img_name))
    # source
    source = doc.createElement('source')
    annotation.appendChild(source)
    database_ = doc.createElement('database')
    database_.appendChild(doc.createTextNode('OID car carplate'))
    source.appendChild(database_)
    url_ = doc.createElement('url')
    url_.appendChild(doc.createTextNode(url))
    source.appendChild(url_)
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
        obj_class = obj['LabelName']
        xmin = round(float(obj['XMin']) * width)
        xmax = round(float(obj['XMax']) * width)
        ymin = round(float(obj['YMin']) * height)
        ymax = round(float(obj['YMax']) * height)
        IsOccluded = int(obj['IsOccluded'])
        IsTruncated = int(obj['IsTruncated'])

        if need_car and obj_class == '/m/0k4j':
            num_car += 1
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
            truncated_.appendChild(doc.createTextNode(str(IsTruncated)))
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

        if need_carplate and obj_class == '/m/01jfm_':
            num_carplate += 1
            # 限制不超过图片上下界
            carplate_xmin = ex.limit_in_bounds(xmin, 1, width)
            carplate_ymin = ex.limit_in_bounds(ymin, 1, height)
            carplate_xmax = ex.limit_in_bounds(xmax, 1, width)
            carplate_ymax = ex.limit_in_bounds(ymax, 1, height)

            # carplate
            object = doc.createElement('object')
            annotation.appendChild(object)
            name = doc.createElement('name')
            name.appendChild(doc.createTextNode("carplate"))
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
            difficult_.appendChild(doc.createTextNode(str(0)))
            object.appendChild(difficult_)
            # the bndbox
            bndbox = doc.createElement('bndbox')
            object.appendChild(bndbox)
            xmin_ = doc.createElement('xmin')
            xmin_.appendChild(doc.createTextNode(str(carplate_xmin)))
            bndbox.appendChild(xmin_)
            ymin_ = doc.createElement('ymin')
            ymin_.appendChild(doc.createTextNode(str(carplate_ymin)))
            bndbox.appendChild(ymin_)
            xmax_ = doc.createElement('xmax')
            xmax_.appendChild(doc.createTextNode(str(carplate_xmax)))
            bndbox.appendChild(xmax_)
            ymax_ = doc.createElement('ymax')
            ymax_.appendChild(doc.createTextNode(str(carplate_ymax)))
            bndbox.appendChild(ymax_)

    # 如果车辆或者车牌数量大于0，才写入文件 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if (need_car and num_car > 0) or (need_carplate and num_carplate > 0):
        fp = open(os.path.join(target_dir, img_name.split('.')[0] + '.xml'), 'w')
        doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")


dics = read_to_dic()
for key, values in dics.items():
    dic = pars_dic(key, values)
    gen_car_and_carplate_independently(dic)
