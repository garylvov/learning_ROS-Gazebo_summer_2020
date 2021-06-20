#!/usr/bin/env python
import rospy
import math
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from geometry_msgs.msg import Twist

rangeAhead = 0.0
maxRange = 0.0
minRange = 0.0
slightLeft = 0.0
slightRight = 0.0

def rangeCallback(msg):
    global rangeAhead, maxRange, minRange, slightLeft, slightRight
    rangeAhead = msg.ranges[int(len(msg.ranges)/2)]
    maxRange = max(msg.ranges)
    minRange = min(msg.ranges)
    theta = math.atan2(.125, maxRange) * 2
    slightLeft = msg.ranges[int(len(msg.ranges)/2) + int(theta)]
    slightRight = msg.ranges[int(len(msg.ranges)/2) - int(theta)]

def velocity():
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
    publ = rospy.Publisher('rangeReading', String, queue_size=10)
    velocity = Twist()
    while not rospy.is_shutdown():
        velocity.angular.z = 0
        if(slightLeft > slightRight):
            if (slightLeft < maxRange and maxRange< slightLeft+.1):
                velocity.angular.z = -.1
        else:
            if (slightRight < maxRange and maxRange < slightRight +.1):
                velocity.angular.z = .1
        if not (minRange < .25):
            velocity.linear.x = .1
        pub.publish(velocity)

if __name__ == '__main__':
    rospy.init_node('testRangerRead')
    rangeSub = rospy.Subscriber('/base_scan', LaserScan, rangeCallback)
    velocity()
