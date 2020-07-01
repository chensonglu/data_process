# 从Cars的mat文件中读取车的bounding box
# 从车牌标注的论文中取出车牌的相应标注
# 共105张
from scipy.io import loadmat
import os
from xml.dom.minidom import Document
import cv2
import exchange_to_std as ex

cars_train_annos = loadmat('/dataset/Cars/devkit/cars_train_annos.mat')
carplate_train_annos_dir = '/dataset/Cars/training-dataset-annotations/cars-dataset'
root_dir = '/dataset/Cars/cars_train'
# 需要根据是否需要车或车牌改变路径
target_dir = '/data/TILT/cars-dataset/car_carplate_two_stage_end2end/Annotations'

def gen_car_and_carplate_two_stage_end2end(dic):
    img_name = dic['img_name']
    height = dic['height']
    width = dic['width']
    channel = dic['channel']
    xmin = dic['xmin']
    ymin = dic['ymin']
    xmax = dic['xmax']
    ymax = dic['ymax']
    carplate_x_top_left = dic['carplate_x_top_left']
    carplate_x_top_right = dic['carplate_x_top_right']
    carplate_x_bottom_right = dic['carplate_x_bottom_right']
    carplate_x_bottom_left = dic['carplate_x_bottom_left']
    carplate_y_top_left = dic['carplate_y_top_left']
    carplate_y_top_right = dic['carplate_y_top_right']
    carplate_y_bottom_right = dic['carplate_y_bottom_right']
    carplate_y_bottom_left = dic['carplate_y_bottom_left']

    # 创建dom文档
    doc = Document()
    # 创建根节点
    annotation = doc.createElement('annotation')
    # 根节点插入dom树
    doc.appendChild(annotation)
    # folder
    folder = doc.createElement('folder')
    annotation.appendChild(folder)
    folder.appendChild(doc.createTextNode('Cars_two_stage_end2end'))
    # filename
    filename = doc.createElement('filename')
    annotation.appendChild(filename)
    filename.appendChild(doc.createTextNode(img_name))
    # source
    source = doc.createElement('source')
    annotation.appendChild(source)
    database_ = doc.createElement('database')
    database_.appendChild(doc.createTextNode('Cars_two_stage_end2end'))
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

    # car
    object = doc.createElement('object')
    annotation.appendChild(object)
    name = doc.createElement('name')
    name.appendChild(doc.createTextNode('car'))
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
    # have carplate
    has_carplate_ = doc.createElement('has_carplate')
    has_carplate_.appendChild(doc.createTextNode(str(1)))
    object.appendChild(has_carplate_)
    # occluded
    occluded_ = doc.createElement('carplate_occluded')
    occluded_.appendChild(doc.createTextNode(str(0)))
    object.appendChild(occluded_)
    # difficult
    difficult_ = doc.createElement('carplate_difficult')
    difficult_.appendChild(doc.createTextNode(str(0)))
    object.appendChild(difficult_)
    # unrecognable
    unrecognable_ = doc.createElement('carplate_unrecognable')
    unrecognable_.appendChild(doc.createTextNode(str(0)))
    object.appendChild(unrecognable_)

    # 限制不超过图片上下界
    car_xmin = ex.limit_in_bounds(xmin, 1, width)
    car_ymin = ex.limit_in_bounds(ymin, 1, height)
    car_xmax = ex.limit_in_bounds(xmax, 1, width)
    car_ymax = ex.limit_in_bounds(ymax, 1, height)

    car_x_center = (car_xmin + car_xmax) / 2
    car_y_center = (car_ymin + car_ymax) / 2

    # the bndbox
    bndbox = doc.createElement('bndbox')
    object.appendChild(bndbox)
    xmin_ = doc.createElement('xmin')
    xmin_.appendChild(doc.createTextNode(str(car_xmin)))
    bndbox.appendChild(xmin_)
    ymin_ = doc.createElement('ymin')
    ymin_.appendChild(doc.createTextNode(str(car_ymin)))
    bndbox.appendChild(ymin_)
    xmax_ = doc.createElement('xmax')
    xmax_.appendChild(doc.createTextNode(str(car_xmax)))
    bndbox.appendChild(xmax_)
    ymax_ = doc.createElement('ymax')
    ymax_.appendChild(doc.createTextNode(str(car_ymax)))
    bndbox.appendChild(ymax_)

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

    carplate_xmin = min(carplate_x_top_left, carplate_x_bottom_left)
    carplate_ymin = min(carplate_y_top_left, carplate_y_top_right)
    carplate_xmax = max(carplate_x_bottom_right, carplate_x_top_right)
    carplate_ymax = max(carplate_y_bottom_right, carplate_y_bottom_left)

    carplate_x_center = (carplate_xmin + carplate_xmax) / 2
    carplate_y_center = (carplate_ymin + carplate_ymax) / 2

    # carplate size and offset
    width_ = doc.createElement('width')
    width_.appendChild(doc.createTextNode(str(carplate_xmax - carplate_xmin + 1)))
    bndbox.appendChild(width_)
    height_ = doc.createElement('height')
    height_.appendChild(doc.createTextNode(str(carplate_ymax - carplate_ymin + 1)))
    bndbox.appendChild(height_)
    x_offset_ = doc.createElement('x_offset')
    x_offset_.appendChild(doc.createTextNode(str(carplate_x_center - car_x_center)))
    bndbox.appendChild(x_offset_)
    y_offset_ = doc.createElement('y_offset')
    y_offset_.appendChild(doc.createTextNode(str(carplate_y_center - car_y_center)))
    bndbox.appendChild(y_offset_)

    # carplate bbox
    carplate_xmin_ = doc.createElement('carplate_xmin')
    carplate_xmin_.appendChild(doc.createTextNode(str(carplate_xmin)))
    bndbox.appendChild(carplate_xmin_)
    carplate_ymin_ = doc.createElement('carplate_ymin')
    carplate_ymin_.appendChild(doc.createTextNode(str(carplate_ymin)))
    bndbox.appendChild(carplate_ymin_)
    carplate_xmax_ = doc.createElement('carplate_xmax')
    carplate_xmax_.appendChild(doc.createTextNode(str(carplate_xmax)))
    bndbox.appendChild(carplate_xmax_)
    carplate_ymax_ = doc.createElement('carplate_ymax')
    carplate_ymax_.appendChild(doc.createTextNode(str(carplate_ymax)))
    bndbox.appendChild(carplate_ymax_)

    # carplate four points
    carplate_x_top_left_ = doc.createElement('carplate_x_top_left')
    carplate_x_top_left_.appendChild(doc.createTextNode(str(carplate_x_top_left)))
    bndbox.appendChild(carplate_x_top_left_)
    carplate_y_top_left_ = doc.createElement('carplate_y_top_left')
    carplate_y_top_left_.appendChild(doc.createTextNode(str(carplate_y_top_left)))
    bndbox.appendChild(carplate_y_top_left_)
    carplate_x_top_right_ = doc.createElement('carplate_x_top_right')
    carplate_x_top_right_.appendChild(doc.createTextNode(str(carplate_x_top_right)))
    bndbox.appendChild(carplate_x_top_right_)
    carplate_y_top_right_ = doc.createElement('carplate_y_top_right')
    carplate_y_top_right_.appendChild(doc.createTextNode(str(carplate_y_top_right)))
    bndbox.appendChild(carplate_y_top_right_)
    carplate_x_bottom_right_ = doc.createElement('carplate_x_bottom_right')
    carplate_x_bottom_right_.appendChild(doc.createTextNode(str(carplate_x_bottom_right)))
    bndbox.appendChild(carplate_x_bottom_right_)
    carplate_y_bottom_right_ = doc.createElement('carplate_y_bottom_right')
    carplate_y_bottom_right_.appendChild(doc.createTextNode(str(carplate_y_bottom_right)))
    bndbox.appendChild(carplate_y_bottom_right_)
    carplate_x_bottom_left_ = doc.createElement('carplate_x_bottom_left')
    carplate_x_bottom_left_.appendChild(doc.createTextNode(str(carplate_x_bottom_left)))
    bndbox.appendChild(carplate_x_bottom_left_)
    carplate_y_bottom_left_ = doc.createElement('carplate_y_bottom_left')
    carplate_y_bottom_left_.appendChild(doc.createTextNode(str(carplate_y_bottom_left)))
    bndbox.appendChild(carplate_y_bottom_left_)

    fp = open(os.path.join(target_dir, str(dic['img_index']).zfill(5) + '.xml'), 'w')
    doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")


