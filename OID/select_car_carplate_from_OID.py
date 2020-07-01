# 首先从OID中把有车牌标注的图片挑选出来,之后把这些图片的车辆和车牌标注提取出来,其余标注不要
# /m/01jfm_: Vehicle registration plate
# /m/0k4j: Car
import csv
import os
import shutil

# !!!!!!!!!!!!!!!!!!!!!!!!!!!
# 需要分别对validation和test做
# 之后用OID_to_VOC分别对validation和test进行转换
# 最后用val_to_test_vice_versa分配训练集和测试集
csv_path = '/dataset/OID/origin/test-annotations-bbox.csv'
img_path = '/dataset/OID/origin/test'
target_img_path = '/dataset/OID/test_with_carplate'
target_csv_path = '/dataset/OID/test_car_carplate.csv'
# url
url_path = '/dataset/OID/origin/test-images.csv'
url_dic = {}


# 将图片名对应url的csv变成图片名为key,url为value的字典
def get_image_url_dic():
    # read url
    url_file = csv.DictReader(open(url_path))
    for con in url_file:
        url_dic[con['image_name']] = con['image_url']


# 把有车牌标注的图片取出来
def get_image_with_carplate():
    # DictReader对每一次读必须重新初始化一次
    csv_file = csv.DictReader(open(csv_path))
    for con in csv_file:
        if con['LabelName'] == "/m/01jfm_" and os.path.exists(os.path.join(img_path, con['ImageID'] + '.jpg')):
            shutil.copy(os.path.join(img_path, con['ImageID'] + '.jpg'), os.path.join(target_img_path, con['ImageID'] + '.jpg'))


# 把有车牌的图片中的车辆和车牌标注提取出来
def keep_label_of_car_carplate():
    # DictReader对每一次读必须重新初始化一次
    csv_file = csv.DictReader(open(csv_path))
    file_list = os.listdir(target_img_path)
    fileheader = csv_file.fieldnames
    fileheader.append('URL')  # 加上URL
    targe_file = open(target_csv_path, 'w+')
    dict_writer = csv.DictWriter(targe_file, fieldnames=fileheader)
    dict_writer.writeheader()

    num = 0
    for con in csv_file:
        con['URL'] = url_dic[con['ImageID'] + '.jpg']
        num += 1
        # 此处如果file_list太大，容易使程序时间过长，所以前面先把符合要求的图片单独提取出来了
        if con['ImageID'] + '.jpg' in file_list and (con['LabelName'] == "/m/01jfm_" or con['LabelName'] == "/m/0k4j"):
            dict_writer.writerow(con)
        if num % 100000 == 0:
            print(num)

    targe_file.close()


def main():
    get_image_url_dic()
    get_image_with_carplate()
    keep_label_of_car_carplate()

main()
