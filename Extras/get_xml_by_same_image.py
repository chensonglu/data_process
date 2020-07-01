# 根据图片名将对应xml移动到相同路径下


import shutil
import os

# 一级目录
root_dir = '/dataset/yz/20171214/night/720p/Annotations'
target_dir = '/dataset/yz/20171214/night/720p'

file_list = os.listdir(target_dir)
for fileitem in file_list:
    if fileitem.endswith('jpg'):
        print(fileitem)
        shutil.move(os.path.join(root_dir, fileitem.split('.')[0] + '.xml'), os.path.join(target_dir, fileitem.split('.')[0] + '.xml'))
