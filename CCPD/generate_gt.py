from logging import root
import os

root_dir = '/data/CCPD/VOC/GT_val'
target_txt = '/data/CCPD/VOC/CCPD_val_gt.txt'
provinces = ["皖", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "京", "闽", "赣", "鲁", "豫", "鄂", "湘", "粤", "桂", "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "警", "学", "O"]
alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
             'X', 'Y', 'Z', 'O']
ads = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
       'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'O']

f = open(target_txt, 'w+')
images_name = os.listdir(root_dir)
for index, image_name in enumerate(images_name):
    if index % 1000 == 0:
        print(index)
    gt = ''
    numbers = image_name.strip().split('-')[-3]
    province = provinces[int(numbers.split('_')[0])]
    gt = gt + province
    alphabet = alphabets[int(numbers.split('_')[1])]
    gt = gt + alphabet
    for i in range(5):
        ad = ads[int(numbers.split('_')[i+2])]
        gt = gt + ad
    f.write(image_name + ' ' + gt + '\n')
f.close()