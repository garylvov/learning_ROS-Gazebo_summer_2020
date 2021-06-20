#This code has a mild bug:
#When traveling left horizontally turtle is erratic
import rospy
import random
import math
import time
import turtlesim.srv
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
#sets coords of turtle1 and goal turtle
myX = 0.0
myY = 0.0
myTheta = 0.0

goalX = 0.0
goalY = 0.0
goalTheta = 0.0

#creates goalTurtle when called at random coords
def createGoalTurtle():
    global goalX, goalY
    goalTurtle = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    goalX = round(random.uniform(1,10), 3)
    goalY = round(random.uniform(1,10), 3)
    goalTheta = round(random.uniform(0,6.3), 3) #6.3 is used as an approximation of 2pi
    goalTurtle(goalX, goalY, goalTheta, 'goalTurtle')
    
#removes goalTurtle when called
def removeTurtle():
    goalTurtle = rospy.ServiceProxy('kill', turtlesim.srv.Kill)
    goalTurtle('goalTurtle')

#callback function to get position
def getMyPos(myPos):
    global myX, myY, myTheta
    myX = myPos.x
    myY= myPos.y
    myTheta = myPos.theta
    
#sets velocity of turtle1
def velocity():
    #Defines velocity angle and sets it to zero
    myVel = Twist()
    myVel.linear.x = 0
    myVel.angular.y = 0
    setVelocity.publish(myVel)
    while not rospy.is_shutdown():
        #x and y components of distance
        xAxis = goalX - myX
        yAxis = goalY - myY
        #calculation of distance between turtles and angle needed for turtle1 to face goalTurtle
        distance = abs(((xAxis**2) + (yAxis**2))**.5)
        relativeAngle = (math.atan2(yAxis, xAxis)-myTheta)
        #turns to face goalTurtle first
        if(-.05 > relativeAngle or relativeAngle > .05):
            myVel.linear.x = distance / 4
            myVel.angular.z = relativeAngle * 5
            if(abs(relativeAngle) > math.pi): #turns in most efficent direction
                myVel.angular.z = (math.pi - relativeAngle) * 5
            setVelocity.publish(myVel)
        myVel.angular.z = 0
        #when facing goalTurtle goes to collide
        if((-.05 < relativeAngle and relativeAngle < .05)):
            myVel.linear.x = distance * 4
            setVelocity.publish(myVel)
        #on collision deletes and respawns turtle
        if(distance < .4):
            removeTurtle()
            createGoalTurtle()

if __name__ == '__main__':
    try:
        createGoalTurtle()
        #initiates node which subscribes to turtle1's pose and publishes to it's velocity
        rospy.init_node('goToGoalTurtleV3', anonymous=False)
        getSelfPose = rospy.Subscriber('turtle1/pose', Pose, getMyPos)
        setVelocity = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size = 10)
        rate = rospy.Rate(10)
        velocity()
    except rospy.ROSInterruptException:
        pass
