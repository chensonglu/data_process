# 将CLPD的文件名变成VOC格式的xml
import os
import cv2
import xml.dom.minidom
from xml.dom.minidom import Document
import csv

import sys
sys.path.append(".")
import shared_function as ex

csv_file = csv.DictReader(open('/home/yzbj/dataset/CLPD/CLPD.csv', 'r', encoding='gbk'))
img_path = '/home/yzbj/dataset/CLPD/CLPD_1200'
target_dir = '/home/yzbj/data/CLPD/VOC/Annotations'
test_path = '/home/yzbj/data/CLPD/VOC/ImageSets/Main/test.txt'


# 将图片中车和车牌的信息读到字典中
def read_to_dic():
    dic = {}

    for line in csv_file:
        img_name = line['path'].strip().split('/')[1].split('.')[0]
        dic[img_name] = line

    return dic


# 将上面得到的字典进一步处理,提取出其中有用的信息,得到进一步的字典
def pars_dic(key, value):
    dic = {}

    img_name = key + '.jpg'
    img = cv2.imread(os.path.join(img_path, img_name))
    height, width, channel = img.shape
    dic['img_name'] = img_name
    dic['height'] = height
    dic['width'] = width
    dic['channel'] = channel
    dic['carplate_x_top_left'] = value['x1']
    dic['carplate_y_top_left'] = value['y1']
    dic['carplate_x_top_right'] = value['x2']
    dic['carplate_y_top_right'] = value['y2']
    dic['carplate_x_bottom_right'] = value['x3']
    dic['carplate_y_bottom_right'] = value['y3']
    dic['carplate_x_bottom_left'] = value['x4']
    dic['carplate_y_bottom_left'] = value['y4']

    return dic


def CLPD_to_VOC(dic):
    img_name = dic['img_name']
    width = int(dic['width'])
    height = int(dic['height'])
    channel = dic['channel']

    carplate_x_top_left = int(dic['carplate_x_top_left'])
    carplate_y_top_left = int(dic['carplate_y_top_left'])
    carplate_x_top_right = int(dic['carplate_x_top_right'])
    carplate_y_top_right = int(dic['carplate_y_top_right'])
    carplate_x_bottom_right = int(dic['carplate_x_bottom_right'])
    carplate_y_bottom_right = int(dic['carplate_y_bottom_right'])
    carplate_x_bottom_left = int(dic['carplate_x_bottom_left'])
    carplate_y_bottom_left = int(dic['carplate_y_bottom_left'])
    
    # 将车牌四点顺序改为标准的左上右上右下左下
    results = ex.exchange_four_points_to_std([carplate_x_top_left, carplate_y_top_left, carplate_x_top_right, carplate_y_top_right,
                                    carplate_x_bottom_right, carplate_y_bottom_right, carplate_x_bottom_left, carplate_y_bottom_left])
    carplate_x_top_left = results['x_top_left']
    carplate_y_top_left = results['y_top_left']
    carplate_x_top_right = results['x_top_right']
    carplate_y_top_right = results['y_top_right']
    carplate_x_bottom_right = results['x_bottom_right']
    carplate_y_bottom_right = results['y_bottom_right']
    carplate_x_bottom_left = results['x_bottom_left']
    carplate_y_bottom_left = results['y_bottom_left']
    # 限制不超过图片上下界
    carplate_x_top_left = ex.limit_in_bounds(carplate_x_top_left, 1, width)
    carplate_y_top_left = ex.limit_in_bounds(carplate_y_top_left, 1, height)
    carplate_x_top_right = ex.limit_in_bounds(carplate_x_top_right, 1, width)
    carplate_y_top_right = ex.limit_in_bounds(carplate_y_top_right, 1, height)
    carplate_x_bottom_right = ex.limit_in_bounds(carplate_x_bottom_right, 1, width)
    carplate_y_bottom_right = ex.limit_in_bounds(carplate_y_bottom_right, 1, height)
    carplate_x_bottom_left = ex.limit_in_bounds(carplate_x_bottom_left, 1, width)
    carplate_y_bottom_left = ex.limit_in_bounds(carplate_y_bottom_left, 1, height)
    # bbox
    carplate_xmin = min(carplate_x_top_left, carplate_x_bottom_left)
    carplate_ymin = min(carplate_y_top_left, carplate_y_top_right)
    carplate_xmax = max(carplate_x_bottom_right, carplate_x_top_right)
    carplate_ymax = max(carplate_y_bottom_right, carplate_y_bottom_left)

    # 创建dom文档
    doc = Document()
    # 创建根节点
    annotation = doc.createElement('annotation')
    # 根节点插入dom树
    doc.appendChild(annotation)
    # folder
    folder = doc.createElement('folder')
    annotation.appendChild(folder)
    folder.appendChild(doc.createTextNode('carplate'))
    # filename
    filename = doc.createElement('filename')
    annotation.appendChild(filename)
    filename.appendChild(doc.createTextNode(str(img_name)))
    # source
    source = doc.createElement('source')
    annotation.appendChild(source)
    database_ = doc.createElement('database')
    database_.appendChild(doc.createTextNode('carplate'))
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
    occluded_.appendChild(doc.createTextNode(str(0)))
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

    x_top_left_ = doc.createElement('x_top_left')
    x_top_left_.appendChild(doc.createTextNode(str(carplate_x_top_left)))
    bndbox.appendChild(x_top_left_)
    y_top_left_ = doc.createElement('y_top_left')
    y_top_left_.appendChild(doc.createTextNode(str(carplate_y_top_left)))
    bndbox.appendChild(y_top_left_)
    x_top_right_ = doc.createElement('x_top_right')
    x_top_right_.appendChild(doc.createTextNode(str(carplate_x_top_right)))
    bndbox.appendChild(x_top_right_)
    y_top_right_ = doc.createElement('y_top_right')
    y_top_right_.appendChild(doc.createTextNode(str(carplate_y_top_right)))
    bndbox.appendChild(y_top_right_)
    x_bottom_right_ = doc.createElement('x_bottom_right')
    x_bottom_right_.appendChild(doc.createTextNode(str(carplate_x_bottom_right)))
    bndbox.appendChild(x_bottom_right_)
    y_bottom_right_ = doc.createElement('y_bottom_right')
    y_bottom_right_.appendChild(doc.createTextNode(str(carplate_y_bottom_right)))
    bndbox.appendChild(y_bottom_right_)
    x_bottom_left_ = doc.createElement('x_bottom_left')
    x_bottom_left_.appendChild(doc.createTextNode(str(carplate_x_bottom_left)))
    bndbox.appendChild(x_bottom_left_)
    y_bottom_left_ = doc.createElement('y_bottom_left')
    y_bottom_left_.appendChild(doc.createTextNode(str(carplate_y_bottom_left)))
    bndbox.appendChild(y_bottom_left_)

    # save xml
    fp = open(os.path.join(target_dir, img_name[:-4] + ".xml"), 'w')
    doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
    # save test txt
    fin = open(test_path, 'a+')
    fin.write(img_name[:-4] + '\n')
    fin.close()


dics = read_to_dic()
for key, value in dics.items():
    dic = pars_dic(key, value)
    CLPD_to_VOC(dic)