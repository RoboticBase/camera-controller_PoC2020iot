#!/usr/bin/python
# -*- coding: utf-8 -*-
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def callback(msg):
    frame = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
    height, width, channels = frame.shape[:3]
    cv2.line(frame, (0, int(height/4)), (width, int(height/4)), (255, 0, 0))
    cv2.line(frame, (0, int(height/2)), (width, int(height/2)), (255, 0, 0))
    cv2.line(frame, (0, int(height/4*3)), (width, int(height/4*3)), (255, 0, 0))
    cv2.line(frame, (int(width/4), 0), (int(width/4), height), (255, 0, 0))
    cv2.line(frame, (int(width/2), 0), (int(width/2), height), (255, 0, 0))
    cv2.line(frame, (int(width/4*3), 0), (int(width/4*3), height), (255, 0, 0))
    dst = cv2.undistort(frame, intrinsic, distortion)
    image_message = bridge.cv2_to_imgmsg(dst, encoding="bgr8")
    pub.publish(image_message)

def main():
    try:
        rospy.init_node(NODE_NAME)
        rospy.Subscriber("image_raw", Image, callback, queue_size=10)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    try:
        NODE_NAME = 'center_line'
        bridge = CvBridge()
        pub = rospy.Publisher("/AR/center_line", Image, queue_size=10)
        fs = cv2.FileStorage(rospy.get_param("calibration_path"), cv2.FILE_STORAGE_READ)
        intrinsic = fs.getNode("intrinsic").mat()
        distortion = fs.getNode("distortion").mat()
        main()
    except KeyboardInterrupt:
        pass
