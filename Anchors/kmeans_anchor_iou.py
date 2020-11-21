from math import sqrt
from itertools import product as product
import glob
import xml.etree.ElementTree as ET
import numpy as np
from kmeans import kmeans, avg_iou, spt_iou

cfg = {
    'min_dim': 300,
    'feature_maps': [38, 19, 10, 5, 3, 1],
    'steps': [8, 16, 32, 64, 100, 300],
    'clip': True,
}


def change_cfg_for_ssd512(cfg):
    cfg['min_dim'] = 512
    cfg['feature_maps'] = [64, 32, 16, 8, 4, 2, 1]
    cfg['steps'] = [8, 16, 32, 64, 128, 256, 512]
    return cfg


# Convert (cx, cy, w, h) to (xmin, ymin, xmax, ymax)
def point_form(boxes):
    min = boxes[:, :2] - boxes[:, 2:4]/2
    max = boxes[:, :2] + boxes[:, 2:4]/2
    return np.concatenate((min, max), axis=1)


def load_dataset(path):
    dataset = []
    dataset_loc = []
    for xml_file in glob.glob("{}/*xml".format(path)):
        tree = ET.parse(xml_file)
        
        height = int(tree.findtext("./size/height"))
        width = int(tree.findtext("./size/width"))
        
        for obj in tree.iter("object"):
            xmin = int(obj.findtext("bndbox/xmin")) / width
            ymin = int(obj.findtext("bndbox/ymin")) / height
            xmax = int(obj.findtext("bndbox/xmax")) / width
            ymax = int(obj.findtext("bndbox/ymax")) / height
            
            dataset.append([xmax - xmin, ymax - ymin])
            dataset_loc.append([xmin, ymin, xmax, ymax])

    return np.array(dataset), np.array(dataset_loc)


# -------------------------------------------like YOLOV3----------------------------------------
print("like YOLOV3")
ANNOTATIONS_PATH = "/data/CCPD/VOC/Annotations_train"
data, data_loc = load_dataset(ANNOTATIONS_PATH)
VAL_ANNOTATIONS_PATH = "/data/CCPD/VOC/Annotations_val"
val_data, val_data_loc = load_dataset(VAL_ANNOTATIONS_PATH)
CLUSTERS = 30
anchor_num_dic = dict(zip(range(6), [4,6,6,6,4,4]))

for s in [300, 512]:
    print("Size: {}".format(str(s)))
    if s == 512:
        cfg = change_cfg_for_ssd512(cfg)
        CLUSTERS = 36
        anchor_num_dic = dict(zip(range(7), [4,6,6,6,6,4,4]))
    
    out = kmeans(data, k=CLUSTERS)
    areas = np.around(out[:, 0] * out[:, 1], decimals=6).tolist()
    area_order = np.argsort(areas)

    anchors = out[area_order]
    print(anchors.shape)
    print("Average IoU before clip: {:.2f}%".format(avg_iou(val_data, anchors) * 100))
    if cfg['clip']:
        anchors = np.clip(anchors, 0, 1)
    print("Average IoU after clip: {:.2f}%".format(avg_iou(val_data, anchors) * 100))

    anchors_loc = []
    for k, f in enumerate(cfg['feature_maps']):
        for i, j in product(range(f), repeat=2):
            f_k = cfg['min_dim'] / cfg['steps'][k]
            # unit center x,y
            cx = (j + 0.5) / f_k
            cy = (i + 0.5) / f_k

            sumcum = 0
            for m in range(k):
                sumcum += anchor_num_dic[m]
            for n in range(sumcum, sumcum+anchor_num_dic[k]):
                anchors_loc.append([cx, cy, anchors[n, 0], anchors[n, 1]])

    anchors_loc = np.array(anchors_loc)
    anchors_loc = point_form(anchors_loc)
    print(anchors_loc.shape)
    print("Spatial IoU before clip: {:.2f}%".format(spt_iou(val_data_loc, anchors_loc) * 100))
    if cfg['clip']:
        anchors_loc = np.clip(anchors_loc, 0, 1)
    print("Spatial IoU after clip: {:.2f}%".format(spt_iou(val_data_loc, anchors_loc) * 100))

print('-----------------------------------------------------')
# -------------------------------------------same anchors----------------------------------------
print("same anchors")
cfg = {
    'min_dim': 300,
    'feature_maps': [38, 19, 10, 5, 3, 1],
    'steps': [8, 16, 32, 64, 100, 300],
    'clip': True,
}

ANNOTATIONS_PATH = "/data/CCPD/VOC/Annotations_train"
data, data_loc = load_dataset(ANNOTATIONS_PATH)
VAL_ANNOTATIONS_PATH = "/data/CCPD/VOC/Annotations_val"
val_data, val_data_loc = load_dataset(VAL_ANNOTATIONS_PATH)
CLUSTERS_4 = 4
CLUSTERS_6 = 6
anchor_num_dic = dict(zip(range(6), [4,6,6,6,4,4]))

for s in [300, 512]:
    print("Size: {}".format(str(s)))
    if s == 512:
        cfg = change_cfg_for_ssd512(cfg)
        anchor_num_dic = dict(zip(range(7), [4,6,6,6,6,4,4]))
    
    out_4 = kmeans(data, k=CLUSTERS_4)
    areas_4 = np.around(out_4[:, 0] * out_4[:, 1], decimals=6).tolist()
    area_order_4 = np.argsort(areas_4)
    anchors_4 = out_4[area_order_4]

    out_6 = kmeans(data, k=CLUSTERS_6)
    areas_6 = np.around(out_6[:, 0] * out_6[:, 1], decimals=6).tolist()
    area_order_6 = np.argsort(areas_6)
    anchors_6 = out_6[area_order_6]

    anchors = np.concatenate((anchors_4, anchors_6), axis=0)
    print("Average IoU before clip: {:.2f}%".format(avg_iou(val_data, anchors) * 100))
    if cfg['clip']:
        anchors = np.clip(anchors, 0, 1)
    print("Average IoU after clip: {:.2f}%".format(avg_iou(val_data, anchors) * 100))

    anchors_loc = []
    for k, f in enumerate(cfg['feature_maps']):
        for i, j in product(range(f), repeat=2):
            f_k = cfg['min_dim'] / cfg['steps'][k]
            # unit center x,y
            cx = (j + 0.5) / f_k
            cy = (i + 0.5) / f_k

            if anchor_num_dic[k] == 4:
                for m in range(anchor_num_dic[k]):
                    anchors_loc.append([cx, cy, anchors_4[m, 0], anchors_4[m, 1]])
            elif anchor_num_dic[k] == 6:
                for m in range(anchor_num_dic[k]):
                    anchors_loc.append([cx, cy, anchors_6[m, 0], anchors_6[m, 1]])

    anchors_loc = np.array(anchors_loc)
    anchors_loc = point_form(anchors_loc)
    print(anchors_loc.shape)
    print("Spatial IoU before clip: {:.2f}%".format(spt_iou(val_data_loc, anchors_loc) * 100))
    if cfg['clip']:
        anchors_loc = np.clip(anchors_loc, 0, 1)
    print("Spatial IoU after clip: {:.2f}%".format(spt_iou(val_data_loc, anchors_loc) * 100))
