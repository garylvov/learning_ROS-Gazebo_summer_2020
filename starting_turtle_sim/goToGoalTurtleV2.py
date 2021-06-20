#This code has two mild bugs:
#When traveling left horizontally turtle is erratic
#Turtles are spawned more than once, deleted, and spawned again when they should only be spawned once
#wait statement on line 28 mostly patches second bug
import rospy
import random
import math
import time
import turtlesim.srv
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
#defines coords of goalTurtle and turtle1
myX = 0.0
myY = 0.0
myTheta = 0.0

goalX = 0.0
goalY = 0.0
goalTheta = 0.0
#creates goalTurtle at random coords
def createGoalTurtle():
    global goalX, goalY
    goalTurtle = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    goalX = round(random.uniform(1,10), 3)
    goalY = round(random.uniform(1,10), 3)
    goalTheta = round(random.uniform(0,6.3), 3) #6.3 is used as an approximation of 2pi
    goalTurtle(goalX, goalY, goalTheta, 'goalTurtle')
    time.sleep(.75)
    
#Removes goalTurtle 
def removeTurtle():
    goalTurtle = rospy.ServiceProxy('kill', turtlesim.srv.Kill)
    goalTurtle('goalTurtle')
    
#Callback function to update coords of turtle1
def getMyPose(myPos):
    global myX, myY, myTheta
    myX = myPos.x
    myY= myPos.y
    myTheta = myPos.theta
    
#Callback function to update coords of goalTurtle
def getGoalPose(goalPos):
    global goalX, goalY, goalTheta
    goalX = goalPos.x
    goalY= goalPos.y
    goalTheta = goalPos.theta
    
#sets velocity of turtle1
def velocity():
    #sets variable type as velocity and sets to zero
    myVel = Twist()
    myVel.linear.x = 0
    myVel.angular.y = 0
    setVelocity.publish(myVel)
    #infinite loop
    while not rospy.is_shutdown():
        #x and y components of distance
        xAxis = goalX - myX
        yAxis = goalY - myY
        #calulates distance and angle need to turn for turtle1
        distance = abs(((xAxis**2) + (yAxis**2))**.5)
        relativeAngle = (math.atan2(yAxis, xAxis)-myTheta)
        #turtle1 turns to face goalTurtle first PID control
        if(-.05 > relativeAngle or relativeAngle > .05):
            myVel.linear.x = distance / 10
            myVel.angular.z = relativeAngle * 4
            #Sets the rotation into the right direction
            if(abs(relativeAngle) > math.pi):
                myVel.angular.z = (math.pi - relativeAngle) * 4
            setVelocity.publish(myVel)
        #once properly turned goes to goal PID control
        if((-.05 < relativeAngle and relativeAngle < .05)):
            myVel.linear.x = distance * 3
            myVel.angular.z = 0
            setVelocity.publish(myVel)
        #collision detection
        if(distance < .4):
            removeTurtle()
            createGoalTurtle()
            velocity()

if __name__ == '__main__':
    try:
        createGoalTurtle()
        #initiates node that subscribes to both turtle's position, and publishes to one turtles velocity
        rospy.init_node('goToGoalTurtleV2', anonymous=False)
        getSelfPose = rospy.Subscriber('turtle1/pose', Pose, getMyPose)
        goalPose = rospy.Subscriber('goalTurtle/pose', Pose, getGoalPose)
        setVelocity = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size = 10)
        rate = rospy.Rate(10)
        velocity()
    except rospy.ROSInterruptException:
        pass
