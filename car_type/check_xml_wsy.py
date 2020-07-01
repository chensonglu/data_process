# coding: utf-8
import os
import xml.dom.minidom
from xml.dom.minidom import Document
import shutil
import sys
reload(sys)
sys.setdefaultencoding('utf8')

'''
代码进行了如下检查：
1.xml文件是否为空
2.车型边界框的存在性
3.是否选择车的远近
4.occlusion和incomplete关联性判断（自动更改）
5.difficult和misc不等于1时，type应当存在（将type改为“请添加车型”，请添加！）
6.type是否为car_types数组中的标准写法（将type改为“不规范车型”，请修改！）
7.若type在easy_types中，则自动删除make、medel
8.车牌边界框的存在性
9.车牌与车型是否相匹配
10.unrecognable不等于1时，label应当存在
11.车牌长度应该不大于8，PS: len('我')==1
12.车牌每个字符是否为carplate_characters中的标准
13.unrecognable和difficult关联性检查，自动修正
14.车牌中'#'的出现和difficult值的关联性检查，自动修正

README：
1.将需要检查的文件夹命名为input（否则自行更改root_dir参数）
2.文件与check_xml.py在同一路径下, 运行py文件
3.结果输出wrong_label.txt日志
4.更改错误后，记得重新check，直到没有出错为止

注：运行环境为windows，若ubuntu环境下需要修改：
    root_dir = ".\\input" 改为 root_dir = "./input"
'''

root_dir = "/dataset/yz/20171214/night/1080p/Annotations"   # windows下的路径用\, 与转义字符\冲突，需要\\
fo = open('wrong_label.txt', 'w+')

# 规范车牌字符
carplate_characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '京', '沪', '津', '渝', '冀', '晋', '蒙', '辽', '吉', '黑', '苏', '浙', '皖', '闽', '赣', '鲁', '豫', '鄂', '湘', '粤', '桂', '琼', '川', '贵', '云', '藏', '陕', '甘', '青', '宁', '新', '领', '学', '使', '警', '挂', '港', '澳', '电', '*', '#']

# 规范二级分类（type）
car_types = ['家用轿车', '家用SUV', '家用MPV', '家用房车', '家用JEEP', '出租车', '公共汽车', '面包车', '小型客车', '大型客车', '箱式货车', '油罐车', '垃圾车', '货运卡车', '小型货运卡车', '校车', '赛车', '消防车', '救护车', '邮政车', '警车', '皮卡', '教练车', '四轮车', '三轮车', '搅拌车']

# 不需要make、medel的二级分类（type）
easy_types = ['公共汽车', '小型客车', '大型客车', '箱式货车', '油罐车', '垃圾车', '校车', '赛车', '消防车', '救护车', '邮政车', '四轮车', '三轮车', '搅拌车']

