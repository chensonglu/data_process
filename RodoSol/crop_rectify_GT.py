from email.mime import image
import os
import cv2
import sys
sys.path.append(".")
import shared_function as ex
import math
import numpy as np

root_dir = '/home/yzbj/dataset/RodoSol/RodoSol-ALPR'
split_txt = '/home/yzbj/dataset/RodoSol/RodoSol-ALPR/split.txt'
train_gt = '/home/yzbj/data/RodoSol/result/GT_Train'
val_gt = '/home/yzbj/data/RodoSol/result/GT_Val'
test_gt = '/home/yzbj/data/RodoSol/result/GT_Test'
test_gt_single = '/home/yzbj/data/RodoSol/result/GT_Test_Single'
test_gt_double = '/home/yzbj/data/RodoSol/result/GT_Test_Double'
test_gt_rectified = '/home/yzbj/data/RodoSol/result/GT_Test_Rectified'
test_gt_rectified_single = '/home/yzbj/data/RodoSol/result/GT_Test_Rectified_Single'
test_gt_rectified_double = '/home/yzbj/data/RodoSol/result/GT_Test_Rectified_Double'
train_txt = '/home/yzbj/data/RodoSol/result/train.txt'
val_txt = '/home/yzbj/data/RodoSol/result/val.txt'
test_txt = '/home/yzbj/data/RodoSol/result/test.txt'
test_txt_single = '/home/yzbj/data/RodoSol/result/test_single.txt'
test_txt_double = '/home/yzbj/data/RodoSol/result/test_double.txt'

fr = open(split_txt, 'r')
lines = fr.readlines()
fr.close()
for line in lines:
    img = cv2.imread(os.path.join(root_dir, line.strip().split(';')[0]))
    label_txt = os.path.join(root_dir, line.strip().split(';')[0].replace('jpg', 'txt'))
    fr = open(label_txt, 'r')
    labels = fr.readlines()
    fr.close()
    corners = labels[3]
    characters = labels[1].strip().split(':')[1].strip()

    img_name = line.strip().split(';')[0].split('/')[-1]
    width = 1280
    height = 720
    channel = 3

    carplate_x_top_left = int(corners.strip().split(':')[1].strip().split(' ')[0].split(',')[0])
    carplate_y_top_left = int(corners.strip().split(':')[1].strip().split(' ')[0].split(',')[1])
    carplate_x_top_right = int(corners.strip().split(':')[1].strip().split(' ')[1].split(',')[0])
    carplate_y_top_right = int(corners.strip().split(':')[1].strip().split(' ')[1].split(',')[1])
    carplate_x_bottom_right = int(corners.strip().split(':')[1].strip().split(' ')[2].split(',')[0])
    carplate_y_bottom_right = int(corners.strip().split(':')[1].strip().split(' ')[2].split(',')[1])
    carplate_x_bottom_left = int(corners.strip().split(':')[1].strip().split(' ')[3].split(',')[0])
    carplate_y_bottom_left = int(corners.strip().split(':')[1].strip().split(' ')[3].split(',')[1])
    
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
    carplate_x_top_left = ex.limit_in_bounds(carplate_x_top_left, 0, width-1)
    carplate_y_top_left = ex.limit_in_bounds(carplate_y_top_left, 0, height-1)
    carplate_x_top_right = ex.limit_in_bounds(carplate_x_top_right, 0, width-1)
    carplate_y_top_right = ex.limit_in_bounds(carplate_y_top_right, 0, height-1)
    carplate_x_bottom_right = ex.limit_in_bounds(carplate_x_bottom_right, 0, width-1)
    carplate_y_bottom_right = ex.limit_in_bounds(carplate_y_bottom_right, 0, height-1)
    carplate_x_bottom_left = ex.limit_in_bounds(carplate_x_bottom_left, 0, width-1)
    carplate_y_bottom_left = ex.limit_in_bounds(carplate_y_bottom_left, 0, height-1)
    # bbox
    carplate_xmin = min(carplate_x_top_left, carplate_x_bottom_left)
    carplate_ymin = min(carplate_y_top_left, carplate_y_top_right)
    carplate_xmax = max(carplate_x_bottom_right, carplate_x_top_right)
    carplate_ymax = max(carplate_y_bottom_right, carplate_y_bottom_left)

    if line.strip().split(';')[-1] == 'training':
        cv2.imwrite(os.path.join(train_gt, img_name), img[carplate_ymin:carplate_ymax, carplate_xmin:carplate_xmax])
        # label
        fin = open(train_txt, 'a+')
        fin.write(img_name + ' ' + characters + '\n')
        fin.close()
    elif line.strip().split(';')[-1] == 'validation':
        cv2.imwrite(os.path.join(val_gt, img_name), img[carplate_ymin:carplate_ymax, carplate_xmin:carplate_xmax])
        # label
        fin = open(val_txt, 'a+')
        fin.write(img_name + ' ' + characters + '\n')
        fin.close()
    elif line.strip().split(';')[-1] == 'testing':
        # label
        fin = open(test_txt, 'a+')
        fin.write(img_name + ' ' + characters + '\n')
        fin.close()
        # GT
        cv2.imwrite(os.path.join(test_gt, img_name), img[carplate_ymin:carplate_ymax, carplate_xmin:carplate_xmax])
        if 'cars' in line:
            fin = open(test_txt_single, 'a+')
            fin.write(img_name + ' ' + characters + '\n')
            fin.close()
            cv2.imwrite(os.path.join(test_gt_single, img_name), img[carplate_ymin:carplate_ymax, carplate_xmin:carplate_xmax])
        elif 'motorcycles' in line:
            fin = open(test_txt_double, 'a+')
            fin.write(img_name + ' ' + characters + '\n')
            fin.close()
            cv2.imwrite(os.path.join(test_gt_double, img_name), img[carplate_ymin:carplate_ymax, carplate_xmin:carplate_xmax])
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
        cv2.imwrite(os.path.join(test_gt_rectified, img_name), carplate_crop)
        if 'cars' in line:
            cv2.imwrite(os.path.join(test_gt_rectified_single, img_name), carplate_crop)
        elif 'motorcycles' in line:
            cv2.imwrite(os.path.join(test_gt_rectified_double, img_name), carplate_crop)
