import os
from xml.dom.minidom import Document

import sys
sys.path.append(".")
import shared_function as ex

training_image_dir = '/dataset/ICDAR2015/ch4_training_images'
training_txt_dir = '/dataset/ICDAR2015/ch4_training_localization_transcription_gt'
testing_image_dir = '/dataset/ICDAR2015/ch4_test_images'
testing_txt_dir = '/dataset/ICDAR2015/Challenge4_Test_Task1_GT'

trainval_txt = '/data/ICDAR2015/training/ImageSets/Main/trainval.txt'
testing_txt = '/data/ICDAR2015/testing/ImageSets/Main/test.txt'

trainval_xml = '/data/ICDAR2015/training/Annotations'
testing_xml = '/data/ICDAR2015/testing/Annotations'

images = os.listdir(training_image_dir)
for image in images:
    fr = open(trainval_txt, 'a+')
    fr.write(image.split('.')[0] + '\n')
    fr.close()

    fr = open(os.path.join(training_txt_dir, 'gt_'+image.split('.')[0]+'.txt'), encoding='utf-8-sig')
    lines = fr.readlines()
    fr.close()

    img_name = image
    width = 1280
    height = 720
    channel = 3

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

    for line in lines:
        carplate_x_top_left = int(line.strip().split(',')[0])
        carplate_y_top_left = int(line.strip().split(',')[1])
        carplate_x_top_right = int(line.strip().split(',')[2])
        carplate_y_top_right = int(line.strip().split(',')[3])
        carplate_x_bottom_right = int(line.strip().split(',')[4])
        carplate_y_bottom_right = int(line.strip().split(',')[5])
        carplate_x_bottom_left = int(line.strip().split(',')[6])
        carplate_y_bottom_left = int(line.strip().split(',')[7])
        
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
    fp = open(os.path.join(trainval_xml, image.split('.')[0] + ".xml"), 'w')
    doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
