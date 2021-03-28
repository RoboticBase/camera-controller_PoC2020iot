#!/usr/bin/env python
import rospy
import tf
from std_msgs.msg import Float32
from geometry_msgs.msg import Point, Quaternion

def main():
    rospy.init_node(NODE_NAME, anonymous=True)
    rospy.loginfo("Publish to the confution_pose %s", rospy.Time.now())
    error_direction = rospy.get_param('~direction')
    error_value = rospy.get_param('~value')
    type_list = [ "position", "orientation" ]
    dir_list = ["x", "y", "z", "w"]
    if not error_direction in dir_list:
        rospy.logerr('the direction is selected form "x", "y", "z", "o":%s ', error_direction)
        exit()
    rospy.loginfo('error direction is :%s ,the value is :%s', error_direction, error_value)
    r = rospy.Rate(1) # 1hz
    while not rospy.is_shutdown():
        if error_direction == "w":
            error_deg.data += error_value
            pub_deg.publish(error_deg)
            rospy.loginfo(error_deg)
        else:
            if error_direction == "x":
                error_pose.x += error_value
            if error_direction == "y":
                error_pose.y += error_value
            if error_direction == "z":
                error_pose.z += error_value
            pub_pose.publish(error_pose)
        r.sleep()

if __name__ == '__main__':
    try:
        NODE_NAME = 'error_pose_generator'
        pub_pose = rospy.Publisher("/RB/confution_pose/position", Point, queue_size=10)
        pub_ori = rospy.Publisher("/RB/confution_pose/orientation", Quaternion, queue_size=10)
        pub_deg = rospy.Publisher("/RB/confution_pose/degree", Float32, queue_size=10)
        error_pose = Point()
        error_quat = Quaternion()
        error_quat.w = 1.0
        error_deg = Float32()
        main()
    except rospy.ROSInterruptException: 
        pass