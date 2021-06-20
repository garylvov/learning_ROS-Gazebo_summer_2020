#!/usr/bin/env python
import rospy
import turtlesim.srv
import random

def createTurtle(name):
    rospy.wait_for_service('spawn')
    create= rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    randomX = round(random.uniform(1,10), 1)
    randomY = round(random.uniform(1,10), 1)
    randomTheta = round(random.uniform(0,6), 1)
    create(randomX, randomY, randomTheta, name)

if __name__ == '__main__':
    rospy.init_node('createFeild')
    createTurtle('missile1')
    createTurtle('missile2')
    createTurtle('missile3')
