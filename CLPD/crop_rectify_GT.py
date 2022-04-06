# 将CCPD中的图片按照GT切割出来,保存为未水平矫正和水平矫正两个版本


import os
import cv2
import xml.dom.minidom
from xml.dom.minidom import Document
import math
import numpy as np
import csv

import sys
sys.path.append(".")
import shared_function as ex

csv_file = csv.DictReader(open('/dataset/CLPD/CLPD.csv', 'r', encoding='gbk'))
img_path = '/dataset/CLPD/CLPD_1200'
GT_target_dir = '/data/CLPD/result/GT'
GT_rectified_target_dir = '/data/CLPD/result/GT_Rectified'


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
    dic['img_name'] = img_name
    dic['carplate_x_top_left'] = value['x1']
    dic['carplate_y_top_left'] = value['y1']
    dic['carplate_x_top_right'] = value['x2']
    dic['carplate_y_top_right'] = value['y2']
    dic['carplate_x_bottom_right'] = value['x3']
    dic['carplate_y_bottom_right'] = value['y3']
    dic['carplate_x_bottom_left'] = value['x4']
    dic['carplate_y_bottom_left'] = value['y4']

    return dic


def crop_rectify_GT(dic):
    img = cv2.imread(os.path.join(img_path, dic['img_name']))
    height, width, channel = img.shape

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

    # GT
    cv2.imwrite(os.path.join(GT_target_dir, dic['img_name']), img[carplate_ymin:carplate_ymax, carplate_xmin:carplate_xmax])
    # GT_rectified
    warp_width = math.sqrt(math.pow(carplate_x_top_left-carplate_x_top_right, 2) + math.pow(carplate_y_top_left-carplate_y_top_right, 2))
    warp_height = math.sqrt(math.pow(carplate_x_top_left-carplate_x_bottom_left, 2) + math.pow(carplate_y_top_left-carplate_y_bottom_left, 2))
    pts1 = np.float32([[carplate_xmin, carplate_ymin+int(warp_height)], [carplate_xmin+int(warp_width), carplate_ymin+int(warp_height)], \
        [carplate_xmin, carplate_ymin], [carplate_xmin+int(warp_width), carplate_ymin]])
    pts2 = np.float32([[carplate_x_bottom_left, carplate_y_bottom_left], [carplate_x_bottom_right, carplate_y_bottom_right], \
            [carplate_x_top_left, carplate_y_top_left], [carplate_x_top_right, carplate_y_top_right]])
    M = cv2.getPerspectiveTransform(pts2, pts1)
    dst = cv2.warpPerspective(img, M, (width, height))
    carplate_crop = dst[carplate_ymin:carplate_ymin+int(warp_height), carplate_xmin:carplate_xmin+int(warp_width)]
    cv2.imwrite(os.path.join(GT_rectified_target_dir, dic['img_name']), carplate_crop)


dics = read_to_dic()
for key, value in dics.items():
    dic = pars_dic(key, value)
    crop_rectify_GT(dic)
