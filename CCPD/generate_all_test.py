import shutil
import os

# 一级目录
root_dir = '/dataset/CCPD/CCPD2019'
root_files = ['ccpd_blur', 'ccpd_db', 'ccpd_fn', 'ccpd_rotate', 'ccpd_tilt', 'ccpd_challenge']
target_dir = '/dataset/CCPD/CCPD2019/ccpd_all_test'
target_file = '/dataset/CCPD/CCPD2019/ccpd_all_test.txt'

file_set = set()
for root_file in root_files:
    root_path = os.path.join(root_dir, root_file)
    file_list = os.listdir(root_path)
    for idx, fileitem in enumerate(file_list):
        if idx % 5000 == 0:
            print(idx)
        file_set.add(fileitem)
        shutil.copy(os.path.join(root_path, fileitem), os.path.join(target_dir, fileitem))

fo = open(target_file, 'a+')
for f in file_set:
    fo.write(f.strip() + '\n')
fo.close()
