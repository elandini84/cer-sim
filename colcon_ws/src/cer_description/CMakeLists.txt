cmake_minimum_required(VERSION 3.10.2)
project(cer_description)

find_package(ament_cmake REQUIRED)

ament_package()

install(DIRECTORY ../../../R1-SIM_urdf DESTINATION share/${PROJECT_NAME}/urdf/R1-SIM_urdf)
install(DIRECTORY ../../../R1SN00x_urdf DESTINATION share/${PROJECT_NAME}/urdf)