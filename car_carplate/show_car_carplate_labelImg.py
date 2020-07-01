# coding=utf-8
# 用于同时展示珠海标注中的车辆和车牌


import os
import cv2
import glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from xml.dom import minidom

import sys
sys.path.append(".")

img_root_dir = 'C:\\Users\\chens\\Desktop\\20171214\\720p\\JPEGImages\\'
xml_root_dir = 'C:\\Users\\chens\\Desktop\\20171214\\720p\\Annotations\\'
xmls = os.listdir(xml_root_dir)
num = len(glob.glob(xml_root_dir + "*.xml"))
print(num)

for i, xml_ in enumerate(xmls):
    if i % 1 != 0:
        continue
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
        cv2.resizeWindow("image", int(width), int(height))

        objects = root.getElementsByTagName('object')
        for index, obj in enumerate(objects):
            if len(obj.getElementsByTagName('name')) == 0 or len(obj.getElementsByTagName('bndbox')) == 0:
                continue
            bndbox = obj.getElementsByTagName('bndbox')[0]
            xmin = bndbox.getElementsByTagName('xmin')[0].childNodes[0].nodeValue
            ymin = bndbox.getElementsByTagName('ymin')[0].childNodes[0].nodeValue
            xmax = bndbox.getElementsByTagName('xmax')[0].childNodes[0].nodeValue
            ymax = bndbox.getElementsByTagName('ymax')[0].childNodes[0].nodeValue

            cv2.rectangle(img, (round(float(xmin)), round(float(ymin))), (round(float(xmax)), round(float(ymax))),
                          (0, 255, 0), 2)

            try:
                carplate = obj.getElementsByTagName('carplate')[0]
            except:
                continue
            else:
                x_top_left = round(float(carplate.getElementsByTagName('x_top_left')[0].childNodes[0].nodeValue))
                y_top_left = round(float(carplate.getElementsByTagName('y_top_left')[0].childNodes[0].nodeValue))
                x_top_right = round(float(carplate.getElementsByTagName('x_top_right')[0].childNodes[0].nodeValue))
                y_top_right = round(float(carplate.getElementsByTagName('y_top_right')[0].childNodes[0].nodeValue))
                x_bottom_right = round(float(carplate.getElementsByTagName('x_bottom_right')[0].childNodes[0].nodeValue))
                y_bottom_right = round(float(carplate.getElementsByTagName('y_bottom_right')[0].childNodes[0].nodeValue))
                x_bottom_left = round(float(carplate.getElementsByTagName('x_bottom_left')[0].childNodes[0].nodeValue))
                y_bottom_left = round(float(carplate.getElementsByTagName('y_bottom_left')[0].childNodes[0].nodeValue))
                try:
                    label = carplate.getElementsByTagName("label")[0].childNodes[0].nodeValue
                    color = carplate.getElementsByTagName("background_color")[0].childNodes[0].nodeValue
                    row = carplate.getElementsByTagName("row")[0].childNodes[0].nodeValue
                except:
                    label = ""
                    color = ""
                    row = ""

            cv2.line(img, (x_top_left, y_top_left), (x_top_right, y_top_right), (0, 0, 255), 2)
            cv2.line(img, (x_top_right, y_top_right), (x_bottom_right, y_bottom_right), (0, 255, 0), 2)
            cv2.line(img, (x_bottom_right, y_bottom_right), (x_bottom_left, y_bottom_left), (255, 0, 0), 2)
            cv2.line(img, (x_bottom_left, y_bottom_left), (x_top_left, y_top_left), (255, 255, 255), 2)

            pos =(round(float(xmin)) + 2, round(float(ymin)) + 2)
            text_size = 20

            img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            img_pil= Image.fromarray(img_rgb) # 转为PIL的图片格式
            draw = ImageDraw.Draw(img_pil)
            font = ImageFont.truetype("simsun.ttc",text_size,encoding="utf-8")
            text =label + "  " + color + "  " + row
            ImageDraw.Draw(img_pil).text(pos,text,(255,0,0),font)  # 第一个参数为打印的坐标、第二个为打印的文本、第三个为字体颜色、第四个为字体
            img = cv2.cvtColor(np.array(img_pil),cv2.COLOR_RGB2BGR)

        cv2.imshow('image', img)
        cv2.waitKey(0)
