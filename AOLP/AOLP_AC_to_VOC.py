# AOLP的txt格式转换为VOC格式
import os
from xml.dom.minidom import Document
import cv2
from car_carplate import exchange_to_std as ex

root_img = '/dataset/AOLP/Subset_AC/Subset_AC/Image'
root_anno = '/dataset/AOLP/Subset_AC/Subset_AC/groundtruth_localization'
target_anno = '/data/AOLP/AOLP_AC/Annotations'

def gen_car_and_carplate_independently(dic):
    img_name = dic['img_name']
    height = dic['height']
    width = dic['width']
    channel = dic['channel']
    xmin = dic['xmin']
    ymin = dic['ymin']
    xmax = dic['xmax']
    ymax = dic['ymax']

    # 创建dom文档
    doc = Document()
    # 创建根节点
    annotation = doc.createElement('annotation')
    # 根节点插入dom树
    doc.appendChild(annotation)
    # folder
    folder = doc.createElement('folder')
    annotation.appendChild(folder)
    folder.appendChild(doc.createTextNode('AOLP_AC'))
    # filename
    filename = doc.createElement('filename')
    annotation.appendChild(filename)
    filename.appendChild(doc.createTextNode(img_name))
    # source
    source = doc.createElement('source')
    annotation.appendChild(source)
    database_ = doc.createElement('database')
    database_.appendChild(doc.createTextNode('The AOLP Access Control'))
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

    # 如果标注出现错误,比如xmin大于xmax,直接跳过,并且不保存xml
    need_save = True
    for i in range(len(xmin)):
        if xmin[i] > xmax[i]:
            print(img_name)
            xmin[i], xmax[i] = xmax[i], xmin[i]
        #     need_save = False
        #     continue
        if ymin[i] > ymax[i]:
            print(img_name)
            ymin[i], ymax[i] = ymax[i], ymin[i]
        #     need_save = False
        #     continue

        # 限制不超过图片上下界
        carplate_xmin = ex.limit_in_bounds(xmin[i], 1, width)
        carplate_ymin = ex.limit_in_bounds(ymin[i], 1, height)
        carplate_xmax = ex.limit_in_bounds(xmax[i], 1, width)
        carplate_ymax = ex.limit_in_bounds(ymax[i], 1, height)

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

    if need_save:
        fp = open(os.path.join(target_anno, str(dic['img_index']) + '.xml'), 'w')
        doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")


dic = {}
file_list = os.listdir(root_anno)
for fileitem in file_list:
    if fileitem.endswith('txt') and '_' not in fileitem:  # 确保不是第二个车牌
        img_index = int(fileitem.split('.')[0])
        dic['img_index'] = str(img_index)
        # print(fileitem)
        xmin = []
        ymin = []
        xmax = []
        ymax = []
        # 从txt中读取车的bounding box
        fi = open(os.path.join(root_anno, fileitem))
        lines = fi.readlines()
        fi.close()
        xmin.append(int(float(lines[0].strip())))
        ymin.append(int(float(lines[1].strip())))
        xmax.append(int(float(lines[2].strip())))
        ymax.append(int(float(lines[3].strip())))
        # 读取图片大小
        img = cv2.imread(os.path.join(root_img, str(img_index) + '.jpg'))
        h, w, c = img.shape
        dic['img_name'] = dic['img_index'] + '.jpg'
        dic['height'] = h
        dic['width'] = w
        dic['channel'] = c
        dic['xmin'] = xmin
        dic['ymin'] = ymin
        dic['xmax'] = xmax
        dic['ymax'] = ymax

        gen_car_and_carplate_independently(dic)

