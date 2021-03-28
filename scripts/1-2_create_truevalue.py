# -*- coding: utf-8 -*-
import csv
import numpy as np
from tf.transformations import quaternion_from_euler
import tf
import math
from ar_func import degrees_to_quaternions, matrix_to_csv

def main():
    output = '/home/minipc1/camera_ws/src/camera-controller/config/source_position/Pose_2020-12-11_162050/floor.csv'
    num = np.array(range(3)).reshape(-1, 1)
    point0 = [ 0, -1,0,0,0,  0]
    point1 = [ 1, 1,0,0,0, 90]
    point2 = [-1, 1,0,0,0, 180]
    true_val = np.array([point0, point1, point2])
    true_dir = true_val[:,0:3].astype(np.float32)
    true_ori = true_val[:,3:7].astype(np.float32)
    true_quat = degrees_to_quaternions(true_ori)
    C = np.hstack((num, true_dir))
    C = np.hstack((C, true_quat))
    buf = matrix_to_csv(C)
    with open(output, mode='w') as f:
        f.write(buf)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
