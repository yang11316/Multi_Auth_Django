cmake_minimum_required(VERSION 3.16)
project(dds_test)

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
add_executable(dds_test ${SOURCE_CPP})
# add_executable(Process open_port_test.cpp)


# target_link_libraries(Process  ${CMAKE_CURRENT_SOURCE_DIR}/lib/libcls.so  ${Openssl_LIB_DIR}/libssl.a ${Openssl_LIB_DIR}/libcrypto.a pthread libjsoncpp.a dl gmp gmpxx)
target_link_libraries(dds_test  ${Openssl_LIB_DIR}/libssl.a ${Openssl_LIB_DIR}/libcrypto.a pthread libjsoncpp.a dl gmp gmpxx)





# gtest 
enable_testing()

set(gtest_headers
        include/cls_lib.h
        include/base_thread.h
        include/server_socket.h
        include/process_parifree.h
        include/tcp_socket.h
        include/crypto_utils.h
        include/common_utils.h
    )
set(gtest_cpps
        cls_lib.cpp
        base_thread.cpp
        server_socket.cpp
        process_parifree.cpp
        tcp_socket.cpp
        crypto_utils.cpp
        common_utils.cpp
        test/config.cpp
    )

add_executable(ClsLibTest test/cls_lib_test.cpp ${gtest_headers} ${gtest_cpps})
# add_executable(CryptoTest test/crypto_test.cpp ${gtest_headers} ${gtest_cpps})

find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})

target_link_libraries(ClsLibTest ${Openssl_LIB_DIR}/libssl.a ${Openssl_LIB_DIR}/libcrypto.a pthread libjsoncpp.a dl gmp gmpxx ${GTEST_LIBRARIES})
# target_link_libraries(CryptoTest ${Openssl_LIB_DIR}/libssl.a ${Openssl_LIB_DIR}/libcrypto.a pthread libjsoncpp.a dl gmp gmpxx ${GTEST_LIBRARIES})
add_test(ClsLibTest ${OUT_PATH}/ClsLibTest)
# add_test(CryptoTest ${OUT_PATH}/CryptoTest)

set_tests_properties(ClsLibTest PROPERTIES
ENVIRONMENT "GTEST_OUTPUT=json:${OUT_PATH}/cls_lib_test_results.json"
)
# set_tests_properties(CryptoTest PROPERTIES
# ENVIRONMENT "GTEST_OUTPUT=json:${OUT_PATH}/crypto_test_results.json"
# )