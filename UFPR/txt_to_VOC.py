import os
from xml.dom.minidom import Document

import sys
sys.path.append(".")
import shared_function as ex

root_dir = '/dataset/UFPR-ALPR/testing'
xml_dir = '/data/UFPR/VOC/Annotations'
txt_path = '/data/UFPR/VOC/ImageSets/Main/test.txt'
test_single_path = '/data/UFPR/VOC/ImageSets/Main/test_single.txt'
test_double_path = '/data/UFPR/VOC/ImageSets/Main/test_double.txt'

for root, dirs, files in os.walk(root_dir):
    for f in files:
        file_path = os.path.join(root, f)
        if file_path.endswith("txt"):
            # dataset split
            fr = open(txt_path, 'a+')
            fr.write(os.path.basename(file_path).split('.')[0] + '\n')
            fr.close()
            # annotation
            fr = open(file_path, 'r')
            lines = fr.readlines()
            fr.close()

            car_type = lines[2].strip().split(':')[1].strip()
            plate_numer = lines[6].strip().split(':')[1].strip().replace('-', '')
            plate_position = lines[7].strip().split(':')[1].strip().split()
            plate_x = plate_position[0]
            plate_y = plate_position[1]
            plate_width = plate_position[2]
            plate_height = plate_position[3]
            if car_type == 'car':
                fr = open(test_single_path, 'a+')
                fr.write(os.path.basename(file_path).split('.')[0] + '\n')
                fr.close()
            elif car_type == 'motorcycle':
                fr = open(test_double_path, 'a+')
                fr.write(os.path.basename(file_path).split('.')[0] + '\n')
                fr.close()

            number = plate_numer

            img_name = f.split('.')[0] + '.png'
            width = 1920
            height = 1080
            channel = 3

            carplate_x_top_left = int(plate_x) + 1
            carplate_y_top_left = int(plate_y) + 1
            carplate_x_top_right = int(plate_x) + int(plate_width) + 1
            carplate_y_top_right = int(plate_y) + 1
            carplate_x_bottom_right = int(plate_x) + int(plate_width) + 1
            carplate_y_bottom_right = int(plate_y) + int(plate_height) + 1
            carplate_x_bottom_left = int(plate_x) + 1
            carplate_y_bottom_left = int(plate_y) + int(plate_height) + 1
            
            # if carplate_x_top_left < 1 or carplate_y_top_left < 1 or carplate_x_top_right < 1 or carplate_y_top_right < 1 \
            #     or carplate_x_bottom_right < 1 or carplate_y_bottom_right < 1 or carplate_x_bottom_left < 1 or carplate_y_bottom_left < 1:
            #     print('line: ', line)

            # 将车牌四点顺序改为标准的左上右上右下左下
            results = ex.exchange_four_points_to_std([carplate_x_top_left, carplate_y_top_left, carplate_x_top_right, carplate_y_top_right,
                                            carplate_x_bottom_right, carplate_y_bottom_right, carplate_x_bottom_left, carplate_y_bottom_left])
            carplate_x_top_left = results['x_top_left']
            carplate_y_top_left = results['y_top_left']
            carplate_x_top_right = results['x_top_right']
            carplate_y_top_right = results['y_top_right']
            carplate_x_bottom_right = results['x_bottom_right']
            carplate_y_bottom_right = results['y_bottom_right']
            carplate_x_bottom_left = results['x_bottom_left']
            carplate_y_bottom_left = results['y_bottom_left']
            # 限制不超过图片上下界
            carplate_x_top_left = ex.limit_in_bounds(carplate_x_top_left, 1, width)
            carplate_y_top_left = ex.limit_in_bounds(carplate_y_top_left, 1, height)
            carplate_x_top_right = ex.limit_in_bounds(carplate_x_top_right, 1, width)
            carplate_y_top_right = ex.limit_in_bounds(carplate_y_top_right, 1, height)
            carplate_x_bottom_right = ex.limit_in_bounds(carplate_x_bottom_right, 1, width)
            carplate_y_bottom_right = ex.limit_in_bounds(carplate_y_bottom_right, 1, height)
            carplate_x_bottom_left = ex.limit_in_bounds(carplate_x_bottom_left, 1, width)
            carplate_y_bottom_left = ex.limit_in_bounds(carplate_y_bottom_left, 1, height)
            # bbox
            carplate_xmin = min(carplate_x_top_left, carplate_x_bottom_left)
            carplate_ymin = min(carplate_y_top_left, carplate_y_top_right)
            carplate_xmax = max(carplate_x_bottom_right, carplate_x_top_right)
            carplate_ymax = max(carplate_y_bottom_right, carplate_y_bottom_left)

            # 创建dom文档
            doc = Document()
            # 创建根节点
            annotation = doc.createElement('annotation')
            # 根节点插入dom树
            doc.appendChild(annotation)
            # folder
            folder = doc.createElement('folder')
            annotation.appendChild(folder)
            folder.appendChild(doc.createTextNode('carplate'))
            # filename
            filename = doc.createElement('filename')
            annotation.appendChild(filename)
            filename.appendChild(doc.createTextNode(str(img_name)))
            # source
            source = doc.createElement('source')
            annotation.appendChild(source)
            database_ = doc.createElement('database')
            database_.appendChild(doc.createTextNode('carplate'))
            source.appendChild(database_)
            # 创建size节点
            size = doc.createElement('size')
            annotation.appendChild(size)
            width_ = doc.createElement('width')
            width_.appendChild(doc.createTextNode(str(width)))
            height_ = doc.createElement('height')
            height_.appendChild(doc.createTextNode(str(height)))
            depth_ = doc.createElement('depth')
            depth_.appendChild(doc.createTextNode(str(channel)))
            size.appendChild(width_)
            size.appendChild(height_)
            size.appendChild(depth_)
            # segmentation
            segmented = doc.createElement('segmented')
            annotation.appendChild(segmented)
            segmented.appendChild(doc.createTextNode(str(0)))

            # carplate
            object = doc.createElement('object')
            annotation.appendChild(object)
            name = doc.createElement('name')
            name.appendChild(doc.createTextNode("carplate"))
            object.appendChild(name)
            # pose
            pose_ = doc.createElement('pose')
            pose_.appendChild(doc.createTextNode('Unspecified'))
            object.appendChild(pose_)
            # occluded
            occluded_ = doc.createElement('occluded')
            occluded_.appendChild(doc.createTextNode(str(0)))
            object.appendChild(occluded_)
            # truncated
            truncated_ = doc.createElement('truncated')
            truncated_.appendChild(doc.createTextNode(str(0)))
            object.appendChild(truncated_)
            # difficult
            difficult_ = doc.createElement('difficult')
            difficult_.appendChild(doc.createTextNode(str(0)))
            object.appendChild(difficult_)
            # number
            number_ = doc.createElement('number')
            number_.appendChild(doc.createTextNode(str(number)))
            object.appendChild(number_)
            # the bndbox
            bndbox = doc.createElement('bndbox')
            object.appendChild(bndbox)
            xmin_ = doc.createElement('xmin')
            xmin_.appendChild(doc.createTextNode(str(carplate_xmin)))
            bndbox.appendChild(xmin_)
            ymin_ = doc.createElement('ymin')
            ymin_.appendChild(doc.createTextNode(str(carplate_ymin)))
            bndbox.appendChild(ymin_)
            xmax_ = doc.createElement('xmax')
            xmax_.appendChild(doc.createTextNode(str(carplate_xmax)))
            bndbox.appendChild(xmax_)
            ymax_ = doc.createElement('ymax')
            ymax_.appendChild(doc.createTextNode(str(carplate_ymax)))
            bndbox.appendChild(ymax_)

            x_top_left_ = doc.createElement('x_top_left')
            x_top_left_.appendChild(doc.createTextNode(str(carplate_x_top_left)))
            bndbox.appendChild(x_top_left_)
            y_top_left_ = doc.createElement('y_top_left')
            y_top_left_.appendChild(doc.createTextNode(str(carplate_y_top_left)))
            bndbox.appendChild(y_top_left_)
            x_top_right_ = doc.createElement('x_top_right')
            x_top_right_.appendChild(doc.createTextNode(str(carplate_x_top_right)))
            bndbox.appendChild(x_top_right_)
            y_top_right_ = doc.createElement('y_top_right')
            y_top_right_.appendChild(doc.createTextNode(str(carplate_y_top_right)))
            bndbox.appendChild(y_top_right_)
            x_bottom_right_ = doc.createElement('x_bottom_right')
            x_bottom_right_.appendChild(doc.createTextNode(str(carplate_x_bottom_right)))
            bndbox.appendChild(x_bottom_right_)
            y_bottom_right_ = doc.createElement('y_bottom_right')
            y_bottom_right_.appendChild(doc.createTextNode(str(carplate_y_bottom_right)))
            bndbox.appendChild(y_bottom_right_)
            x_bottom_left_ = doc.createElement('x_bottom_left')
            x_bottom_left_.appendChild(doc.createTextNode(str(carplate_x_bottom_left)))
            bndbox.appendChild(x_bottom_left_)
            y_bottom_left_ = doc.createElement('y_bottom_left')
            y_bottom_left_.appendChild(doc.createTextNode(str(carplate_y_bottom_left)))
            bndbox.appendChild(y_bottom_left_)

            # save xml
            fp = open(os.path.join(xml_dir, img_name[:-4] + ".xml"), 'w')
            doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
