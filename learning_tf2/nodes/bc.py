#!/usr/bin/env python
#defunct, replaced by bcOptimized.py 
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
    rospy.init_node('tf2TurtleBroadcaster')
    turtleName = rospy.get_param('~turtle')
    rospy.Subscriber('/%s/pose' % turtleName,
                     turtlesim.msg.Pose,
                     sendtf,
                     turtleName)
    rospy.spin()

#WITH UNOPTIMIZED BROADCASTER THESE LINES ARE NEEDED IN THE LAUNCH FILE

'''
    <node name="turtle1_tf2_Broadcaster" pkg="learning_tf2" type="bc.py" respawn="false" output="screen">
      <param name="turtle" type="string" value="turtle1" />
    </node>

    <node name="asteroid1_tf2_Broadcaster" pkg="learning_tf2" type="bc.py" respawn="false" output="screen">
      <param name="turtle" type="string" value="asteroid1" />
    </node>

    <node name="asteroid2_tf2_Broadcaster" pkg="learning_tf2" type="bc.py" respawn="false" output="screen">
      <param name="turtle" type="string" value="asteroid2" />
    </node>

    <node name="asteroid3_TF2_Broadcaster" pkg="learning_tf2" type="bc.py" respawn="false" output="screen">
      <param name="turtle" type="string" value="asteroid3" />
    </node>

    <node name="asteroid4_TF2_Broadcaster" pkg="learning_tf2" type="bc.py" respawn="false" output="screen">
      <param name="turtle" type="string" value="asteroid4" />
    </node>

    <node name="missile1_TF2_Broadcaster" pkg="learning_tf2" type="bc.py" respawn="false" output="screen">
      <param name="turtle" type="string" value="missile1" />
    </node>

    <node name="missile2_TF2_Broadcaster" pkg="learning_tf2" type="bc.py" respawn="false" output="screen">
      <param name="turtle" type="string" value="missile2" />
    </node>

    <node name="missile3_TF2_Broadcaster" pkg="learning_tf2" type="bc.py" respawn="false" output="screen">
      <param name="turtle" type="string" value="missile3" />
    </node>
'''
