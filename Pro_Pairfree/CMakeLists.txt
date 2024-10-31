cmake_minimum_required(VERSION 3.16)
project(Process)

set(CMAKE_CXX_STANDARD 11)
set(OUT_PATH ${CMAKE_CURRENT_SOURCE_DIR}/bin)
set(EXECUTABLE_OUTPUT_PATH ${OUT_PATH})


set(Openssl_INCLUDE_DIR /usr/local/openssl/include)
set(Openssl_LIB_DIR /usr/local/openssl/lib64)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)
include_directories(${Openssl_INCLUDE_DIR})
include_directories(/usr/local/include/jsoncpp)

# generate a static library
# set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/static)
# add_library(cls STATIC 
#             cls_lib.cpp
#             crypto_utils.cpp
#             data_buffer.cpp
#             process_parifree.cpp
#             server_socket.cpp
#             tcp_socket.cpp
#             utils.cpp            
# )
# target_include_directories(cls PUBLIC
#                           ${CMAKE_CURRENT_SOURCE_DIR}/include  
# )   

######################################
# generate the shared library from the library sources
# set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/lib) 
# add_library(cls SHARED 
#             cls_lib.cpp
#             crypto_utils.cpp
#             data_buffer.cpp
#             process_parifree.cpp
#             server_socket.cpp
#             tcp_socket.cpp
#             utils.cpp            
# )
# target_include_directories(cls PUBLIC
#                           ${CMAKE_CURRENT_SOURCE_DIR}/include  
# )   

# create an executable
link_directories(${Openssl_LIB_DIR})
link_directories(/usr/local/lib/x86_64-linux-gnu)
# link_directories(${CMAKE_CURRENT_SOURCE_DIR}/lib)

file(GLOB SOURCE_CPP *.cpp)
add_executable(Process ${SOURCE_CPP})
# add_executable(Process open_port_test.cpp)


# target_link_libraries(Process  ${CMAKE_CURRENT_SOURCE_DIR}/lib/libcls.so  ${Openssl_LIB_DIR}/libssl.a ${Openssl_LIB_DIR}/libcrypto.a pthread libjsoncpp.a dl gmp gmpxx)
target_link_libraries(Process   ${Openssl_LIB_DIR}/libssl.a ${Openssl_LIB_DIR}/libcrypto.a pthread libjsoncpp.a dl gmp gmpxx)
