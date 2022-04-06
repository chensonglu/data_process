# 将CCPD中的图片按照GT切割出来,保存为未水平矫正和水平矫正两个版本


import os
import cv2
import xml.dom.minidom
from xml.dom.minidom import Document
import math
import numpy as np

import sys
sys.path.append(".")
import shared_function as ex

root_dir = '/dataset/CCPD/CCPD2019/ccpd_all_test'
root_txt_dir = '/data/CCPD/test/ccpd_all_test/ImageSets/Main/test.txt'
GT_target_dir = '/data/CCPD/result/GT'
GT_rectified_target_dir = '/data/CCPD/result/GT_Rectified'


def crop_rectify_GT(fileitem):
    img = cv2.imread(os.path.join(root_dir, fileitem))
    height = 1160
    width = 720
    depth = 3
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

    # GT
    cv2.imwrite(os.path.join(GT_target_dir, fileitem), img[carplate_ymin:carplate_ymax, carplate_xmin:carplate_xmax])
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
    cv2.imwrite(os.path.join(GT_rectified_target_dir, fileitem), carplate_crop)


fi = open(root_txt_dir)
lines = fi.readlines()
for idx, line in enumerate(lines):
    if idx % 5000 == 0:
        print(idx)
    crop_rectify_GT(line.strip() + '.jpg')
