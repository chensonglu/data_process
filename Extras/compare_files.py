# 比较两个文件是否相同


import filecmp
import os

root_dir = '/dataset/yz/wrong/083327_00000034.xml'
target_dir = '/dataset/yz/20171214/day/JPEGImages'

file_list = os.listdir(target_dir)
for fileitem in file_list:
    if fileitem.endswith('xml'):
        if filecmp.cmp(root_dir, os.path.join(target_dir, fileitem)):
            print(fileitem)