# 根据YOLO的数据集txt，将其中子集（训练集或者测试集）的图片和对应标注取出来


import os
import shutil

root_dir = '/dataset/egohands_data/images'
root_file = '/dataset/egohands_data/test.txt'

target_dir = '/dataset/egohands_data/quantization_set'

fi = open(root_file)
lines = fi.readlines()
fi.close()
for line in lines:
    img_name = line.strip().split('/')[-1]
    xml_name = img_name.split('.')[0] + '.xml'
    shutil.copy(os.path.join(root_dir, img_name), os.path.join(target_dir, img_name))
    shutil.copy(os.path.join(root_dir, xml_name), os.path.join(target_dir, xml_name))
