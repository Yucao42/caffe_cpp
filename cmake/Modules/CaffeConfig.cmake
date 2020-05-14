# Config file for the Caffe package.
#
# Note:
#   Caffe and this config file depends on opencv,
#   so put `find_package(OpenCV)` before searching Caffe
#   via `find_package(Caffe)`. All other lib/includes
#   dependencies are hard coded in the file
#
# After successful configuration the following variables
# will be defined:
#
#   Caffe_LIBRARIES    - IMPORTED targets to link against
#                        (There is no Caffe_INCLUDE_DIRS and Caffe_DEFINITIONS
#                         because they are specified in the IMPORTED target interface.)
#
#   Caffe_HAVE_CUDA    - signals about CUDA support
#   Caffe_HAVE_CUDNN   - signals about cuDNN support


# OpenCV dependency (optional)

if(ON)
  if(NOT OpenCV_FOUND)
    set(Caffe_OpenCV_CONFIG_PATH "@OpenCV_CONFIG_PATH@")
    if(Caffe_OpenCV_CONFIG_PATH)
      get_filename_component(Caffe_OpenCV_CONFIG_PATH ${Caffe_OpenCV_CONFIG_PATH} ABSOLUTE)

      if(EXISTS ${Caffe_OpenCV_CONFIG_PATH} AND NOT TARGET opencv_core)
        message(STATUS "Caffe: using OpenCV config from ${Caffe_OpenCV_CONFIG_PATH}")
	include(${Caffe_OpenCV_CONFIG_PATH}/OpenCVConfig.cmake)
      endif()

    else()
      find_package(OpenCV REQUIRED)
    endif()
    unset(Caffe_OpenCV_CONFIG_PATH)
  endif()
endif()

# Compute paths
set(Caffe_DEFINITIONS "-DUSE_OPENCV;-DUSE_LMDB;-DUSE_LEVELDB")
get_filename_component(Caffe_CMAKE_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)
message(STATUS "Caffe cmake dir ${Caffe_CMAKE_DIR}")
set(Caffe_INCLUDE_DIRS 
    /usr/include
    /usr/local/cuda/include
    /usr/include/opencv
    /usr/include/openblas
    $ENV{CAFFEPATH}/include
    $ENV{CAFFEPATH}/build/src
    )

# List of IMPORTED libs created by CaffeTargets.cmake
# These targets already specify all needed definitions and include pathes
set(Caffe_LINK_DIRECTORIES $ENV{CAFFEPATH}/build/lib 
    $ENV{CONDAPATH}/lib)
set(Caffe_LIBRARIES glog boost_system caffe )

set(Caffe_CPU_ONLY OFF)
set(Caffe_HAVE_CUDA TRUE)
set(Caffe_HAVE_CUDNN FALSE)
