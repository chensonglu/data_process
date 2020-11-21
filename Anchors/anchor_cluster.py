import glob
import xml.etree.ElementTree as ET
import numpy as np
from kmeans import kmeans, avg_iou

ANNOTATIONS_PATH = "/data/CCPD/VOC/Annotations_train"
CLUSTERS = 4


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
ratios = np.around(out[:, 0] / out[:, 1], decimals=2).tolist()
print("Sorted Ratios:\n {}".format(sorted(ratios)))
areas = np.around(out[:, 0] * out[:, 1], decimals=6).tolist()
area_order = np.argsort(areas)
print("Sorted Areas:\n {}".format(sorted(areas)))
print("Sorted Boxes:\n {}".format(out[area_order]))