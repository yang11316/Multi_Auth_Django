cmake_minimum_required(VERSION 3.16)
project(Process)

set(CMAKE_CXX_STANDARD 11)

set(Openssl_INCLUDE_DIR /usr/local/openssl/include)
set(Openssl_LIB_DIR /usr/local/openssl/lib64)

include_directories(${Openssl_INCLUDE_DIR})

link_directories(${Openssl_LIB_DIR})

add_executable(Process test.cpp
comm_parifree.h
process_parifree.h
process_parifree.cpp
crypto_utils.h
crypto_utils.cpp
)
target_link_libraries(Process ${Openssl_LIB_DIR}/libssl.a ${Openssl_LIB_DIR}/libcrypto.a pthread dl gmp gmpxx)

# gtest 
enable_testing()
add_executable(CryptoTest crypto_test.cpp
process_parifree.h
process_parifree.cpp
crypto_utils.h
crypto_utils.cpp
)

find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})

target_link_libraries(CryptoTest ${Openssl_LIB_DIR}/libssl.a ${Openssl_LIB_DIR}/libcrypto.a pthread dl gmp gmpxx ${GTEST_LIBRARIES})
add_test(CryptoTest ${CMAKE_BINARY_DIR}/CryptoTest)

set_tests_properties(CryptoTest PROPERTIES
    ENVIRONMENT "GTEST_OUTPUT=json:${CMAKE_BINARY_DIR}/gtest_results.json"
)