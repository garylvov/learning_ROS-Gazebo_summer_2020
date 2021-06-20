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
left = 0.0
right = 0.0

def rangeCallback(msg):
    global rangeAhead, maxRange, minRange, slightLeft, slightRight, left, right
    rangeAhead = msg.ranges[int(len(msg.ranges)/2)]
    maxRange = max(msg.ranges)
    minRange = min(msg.ranges)
    theta = abs(math.atan2(.125, maxRange)* 2)
    slightLeft = msg.ranges[int(len(msg.ranges)/2) + int(theta)]
    slightRight = msg.ranges[int(len(msg.ranges)/2) - int(theta)]
    left = msg.ranges[len(msg.ranges)-1]
    right = msg.ranges[0]

def velocity():
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
    publ = rospy.Publisher('rangeReading', String, queue_size=10)
    blockVelocity = Twist()

    while not rospy.is_shutdown():
        blockVelocity.angular.z *= .5
        blockVelocity.angular.x *= .5
        pub.publish(blockVelocity)
        if(slightLeft > slightRight):
            if (slightLeft < rangeAhead and rangeAhead < slightLeft+.05):
                blockVelocity.angular.z = -.1
        else:
            if (slightRight < rangeAhead and rangeAhead < slightRight +.05):
                blockVelocity.angular.z = .1


        if (minRange > .25):
            blockVelocity.linear.x = .1
            blockVelocity.angular.z = 0
        else:
            blockVelocity.linear.x = 0
            blockVelocity.angular.z = -.25
            if(left>right):
                blockVelocity.angular.z = .25
        pub.publish(blockVelocity)

if __name__ == '__main__':
    rospy.init_node('navCircle')
    rangeSub = rospy.Subscriber('/base_scan', LaserScan, rangeCallback)
    velocity()
