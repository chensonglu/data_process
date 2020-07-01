# 包含其他数据处理程序共享的功能


# 将车牌的四点转换为标准的左上右上右下左下顺序
def exchange_four_points_to_std(coor):
    sum = []
    dic = {}
    results = {}
    sub_coor = [0] * 4

    for i in range(4):
        sum.append([int(coor[i*2+0]), int(coor[i*2+1])])
    for index, value in enumerate(sum):
        dic[index] = value[0] + value[1]
    sorted_dic = sorted(dic.items(), key=lambda d: d[1], reverse=True)
    sub_coor[0] = sum[sorted_dic[3][0]]
    sub_coor[2] = sum[sorted_dic[0][0]]
    sub_coor[1] = sum[sorted_dic[1][0]]
    sub_coor[3] = sum[sorted_dic[2][0]]
    if (sub_coor[1][0] < sub_coor[3][0]):
        tmp = sub_coor[1]
        sub_coor[1] = sub_coor[3]
        sub_coor[3] = tmp

    x_top_left = sub_coor[0][0]
    y_top_left = sub_coor[0][1]
    x_top_right = sub_coor[1][0]
    y_top_right = sub_coor[1][1]
    x_bottom_right = sub_coor[2][0]
    y_bottom_right = sub_coor[2][1]
    x_bottom_left = sub_coor[3][0]
    y_bottom_left = sub_coor[3][1]

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
