# 在车牌周围随机扩大，生成包含车牌的周围区域图片，并根据数据集划分情况将新生成的数据集进行划分，从珠海标注的格式转换为VOC的xml格式
# 一张图片中包含多辆车，每辆车可能包含车牌也可能没有车牌


import os
import cv2
import random
import xml.dom.minidom
from xml.dom.minidom import Document

import sys
sys.path.append(".")
import shared_function as ex

root_xmls = r'C:\Users\chens\Desktop\20171214_20180203\720p\Annotations'
root_imgs = r'C:\Users\chens\Desktop\20171214_20180203\720p\JPEGImages'

target_xmls = r'C:\Users\chens\Desktop\20171214_20180203\720p\carplate_four_corners_local_region\Annotations'
target_imgs = r'C:\Users\chens\Desktop\20171214_20180203\720p\carplate_four_corners_local_region\JPEGImages'

root_imagesets = r'C:\Users\chens\Desktop\20171214_20180203\720p\ImageSets\Main'
target_imagesets = r'C:\Users\chens\Desktop\20171214_20180203\720p\carplate_four_corners_local_region\ImageSets\Main'

expand_num = 6


# 将车牌的背景随机扩大n倍
def expand_carplate(fileitem, n):
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

        # 003786.xml是一辆车两个车牌
        carplates = obj.getElementsByTagName('carplate')
        if len(carplates) == 0:
            continue
        else:
            # 如果只有一个车牌的情况，多于一个车牌直接跳过，不然容易造成干扰
            if len(carplates) == 1:
                carplate = carplates[0]
                carplate_x_top_left = round(
                    float(carplate.getElementsByTagName('x_top_left')[0].childNodes[0].nodeValue))
                carplate_y_top_left = round(
                    float(carplate.getElementsByTagName('y_top_left')[0].childNodes[0].nodeValue))
                carplate_x_top_right = round(
                    float(carplate.getElementsByTagName('x_top_right')[0].childNodes[0].nodeValue))
                carplate_y_top_right = round(
                    float(carplate.getElementsByTagName('y_top_right')[0].childNodes[0].nodeValue))
                carplate_x_bottom_right = round(
                    float(carplate.getElementsByTagName('x_bottom_right')[0].childNodes[0].nodeValue))
                carplate_y_bottom_right = round(
                    float(carplate.getElementsByTagName('y_bottom_right')[0].childNodes[0].nodeValue))
                carplate_x_bottom_left = round(
                    float(carplate.getElementsByTagName('x_bottom_left')[0].childNodes[0].nodeValue))
                carplate_y_bottom_left = round(
                    float(carplate.getElementsByTagName('y_bottom_left')[0].childNodes[0].nodeValue))

                # 将车牌四点顺序改为标准的左上右上右下左下
                results = ex.exchange_four_points_to_std(
                    [carplate_x_top_left, carplate_y_top_left, carplate_x_top_right, carplate_y_top_right,
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

                carplate_width = carplate_xmax - carplate_xmin
                carplate_height = carplate_ymax - carplate_ymin

                for x in range(1, expand_num+1):
                    print("generate NO. " + str(x) + "'s data.")
                    # 产生左上角随机偏移(xrand, yrand)
                    xrand = int(random.uniform(0, (n - 1) * carplate_width))
                    yrand = int(random.uniform(0, (n - 1) * carplate_height))
                    roi_xmin = max(int(carplate_xmin - xrand), car_xmin)
                    roi_ymin = max(int(carplate_ymin - yrand), car_ymin)
                    roi_xmax = min(int(roi_xmin + n * carplate_width), car_xmax)
                    roi_ymax = min(int(roi_ymin + n * carplate_height), car_ymax)
                    roi_x_top_left = int(carplate_x_top_left) - roi_xmin
                    roi_y_top_left = int(carplate_y_top_left) - roi_ymin
                    roi_x_top_right = int(carplate_x_top_right) - roi_xmin
                    roi_y_top_right = int(carplate_y_top_right) - roi_ymin
                    roi_x_bottom_right = int(carplate_x_bottom_right) - roi_xmin
                    roi_y_bottom_right = int(carplate_y_bottom_right) - roi_ymin
                    roi_x_bottom_left = int(carplate_x_bottom_left) - roi_xmin
                    roi_y_bottom_left = int(carplate_y_bottom_left) - roi_ymin

                    carplate_xmin_new = min(roi_x_top_left, roi_x_bottom_left)
                    carplate_ymin_new = min(roi_y_top_left, roi_y_top_right)
                    carplate_xmax_new = max(roi_x_bottom_right, roi_x_top_right)
                    carplate_ymax_new = max(roi_y_bottom_right, roi_y_bottom_left)

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
                    filename.appendChild(doc.createTextNode(fileitem.split('.')[0] + '_' + str(index + 1) + '_' + str(x) + '.jpg'))
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
                    width_.appendChild(doc.createTextNode(str(roi_xmax - roi_xmin)))
                    height_ = doc.createElement('height')
                    height_.appendChild(doc.createTextNode(str(roi_ymax - roi_ymin)))
                    depth_ = doc.createElement('depth')
                    depth_.appendChild(doc.createTextNode(str(depth)))
                    size.appendChild(width_)
                    size.appendChild(height_)
                    size.appendChild(depth_)
                    # segmentation
                    segmented = doc.createElement('segmented')
                    annotation.appendChild(segmented)
                    segmented.appendChild(doc.createTextNode(str(0)))

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
                    xmin_.appendChild(doc.createTextNode(str(carplate_xmin_new)))
                    bndbox.appendChild(xmin_)
                    ymin_ = doc.createElement('ymin')
                    ymin_.appendChild(doc.createTextNode(str(carplate_ymin_new)))
                    bndbox.appendChild(ymin_)
                    xmax_ = doc.createElement('xmax')
                    xmax_.appendChild(doc.createTextNode(str(carplate_xmax_new)))
                    bndbox.appendChild(xmax_)
                    ymax_ = doc.createElement('ymax')
                    ymax_.appendChild(doc.createTextNode(str(carplate_ymax_new)))
                    bndbox.appendChild(ymax_)

                    x_top_left_ = doc.createElement('x_top_left')
                    x_top_left_.appendChild(doc.createTextNode(str(roi_x_top_left)))
                    bndbox.appendChild(x_top_left_)
                    y_top_left_ = doc.createElement('y_top_left')
                    y_top_left_.appendChild(doc.createTextNode(str(roi_y_top_left)))
                    bndbox.appendChild(y_top_left_)
                    x_top_right_ = doc.createElement('x_top_right')
                    x_top_right_.appendChild(doc.createTextNode(str(roi_x_top_right)))
                    bndbox.appendChild(x_top_right_)
                    y_top_right_ = doc.createElement('y_top_right')
                    y_top_right_.appendChild(doc.createTextNode(str(roi_y_top_right)))
                    bndbox.appendChild(y_top_right_)
                    x_bottom_right_ = doc.createElement('x_bottom_right')
                    x_bottom_right_.appendChild(doc.createTextNode(str(roi_x_bottom_right)))
                    bndbox.appendChild(x_bottom_right_)
                    y_bottom_right_ = doc.createElement('y_bottom_right')
                    y_bottom_right_.appendChild(doc.createTextNode(str(roi_y_bottom_right)))
                    bndbox.appendChild(y_bottom_right_)
                    x_bottom_left_ = doc.createElement('x_bottom_left')
                    x_bottom_left_.appendChild(doc.createTextNode(str(roi_x_bottom_left)))
                    bndbox.appendChild(x_bottom_left_)
                    y_bottom_left_ = doc.createElement('y_bottom_left')
                    y_bottom_left_.appendChild(doc.createTextNode(str(roi_y_bottom_left)))
                    bndbox.appendChild(y_bottom_left_)

                    # save xml
                    fp = open(os.path.join(target_xmls, fileitem.split('.')[0] + '_' + str(index + 1) + '_' + str(x) + '.xml'), 'w')
                    doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
                    # save image
                    img = cv2.imread(os.path.join(root_imgs, fileitem.split('.')[0] + '.jpg'))
                    roi = img[roi_ymin:roi_ymax, roi_xmin:roi_xmax, :]
                    cv2.imwrite(os.path.join(target_imgs, fileitem.split('.')[0] + '_' + str(index + 1) + '_' + str(x) + '.jpg'), roi)


file_list = os.listdir(root_xmls)
for fileitem in file_list:
    if fileitem.endswith('xml'):
        print(fileitem)
        expand_carplate(fileitem, 3)


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
            if (len(fileitem_split) == 3 and line.strip() == fileitem_split[0]) or (len(fileitem_split) == 4 and line.strip() == fileitem_split[0] + '_' + fileitem_split[1]):
                fi_1.write(fileitem.strip().split(".")[0] + '\n')
    fi_1.close()
    fi.close()

