# -*- coding: utf-8 -*-
import csv
import cv2
import numpy as np
from tf.transformations import quaternion_from_matrix, euler_from_matrix, quaternion_from_euler, quaternion_matrix
import math
from ar_func import read_csv2, matrix_to_csv, get_translate_matrix
from ar_func import estimate

def array1_csv(arr):
    buf = ""
    for n in arr:
        buf = buf + str(n) + " ,"
    buf = buf[:-2]
    return buf    

def title_pose(str1):
    buf = str1 + "_x" + " ,"
    buf = buf + str1 + "_y" + " ,"
    buf = buf + str1 + "_z" + " ,"
    buf = buf + str1 + "_qx" + " ,"
    buf = buf + str1 + "_qy" + " ,"
    buf = buf + str1 + "_qz" + " ,"
    buf = buf + str1 + "_qw" + " ,"
    return buf

def title_diff(str1, str2):
    buf = str1 + "-" + str2 + "_x" + " ,"
    buf = buf + str1 + "-" + str2 + "_y" + " ,"
    buf = buf + str1 + "-" + str2 + "_z" + " ,"
    buf = buf + str1 + "-" + str2 + "_roll" + " ,"
    buf = buf + str1 + "-" + str2 + "_pitch" + " ,"
    buf = buf + str1 + "-" + str2 + "_yaw" + " ,"
    return buf

def title():
    buf = ""
    buf = buf + title_pose("floor")
    buf = buf + title_pose("camera")
    buf = buf + title_pose("est_cam")
    buf = buf + title_pose("robot")
    buf = buf + title_pose("est_robot")
    buf = buf + title_diff("est_cam", "floor")
    buf = buf + title_diff("est_robot", "floor")
    buf = buf + title_diff("robot", "floor")
    buf = buf + title_diff("est_cam", "robot")
    buf = buf[:-2]
    buf = buf + "\n"
    return buf

def title_ar():
    buf = ""
    buf = buf + title_pose("floor")
    buf = buf + title_pose("camera")
    buf = buf + title_pose("est_cam")
    buf = buf + title_diff("est_cam", "floor")
    buf = buf[:-2]
    buf = buf + "\n"
    return buf

def title_rb():
    buf = ""
    buf = buf + title_pose("floor")
    buf = buf + title_pose("robot")
    buf = buf + title_pose("est_rb")
    buf = buf + title_diff("est_rb", "floor")
    buf = buf[:-2]
    buf = buf + "\n"
    return buf

def title_difference():
    buf = ""
    buf = buf + title_pose("floor")
    buf = buf + title_pose("est_cam")
    buf = buf + title_pose("est_rb")
    buf = buf + title_diff("est_cam", "est_rb")
    buf = buf[:-2]
    buf = buf + "\n"
    return buf

