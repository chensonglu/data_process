# 将文件夹内的文件重命名，按照000000的格式


import shutil
import os

# 一级目录
root_dir = '/dataset/yz/20171214/day/1080p/tmp'
target_dir = '/dataset/yz/20171214/day/1080p/night'

index = 816
file_list = os.listdir(root_dir)
for fileitem in file_list:
    if fileitem.endswith('xml'):
        print(fileitem)
        shutil.move(os.path.join(root_dir, fileitem), os.path.join(target_dir, str(index).zfill(6) + '.xml'))
        shutil.move(os.path.join(root_dir, fileitem.split('.')[0] + '.jpg'),
                    os.path.join(target_dir, str(index).zfill(6) + '.jpg'))
        index = index + 1