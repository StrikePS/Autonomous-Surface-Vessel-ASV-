cmake_minimum_required(VERSION 3.8)
project(wave_sim_bridgeup)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(gz-transport13 REQUIRED)
find_package(gz-msgs10 REQUIRED)

add_executable(custom_gazebo_bridge src/custom_bridge.cpp)
ament_target_dependencies(custom_gazebo_bridge rclcpp sensor_msgs nav_msgs)
target_link_libraries(custom_gazebo_bridge
  gz-transport13::gz-transport13
  gz-msgs10::gz-msgs10
)

install(TARGETS custom_gazebo_bridge
  DESTINATION lib/${PROJECT_NAME})

# Install all your custom directories
install(DIRECTORY
  launch
  scripts
  config
  DESTINATION share/${PROJECT_NAME}
)

# Make the shell script executable after install
install(PROGRAMS
  scripts/gazebo_ros_bridge.sh
  DESTINATION share/${PROJECT_NAME}/scripts
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
