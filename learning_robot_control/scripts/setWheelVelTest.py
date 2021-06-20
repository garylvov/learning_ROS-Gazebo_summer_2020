#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import Float64
import threading

def setVel(name, velocity, duration):
    pubName = '/kinectbotWithCaster/'+name+'_velocity_controller/command'
    pub = rospy.Publisher(pubName, Float64, queue_size=10)
    t0 = time.time()
    elapsedTime = 0
    while(elapsedTime < duration):
        pub.publish(velocity)
        elapsedTime = time.time() - t0
    pub.publish(0)

if __name__ == '__main__':
    rospy.init_node('setVelocities')
    rightFrontWheel = threading.Thread(target = setVel,args = ('rightFrontWheel',5,1))
    leftFrontWheel = threading.Thread(target = setVel,args = ('leftFrontWheel',-5,1))
    leftFrontWheel.start()
    rightFrontWheel.start()
