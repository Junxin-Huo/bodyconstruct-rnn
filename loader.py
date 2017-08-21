from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import os
import math

FRAME_COUNT = 10


def loadDataLabel(dir_name, batch_size):
    assert os.path.isdir(dir_name), "dir_name is not dir"
    dir = os.listdir(dir_name)
    dir.sort()
    len_dir = len(dir)
    datas_1 = []
    # datas_2 = []
    labels_1 = []
    # labels_2 = []
    righthand_position = np.zeros((3))
    righthand_rotation = np.zeros((6))
    lefthand_position = np.zeros((3))
    lefthand_rotation = np.zeros((6))
    rightelbow_position = np.zeros((3))
    rightelbow_rotation = np.zeros((6))
    leftelbow_position = np.zeros((3))
    leftelbow_rotation = np.zeros((6))
    camera_position = np.zeros((3))
    camera_rotation = np.zeros((6))
    for i in range(len_dir):
        if os.path.isdir(dir_name + '/' + dir[i]):
            continue
        f = open(dir_name + '/' + dir[i], "r")
        lines = f.readlines()
        count = 0
        for line in lines:
            if count == 0:
                pass
            elif count == 1:
                words = line.split(' ')
                if words[0] == "RH":
                    righthand_position[0] = float(words[1])
                    righthand_position[1] = float(words[2])
                    righthand_position[2] = float(words[3])
                    righthand_rotation[0] = float(words[4])
                    righthand_rotation[1] = float(words[5])
                    righthand_rotation[2] = float(words[6])
                    righthand_rotation[3] = float(words[7])
                    righthand_rotation[4] = float(words[8])
                    righthand_rotation[5] = float(words[9])
                else:
                    count = (count - 1) % 6
            elif count == 2:
                words = line.split(' ')
                lefthand_position[0] = float(words[1])
                lefthand_position[1] = float(words[2])
                lefthand_position[2] = float(words[3])
                lefthand_rotation[0] = float(words[4])
                lefthand_rotation[1] = float(words[5])
                lefthand_rotation[2] = float(words[6])
                lefthand_rotation[3] = float(words[7])
                lefthand_rotation[4] = float(words[8])
                lefthand_rotation[5] = float(words[9])
            elif count == 3:
                words = line.split(' ')
                rightelbow_position[0] = float(words[1])
                rightelbow_position[1] = float(words[2])
                rightelbow_position[2] = float(words[3])
                rightelbow_rotation[0] = float(words[4])
                rightelbow_rotation[1] = float(words[5])
                rightelbow_rotation[2] = float(words[6])
                rightelbow_rotation[3] = float(words[7])
                rightelbow_rotation[4] = float(words[8])
                rightelbow_rotation[5] = float(words[9])
            elif count == 4:
                words = line.split(' ')
                leftelbow_position[0] = float(words[1])
                leftelbow_position[1] = float(words[2])
                leftelbow_position[2] = float(words[3])
                leftelbow_rotation[0] = float(words[4])
                leftelbow_rotation[1] = float(words[5])
                leftelbow_rotation[2] = float(words[6])
                leftelbow_rotation[3] = float(words[7])
                leftelbow_rotation[4] = float(words[8])
                leftelbow_rotation[5] = float(words[9])
            elif count == 5:
                words = line.split(' ')
                camera_position[0] = float(words[1])
                camera_position[1] = float(words[2])
                camera_position[2] = float(words[3])
                camera_rotation[0] = float(words[4])
                camera_rotation[1] = float(words[5])
                camera_rotation[2] = float(words[6])
                camera_rotation[3] = float(words[7])
                camera_rotation[4] = float(words[8])
                camera_rotation[5] = float(words[8])

                data = np.zeros((3, 3))
                label = np.zeros(3)
                for j in range(3):
                    data[0][j] = righthand_position[j]
                    data[1][j] = righthand_rotation[j]
                    data[2][j] = righthand_rotation[j + 3]
                    label[j] = rightelbow_position[j]
                datas_1.append(np.reshape(data, -1))
                labels_1.append(np.reshape(label, -1))

                # data_l = np.zeros((3, 3))
                # label_l = np.zeros(3)
                # for j in range(3):
                #     data_l[0][j] = lefthand_position[j]
                #     data_l[1][j] = lefthand_rotation_sin[j]
                #     data_l[2][j] = lefthand_rotation_cos[j]
                #     label_l[j] = leftelbow_position[j]
                # datas_2.append(np.reshape(data_l, -1))
                # labels_2.append(np.reshape(label_l, -1))

            count = (count + 1) % 6
        f.close()
        # datas_1.extend(datas_2)
        # labels_1.extend(labels_2)

    data_len = len(datas_1)
    batch_len = data_len // batch_size
    epoch_size = batch_len // FRAME_COUNT
    datas = np.asarray(datas_1, dtype=np.float32)
    labels = np.asarray(labels_1, dtype=np.float32)

    _datas = np.reshape(datas[0: FRAME_COUNT * epoch_size * batch_size, ...], [batch_size, epoch_size, FRAME_COUNT, 9])
    _labels = np.reshape(labels[0: FRAME_COUNT * epoch_size * batch_size, ...], [batch_size, epoch_size, FRAME_COUNT, 3])

    return _datas, _labels


