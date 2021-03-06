#!/usr/bin/python
# -*- coding: utf-8 -*-
import rospy
import numpy as np
from geometry_msgs.msg import PoseStamped
from ar_func import read_csv2, quaternion_to_vector, PoseStamped_to_Numpyarray, estimate

def common(translate_matrix, inputTQ):
    Est_Quat, Est_pos = estimate(translate_matrix, inputTQ)
    p = PoseStamped()
    p.header.frame_id = "map"
    p.header.stamp = rospy.Time.now()
    p.pose.position.x = Est_pos[0]
    p.pose.position.y = Est_pos[1]
    p.pose.position.z = Est_pos[2]
    p.pose.orientation.x = Est_Quat[0]
    p.pose.orientation.y = Est_Quat[1]
    p.pose.orientation.z = Est_Quat[2]
    p.pose.orientation.w = Est_Quat[3]
    return p

def callback(msg, args):
    _, _, inputTQ = PoseStamped_to_Numpyarray(msg)
    translate_matrix = args
    p = common(translate_matrix, inputTQ)
    pub.publish(p)

def callback2(msg, args):
    _, _, inputTQ = PoseStamped_to_Numpyarray(msg)
    translate_matrix = args
    p = common(translate_matrix, inputTQ)
    pub2.publish(p)

def main():
    try:
        rospy.init_node(NODE_NAME)
        rospy.Subscriber("/AR/estimated_pose", PoseStamped, callback, reverse_matrix, queue_size=10)
        rospy.Subscriber("/RB/confution_pose", PoseStamped, callback2, reverse_matrix, queue_size=10)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    try:
        NODE_NAME = 'demo'
        pose_dir = rospy.get_param("matrix_path")
        pose_file = pose_dir + "tmatrix_f_rb.csv"
        tmatrix = read_csv2(pose_file)
        translate_matrix = tmatrix.astype(np.float32)
        rospy.loginfo(translate_matrix)
        reverse_matrix = np.linalg.inv(translate_matrix)
        rospy.loginfo(reverse_matrix)
        rospy.loginfo(np.dot(translate_matrix, reverse_matrix))
        pub = rospy.Publisher("/AR/demo_pose", PoseStamped, queue_size=10)
        pub2 = rospy.Publisher("/RB/demo_pose", PoseStamped, queue_size=10)
        main()

    except KeyboardInterrupt:
        pass
