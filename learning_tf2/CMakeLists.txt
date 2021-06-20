cmake_minimum_required(VERSION 3.0.2)
project(learning_tf2)

find_package(catkin REQUIRED COMPONENTS
  rospy
  tf2
  tf2_ros
  turtlesim
)

catkin_package()

include_directories(${catkin_INCLUDE_DIRS})
