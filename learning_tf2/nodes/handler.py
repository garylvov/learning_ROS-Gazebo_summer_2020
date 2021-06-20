#!/usr/bin/env python
import rospy
import math
import tf2_ros
import geometry_msgs.msg
import turtlesim.srv
import threading

def interpert(name, speed):
    infoDelay = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(infoDelay)
    missileVel = rospy.Publisher('%s/cmd_vel' % name, geometry_msgs.msg.Twist, queue_size = 10)
    rate = rospy.Rate(10)
    missile = geometry_msgs.msg.Twist()
    turtleExists = True
    while turtleExists and not rospy.is_shutdown():
        try:
            relative = infoDelay.lookup_transform(name, 'turtle1', rospy.Time())
        except(tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rate.sleep()
            continue

        missile.angular.z =  4 * math.atan2(relative.transform.translation.y, relative.transform.translation.x)
        missile.linear.x = speed * math.sqrt(relative.transform.translation.x ** 2 + relative.transform.translation.y ** 2)
        missileVel.publish(missile)

        if(.5 > (math.sqrt(relative.transform.translation.x ** 2 + relative.transform.translation.y ** 2))):
            rospy.wait_for_service('kill')
            remove = rospy.ServiceProxy('kill', turtlesim.srv.Kill)
            remove('turtle1')
            turtleExists = False

if __name__ == '__main__':
    rospy.init_node('handleTurtles')

    missile1 = threading.Thread(target = interpert, kwargs = dict(name = 'missile1', speed = .7))
    missile1.start()
    missile2 = threading.Thread(target = interpert, kwargs = dict(name = 'missile2', speed = .5))
    missile2.start()
    missile3 = threading.Thread(target = interpert, kwargs = dict(name = 'missile3', speed = .3))
    missile3.start()