def main():
    path = '/home/minipc1/camera_ws/src/camera-controller/config/source_position/Pose_2020-12-11_162050/'
    #source_list = [1, 4, 6]
    #source_list = [0, 2, 4]
    #source_list = [14, 20, 24]
    source_list = [0, 1, 2]#[12, 16, 22]#
    
    ar_path = path + 'ar.csv'
    floor_path = path + 'floor.csv'
    rb_path = path + 'pose.csv'
    result_path = path + 'result_deference.csv'
    result_ar = path + 'result_ar.csv'
    result_rb = path + 'result_rb.csv'
    result_dif = path + 'result_diff.csv'
    tmatrix_f_ar = path + 'tmatrix_f_ar.csv'
    tmatrix_f_rb = path + 'tmatrix_f_rb.csv'
    ar = read_csv2(ar_path)
    floor = read_csv2(floor_path)
    rb = read_csv2(rb_path)
    ar = ar[:,1:].astype(np.float32)
    ar_source = ar[source_list]
    floor = floor[:,1:].astype(np.float32)
    floor_source = floor[source_list]
    rb = rb[:,1:].astype(np.float32)
    rb_source = rb[source_list]

    tmatrix_ar_floor = get_translate_matrix(floor_source, ar_source)
    buf = matrix_to_csv(tmatrix_ar_floor)
    with open(tmatrix_f_ar, mode='w') as f:
        f.write(buf)
    tmatrix_rb_floor = get_translate_matrix(floor_source, rb_source)
    buf = matrix_to_csv(tmatrix_rb_floor)
    with open(tmatrix_f_rb, mode='w') as f:
        f.write(buf)

    ar_buf = title_ar()
    rb_buf = title_rb()
    diff_buf = title_difference()
    print(diff_buf)
    buf = title()
    for (floor_pose, ar_pose, rb_pose) in zip(floor, ar, rb):
        floor_R = quaternion_matrix(floor_pose[3:].astype(np.float32))[:3,:3]

        est_ar_quat, est_ar_pos = estimate(tmatrix_ar_floor, ar_pose)
        diff_est_ar_floor = est_ar_pos - floor_pose[:3].astype(np.float32)
        est_ar_R = quaternion_matrix(est_ar_quat)[:3,:3]
        diff_R_est_ar_floor = np.dot(np.linalg.inv(floor_R), est_ar_R)
        diff_rad_est_ar_floor = euler_from_matrix(diff_R_est_ar_floor)
        ar_buf = ar_buf + array1_csv(floor_pose) + " ,"
        ar_buf = ar_buf + array1_csv(ar_pose) + " ,"
        ar_buf = ar_buf + array1_csv(est_ar_pos) + " ,"
        ar_buf = ar_buf + array1_csv(est_ar_quat) + " ,"
        ar_buf = ar_buf + array1_csv(diff_est_ar_floor) + " ,"
        ar_buf = ar_buf + array1_csv(diff_rad_est_ar_floor) + "\n" 

        est_rb_quat, est_rb_pos = estimate(tmatrix_rb_floor, rb_pose)
        diff_est_rb_floor = est_rb_pos - floor_pose[:3].astype(np.float32)
        est_rb_R = quaternion_matrix(est_rb_quat)[:3,:3]
        diff_R_est_rb_floor = np.dot(np.linalg.inv(floor_R), est_rb_R)
        diff_rad_est_rb_floor = euler_from_matrix(diff_R_est_rb_floor)

        rb_buf = rb_buf + array1_csv(floor_pose) + " ,"
        rb_buf = rb_buf + array1_csv(rb_pose) + " ,"
        rb_buf = rb_buf + array1_csv(est_rb_pos) + " ,"
        rb_buf = rb_buf + array1_csv(est_rb_quat) + " ,"
        rb_buf = rb_buf + array1_csv(diff_est_rb_floor) + " ,"
        rb_buf = rb_buf + array1_csv(diff_rad_est_rb_floor) + "\n" 

        robot_R = quaternion_matrix(rb_pose[3:].astype(np.float32))[:3,:3]
        diff_est_ar_robot = est_ar_pos - rb_pose[:3].astype(np.float32)
        diff_robot_floor = rb_pose[:3].astype(np.float32) - floor_pose[:3].astype(np.float32)
        diff_R_est_ar_robot = np.dot(np.linalg.inv(robot_R), est_ar_R)
        diff_R_robot_floor = np.dot(np.linalg.inv(floor_R), robot_R)
        diff_rad_est_ar_robot = euler_from_matrix(diff_R_est_ar_robot)
        diff_rad_robot_floor = euler_from_matrix(diff_R_robot_floor)
        buf = buf + array1_csv(floor_pose) + " ,"
        buf = buf + array1_csv(ar_pose) + " ,"
        buf = buf + array1_csv(est_ar_pos) + " ,"
        buf = buf + array1_csv(est_ar_quat) + " ,"
        buf = buf + array1_csv(rb_pose) + " ,"
        buf = buf + array1_csv(est_rb_pos) + " ,"
        buf = buf + array1_csv(est_rb_quat) + " ,"
        buf = buf + array1_csv(diff_est_ar_floor) + " ,"
        buf = buf + array1_csv(diff_rad_est_ar_floor) + " ,"
        buf = buf + array1_csv(diff_est_rb_floor) + " ,"
        buf = buf + array1_csv(diff_rad_est_rb_floor) + " ,"
        buf = buf + array1_csv(diff_robot_floor) + " ,"
        buf = buf + array1_csv(diff_rad_robot_floor) + " ,"
        buf = buf + array1_csv(diff_est_ar_robot) + " ,"
        buf = buf + array1_csv(diff_rad_est_ar_robot) + "\n" 

        diff_est_ar_est_rb = est_ar_pos - est_rb_pos
        diff_R_est_ar_est_rb = np.dot(np.linalg.inv(est_rb_R), est_ar_R)
        diff_rad_est_ar_est_rb = euler_from_matrix(diff_R_est_ar_est_rb)
        diff_buf = diff_buf + array1_csv(floor_pose) + " ,"
        diff_buf = diff_buf + array1_csv(est_ar_pos) + " ,"
        diff_buf = diff_buf + array1_csv(est_ar_quat) + " ,"
        diff_buf = diff_buf + array1_csv(est_rb_pos) + " ,"
        diff_buf = diff_buf + array1_csv(est_rb_quat) + " ,"
        diff_buf = diff_buf + array1_csv(diff_est_ar_est_rb) + " ,"
        diff_buf = diff_buf + array1_csv(diff_rad_est_ar_est_rb) + "\n" 

    with open(result_ar, mode='w') as f:
        f.write(ar_buf)
    with open(result_rb, mode='w') as f:
        f.write(rb_buf)
    with open(result_path, mode='w') as f:
        f.write(buf)
    with open(result_dif, mode='w') as f:
        f.write(diff_buf)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
