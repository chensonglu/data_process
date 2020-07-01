# 下面代码是根据新的test集，找到新的trainval集


import os

a = set()
b = set()

fi = open('ImageSets/Main/all.txt')
lines = fi.readlines()
fi.close()
for line in lines:
    a.add(line.strip().split('.')[0])

fi = open('ImageSets/Main/test_new.txt')
lines = fi.readlines()
fi.close()
for line in lines:
    b.add(line.strip().split('.')[0])

print(a - b)

fo = open('trainval_new.txt', 'w+')
for line in (a - b):
    fo.write(line + '\n')
fo.close()
