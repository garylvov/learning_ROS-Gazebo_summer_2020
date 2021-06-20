cmake_minimum_required(VERSION 3.0.2)
project(learning_robot_control)

find_package(catkin REQUIRED COMPONENTS
  controller_manager
  joint_state_controller
  robot_state_publisher
)

catkin_package()

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)
