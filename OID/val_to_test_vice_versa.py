# 这里的训练验证集来自于OID的测试集,测试集来自于OID的验证集,在分配的时候需要提前定好
# trian.txt和val.txt与trainval.txt相同
import os
import shutil

# OID验证集做测试集,只有当有对应xml时才写入,以防出现没有物体的现象
target_file = '/data/OID/OID_carplate/VOC/ImageSets/Main/test.txt'
file_list = os.listdir('/dataset/OID/validation_with_carplate')
anno_list = os.listdir('/data/OID/OID_carplate/VOC/Annotations')

fo = open(target_file, 'w')
for file in file_list:
    if file.strip().split('.')[0] + '.xml' in anno_list:
        fo.write(file.strip().split('.')[0] + '\n')
fo.close()

# OID测试集做训练集,只有当有对应xml时才写入,以防出现没有物体的现象
target_file = '/data/OID/OID_carplate/VOC/ImageSets/Main/trainval.txt'
file_list = os.listdir('/dataset/OID/test_with_carplate')
anno_list = os.listdir('/data/OID/OID_carplate/VOC/Annotations')

fo = open(target_file, 'w')
for file in file_list:
    if file.strip().split('.')[0] + '.xml' in anno_list:
        fo.write(file.strip().split('.')[0] + '\n')
fo.close()

# 这里train和val都用trainval,之后YOLO会用到
shutil.copy('/data/OID/OID_carplate/VOC/ImageSets/Main/trainval.txt', '/data/OID/OID_carplate/VOC/ImageSets/Main/train.txt')
shutil.copy('/data/OID/OID_carplate/VOC/ImageSets/Main/trainval.txt', '/data/OID/OID_carplate/VOC/ImageSets/Main/val.txt')
