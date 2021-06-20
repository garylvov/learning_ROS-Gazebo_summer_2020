import rospy
import random
import turtlesim.srv
from std_msgs.msg import String


goalTheta = 0.0
goalX = 0.0
goalY = 0.0

#creates goal turtle at random coords
def createGoalTurtle():
    global goalX, goalY, goalTheta
    goalTurtle = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    goalX = round(random.uniform(1,10), 1)
    goalY = round(random.uniform(1,10), 1)
    goalTheta = round(random.uniform(0,6), 1)
    goalTurtle(goalX, goalY, goalTheta, 'goalTurtle')

#Prints coordinates to the console and log to ensure code is working properly
def checkGlobalVariables():
    pub = rospy.Publisher('globalVars', String, queue_size=10)
    rospy.init_node('GoalTurtlePos', anonymous=True)
    rate = rospy.Rate(1) #1 hz
    while not rospy.is_shutdown():
        output = str(goalX)+" "+str(goalY)+" "+str(goalTheta)
        rospy.loginfo(output)
        pub.publish(output)
        rate.sleep()

if __name__ == '__main__':
    try:
        createGoalTurtle()
        checkGlobalVariables()
    except rospy.ROSInterruptException:
     