def check_xml(root_path, fileitem):
    try:
        # 尝试从xml文件得到dom对象
        dom = xml.dom.minidom.parse(os.path.join(root_path, fileitem))
    except Exception as e:
        # 读取失败则写入日志
        fo.write(os.path.join(root_path, fileitem) + '\n')
        fo.write('\t' + '空xml' + '\n')
        return
    
    # 获取根节点，再根据标签名获取元素节点
    root = dom.documentElement
    objects = root.getElementsByTagName('object')

    for index, obj in enumerate(objects):
        difficult_value = int(obj.getElementsByTagName('difficult')[0].childNodes[0].nodeValue)
        misc_value = int(obj.getElementsByTagName('misc')[0].childNodes[0].nodeValue)
        occlusion_value = int(obj.getElementsByTagName('occlusion')[0].childNodes[0].nodeValue)
        incomplete_value = int(obj.getElementsByTagName('incomplete')[0].childNodes[0].nodeValue)

        # 对边界框存在性检查   
        try:
            bndbox = obj.getElementsByTagName('bndbox')[0]
        except Exception as e:
            fo.write(os.path.join(root_path, fileitem) + '\n')
            fo.write('\t' + '车型没有边界框bndbox' + '\n')
            continue
        car_xmin = int(bndbox.getElementsByTagName('xmin')[0].childNodes[0].nodeValue)
        car_ymin = int(bndbox.getElementsByTagName('ymin')[0].childNodes[0].nodeValue)
        car_xmax = int(bndbox.getElementsByTagName('xmax')[0].childNodes[0].nodeValue)
        car_ymax = int(bndbox.getElementsByTagName('ymax')[0].childNodes[0].nodeValue)

        # 距离属性存在性检查
        try:
            distance = obj.getElementsByTagName('distance')[0]
        except Exception as e:
            fo.write(os.path.join(root_path, fileitem) + '\n')
            fo.write('\t' + '没有选距离distance')
            fo.write('\t' + '——出错车型的xmin值=' + str(car_xmin) + '\n')   # 用xmin来唯一标识没有distance的车型

        # occlusion和incomplete关联性判断
        if occlusion_value == 1 and incomplete_value == 0:
            incomplete = obj.getElementsByTagName('incomplete')[0].childNodes[0]
            incomplete.replaceWholeText(u'1')   # 自动更改incomplete的值为1
            # fo.write(os.path.join(root_path, fileitem) + '\n')
            # fo.write('\t' + '勾选occlusion，却没有勾选incomplete')
            # fo.write('\t' + '——已自动更正' + '\n')

        # 对车型type检查
        if difficult_value != 1 and misc_value != 1:    # 此时应有type值
            try:
                type = obj.getElementsByTagName('type')[0].childNodes[0]
                type_value = type.nodeValue
                if type_value not in car_types:
                    type.replaceWholeText(u'不规范车型')  # 自动将type改为“不规范车型”
                    fo.write(os.path.join(root_path, fileitem) + '\n')
                    fo.write('\t' + '不规范的车型type：' + type_value)
                    fo.write('\t' + '——已将type改为“不规范车型”，请修改！' + '\n')

                # 若type在easy_types中，则自动删除make、medel
                if type_value in easy_types:
                    try:
                        make = obj.getElementsByTagName('make')[0]
                        try:
                            obj.removeChild(make)
                            # 去除空行
                            space = obj.childNodes[4]
                            space.replaceWholeText(u'\n\t\t')
                        except Exception as e:
                            fo.write(os.path.join(root_path, fileitem) + '\n')
                            fo.write('\t' + '自动删除“' + type_value + '”的make失败。（本不应该有make,请手动删除！）' + '\n')
                    except Exception as e:
                        pass
                    try:
                        model = obj.getElementsByTagName('model')[0]
                        try:
                            obj.removeChild(model)
                            # 去除空行
                            space = obj.childNodes[4]
                            space.replaceWholeText(u'\n\t\t')
                        except Exception as e:
                            fo.write(os.path.join(root_path, fileitem) + '\n')
                            fo.write('\t' + '自动删除“' + type_value + '”的model失败。（本不应该有make,请手动删除！）' + '\n')
                    except Exception as e:
                        pass
            except Exception as e:
                # 添加车型type节点：默认家用轿车
                type = dom.createElement('type')
                type.appendChild(dom.createTextNode(u'请添加车型'))
                difficult = obj.getElementsByTagName('difficult')[0]
                obj.insertBefore(type, difficult)
                obj.insertBefore(dom.createTextNode('\n\t\t'), difficult)
                fo.write(os.path.join(root_path, fileitem) + '\n')
                fo.write('\t' + 'difficult和misc不等于1时，type应当存在')
                fo.write('\t' + '——已将type改为“请添加车型”，请添加！' + '\n')   

        # 对车牌检查
        try:
            carplates = obj.getElementsByTagName('carplate')
        except Exception as e:
            continue
        for index, plate in enumerate(carplates):
            plate_difficult = plate.getElementsByTagName('difficult')[0].childNodes[0]
            plate_difficult_value = int(plate_difficult.nodeValue)
            unrecognable_value = int(plate.getElementsByTagName('unrecognable')[0].childNodes[0].nodeValue)

            # 边界存在检查
            try:
                plate_bndbox = plate.getElementsByTagName('bndbox')[0]
            except Exception as e:
                fo.write(os.path.join(root_path, fileitem) + '\n')
                fo.write('\t' + '车牌没有边界框bndbox' + '\n')
                continue
            palte_xmin = int(plate_bndbox.getElementsByTagName('xmin')[0].childNodes[0].nodeValue)
            palte_ymin = int(plate_bndbox.getElementsByTagName('ymin')[0].childNodes[0].nodeValue)
            palte_xmax = int(plate_bndbox.getElementsByTagName('xmax')[0].childNodes[0].nodeValue)
            palte_ymax = int(plate_bndbox.getElementsByTagName('ymax')[0].childNodes[0].nodeValue)
            

            # 车牌与车型对应检查
            xcenter = (palte_xmin + palte_xmax) / 2
            ycenter = (palte_ymin + palte_ymax) / 2
            if xcenter > car_xmin and xcenter < car_xmax and ycenter > car_ymin and ycenter < car_ymax:
                pass
            else:
                fo.write(os.path.join(root_path, fileitem) + '\n')
                fo.write('\t' + '车牌和车型不匹配')
                fo.write('\t' + '——出错车牌的xmin值=' + str(palte_xmin) + '\n')   # 用palte_xmin来唯一标识错位的车牌

            # 车牌规范性检查
            # unrecognable和difficult关联性自检自修正
            if unrecognable_value == 1 and plate_difficult_value == 0:
                plate_difficult.replaceWholeText(u'1')
            if unrecognable_value == 0:     # 此时应有label值和车牌背景
                #  print("!!!!!!!!!!")
            	# 车牌背景存在性检查
                try:
                    background_color = plate.getElementsByTagName('background_color')[0]
                except Exception as e:
                    fo.write(os.path.join(root_path, fileitem) + '\n')
                    fo.write('\t' + '没有选择车牌背景background_color')
                    fo.write('\t' + '——出错车牌的xmin值=' + str(palte_xmin) + '\n')   # 用plate_min来唯一标识没有背景的车型                
                # 车牌存在性检查
                try:
                    label_value = plate.getElementsByTagName('label')[0].childNodes[0].nodeValue
                except Exception as e:
                    fo.write(os.path.join(root_path, fileitem) + '\n')
                    fo.write('\t' + 'unrecognable不等于1时，label应当存在')
                    fo.write('\t' + '——出错车牌的xmin值=' + str(palte_xmin) + '\n')   # 用plate_min来唯一标识没有plate的车型
                    continue
                # 车牌长度检查
                if len(label_value) > 8:
                    fo.write(os.path.join(root_path, fileitem) + '\n')
                    fo.write('\t' + '车牌"' + label_value + '"的长度超过8' + '\n')
                    continue
                # 车牌字符规范检查
                flag = 0	# 记录是否有'#'出现
                for char in label_value:
                    if char not in carplate_characters:
                        fo.write(os.path.join(root_path, fileitem) + '\n')
                        fo.write('\t' + '车牌"' + label_value + '"中含有不规范字符：' + char + '\n')
                    if char == '#':
                        flag = 1
                        # 有'#'车牌difficult应该为1，自动修改
                        if plate_difficult_value != 1:
                            plate_difficult.replaceWholeText(u'1')
                # 车牌未出现'#'（unrecognable_value = 0）时difficult应该为0，自动修改
            	if flag == 0 and plate_difficult_value == 1:	# 此时unrecognable_value != 1
                    plate_difficult.replaceWholeText(u'0')
            

    # 完成对xml的修改，不能缺失！
    f_xml = open(os.path.join(root_path, fileitem), 'w')
    dom.writexml(f_xml, encoding="utf-8")
    f_xml.close()


file_list = os.listdir(root_dir)
for fileitem in file_list:
    if fileitem.endswith('xml'):
        check_xml(root_dir, fileitem)


