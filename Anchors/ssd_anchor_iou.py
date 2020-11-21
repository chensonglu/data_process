from math import sqrt
from itertools import product as product
import numpy as np
import glob
import xml.etree.ElementTree as ET
from kmeans import avg_iou, spt_iou

cfg = {
    'min_dim': 300,
    'feature_maps': [38, 19, 10, 5, 3, 1],
    'min_sizes': [30.0, 60.0, 111.0, 162.0, 213.0, 264.0],
    'max_sizes': [60.0, 111.0, 162.0, 213.0, 264.0, 315.0],
    'aspect_ratios': [[2], [2, 3], [2, 3], [2, 3], [2], [2]],
    'clip': True,
}


def change_cfg_for_ssd512(cfg):
    cfg['min_dim'] = 512
    cfg['feature_maps'] = [64, 32, 16, 8, 4, 2, 1]
    cfg['min_sizes'] = [35.84, 76.8, 153.6, 230.4, 307.2, 384.0, 460.8]
    cfg['max_sizes'] = [76.8, 153.6, 230.4, 307.2, 384.0, 460.8, 537.6]
    cfg['aspect_ratios']= [[2], [2, 3], [2, 3], [2, 3], [2, 3], [2], [2]]
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

ANNOTATIONS_PATH = "/data/TILT/720p/carplate_only/Annotations"
data, data_loc = load_dataset(ANNOTATIONS_PATH)

for s in [300, 512]:
    print("Size: {}".format(str(s)))
    if s == 512:
        cfg = change_cfg_for_ssd512(cfg)
    anchors = []
    for k, _ in enumerate(cfg['feature_maps']):
        # aspect_ratio: 1
        # rel size: min_size
        s_k = cfg['min_sizes'][k]/cfg['min_dim']
        anchors.append([s_k, s_k])

        # aspect_ratio: 1
        # rel size: sqrt(s_k * s_(k+1))
        s_k_prime = sqrt(s_k * (cfg['max_sizes'][k]/cfg['min_dim']))
        anchors.append([s_k_prime, s_k_prime])

        # rest of aspect ratios
        for ar in cfg['aspect_ratios'][k]:
            anchors.append([s_k*sqrt(ar), s_k/sqrt(ar)])
            anchors.append([s_k/sqrt(ar), s_k*sqrt(ar)])

    anchors = np.array(anchors)
    print(anchors.shape)
    print("Average IoU before clip: {:.2f}%".format(avg_iou(data, anchors) * 100))
    if cfg['clip']:
        anchors = np.clip(anchors, 0, 1)
    print("Average IoU after clip: {:.2f}%".format(avg_iou(data, anchors) * 100))

    anchors_loc = []
    for k, f in enumerate(cfg['feature_maps']):
        for i, j in product(range(f), repeat=2):
            f_k = cfg['feature_maps'][k]
            # unit center x,y
            cx = (j + 0.5) / f_k
            cy = (i + 0.5) / f_k

            # aspect_ratio: 1
            # rel size: min_size
            s_k = cfg['min_sizes'][k]/cfg['min_dim']
            anchors_loc.append([cx, cy, s_k, s_k])

            # aspect_ratio: 1
            # rel size: sqrt(s_k * s_(k+1))
            s_k_prime = sqrt(s_k * (cfg['max_sizes'][k]/cfg['min_dim']))
            anchors_loc.append([cx, cy, s_k_prime, s_k_prime])

            # rest of aspect ratios
            for ar in cfg['aspect_ratios'][k]:
                anchors_loc.append([cx, cy, s_k*sqrt(ar), s_k/sqrt(ar)])
                anchors_loc.append([cx, cy, s_k/sqrt(ar), s_k*sqrt(ar)])

    anchors_loc = np.array(anchors_loc)
    anchors_loc = point_form(anchors_loc)
    print(anchors_loc.shape)
    print("Spatial IoU before clip: {:.2f}%".format(spt_iou(data_loc, anchors_loc) * 100))
    if cfg['clip']:
        anchors_loc = np.clip(anchors_loc, 0, 1)
    print("Spatial IoU after clip: {:.2f}%".format(spt_iou(data_loc, anchors_loc) * 100))