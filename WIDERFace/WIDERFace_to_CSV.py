# 处理WIDERFace的txt文件，将其变为image_path/image_name x1 y1 x2 y2 label的格式
# 如果没有人脸变为image_path/image_name . . . . .
# 跳过一些宽或高为0的人脸
# 训练集和验证集要分开生成，因为图片路径不一致
import os

# 图片要加上绝对路径
abs_path = '/dataset/WIDERFace/WIDER_train/images'
# abs_path = '/dataset/WIDERFace/WIDER_val/images'

root_dir = '/dataset/WIDERFace/wider_face_split'
target_dir = '/data/WIDERFace'


def read_file_to_dict(ofs, lines):
    key = lines[ofs]
    values = []
    ofs = ofs + 1
    num = int(lines[ofs])
    # 注意一些没有人脸的图片
    if num == 0:
        print('no face')
        print(key)
        ofs = ofs + 1
        return key, values, ofs

    for i in range(num):
        ofs = ofs + 1
        value = lines[ofs]
        items = value.split()
        x1 = int(items[0])
        y1 = int(items[1])
        w = int(items[2])
        h = int(items[3])
        # 有些长宽小于1的人脸
        if w < 1 or h < 1:
            print('face less than 1')
            print(key)
            continue
        # 这个地方有一个疑问，x2和x1是否差了一个像素
        x2 = x1 + w
        y2 = y1 + h
        values.append([str(x1), str(y1), str(x2), str(y2)])
    ofs = ofs + 1

    return key, values, ofs


def write_to_csv(dics, write_file_name):
    fp = open(write_file_name, 'a+')

    for key, values in dics.items():
        # 首先判断人脸图片是否存在
        if not os.path.exists(os.path.join(abs_path, key)):
            print('image not exist')
            print(os.path.join(abs_path, key))
            continue
        if len(values) == 0:
            fp.write(os.path.join(abs_path, key) + ' . . . . .' + '\n')
            # continue
        else:
            for value in values:
                fp.write(os.path.join(abs_path, key) + ' ' + ' '.join(value) + ' face' + '\n')

    fp.close()


def read_file(file_name):
    # 将txt所有内容读入lines数组
    lines = []
    fp = open(file_name)
    for line in fp:
        # 别忘了strip
        lines.append(line.strip())
    fp.close()

    dics = {}
    ofs = 0
    while ofs < len(lines):
        key, values, ofs = read_file_to_dict(ofs, lines)
        dics[key] = values

    return dics


def main(file_name, write_file_name):
    dics = read_file(file_name)
    write_to_csv(dics, write_file_name)

main(os.path.join(root_dir, 'wider_face_train_bbx_gt.txt'), os.path.join(target_dir, 'train.txt'))
# main(os.path.join(root_dir, 'wider_face_val_bbx_gt.txt'), os.path.join(target_dir, 'val.txt'))