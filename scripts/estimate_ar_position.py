#!/usr/bin/python
# -*- coding: utf-8 -*-
import rospy
import csv
import numpy as np
from geometry_msgs.msg import PoseStamped
from ar_func import PoseStamped_to_Numpyarray, estimate

def callback(msg, args):
    inputTvec, inputQuat, inputTQ = PoseStamped_to_Numpyarray(msg)
    translate_matrix = args
    Est_Quat, Est_pos = estimate(translate_matrix, inputTQ)
    p = PoseStamped()
    p.header.frame_id = "estimate"
    p.header.stamp = rospy.Time.now()
    p.pose.position.x = Est_pos[0]
    p.pose.position.y = Est_pos[1]
    p.pose.position.z = Est_pos[2]
    p.pose.orientation.x = Est_Quat[0]
    p.pose.orientation.y = Est_Quat[1]
    p.pose.orientation.z = Est_Quat[2]
    p.pose.orientation.w = Est_Quat[3]
    pub.publish(p)

def main():
    try:
        rospy.init_node(NODE_NAME)
        rospy.Subscriber("/AR/camera_pose", PoseStamped, callback, translate_matrix, queue_size=10)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    try:
        NODE_NAME = 'estimate_ar_position'
        file_path = rospy.get_param("matrix_path")
        pose_file = file_path + "tmatrix_f_ar.csv"
        rospy.loginfo("READED tMatrix from ", pose_file)
        csv_obj = csv.reader(open(pose_file, "r"))
        l = [row for row in csv_obj]
        tmatrix = np.array(l)
        translate_matrix = tmatrix.astype(np.float32)
        pub = rospy.Publisher("/AR/estimated_pose", PoseStamped, queue_size=10)
        main()

    except KeyboardInterrupt:
        pass
