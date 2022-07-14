import os
import numpy as np

result_dir = '/data/ICDAR2015/testing/VOC/protocol'
result_txt = 'det_test_carplate_BB.txt'
save_dir = '/data/ICDAR2015/testing/VOC/protocol/BB'

fin = open(os.path.join(result_dir, result_txt))
lines = fin.readlines()
fin.close()

for line in lines:
    fin = open(os.path.join(save_dir, 'res_'+line.strip().split(' ')[0].strip()+'.txt'), 'a+')
    if float(line.strip().split(' ')[1].strip()) >= 0.5:
        vertices_list = line.strip().split(' ')[6:]
        vertices_array = np.array(vertices_list).astype(np.float32)
        vertices_rounded_array = np.around(vertices_array).astype(np.int)
        vertices_rounded_list = vertices_rounded_array.tolist()
        vertices_rounded_str = ','.join('%s' %id for id in vertices_rounded_list)
        fin.write(vertices_rounded_str+ '\n')
    fin.close()
