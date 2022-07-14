import cv2
import numpy as np
import os
import xml.dom.minidom
from xml.dom.minidom import Document
from matplotlib import pyplot as plt

root_xml_dir = '/data/CCPD/test/ccpd_rotate/Annotations/'
root_img_dir = '/data/CCPD/test/ccpd_rotate/JPEGImages/'

fs = os.listdir(root_xml_dir)
for f in fs:
    xml_path = os.path.join(root_xml_dir, f)
    img_path = os.path.join(root_img_dir, f.split('.')[0]+'.jpg')
    image = cv2.imread(img_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_h, img_w, _ = image.shape

    dom = xml.dom.minidom.parse(xml_path)
    root = dom.documentElement

    # iteration
    objects = root.getElementsByTagName('object')
    for index, obj in enumerate(objects):
        if index > 0:
            continue
        bndbox = obj.getElementsByTagName('bndbox')[0]

        x_top_left = round(float(bndbox.getElementsByTagName('x_top_left')[0].childNodes[0].nodeValue))
        y_top_left = round(float(bndbox.getElementsByTagName('y_top_left')[0].childNodes[0].nodeValue))
        x_top_right = round(float(bndbox.getElementsByTagName('x_top_right')[0].childNodes[0].nodeValue))
        y_top_right = round(float(bndbox.getElementsByTagName('y_top_right')[0].childNodes[0].nodeValue))
        x_bottom_right = round(float(bndbox.getElementsByTagName('x_bottom_right')[0].childNodes[0].nodeValue))
        y_bottom_right = round(float(bndbox.getElementsByTagName('y_bottom_right')[0].childNodes[0].nodeValue))
        x_bottom_left = round(float(bndbox.getElementsByTagName('x_bottom_left')[0].childNodes[0].nodeValue))
        y_bottom_left = round(float(bndbox.getElementsByTagName('y_bottom_left')[0].childNodes[0].nodeValue))

        xmin = min(x_top_left, x_bottom_left)
        ymin = min(y_top_left, y_top_right)
        xmax = max(x_bottom_right, x_top_right)
        ymax = max(y_bottom_right, y_bottom_left)

        xcenter = (xmin + xmax)/2
        ycenter = (ymin + ymax)/2
        w = np.linalg.norm(np.array([x_top_left - x_top_right, y_top_left - y_top_right]))
        h = np.linalg.norm(np.array([x_top_left - x_bottom_left, y_top_left - y_bottom_left]))
        # expand
        xmin_new = xcenter - 0.6*w
        ymin_new = ycenter - 0.6*h
        xmax_new = xcenter + 0.6*w
        ymax_new = ycenter + 0.6*h
        psts2 = np.float32([[xcenter - w/2, ycenter - h/2],
                            [xcenter + w/2, ycenter - h/2],
                            [xcenter - w/2, ycenter + h/2]
                                       ])

        psts1 = np.float32([[x_top_left, y_top_left],
                            [x_top_right, y_top_right],
                            [x_bottom_left, y_bottom_left]
                                       ])
        
        M = cv2.getAffineTransform(psts1, psts2)
        dst = cv2.warpAffine(image, M, (img_w, img_h))
        # img_crop = dst[int(ymin):int(ymax)+1, int(xmin):int(xmax)+1]

        plt.figure(figsize=(10, 10))
        ax1 = plt.subplot(121)
        plt.imshow(image[int(ymin):int(ymax)+1, int(xmin):int(xmax)+1])
        ax2 = plt.subplot(122)
        plt.imshow(dst[int(ymin_new):int(ymax_new)+1, int(xmin_new):int(xmax_new)+1])

        plt.show()