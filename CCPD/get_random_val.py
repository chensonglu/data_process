# 从CCPD的验证集随机选取3000张作为训练时的验证集,以防99996张验证速度太慢


import random
from random import randint

random.seed(10)

fi = open('/data/CCPD/VOC/ImageSets/Main/val.txt')
lines = fi.readlines()
print(len(lines))
fi.close()

l = [randint(0, len(lines)-1) for i in range(3000)]

fi = open('/data/CCPD/VOC/ImageSets/Main/test.txt', 'w')
for idx in l:
    fi.write(lines[idx])
fi.close()
