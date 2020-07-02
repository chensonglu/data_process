# -*- coding: UTF-8 -*-
# 将图片中车辆抠出来，并获取其中车牌相对车辆的位置，并根据数据集划分情况将新生成的数据集进行划分，从珠海标注的格式转换为VOC的xml格式


import os
import xml.dom.minidom
from xml.dom.minidom import Document
import cv2
import shutil

import sys
sys.path.append(".")
import shared_function as ex

root_xmls = r'C:\Users\chens\Desktop\20171214_20180203\720p\Annotations'
root_imgs = r'C:\Users\chens\Desktop\20171214_20180203\720p\JPEGImages'

target_xmls = r'C:\Users\chens\Desktop\20171214_20180203\720p\carplate_in_car\Annotations'
target_imgs = r'C:\Users\chens\Desktop\20171214_20180203\720p\carplate_in_car\JPEGImages'

root_imagesets = r'C:\Users\chens\Desktop\20171214_20180203\720p\ImageSets\Main'
target_imagesets = r'C:\Users\chens\Desktop\20171214_20180203\720p\carplate_in_car\ImageSets\Main'


def gen_carplate_in_car(fileitem):
    # read image
    img = cv2.imread(os.path.join(root_imgs, fileitem.split('.')[0] + '.jpg'))
    # read xml
    dom = xml.dom.minidom.parse(os.path.join(root_xmls, fileitem))
    root = dom.documentElement

    # size
    size = root.getElementsByTagName('size')[0]
    width = int(size.getElementsByTagName('width')[0].childNodes[0].nodeValue)
    height = int(size.getElementsByTagName('height')[0].childNodes[0].nodeValue)
    depth = int(size.getElementsByTagName('depth')[0].childNodes[0].nodeValue)

    # notice object and obj
    objects = root.getElementsByTagName('object')
    for index, obj in enumerate(objects):
        bndbox = obj.getElementsByTagName('bndbox')[0]

        car_xmin = int(bndbox.getElementsByTagName('xmin')[0].childNodes[0].nodeValue)
        car_ymin = int(bndbox.getElementsByTagName('ymin')[0].childNodes[0].nodeValue)
        car_xmax = int(bndbox.getElementsByTagName('xmax')[0].childNodes[0].nodeValue)
        car_ymax = int(bndbox.getElementsByTagName('ymax')[0].childNodes[0].nodeValue)
        # 限制不超过图片上下界
        car_xmin = ex.limit_in_bounds(car_xmin, 1, width)
        car_ymin = ex.limit_in_bounds(car_ymin, 1, height)
        car_xmax = ex.limit_in_bounds(car_xmax, 1, width)
        car_ymax = ex.limit_in_bounds(car_ymax, 1, height)
        # car size
        car_width = car_xmax - car_xmin
        car_height = car_ymax - car_ymin

        # 创建dom文档
        doc = Document()
        # 创建根节点
        annotation = doc.createElement('annotation')
        # 根节点插入dom树
        doc.appendChild(annotation)
        # folder
        folder = doc.createElement('folder')
        annotation.appendChild(folder)
        folder.appendChild(doc.createTextNode('carplate in car'))
        # filename
        filename = doc.createElement('filename')
        annotation.appendChild(filename)
        filename.appendChild(doc.createTextNode(fileitem.split('.')[0] + '.jpg'))
        # source
        source = doc.createElement('source')
        annotation.appendChild(source)
        database_ = doc.createElement('database')
        database_.appendChild(doc.createTextNode('carplate in car'))
        source.appendChild(database_)
        # 创建size节点
        size = doc.createElement('size')
        annotation.appendChild(size)
        width_ = doc.createElement('width')
        width_.appendChild(doc.createTextNode(str(car_width)))
        height_ = doc.createElement('height')
        height_.appendChild(doc.createTextNode(str(car_height)))
        depth_ = doc.createElement('depth')
        depth_.appendChild(doc.createTextNode(str(depth)))
        size.appendChild(width_)
        size.appendChild(height_)
        size.appendChild(depth_)
        # segmentation
        segmented = doc.createElement('segmented')
        annotation.appendChild(segmented)
        segmented.appendChild(doc.createTextNode(str(0)))

        # 003786.xml是一辆车两个车牌
        carplates = obj.getElementsByTagName('carplate')
        if len(carplates) == 0:
            continue
        else:
            for i in range(len(carplates)):
                carplate = carplates[i]
                carplate_x_top_left = round(float(carplate.getElementsByTagName('x_top_left')[0].childNodes[0].nodeValue))
                carplate_y_top_left = round(float(carplate.getElementsByTagName('y_top_left')[0].childNodes[0].nodeValue))
                carplate_x_top_right = round(float(carplate.getElementsByTagName('x_top_right')[0].childNodes[0].nodeValue))
                carplate_y_top_right = round(float(carplate.getElementsByTagName('y_top_right')[0].childNodes[0].nodeValue))
                carplate_x_bottom_right = round(float(carplate.getElementsByTagName('x_bottom_right')[0].childNodes[0].nodeValue))
                carplate_y_bottom_right = round(float(carplate.getElementsByTagName('y_bottom_right')[0].childNodes[0].nodeValue))
                carplate_x_bottom_left = round(float(carplate.getElementsByTagName('x_bottom_left')[0].childNodes[0].nodeValue))
                carplate_y_bottom_left = round(float(carplate.getElementsByTagName('y_bottom_left')[0].childNodes[0].nodeValue))
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
            
                carplate_xmin = min(carplate_x_top_left, carplate_x_bottom_left)
                carplate_ymin = min(carplate_y_top_left, carplate_y_top_right)
                carplate_xmax = max(carplate_x_bottom_right, carplate_x_top_right)
                carplate_ymax = max(carplate_y_bottom_right, carplate_y_bottom_left)
                # new four points in car
                carplate_x_top_left = ex.limit_in_bounds(carplate_x_top_left - car_xmin + 1, 1, car_width)
                carplate_y_top_left = ex.limit_in_bounds(carplate_y_top_left - car_ymin + 1, 1, car_height)
                carplate_x_top_right = ex.limit_in_bounds(carplate_x_top_right - car_xmin + 1, 1, car_width)
                carplate_y_top_right = ex.limit_in_bounds(carplate_y_top_right - car_ymin + 1, 1, car_height)
                carplate_x_bottom_right = ex.limit_in_bounds(carplate_x_bottom_right - car_xmin + 1, 1, car_width)
                carplate_y_bottom_right = ex.limit_in_bounds(carplate_y_bottom_right - car_ymin + 1, 1, car_height)
                carplate_x_bottom_left = ex.limit_in_bounds(carplate_x_bottom_left - car_xmin + 1, 1, car_width)
                carplate_y_bottom_left = ex.limit_in_bounds(carplate_y_bottom_left - car_ymin + 1, 1, car_height)
                # new bounding box in car
                carplate_xmin = ex.limit_in_bounds(carplate_xmin - car_xmin + 1, 1, car_width)
                carplate_ymin = ex.limit_in_bounds(carplate_ymin - car_ymin + 1, 1, car_height)
                carplate_xmax = ex.limit_in_bounds(carplate_xmax - car_xmin + 1, 1, car_width)
                carplate_ymax = ex.limit_in_bounds(carplate_ymax - car_ymin + 1, 1, car_height)
            
                IsOccluded = int(carplate.getElementsByTagName('occlusion')[0].childNodes[0].nodeValue)
                IsDifficult = int(carplate.getElementsByTagName('difficult')[0].childNodes[0].nodeValue)
            
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
                truncated_.appendChild(doc.createTextNode(str(0)))
                object.appendChild(truncated_)
                # difficult
                difficult_ = doc.createElement('difficult')
                difficult_.appendChild(doc.createTextNode(str(IsDifficult)))
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

        fp = open(os.path.join(target_xmls, fileitem.split('.')[0] + "_" + str(index) + ".xml"), 'w')
        doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
        # write image
        cv2.imwrite(os.path.join(target_imgs, fileitem.split('.')[0] + "_" + str(index) + ".jpg"),
                    img[car_ymin:car_ymax, car_xmin:car_xmax])


file_list = os.listdir(root_xmls)
for fileitem in file_list:
    if fileitem.endswith('xml'):
        print(fileitem)
        gen_carplate_in_car(fileitem)


for dataset in ['test.txt', 'train.txt', 'trainval.txt', 'val.txt']:
    dataset_path = os.path.join(root_imagesets, dataset)
    target_path = os.path.join(target_imagesets, dataset)
    file_list = os.listdir(target_xmls)
    fi = open(dataset_path)
    fi_1 = open(target_path, "a+")
    lines = fi.readlines()
    for line in lines:
        for fileitem in file_list:
            fileitem_split = fileitem.strip().split("_")
            # 这里是因为有些图片名字本身带着下划线，用名字前半部分与txt中匹配，如果包含则写入新的数据集分布
            if (len(fileitem_split) == 2 and line.strip() == fileitem_split[0]) or (len(fileitem_split) == 3 and line.strip() == fileitem_split[0] + '_' + fileitem_split[1]):
                fi_1.write(fileitem.strip().split(".")[0] + '\n')
    fi_1.close()
    fi.close()