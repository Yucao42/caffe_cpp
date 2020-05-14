cmake_minimum_required(VERSION 2.8)
project(myProject)

set(CMAKE_PREFIX_PATH ${PROJECT_SOURCE_DIR}/cmake/Modules)

find_package(OpenCV REQUIRED)
find_package(Caffe REQUIRED)
include_directories(${Caffe_INCLUDE_DIRS} )
link_directories(${Caffe_LINK_DIRECTORIES})
message(STATUS ${Caffe_INCLUDE_DIRS})
message(STATUS ${Caffe_LINK_DIRECTORIES})
message(STATUS ${OpenCV_LIBS})
add_executable(myProject classification.cpp)
target_compile_definitions(myProject PRIVATE USE_OPENCV=1)
target_link_libraries(myProject ${OpenCV_LIBS} ${Caffe_LIBRARIES} )