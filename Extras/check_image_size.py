# 查看文件夹下的图片是否符合尺寸要求
# 将不符合要求的图片筛选出来

import cv2
import os
import shutil
import sys

# 一级目录
root_dir = '/dataset/yz/201180203/night/720p/JPEGImages'
target_dir = '/dataset/yz/201180203/night/720p'

file_list = os.listdir(root_dir)
for fileitem in file_list:
    if fileitem.endswith('jpg'):
        img = cv2.imread(os.path.join(root_dir, fileitem))
        h, w, _ = img.shape
        if h != 720 or w != 1280:
            print(fileitem)
            shutil.move(os.path.join(root_dir, fileitem), os.path.join(target_dir, fileitem))
