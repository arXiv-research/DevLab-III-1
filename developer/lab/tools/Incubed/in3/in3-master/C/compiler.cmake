if(MSVC)
  set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fPIC -Wall -funsigned-char -std=c99")
  set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC -Wall -funsigned-char  -std=c99 -D__FILENAME__=none")
else(MSVC)
  set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fPIC -Wall -funsigned-char -Wextra -std=c99")
  if (NOT DEFINED ANDROID_ABI AND NOT ${CMAKE_GENERATOR} MATCHES "Ninja")
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC -Wall -funsigned-char -Wextra  -std=c99 -D__FILENAME__='\"$(subst ${CMAKE_SOURCE_DIR}/,,$(abspath $<))\"'")
  else()
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC -Wall -funsigned-char -Wextra  -std=c99 -D__FILENAME__=none")
  endif()
endif(MSVC)
if (WASM)
  set (CMAKE_C_FLAGS "-Wall -funsigned-char -Wextra -std=c99 ")
  set (CMAKE_CXX_FLAGS "-Wall -funsigned-char -Wextra  -std=c99 -D__FILENAME__='\"$(subst ${CMAKE_SOURCE_DIR}/,,$(abspath $<))\"'")
  if (CMAKE_BUILD_TYPE MATCHES Debug)
    set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fsanitize=undefined,address -fsanitize-minimal-runtime")
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=undefined,address -fsanitize-minimal-runtime")
  endif()
else (WASM)
  set(CMAKE_POSITION_INDEPENDENT_CODE ON)
endif(WASM)

if(MSVC)
  set (CMAKE_C_FLAGS "${CMAKE_CXX_FLAGS} /W4 /WX")
elseif(WASM)
  set (CMAKE_C_FLAGS "${CMAKE_CXX_FLAGS} -Werror -Wno-missing-braces")
else()
  set (CMAKE_C_FLAGS "${CMAKE_CXX_FLAGS} -Werror=vla -Wno-missing-braces")
endif()

set_property(GLOBAL PROPERTY C_STANDARD 99)

# Set DEAD_STRIP_LINKER_OPT
if(NOT CYGWIN AND NOT MINGW)
  if(NOT ${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    SET(CMAKE_CXX_FLAGS
            "${CMAKE_CXX_FLAGS}  -ffunction-sections -fdata-sections")
  endif()
endif()
if(NOT LLVM_NO_DEAD_STRIP)
  if(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    set_property(GLOBAL PROPERTY DEAD_STRIP_LINKER_OPT "-Wl,-dead_strip")
  elseif(WASM)
    set_property(GLOBAL PROPERTY DEAD_STRIP_LINKER_OPT "")
  elseif(NOT WIN32)
    set_property(GLOBAL PROPERTY DEAD_STRIP_LINKER_OPT "-Wl,--gc-sections")
  endif()
endif()

# Only CMake >=3.13 has add_link_options(). For previous versions,
# DEAD_STRIP_LINKER_OPT can be used with target_link_libraries()
if(${CMAKE_VERSION} VERSION_GREATER "3.12.4")
  get_property(DEAD_STRIP_LINKER_OPT GLOBAL PROPERTY DEAD_STRIP_LINKER_OPT)
  add_link_options(${DEAD_STRIP_LINKER_OPT})
  set_property(GLOBAL PROPERTY DEAD_STRIP_LINKER_OPT "")
endif()

if (CODE_COVERAGE)
  add_compile_options(-fprofile-instr-generate -fcoverage-mapping)
  set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fprofile-instr-generate -fcoverage-mapping")
  set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fprofile-instr-generate -fcoverage-mapping")
  set (LDFLAGS "${LDFLAGS} -fprofile-instr-generate -fcoverage-mapping")
  set (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -fprofile-instr-generate -fcoverage-mapping")
endif()

