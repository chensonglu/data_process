# 将egohands的文件夹名和文件名拼接，组成独一无二的名字


from pathlib import Path
import os
import shutil

ZHhands_path = r'C:\Users\chens\Desktop\ZHhands'
output_dir = r'C:\Users\chens\Desktop\ZHhands\labels'

p = Path(ZHhands_path).joinpath('kehu')
for scene_path in p.iterdir():
    # sort xmls as .m file stores points in alphabetical order
    xmls_per_scene = list(scene_path.glob('*.xml'))
    xmls_per_scene.sort()
    for i, xml_path in enumerate(xmls_per_scene):
        unique_filename = xml_path.parent.name + '_' + xml_path.stem
        output_xml_path = Path(output_dir).joinpath(Path(unique_filename + '.xml'))
        img_path = str(xml_path).split('.')[0] + '.jpg'
        output_img_path = str(output_xml_path).split('.')[0] + '.jpg'
        # 如果对应xml的jpg存在才拷贝
        if os.path.exists(str(img_path)):
            shutil.copy(str(xml_path), str(output_xml_path))
            shutil.copy(str(img_path), str(output_img_path))