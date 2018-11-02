"""XXXX."""
# import math
# import os
import pandas as pd
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
# import h5py


def read_txt(file_name):
    """读取文本文件。

    用Pandas读取文本文件。

    Args:
        file_name: 文件路径。

    Returns:
        DataFrame格式的数据
    """
    return pd.read_table(file_name, sep='\t', header=None, encoding="utf-8")


def read_img(file_name):
    """读取图片。

    使用skimage读取图片。

    Args:
        file_name: 文件路径。

    Returns:
        图片的ndarray数组。
    """
    return io.imread(file_name)


# def crop_img(df, img):
# 	p1 = np.array(df[0,:]).reshape((3,1))
# 	p2 = np.array(df[1,:]).reshape((3,1))
# 	p3 = np.array(df[2,:]).reshape((3,1))
# 	p4 = np.array(df[3,:]).reshape((3,1))
# 	offset = np.array([[0], [0], [0]])

# 	if p1[0][0] != p2[0][0]:
# 		sin, cos = compute_angles(p1, p3)
# 		height, width, _ = img.shape
# 		m = rotation_matrix(sin, cos, width/2, -height/2)
# 		p1 = np.dot(m, p1)
# 		p2 = np.dot(m, p2)                                                                                                                                                                                                                                                                                                                        
# 		p3 = np.dot(m, p3)
# 		p4 = np.dot(m, p4)
# 		# print(math.acos(cos))
# 		# print(math.asin(sin))
# 		img = transform.rotate(img, -math.degrees(math.acos(cos)), resize=True)
# 		shape = img.shape
# 		offset_x = shape[0] - width 
# 		offset_y = shape[1] - height
# 		offset[0][0] = offset_x
# 		offset[1][0] = offset_y

# 	p1 = np.rint(p1)
# 	p4 = np.rint(p4)
# 	p1 = p1 + offset
# 	p2 = p2 + offset
# 	p3 = p3 + offset
# 	p4 = p4 + offset
# 	imgshow(p1[0][0], p1[1][0], p3[0][0], p3[1][0], 0, 0, 0, 0, img)
# 	start_x = int(p1[0][0])
# 	start_y = int(p1[1][0])
# 	end_x = int(p4[0][0])
# 	end_y = int(p4[1][0])
# 	return img[start_y : end_y, start_x: end_x, :]
def crop_img(box, img):
    """裁剪图片。

    用传入的矩形裁剪图片。

    Args:
        box: 裁剪的矩形区域。
        img: 被裁剪的图片数组。

    Returns:
        裁剪后的图片数组。
    """
    return img[box[0]:box[2], box[1]:box[3], :]


def compute_angles(p_1, p_2):
    """计算两点连线与x轴的角度。

    Args:
        p_1: 第一个点。
        p_2: 第二个点。

    Returns:
        返回存有cos和sin的列表。
    """
    new_p = p_2 - p_1
    print(new_p)
    distance = np.linalg.norm(new_p)
    cos = new_p[0][0] / distance
    sin = new_p[1][0] / distance
    return [cos, sin]


def rotation_matrix(sin, cos, t_x, t_y):
    """求旋转矩阵。

    Args:
        sin: 旋转角度的sin值。
        cos: 旋转角度的cos值。
        t_x: x轴的位移。
        t_y: y轴的位移。
    
    Returns:
        返回旋转矩阵。
    """
    return np.array([
        [cos, -sin, (1 - cos) * t_x - t_y * sin],
        [sin, cos, (1 - cos) * -t_y - t_x * sin],
        [0, 0, 1]
    ])


# def imgshow(x1, y1, x2, y2, x3, y3, x4, y4, img):
#     """测试用。"""
#     plt.imshow(img)
#     plt.plot(x1, y1, 'o')
#     plt.plot(x2, y2, 'o')
#     plt.plot(x3, y3, 'o')
#     plt.plot(x4, y4, 'o')
#     plt.show()


def imgshow_pd(data_frame, img):
    """测试用。"""
    plt.imshow(img)
    plt.plot(data_frame[0], data_frame[1], 'o')
    plt.plot(data_frame[2], data_frame[3], 'o')
    plt.plot(data_frame[4], data_frame[5], 'o')
    plt.plot(data_frame[6], data_frame[7], 'o')
    plt.show()


def sort_points(arr):
    """排序矩形的顶点。

    Args:
        arr: 顶点数组。

    Returns:
        返回排序后的定点数组。
    """
    i = 0
    new_arr = []

    while i < 8:
        point = [arr[i], arr[i + 1], 1]
        new_arr.append(point)
        i += 2

    new_arr.sort(key=lambda x: (x[0], x[1]))

    if new_arr[2][1] > new_arr[3][1]:
        _ = new_arr[2]
        new_arr[2] = new_arr[3]
        new_arr[3] = _

    return new_arr


def fit(arr):
    """拟合矩形。"""
    x_arr = arr[0::2]
    y_arr = arr[1::2]
    min_x = np.min(x_arr)
    min_y = np.min(y_arr)
    max_x = np.max(x_arr)
    max_y = np.max(y_arr)
    return [min_x, min_y, max_x, max_y]


# def save_h5(file_name, data, name):
#     """不清楚干了啥。
#     """
#     if not os.path.isfile(file_name):
#         h5 = h5py.File(file_name, 'w')
#         shape = data.shape
#         dataset = h5.create_dataset(name, data=data, maxshape=(None, shape[1], shape[2], shape[3]))
#     else:
#         h5 = h5py.File(file_name, 'r+')
#         shape = data.shape
#         # length = dataset.shape[0]
#         # dataset.resize((length + shape[0], shape[1], shape[2], shape[3]))
#         # dataset[dataset.shape[0]:length + shape[0]] = data
#         h5.close()


# def load_h5(file_name, name):
#     h5 = h5py.File(file_name, 'r')
#     return h5[name]


# def hello():
#     return 'hello'