dic = {}
file_list = os.listdir(carplate_train_annos_dir)
for fileitem in file_list:
    if fileitem.endswith('txt'):
        img_index = int(fileitem.split('.')[0])
        dic['img_index'] = str(img_index)
        print(fileitem)
        # 从mat中读取车的bounding box
        xmin = cars_train_annos['annotations'][0][img_index - 1][0]
        ymin = cars_train_annos['annotations'][0][img_index - 1][1]
        xmax = cars_train_annos['annotations'][0][img_index - 1][2]
        ymax = cars_train_annos['annotations'][0][img_index - 1][3]
        # 读取图片大小
        img = cv2.imread(os.path.join(root_dir, str(img_index).zfill(5) + '.jpg'))
        h, w, c = img.shape
        dic['img_name'] = str(img_index).zfill(5) + '.jpg'
        dic['height'] = h
        dic['width'] = w
        dic['channel'] = c
        dic['xmin'] = int(xmin)
        dic['ymin'] = int(ymin)
        dic['xmax'] = int(xmax)
        dic['ymax'] = int(ymax)
        # 从论文中车牌标注中读取车牌四点坐标
        fo = open(os.path.join(carplate_train_annos_dir, str(img_index).zfill(5) + '.txt'))
        lines = fo.readlines()
        fo.close()
        line = lines[0].strip().split(',')
        carplate_x_top_left = float(line[1]) * w
        carplate_x_top_right = float(line[2]) * w
        carplate_x_bottom_right = float(line[3]) * w
        carplate_x_bottom_left = float(line[4]) * w
        carplate_y_top_left = float(line[5]) * h
        carplate_y_top_right = float(line[6]) * h
        carplate_y_bottom_right = float(line[7]) * h
        carplate_y_bottom_left = float(line[8]) * h
        dic['carplate_x_top_left'] = round(carplate_x_top_left)
        dic['carplate_x_top_right'] = round(carplate_x_top_right)
        dic['carplate_x_bottom_right'] = round(carplate_x_bottom_right)
        dic['carplate_x_bottom_left'] = round(carplate_x_bottom_left)
        dic['carplate_y_top_left'] = round(carplate_y_top_left)
        dic['carplate_y_top_right'] = round(carplate_y_top_right)
        dic['carplate_y_bottom_right'] = round(carplate_y_bottom_right)
        dic['carplate_y_bottom_left'] = round(carplate_y_bottom_left)

        gen_car_and_carplate_two_stage_end2end(dic)
