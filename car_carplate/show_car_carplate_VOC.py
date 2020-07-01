# coding=utf-8
# 用于同时展示转换后VOC格式中的车辆和车牌


import os
import cv2
import glob
from xml.dom import minidom

img_root_dir = 'C:\\Users\\chens\\Desktop\\20171214\\720p\\JPEGImages\\'
xml_root_dir = 'C:\\Users\\chens\\Desktop\\20171214\\720p\\car_carplate\\'
xmls = os.listdir(xml_root_dir)
num = len(glob.glob(xml_root_dir +"*.xml"))
print(num)

for i, xml_ in enumerate(xmls):
    if i % 1 != 0:
        continue
    # if xml_ != '003918_2_2.xml':
    #     continue
    if xml_.endswith('xml'):
        img_name = img_root_dir + xml_.split('.')[0] + '.jpg'
        xml_name = xml_root_dir +xml_
        print(img_name)
        print(xml_name)
        img = cv2.imread(img_name)
        img_h, img_w, img_c = img.shape
        doc = minidom.parse(xml_name)
        root = doc.documentElement
        size = root.getElementsByTagName('size')[0]
        width = size.getElementsByTagName('width')[0].childNodes[0].nodeValue
        height = size.getElementsByTagName('height')[0].childNodes[0].nodeValue

        cv2.namedWindow("image", 0)
        cv2.resizeWindow("image", int(500), int(500))

        objects = root.getElementsByTagName('object')
        for index, object in enumerate(objects):
            if len(object.getElementsByTagName('name')) == 0 or len(object.getElementsByTagName('bndbox')) == 0:
                continue
            bndbox = object.getElementsByTagName('bndbox')[0]
            xmin = bndbox.getElementsByTagName('xmin')[0].childNodes[0].nodeValue
            ymin = bndbox.getElementsByTagName('ymin')[0].childNodes[0].nodeValue
            xmax = bndbox.getElementsByTagName('xmax')[0].childNodes[0].nodeValue
            ymax = bndbox.getElementsByTagName('ymax')[0].childNodes[0].nodeValue

            # cv2.rectangle(img, (round(float(xmin)), round(float(ymin))), (round(float(xmax)), round(float(ymax))),
            #               (0, 255, 0), 2)

            try:
                x_top_left = round(float(bndbox.getElementsByTagName('x_top_left')[0].childNodes[0].nodeValue))
                y_top_left = round(float(bndbox.getElementsByTagName('y_top_left')[0].childNodes[0].nodeValue))
                x_top_right = round(float(bndbox.getElementsByTagName('x_top_right')[0].childNodes[0].nodeValue))
                y_top_right = round(float(bndbox.getElementsByTagName('y_top_right')[0].childNodes[0].nodeValue))
                x_bottom_right = round(float(bndbox.getElementsByTagName('x_bottom_right')[0].childNodes[0].nodeValue))
                y_bottom_right = round(float(bndbox.getElementsByTagName('y_bottom_right')[0].childNodes[0].nodeValue))
                x_bottom_left = round(float(bndbox.getElementsByTagName('x_bottom_left')[0].childNodes[0].nodeValue))
                y_bottom_left = round(float(bndbox.getElementsByTagName('y_bottom_left')[0].childNodes[0].nodeValue))
            except:
                continue

            cv2.line(img, (x_top_left, y_top_left), (x_top_right, y_top_right), (0, 0, 255), 2)
            cv2.line(img, (x_top_right, y_top_right), (x_bottom_right, y_bottom_right), (0, 255, 0), 2)
            cv2.line(img, (x_bottom_right, y_bottom_right), (x_bottom_left, y_bottom_left), (255, 0, 0), 2)
            cv2.line(img, (x_bottom_left, y_bottom_left), (x_top_left, y_top_left), (255, 255, 255), 2)

        cv2.imshow('image', img)
        cv2.waitKey(0)
