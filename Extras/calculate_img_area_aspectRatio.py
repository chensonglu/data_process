# 寻找图片的最大面积和最小面积,以及最大和最小的宽高比
# 一级目录


import cv2
import os
import shutil
import sys

root_dir = '/data/Cars_car_carplate/JPEGImages'
min_size = sys.float_info.max
max_size = 0
min_ar = sys.float_info.max
max_ar = 0

min_h = 0
min_w = 0
max_h = 0
max_w = 0

fi = open('/data/Cars_car_carplate/ImageSets/Main/all.txt')
file_list = fi.readlines()

# file_list = os.listdir(root_dir)
for fileitem in file_list:
    # img = cv2.imread(os.path.join(root_dir, fileitem))
    img = cv2.imread(os.path.join(root_dir, fileitem.strip() + '.jpg'))
    h, w, _ = img.shape
    if h*w > max_size:
        max_size = h*w
        max_h = h
        max_w = w
    if h*w < min_size:
        min_size = h * w
        min_h = h
        min_w = w

    if w/h > max_ar:
        max_ar = w/h
    if w/h < min_ar:
        min_ar = w/h

print(min_size)
print(min_h)
print(min_w)
print(max_size)
print(max_h)
print(max_w)
print(min_ar)
print(max_ar)