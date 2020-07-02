# 将egohands的文件夹名和文件名拼接，组成独一无二的名字


from pathlib import Path
import os
import shutil

egohands_path = '/dataset/egohands_data'
output_dir = '/dataset/egohands_data/tmp'

p = Path(egohands_path).joinpath('_LABELLED_SAMPLES')
for scene_path in p.iterdir():
    # sort images as .m file stores points in alphabetical order
    images_per_scene = list(scene_path.glob('*.jpg'))
    images_per_scene.sort()
    for i, image_path in enumerate(images_per_scene):
        unique_filename = os.path.join(image_path.parent.name, '_', image_path.stem)
        output_image_path = Path(output_dir).joinpath(Path(unique_filename + '.jpg'))
        shutil.copy(str(image_path), str(output_image_path))