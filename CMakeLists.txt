cmake_minimum_required(VERSION 2.8)
project(caffe_classification)

set(CMAKE_PREFIX_PATH ${PROJECT_SOURCE_DIR}/cmake/Modules)
list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake/Modules)

find_package(OpenCV REQUIRED)
find_package(GFlags REQUIRED)
find_package(Glog REQUIRED)
find_package(Caffe REQUIRED)
find_package(yaml-cpp REQUIRED)

include_directories(${Caffe_INCLUDE_DIRS} $ENV{LOCAL}/usr/local/include $ENV{CONDAPATH}/envs/vas/include)
link_directories(${Caffe_LINK_DIRECTORIES} $ENV{CONDAPATH}/envs/vas/lib)
add_executable(caffe_classification classification.cpp)
target_compile_definitions(caffe_classification PRIVATE USE_OPENCV=1)
target_link_libraries(caffe_classification ${OpenCV_LIBS} ${Caffe_LIBRARIES} )

link_directories(${Caffe_LINK_DIRECTORIES} $ENV{CONDAPATH}/envs/vas/lib)
add_executable(ssd_detector ssd_detect.cpp)
target_compile_definitions(ssd_detector PRIVATE USE_OPENCV=1)
target_link_libraries(ssd_detector ${OpenCV_LIBS} ${Caffe_LIBRARIES} ${GLOG_LIBRARY} glog gflags yaml-cpp)
