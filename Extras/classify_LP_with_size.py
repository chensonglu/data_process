# 根据车牌左上点到左下右下组成直线的距离,将车牌分为大中小三类

import numpy as np
import os
import xml.dom.minidom
from xml.dom.minidom import Document
import cv2
import shutil

import sys
sys.path.append(".")
import shared_function as ex

root_xml_dir = '/data/TILT/720p/carplate_only/Annotations/'
root_xml_txt = '/data/TILT/720p/carplate_only/ImageSets/Main/test.txt'
root_img_dir = '/data/TILT/720p/carplate_only/JPEGImages/'

target_img_dir = '/data/TILT/720p/carplate_size/'

shutil.rmtree(os.path.join(target_img_dir, 'small'))
shutil.rmtree(os.path.join(target_img_dir, 'medium'))
shutil.rmtree(os.path.join(target_img_dir, 'large'))
os.mkdir(os.path.join(target_img_dir, 'small'))
os.mkdir(os.path.join(target_img_dir, 'medium'))
os.mkdir(os.path.join(target_img_dir, 'large'))


def gen_carplate_size(fileitem):
    dom = xml.dom.minidom.parse(os.path.join(root_xml_dir, fileitem))
    root = dom.documentElement

    # size
    size = root.getElementsByTagName('size')[0]
    width = int(size.getElementsByTagName('width')[0].childNodes[0].nodeValue)
    height = int(size.getElementsByTagName('height')[0].childNodes[0].nodeValue)
    depth = int(size.getElementsByTagName('depth')[0].childNodes[0].nodeValue)

    # iteration
    objects = root.getElementsByTagName('object')
    for index, obj in enumerate(objects):
        bndbox = obj.getElementsByTagName('bndbox')[0]

        carplate_x_top_left = round(float(bndbox.getElementsByTagName('x_top_left')[0].childNodes[0].nodeValue))
        carplate_y_top_left = round(float(bndbox.getElementsByTagName('y_top_left')[0].childNodes[0].nodeValue))
        carplate_x_top_right = round(float(bndbox.getElementsByTagName('x_top_right')[0].childNodes[0].nodeValue))
        carplate_y_top_right = round(float(bndbox.getElementsByTagName('y_top_right')[0].childNodes[0].nodeValue))
        carplate_x_bottom_right = round(float(bndbox.getElementsByTagName('x_bottom_right')[0].childNodes[0].nodeValue))
        carplate_y_bottom_right = round(float(bndbox.getElementsByTagName('y_bottom_right')[0].childNodes[0].nodeValue))
        carplate_x_bottom_left = round(float(bndbox.getElementsByTagName('x_bottom_left')[0].childNodes[0].nodeValue))
        carplate_y_bottom_left = round(float(bndbox.getElementsByTagName('y_bottom_left')[0].childNodes[0].nodeValue))

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

        QP = np.array([carplate_x_top_left - carplate_x_bottom_left, carplate_y_top_left - carplate_y_bottom_left])
        v = np.array([carplate_x_bottom_left - carplate_x_bottom_right, carplate_y_bottom_left - carplate_y_bottom_right])

        h = np.linalg.norm(np.cross(QP, v))/np.linalg.norm(v)

        # save image
        img = cv2.imread(os.path.join(root_img_dir, fileitem.split('.')[0] + '.jpg'))
        roi = img[carplate_ymin:carplate_ymax, carplate_xmin:carplate_xmax, :]
        if h <= 16:
            cv2.imwrite(os.path.join(target_img_dir + 'small', fileitem.split('.')[0] + '_' + str(index + 1) + '.jpg'), roi)
        elif h > 16 and h <= 32:
            cv2.imwrite(os.path.join(target_img_dir + 'medium', fileitem.split('.')[0] + '_' + str(index + 1) + '.jpg'), roi)
        else:
            cv2.imwrite(os.path.join(target_img_dir + 'large', fileitem.split('.')[0] + '_' + str(index + 1) + '.jpg'), roi)


fi = open(root_xml_txt)
lines = fi.readlines()
for line in lines:
    print(line)
    gen_carplate_size(line.strip() + '.xml')
