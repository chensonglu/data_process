import os
import xml.dom.minidom
from xml.dom.minidom import Document

root_file = '/data/TILT/1080p/carplate_only/ImageSets/Main/test.txt'
root_dir = '/data/TILT/1080p/carplate_only/Annotations'
target_dir = '/data/TILT/1080p/carplate_only/groundtruths'

fi = open(root_file)
lines = fi.readlines()
for line in lines:
    dom = xml.dom.minidom.parse(os.path.join(root_dir, line.strip()+'.xml'))
    root = dom.documentElement
    objects = root.getElementsByTagName('object')

    fo = open(os.path.join(target_dir, line.strip()+'.txt'), 'w')
    for index, obj in enumerate(objects):
        bndbox = obj.getElementsByTagName('bndbox')[0]
        xmin = bndbox.getElementsByTagName('xmin')[0].childNodes[0].nodeValue
        ymin = bndbox.getElementsByTagName('ymin')[0].childNodes[0].nodeValue
        xmax = bndbox.getElementsByTagName('xmax')[0].childNodes[0].nodeValue
        ymax = bndbox.getElementsByTagName('ymax')[0].childNodes[0].nodeValue
        fo.write("%s %s %s %s %s\n"%("carplate", xmin, ymin, xmax, ymax))
    fo.close()
fi.close()