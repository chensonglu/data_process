# ['000735', '004197', '000131']
# 下面代码找出哪三个没有车牌标注


import os

xmls = os.listdir('Annotations')

a = set()
b = set()

for xml in xmls:
	a.add(xml.split('.')[0])

fi = open('ImageSets/Main/all.txt')

lines = fi.readlines()

for line in lines:
	b.add(line.strip().split('.')[0])

print(a - b)
