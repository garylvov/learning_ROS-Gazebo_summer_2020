#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String

rangeAhead = 0.0

def rangeCallback(msg):
    global rangeAhead
    rangeAhead = msg.ranges[int(len(msg.ranges)/2)]

def checkScan():
    pub = rospy.Publisher('rangeReading', String, queue_size=10)
    rate = rospy.Rate(1) #1 hz
    while not rospy.is_shutdown():
        output = "Range Ahead:" + str(rangeAhead)
        rospy.loginfo(output)
        pub.publish(output)
        rate.sleep()

if __name__ == '__main__':
    rospy.init_node('testRangerRead')
    rangeSub = rospy.Subscriber('/base_scan', LaserScan, rangeCallback)
    checkScan()
