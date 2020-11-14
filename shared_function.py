# 包含其他数据处理程序共享的功能


import shapely
from shapely.geometry import LineString, Point

# 将车牌的四点转换为标准的左上右上右下左下顺序
def exchange_four_points_to_std(coor):
    # 初始化
    x_top_left = 0
    y_top_left = 0
    x_top_right = 0
    y_top_right = 0
    x_bottom_right = 0
    y_bottom_right = 0
    x_bottom_left = 0
    y_bottom_left = 0
    results = {}

    # 四个点组成二维数组
    points = []
    for i in range(4):
        points.append([int(coor[i*2+0]), int(coor[i*2+1])])

    # 求两对角线交点坐标
    line1 = LineString([points[0], points[2]])
    line2 = LineString([points[1], points[3]])
    int_pt = line1.intersection(line2)

    center_x = int_pt.x
    center_y = int_pt.y

    # 首先按照位于对角线交点左边还是右边划分,理想情况左右各两个点,但也有一条对角线是垂直的情况,那就是左右各三个点
    left_points = []
    right_points = []
    for point in points:
        # left
        if point[0] <= center_x:
            left_points.append(point)
        # right
        if point[0] >= center_x:
            right_points.append(point)

    assert (len(left_points)==2 and len(right_points)==2) or\
        (len(left_points)==3 and len(right_points)==3), "wrong four corners"

    if len(left_points)==2 and len(right_points)==2:
        # 交点左边的点按照x和y的大小关系分配是左上还是左下:当纵坐标不同时,纵坐标小的是左上;当纵坐标相同时,横坐标大的是左上
        if left_points[0][1] < left_points[1][1] or (left_points[0][1] == left_points[1][1] and left_points[0][0] > left_points[1][0]):
            x_top_left = left_points[0][0]
            y_top_left = left_points[0][1]
            x_bottom_left = left_points[1][0]
            y_bottom_left = left_points[1][1]
        elif left_points[0][1] > left_points[1][1] or (left_points[0][1] == left_points[1][1] and left_points[0][0] < left_points[1][0]):
            x_top_left = left_points[1][0]
            y_top_left = left_points[1][1]
            x_bottom_left = left_points[0][0]
            y_bottom_left = left_points[0][1]
        # 交点右边的点按照x和y的大小关系分配是右上还是右下:当纵坐标不同时,纵坐标小的是右上;当纵坐标相同时,横坐标小的是右上
        if right_points[0][1] < right_points[1][1] or (right_points[0][1] == right_points[1][1] and right_points[0][0] < right_points[1][0]):
            x_top_right = right_points[0][0]
            y_top_right = right_points[0][1]
            x_bottom_right = right_points[1][0]
            y_bottom_right = right_points[1][1]
        elif right_points[0][1] > right_points[1][1] or (right_points[0][1] == right_points[1][1] and right_points[0][0] > right_points[1][0]):
            x_top_right = right_points[1][0]
            y_top_right = right_points[1][1]
            x_bottom_right = right_points[0][0]
            y_bottom_right = right_points[0][1]

    # 这种情况下说明车牌倾斜较大,有一条对角线垂直于横坐标,最好还是人工修改下标注,程序很难判断
    # 其实可以根据非垂直对角线的角度进行判断,太麻烦了,分三种情况(1-3象限,2-4象限以及与x轴重合),也没有太大必要
    if len(left_points)==3 and len(right_points)==3:
        assert False, "车牌倾斜很大,有一条对角线垂直于横坐标,需要人工修改标注"

    # 其次四点确定后符合特定的关系
    assert x_top_left < x_top_right, "x_top_right should large than x_top_left"
    assert y_top_left <= y_bottom_left, "y_bottom_left should not small than y_top_left"
    assert x_bottom_left < x_bottom_right, "x_bottom_right should large than x_bottom_left"
    assert y_top_right <= y_bottom_right, "y_bottom_right should not small than y_top_right"

    # 最后确定由四点组成的矩形符合特定的关系
    xmin = min(x_top_left, x_bottom_left)
    ymin = min(y_top_left, y_top_right)
    xmax = max(x_bottom_right, x_top_right)
    ymax = max(y_bottom_right, y_bottom_left)
    assert xmin < xmax, "xmax should large than xmin"
    assert ymin < ymax, "ymax should large than ymin"

    results['x_top_left'] = x_top_left
    results['y_top_left'] = y_top_left
    results['x_top_right'] = x_top_right
    results['y_top_right'] = y_top_right
    results['x_bottom_right'] = x_bottom_right
    results['y_bottom_right'] = y_bottom_right
    results['x_bottom_left'] = x_bottom_left
    results['y_bottom_left'] = y_bottom_left

    return results


# 确保数值在图片中不越界
def limit_in_bounds(num, low_bound, sup_bound):
    if num < low_bound:
        num = low_bound
    if num > sup_bound:
        num = sup_bound

    return num
