# 从CCPD的验证集随机不重复选取5000张作为训练时的验证集,以防99996张验证速度太慢


import random

random.seed(10)

fi = open('/data/CCPD/VOC/ImageSets/Main/val.txt')
lines = fi.readlines()
print(len(lines))
fi.close()

l = random.sample(range(len(lines)), 5000)

fi = open('/data/CCPD/VOC/ImageSets/Main/test.txt', 'w')
for idx in l:
    fi.write(lines[idx])
fi.close()
