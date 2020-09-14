# 将ZHhands的文件夹名和文件名拼接，组成独一无二的名字


from pathlib import Path
import os
import shutil
import xml.dom.minidom
from xml.dom.minidom import Document

ZHhands_path = '/dataset/ZHhands/training_set'
output_dir = '/dataset/ZHhands/labels'

ZHhands_sub_paths = os.listdir(ZHhands_path)
for sub_path in ZHhands_sub_paths:
    p = Path(ZHhands_path).joinpath(sub_path)
    for scene_path in p.iterdir():
        # sort xmls as .m file stores points in alphabetical order
        xmls_per_scene = list(scene_path.glob('*.xml'))
        xmls_per_scene.sort()
        for i, xml_path in enumerate(xmls_per_scene):
            unique_filename = sub_path + '_' + xml_path.parent.name + '_' + xml_path.stem
            output_xml_path = Path(output_dir).joinpath(Path(unique_filename + '.xml'))
            img_path = str(xml_path).split('.')[0] + '.jpg'
            output_img_path = str(output_xml_path).split('.')[0] + '.jpg'
            # 如果对应xml的jpg存在才拷贝
            if os.path.exists(str(img_path)):
                print(str(xml_path))
                dom = xml.dom.minidom.parse(str(xml_path))
                root = dom.documentElement

                # if xml dont have any object, continue
                objects = root.getElementsByTagName('object')
                if len(objects) == 0:
                    continue
                # if all are other, continue
                all_other = True
                for index, obj in enumerate(objects):
                    name = int(obj.getElementsByTagName('name')[0].childNodes[0].nodeValue)
                    if name != 0:
                        all_other = False
                if all_other:
                    continue

                shutil.copy(str(xml_path), str(output_xml_path))
                shutil.copy(str(img_path), str(output_img_path))