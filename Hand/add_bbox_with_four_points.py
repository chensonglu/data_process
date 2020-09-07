# add four points to xml with only bbox


from pathlib import Path
import os
import shutil
import xml.dom.minidom
from xml.dom.minidom import Document
import sys
sys.path.append(".")
import shared_function as ex
import cv2


ZHhands_path = '/dataset/ZHhands/training_set/2020-08-12'
output_dir = '/dataset/ZHhands/training_set/2020-08-12-new'


ZHhands_sub_paths = os.listdir(ZHhands_path)
for sub_path in ZHhands_sub_paths:
    p = Path(ZHhands_path).joinpath(sub_path)
    p_new = Path(output_dir).joinpath(sub_path)
    if not os.path.exists(str(p_new)):
        os.mkdir(str(p_new))
    # sort xmls as .m file stores points in alphabetical order
    xmls_per_scene = list(p.glob('*.xml'))
    xmls_per_scene.sort()
    for i, xml_path in enumerate(xmls_per_scene):
        img_path = str(xml_path).split('.')[0] + '.jpg'
        # 如果对应xml的jpg存在才拷贝
        if os.path.exists(str(img_path)):
            # shutil.copy(str(xml_path), str(output_xml_path))
            # shutil.copy(str(img_path), str(output_img_path))
            print(str(xml_path))
            dom = xml.dom.minidom.parse(str(xml_path))
            root = dom.documentElement
            # size
            size = root.getElementsByTagName('size')[0]
            width = int(size.getElementsByTagName('width')[0].childNodes[0].nodeValue)
            height = int(size.getElementsByTagName('height')[0].childNodes[0].nodeValue)
            depth = int(size.getElementsByTagName('depth')[0].childNodes[0].nodeValue)
            # if xml dont have any object, continue
            objects = root.getElementsByTagName('object')
            if len(objects) == 0:
                continue

            # 创建dom文档
            doc = Document()
            # 创建根节点
            annotation = doc.createElement('annotation')
            # 根节点插入dom树
            doc.appendChild(annotation)
            # 创建size节点
            size = doc.createElement('size')
            annotation.appendChild(size)
            width_ = doc.createElement('width')
            width_.appendChild(doc.createTextNode(str(height)))
            height_ = doc.createElement('height')
            height_.appendChild(doc.createTextNode(str(width)))
            depth_ = doc.createElement('depth')
            depth_.appendChild(doc.createTextNode(str(depth)))
            size.appendChild(width_)
            size.appendChild(height_)
            size.appendChild(depth_)
            for index, obj in enumerate(objects):
                bndbox = obj.getElementsByTagName('bndbox')[0]
                name = int(obj.getElementsByTagName('name')[0].childNodes[0].nodeValue)
                x_min = int(obj.getElementsByTagName('xmin')[0].childNodes[0].nodeValue)
                y_min = int(obj.getElementsByTagName('ymin')[0].childNodes[0].nodeValue)
                x_max = int(obj.getElementsByTagName('xmax')[0].childNodes[0].nodeValue)
                y_max = int(obj.getElementsByTagName('ymax')[0].childNodes[0].nodeValue)

                x_top_left = x_min
                y_top_left = y_min
                x_top_right = x_max
                y_top_right = y_min
                x_bottom_right = x_max
                y_bottom_right = y_max
                x_bottom_left = x_min
                y_bottom_left = y_max
                
                # 将车牌四点顺序改为标准的左上右上右下左下
                results = ex.exchange_four_points_to_std([x_top_left, y_top_left, x_top_right, y_top_right,
                                                x_bottom_right, y_bottom_right, x_bottom_left, y_bottom_left])
                x_top_left = results['x_top_left']
                y_top_left = results['y_top_left']
                x_top_right = results['x_top_right']
                y_top_right = results['y_top_right']
                x_bottom_right = results['x_bottom_right']
                y_bottom_right = results['y_bottom_right']
                x_bottom_left = results['x_bottom_left']
                y_bottom_left = results['y_bottom_left']

                # hand
                object = doc.createElement('object')
                annotation.appendChild(object)
                name_ = doc.createElement('name')
                name_.appendChild(doc.createTextNode(str(name)))
                object.appendChild(name_)
                # misc
                misc_ = doc.createElement('misc')
                misc_.appendChild(doc.createTextNode(str(0)))
                object.appendChild(misc_)
                # occluded
                occluded_ = doc.createElement('occlusion')
                occluded_.appendChild(doc.createTextNode(str(0)))
                object.appendChild(occluded_)
                # truncated
                truncated_ = doc.createElement('truncated')
                truncated_.appendChild(doc.createTextNode(str(0)))
                object.appendChild(truncated_)
                # the bndbox
                bndbox_ = doc.createElement('bndbox')
                object.appendChild(bndbox_)
                xmin_ = doc.createElement('xmin')
                xmin_.appendChild(doc.createTextNode(str(x_min)))
                bndbox_.appendChild(xmin_)
                ymin_ = doc.createElement('ymin')
                ymin_.appendChild(doc.createTextNode(str(y_min)))
                bndbox_.appendChild(ymin_)
                xmax_ = doc.createElement('xmax')
                xmax_.appendChild(doc.createTextNode(str(x_max)))
                bndbox_.appendChild(xmax_)
                ymax_ = doc.createElement('ymax')
                ymax_.appendChild(doc.createTextNode(str(y_max)))
                bndbox_.appendChild(ymax_)
                x_top_left_ = doc.createElement('x_top_left')
                x_top_left_.appendChild(doc.createTextNode(str(x_top_left)))
                bndbox_.appendChild(x_top_left_)
                y_top_left_ = doc.createElement('y_top_left')
                y_top_left_.appendChild(doc.createTextNode(str(y_top_left)))
                bndbox_.appendChild(y_top_left_)
                x_top_right_ = doc.createElement('x_top_right')
                x_top_right_.appendChild(doc.createTextNode(str(x_top_right)))
                bndbox_.appendChild(x_top_right_)
                y_top_right_ = doc.createElement('y_top_right')
                y_top_right_.appendChild(doc.createTextNode(str(y_top_right)))
                bndbox_.appendChild(y_top_right_)
                x_bottom_right_ = doc.createElement('x_bottom_right')
                x_bottom_right_.appendChild(doc.createTextNode(str(x_bottom_right)))
                bndbox_.appendChild(x_bottom_right_)
                y_bottom_right_ = doc.createElement('y_bottom_right')
                y_bottom_right_.appendChild(doc.createTextNode(str(y_bottom_right)))
                bndbox_.appendChild(y_bottom_right_)
                x_bottom_left_ = doc.createElement('x_bottom_left')
                x_bottom_left_.appendChild(doc.createTextNode(str(x_bottom_left)))
                bndbox_.appendChild(x_bottom_left_)
                y_bottom_left_ = doc.createElement('y_bottom_left')
                y_bottom_left_.appendChild(doc.createTextNode(str(y_bottom_left)))
                bndbox_.appendChild(y_bottom_left_)

            unique_filename = xml_path.stem
            output_xml_path = Path(output_dir).joinpath(Path(sub_path + '/' + unique_filename + '.xml'))
            img_path = str(xml_path).split('.')[0] + '.jpg'
            img = cv2.imread(img_path)
            output_img_path = str(output_xml_path).split('.')[0] + '.jpg'

            fp = open(str(output_xml_path), 'w')
            doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
            cv2.imwrite(output_img_path, img)
