import rospy
import turtlesim.srv

#removes the turtle goalTurtle: must first be created to be removed
def removeTurtle():
    goalTurtle = rospy.ServiceProxy('kill', turtlesim.srv.Kill)
    goalTurtle('goalTurtle')

if __name__ == '__main__':
    try:
        removeTurtle()
    except rospy.ROSInterruptException:
        pass
