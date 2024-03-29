#!/usr/bin/python
# -*- coding=utf-8 -*-

# 将xml中车辆的20多种中文type替换成6种英文type，保持原始的珠海标注格式不变
 
from xml.etree.ElementTree import ElementTree,Element
import os
 
def read_xml(in_path):
  '''读取并解析xml文件
    in_path: xml路径
    return: ElementTree'''
  tree = ElementTree()
  tree.parse(in_path)
  return tree
 
def write_xml(tree, out_path):
  '''将xml文件写出
    tree: xml树
    out_path: 写出路径'''
  tree.write(out_path, encoding="utf-8",xml_declaration=True)
 
def if_match(node, kv_map):
  '''判断某个节点是否包含所有传入参数属性
    node: 节点
    kv_map: 属性及属性值组成的map'''
  for key in kv_map:
    if node.get(key) != kv_map.get(key):
      return False
  return True
 
#---------------search -----
def find_nodes(tree, path):
  '''查找某个路径匹配的所有节点
    tree: xml树
    path: 节点路径'''
  return tree.findall(path)
 
def get_node_by_keyvalue(nodelist, kv_map):
  '''根据属性及属性值定位符合的节点，返回节点
    nodelist: 节点列表
    kv_map: 匹配属性及属性值map'''
  result_nodes = []
  for node in nodelist:
    if if_match(node, kv_map):
      result_nodes.append(node)
  return result_nodes
 
#---------------change -----
def change_node_properties(nodelist, kv_map, is_delete=False):
  '''修改/增加 /删除 节点的属性及属性值
    nodelist: 节点列表
    kv_map:属性及属性值map'''
  for node in nodelist:
    for key in kv_map:
      if is_delete:
        if key in node.attrib:
          del node.attrib[key]
      else:
        node.set(key, kv_map.get(key))
 
def change_node_text(nodelist, text, is_add=False, is_delete=False):
  '''改变/增加/删除一个节点的文本
    nodelist:节点列表
    text : 更新后的文本'''
  for node in nodelist:
    if is_add:
      node.text += text
    elif is_delete:
      node.text = ""
    else:
      node.text = text
 
def create_node(tag, property_map, content):
  '''新造一个节点
    tag:节点标签
    property_map:属性及属性值map
    content: 节点闭合标签里的文本内容
    return 新节点'''
  element = Element(tag, property_map)
  element.text = content
  return element
 
def add_child_node(nodelist, element):
  '''给一个节点添加子节点
    nodelist: 节点列表
    element: 子节点'''
  for node in nodelist:
    node.append(element)
 
def del_node_by_tagkeyvalue(nodelist, tag, kv_map):
  '''同过属性及属性值定位一个节点，并删除之
    nodelist: 父节点列表
    tag:子节点标签
    kv_map: 属性及属性值列表'''
  for parent_node in nodelist:
    children = parent_node.getchildren()
    for child in children:
      if child.tag == tag and if_match(child, kv_map):
        parent_node.remove(child)
 

sedan = ['家用轿车', '出租车', '赛车', '教练车']
suv = ['家用SUV', '家用MPV', '家用房车', '家用JEEP', '警车', '四轮车']
mini_bus = ['面包车', '救护车', '邮政车']
bus = ['公共汽车', '小型客车', '大型客车', '校车']
truck = ['油罐车', '垃圾车', '货运卡车', '小型货运卡车', '消防车', '皮卡', '搅拌车', '三轮车']
van = ['箱式货车']

merged_type = {}
merged_type['sedan'] = sedan
merged_type['suv'] = suv
merged_type['mini_bus'] = mini_bus
merged_type['bus'] = bus
merged_type['truck'] = truck
merged_type['van'] = van


if __name__ == "__main__":
  #1. 读取xml文件
  root_dir = r'C:\Users\chens\Desktop\20171214\720p\Annotations'
  target_dir = r'C:\Users\chens\Desktop\20171214\720p\tmp'
  file_list = os.listdir(root_dir)
  for fileitem in file_list:
    if fileitem.endswith('xml'):
      print(fileitem)
      tree = read_xml(os.path.join(root_dir, fileitem))
      #2. 属性修改
      nodes = find_nodes(tree, "object/type")
      for node in nodes:
          for k, v in merged_type.items():
              if node.text in v:
                  node.text = k
                  break
      #3. 输出到结果文件
      write_xml(tree, os.path.join(target_dir, fileitem))
 