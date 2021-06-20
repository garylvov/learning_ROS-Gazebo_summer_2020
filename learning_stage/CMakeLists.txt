cmake_minimum_required(VERSION 3.0.2)
project(learning_stage)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  rospy
  rospy
  sensor_msgs
  std_msgs
)

catkin_package(

)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)
