import glob
import xml.etree.ElementTree as ET
import numpy as np

ANNOTATIONS_PATH = "/data/CCPD/VOC/Annotations"
CLUSTERS = 6


def iou(box, clusters):
    """
    Calculates the Intersection over Union (IoU) between a box and k clusters.
    :param box: tuple or array, shifted to the origin (i. e. width and height)
    :param clusters: numpy array of shape (k, 2) where k is the number of clusters
    :return: numpy array of shape (k, 0) where k is the number of clusters
    """
    x = np.minimum(clusters[:, 0], box[0])
    y = np.minimum(clusters[:, 1], box[1])
    if np.count_nonzero(x == 0) > 0 or np.count_nonzero(y == 0) > 0:
        raise ValueError("Box has no area")

    intersection = x * y
    box_area = box[0] * box[1]
    cluster_area = clusters[:, 0] * clusters[:, 1]

    iou_ = intersection / (box_area + cluster_area - intersection)

    return iou_


def avg_iou(boxes, clusters):
    """
    Calculates the average Intersection over Union (IoU) between a numpy array of boxes and k clusters.
    :param boxes: numpy array of shape (r, 2), where r is the number of rows
    :param clusters: numpy array of shape (k, 2) where k is the number of clusters
    :return: average IoU as a single float
    """
    return np.mean([np.max(iou(boxes[i], clusters)) for i in range(boxes.shape[0])])


def translate_boxes(boxes):
    """
    Translates all the boxes to the origin.
    :param boxes: numpy array of shape (r, 4)
    :return: numpy array of shape (r, 2)
    """
    new_boxes = boxes.copy()
    for row in range(new_boxes.shape[0]):
        new_boxes[row][2] = np.abs(new_boxes[row][2] - new_boxes[row][0])
        new_boxes[row][3] = np.abs(new_boxes[row][3] - new_boxes[row][1])
    return np.delete(new_boxes, [0, 1], axis=1)


def kmeans(boxes, k, dist=np.median):
    """
    Calculates k-means clustering with the Intersection over Union (IoU) metric.
    :param boxes: numpy array of shape (r, 2), where r is the number of rows
    :param k: number of clusters
    :param dist: distance function
    :return: numpy array of shape (k, 2)
    """
    rows = boxes.shape[0]

    distances = np.empty((rows, k))
    last_clusters = np.zeros((rows,))

    np.random.seed()

    # the Forgy method will fail if the whole array contains the same rows
    clusters = boxes[np.random.choice(rows, k, replace=False)]

    while True:
        for row in range(rows):
            distances[row] = 1 - iou(boxes[row], clusters)

        nearest_clusters = np.argmin(distances, axis=1)

        if (last_clusters == nearest_clusters).all():
            break

        for cluster in range(k):
            clusters[cluster] = dist(boxes[nearest_clusters == cluster], axis=0)

        last_clusters = nearest_clusters

    return clusters


def load_dataset(path):
	dataset = []
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

	return np.array(dataset)


data = load_dataset(ANNOTATIONS_PATH)
out = kmeans(data, k=CLUSTERS)
print("Accuracy: {:.2f}%".format(avg_iou(data, out) * 100))
print("Boxes:\n {}".format(out))

ratios = np.around(out[:, 0] / out[:, 1], decimals=2).tolist()
print("Ratios:\n {}".format(sorted(ratios)))

input = np.array([512, 512])
print("Sizes with input 512*512:\n {}".format(out*input))

input = np.array([300, 300])
print("Sizes with input 300*300:\n {}".format(out*input))

# Accuracy: 82.23%
# Boxes:
#  [[0.4375     0.11896552]
#  [0.37638889 0.08965517]
#  [0.24166667 0.05603448]
#  [0.31111111 0.07155172]]
# Ratios:
#  [3.68, 4.2, 4.31, 4.35]
# Sizes with input 512*512:
#  [[224.          60.91034483]
#  [192.71111111  45.90344828]
#  [123.73333333  28.68965517]
#  [159.28888889  36.63448276]]
# Sizes with input 300*300:
#  [[131.25        35.68965517]
#  [112.91666667  26.89655172]
#  [ 72.5         16.81034483]
#  [ 93.33333333  21.46551724]]

# Accuracy: 85.00%
# Boxes:
#  [[0.46805556 0.125     ]
#  [0.425      0.09396552]
#  [0.2375     0.05517241]
#  [0.35555556 0.07931034]
#  [0.33055556 0.10948276]
#  [0.29444444 0.06982759]]
# Ratios:
#  [3.02, 3.74, 4.22, 4.3, 4.48, 4.52]
# Sizes with input 512*512:
#  [[239.64444444  64.        ]
#  [217.6         48.11034483]
#  [121.6         28.24827586]
#  [182.04444444  40.60689655]
#  [169.24444444  56.05517241]
#  [150.75555556  35.75172414]]
# Sizes with input 300*300:
#  [[140.41666667  37.5       ]
#  [127.5         28.18965517]
#  [ 71.25        16.55172414]
#  [106.66666667  23.79310345]
#  [ 99.16666667  32.84482759]
#  [ 88.33333333  20.94827586]]
