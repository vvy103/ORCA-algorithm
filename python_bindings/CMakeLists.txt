cmake_minimum_required(VERSION 3.12)
project(orca_python_bindings)

# Set C++ standard to match original project
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find required packages
find_package(pybind11 REQUIRED)

# Include directories
include_directories(../include)
include_directories(../src)
include_directories(../external/tinyxml2)

# Add tinyxml2 subdirectory
add_subdirectory(../external/tinyxml2 tinyxml2)

# Collect binding source files
set(BINDING_SOURCES
    main_binding.cpp
    core/geometry_bindings.cpp
    core/agent_bindings.cpp
    core/mission_bindings.cpp
)

# Use the same source files as the original project
set(ORCA_SOURCES
    ../src/agent.cpp
    ../src/xml_logger.cpp
    ../src/mission.cpp
    ../src/map.cpp
    ../src/xml_reader.cpp
    ../src/thetastar.cpp
    ../src/geom.cpp
    ../src/environment_options.cpp
    ../src/direct_planner.cpp
    ../src/orca_agent.cpp
    ../src/orca_diff_drive_agent.cpp
    ../src/agent_pnr.cpp
    ../src/sub_map.cpp
    ../src/mapf_instances_logger.cpp
    ../src/mapf/push_and_rotate.cpp
    ../src/mapf/mapf_actor_set.cpp
    ../src/mapf/mapf_actor.cpp
    ../src/mapf/isearch.cpp
    ../src/mapf/astar.cpp
    ../src/mapf/search_queue.cpp
    ../src/mapf/constraints.cpp
    ../src/mapf/conflict_avoidance_table.cpp
    ../src/mapf/cbs.cpp
    ../src/mapf/conflict_set.cpp
    ../src/mapf/mdd.cpp
    ../src/mapf/focal_search.cpp
    ../src/mapf/scipp.cpp
    ../src/mapf/sipp.cpp
    ../src/agent_pnr_ecbs.cpp
    ../src/agent_returning.cpp
)

# Create the Python module
pybind11_add_module(orca_core ${BINDING_SOURCES} ${ORCA_SOURCES})

# Add compile definitions to match original project
target_compile_definitions(orca_core PRIVATE 
    FULL_OUTPUT=true
    FULL_LOG=true
    MAPF_LOG=false
)

# Set properties
set_target_properties(orca_core PROPERTIES
    CXX_VISIBILITY_PRESET "hidden"
    VISIBILITY_INLINES_HIDDEN YES
)

# Link tinyxml2
target_link_libraries(orca_core PRIVATE tinyxml2)

# Installation
install(TARGETS orca_core DESTINATION .)