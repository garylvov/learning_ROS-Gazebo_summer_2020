#!/usr/bin/env python
import rospy
import tf_conversions
import tf2_ros
import geometry_msgs.msg
import turtlesim.msg

def sendtf(msg, turtleName):
        broadcaster = tf2_ros.TransformBroadcaster()
        t = geometry_msgs.msg.TransformStamped()
        t.header.stamp = rospy.Time.now()
        t.header.frame_id = "world"
        t.child_frame_id = turtleName
        t.transform.translation.x = msg.x
        t.transform.translation.y = msg.y
        t.transform.translation.z = 0.0
        q = tf_conversions.transformations.quaternion_from_euler(0, 0, msg.theta)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]
        broadcaster.sendTransform(t)

if __name__ == '__main__':
    rospy.init_node('test')
    listOfTurtles = ['turtle1', 'missile1', 'missile2', 'missile3', 'asteroid1', 'asteroid2', 'asteroid3', 'asteroid4']
    
    for turtle in listOfTurtles:
        rospy.Subscriber('/%s/pose' % turtle, turtlesim.msg.Pose, sendtf, turtle)
    rospy.spin()
