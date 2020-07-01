# 将FTP上的多级文件合并到day和night文件夹里，并且重命名


import shutil
import os

# 一级目录
root_dir = '/dataset/yz/beijing_car_carplate/night'
target_dir = '/dataset/yz/beijing_car_carplate/tmp'

index = 0
file_list = os.listdir(root_dir)
for fileitem in file_list:
    if fileitem.endswith('xml'):
        print(fileitem)
        shutil.move(os.path.join(root_dir, fileitem), os.path.join(target_dir, str(index).zfill(6) + '.xml'))
        shutil.move(os.path.join(root_dir, fileitem.split('.')[0] + '.jpg'), os.path.join(target_dir, str(index).zfill(6) + '.jpg'))
        index = index + 1

# # 二级目录
# root_dir = '/dataset/yz/macao/day'
# target_dir = '/dataset/yz/macao/tmp'
#
# index = 0
# second_level_dirs = os.listdir(root_dir)
# for second_level_dir in second_level_dirs:
#     for fileitem in os.listdir(os.path.join(root_dir, second_level_dir)):
#         if fileitem.endswith('xml'):
#             print(fileitem)
#             shutil.copy(os.path.join(root_dir, second_level_dir, fileitem), os.path.join(target_dir, str(index).zfill(6) + '.xml'))
#             shutil.copy(os.path.join(root_dir, second_level_dir, fileitem.split('.')[0] + '.jpg'), os.path.join(target_dir, str(index).zfill(6) + '.jpg'))
#             index = index + 1