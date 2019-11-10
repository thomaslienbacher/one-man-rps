cmake_minimum_required(VERSION 3.14)
project(videostreaming)

set(CMAKE_CXX_STANDARD 17)

add_executable(videostreaming main.cpp)

find_package(OpenCV REQUIRED)
target_link_libraries(videostreaming ${OpenCV_LIBS})
target_link_libraries(videostreaming libssh)
