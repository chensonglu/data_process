# 将CCPD的文件名变成VOC格式的xml


import os
import cv2
import xml.dom.minidom
from xml.dom.minidom import Document

import sys
sys.path.append(".")
import shared_function as ex

root_dir = '/dataset/CCPD/CCPD2019/ccpd_all_test'
root_txt_dir = '/data/CCPD/test/ccpd_all_test/ImageSets/Main/test.txt'
target_dir = '/data/CCPD/test/ccpd_all_test/Annotations'


def CCPD_to_VOC(fileitem):
    # image info
    # img = cv2.imread(os.path.join(root_dir, fileitem))
    # height, width, depth = img.shape
    height = 1160
    width = 720
    depth = 3

    # check image size
    if height != 1160 or width != 720:
        print("wrong size")
        print(fileitem)

    # four corners
    four_corners = fileitem.split('-')[3]
    if len(four_corners.split('_')) != 4:
        print("wrong four corners")
        print(fileitem)

    carplate_x_bottom_right = int(four_corners.split('_')[0].split('&')[0])
    carplate_y_bottom_right = int(four_corners.split('_')[0].split('&')[1])
    carplate_x_bottom_left = int(four_corners.split('_')[1].split('&')[0])
    carplate_y_bottom_left = int(four_corners.split('_')[1].split('&')[1])
    carplate_x_top_left = int(four_corners.split('_')[2].split('&')[0])
    carplate_y_top_left = int(four_corners.split('_')[2].split('&')[1])
    carplate_x_top_right = int(four_corners.split('_')[3].split('&')[0])
    carplate_y_top_right = int(four_corners.split('_')[3].split('&')[1])

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

    # 官方自带的bbox,视觉效果很不准,还是通过四点得到bbox
    # # bbox
    # bbox = fileitem.split('-')[2]
    # if len(bbox.split('_')) != 2:
    #     print("wrong bbox")
    #     print(fileitem)

    # carplate_xmin = int(bbox.split('_')[0].split('&')[0])
    # carplate_ymin = int(bbox.split('_')[0].split('&')[1])
    # carplate_xmax = int(bbox.split('_')[1].split('&')[0])
    # carplate_ymax = int(bbox.split('_')[1].split('&')[1])
    # # 限制不超过图片上下界
    # carplate_xmin = ex.limit_in_bounds(carplate_xmin, 1, width)
    # carplate_ymin = ex.limit_in_bounds(carplate_ymin, 1, height)
    # carplate_xmax = ex.limit_in_bounds(carplate_xmax, 1, width)
    # carplate_ymax = ex.limit_in_bounds(carplate_ymax, 1, height)

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
    filename.appendChild(doc.createTextNode(str(fileitem)))
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
    depth_.appendChild(doc.createTextNode(str(depth)))
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
    fp = open(os.path.join(target_dir, fileitem[:-4] + ".xml"), 'w')
    doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")


fi = open(root_txt_dir)
lines = fi.readlines()
for idx, line in enumerate(lines):
    if idx % 5000 == 0:
        print(idx)
    CCPD_to_VOC(line.strip() + '.jpg')
