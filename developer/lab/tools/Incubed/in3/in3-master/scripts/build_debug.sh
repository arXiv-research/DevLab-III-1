#!/bin/sh
cd ..
mkdir -p build
cd build
rm -rf *
export CTEST_OUTPUT_ON_FAILURE=1
cp ../scripts/cmake_modules/CMakeGraphVizOptions.cmake .
cmake --graphviz=in3.dot  -DCMAKE_EXPORT_COMPILE_COMMANDS=true -DUSE_CURL=true -DCURL_BLOCKING=false -DIN3_LIB=true -DTEST=true -DUSE_SEGGER_RTT=false -DBUILD_DOC=true -DJAVA=true -DCMAKE_BUILD_TYPE=Debug .. 
#dot -Tsvg -o in3.svg in3.dot 
make -j8
#cmake -DTEST=true -DEVM_GAS=true -DCMAKE_BUILD_TYPE=Debug .. && make && make test
#cmake -GNinja -DTEST=true -DCMAKE_BUILD_TYPE=Debug .. && ninja && ninja test
#cmake -DTEST=true -DEVM_GAS=true -GNinja -DCMAKE_BUILD_TYPE=Release .. && ninja
cd ../scripts
