#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

rangeAhead = 0
maxRange = 0
minRange = 0
right = 0
left = 0

def rangeCallback(msg):
    global rangeAhead, maxRange, minRange, left, right
    rangeAhead = msg.ranges[int(len(msg.ranges) / 2)]
    maxRange = max(msg.ranges)
    minRange = min(msg.ranges)
    right = msg.ranges[0]
    left = msg.ranges[len(msg.ranges) - 1]

def botHandler():
    pub = rospy.Publisher('hokuyobot/cmd_vel', Twist, queue_size = 10 )
    vel = Twist()
    while not (rospy.is_shutdown()):

        if(minRange != 0 and minRange < .45):
            if(left < right):
                vel.angular.z = 2/minRange
            else:
                vel.angular.z = -2/minRange
        else:
            vel.angular.z = 0
        vel.linear.x = rangeAhead * .75
        pub.publish(vel)

if __name__ == '__main__':
    rospy.init_node('Navigate')
    rangeSub = rospy.Subscriber('hokuyobot/laser/scan', LaserScan, rangeCallback)
    botHandler()
