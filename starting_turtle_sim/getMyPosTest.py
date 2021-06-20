import rospy
from turtlesim.msg import Pose
from std_msgs.msg import String
from geometry_msgs.msg import Twist
#coords of turtle 1
myX = 0.0
myY = 0.0
myTheta = 0.0

#initializes node and subscribes 
def nodes():
        rospy.init_node('readPOS', anonymous=True)
        getSelfPose = rospy.Subscriber('turtle1/pose', Pose, getMyPose)
        
#Callback funciton to update coords         
def getMyPose(myPose):
    global myX, myY, myTheta
    myX = myPose.x
    myY= myPose.y
    myTheta = myPose.theta
#Prints and publishes coords to ensure it is working correctly
def checkPose():
    pub = rospy.Publisher('myPOS', String, queue_size=10)
    rate = rospy.Rate(1) #1 hz
    while not rospy.is_shutdown():
        output = "X Coord: "+str(myX)+" Y Coord: "+str(myY)+" Theta Orentation: "+str(myTheta)
        rospy.loginfo(output)
        pub.publish(output)
        rate.sleep()

if __name__ == '__main__':
    try:
        nodes()
        checkPose()
    except rospy.ROSInterruptException:
        pass
