import os
import sys
from pybind11.setup_helpers import Pybind11Extension, build_ext
import pybind11
from setuptools import setup

# Define source files
binding_sources = [
    "main_binding.cpp",
    "core/geometry_bindings.cpp", 
    "core/agent_bindings.cpp",
    "core/mission_bindings.cpp"
]

# ORCA source files (matching CMakeLists.txt)
orca_sources = [
    "../src/agent.cpp",
    "../src/xml_logger.cpp", 
    "../src/mission.cpp",
    "../src/map.cpp",
    "../src/xml_reader.cpp",
    "../src/thetastar.cpp",
    "../src/geom.cpp",
    "../src/environment_options.cpp",
    "../src/direct_planner.cpp",
    "../src/orca_agent.cpp",
    "../src/orca_diff_drive_agent.cpp",
    "../src/agent_pnr.cpp",
    "../src/sub_map.cpp",
    "../src/mapf_instances_logger.cpp",
    "../src/mapf/push_and_rotate.cpp",
    "../src/mapf/mapf_actor_set.cpp",
    "../src/mapf/mapf_actor.cpp",
    "../src/mapf/isearch.cpp",
    "../src/mapf/astar.cpp",
    "../src/mapf/search_queue.cpp",
    "../src/mapf/constraints.cpp",
    "../src/mapf/conflict_avoidance_table.cpp",
    "../src/mapf/cbs.cpp",
    "../src/mapf/conflict_set.cpp",
    "../src/mapf/mdd.cpp",
    "../src/mapf/focal_search.cpp",
    "../src/mapf/scipp.cpp",
    "../src/mapf/sipp.cpp",
    "../src/agent_pnr_ecbs.cpp",
    "../src/agent_returning.cpp"
]

# Combine all sources
all_sources = binding_sources + orca_sources

# Define the extension module
ext_modules = [
    Pybind11Extension(
        "orca_core",
        sources=all_sources,
        include_dirs=[
            "../include",
            "../src", 
            "../external/tinyxml2",
            pybind11.get_include()
        ],
        language='c++',
        cxx_std=14,  # Match original project
        define_macros=[
            ("FULL_OUTPUT", "true"),
            ("FULL_LOG", "true"), 
            ("MAPF_LOG", "false")
        ]
    ),
]

setup(
    name="orca-algorithm",
    version="0.1.0",
    author="ORCA Python Bindings",
    description="Python bindings for ORCA multi-agent pathfinding algorithm",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=[
        "pybind11>=2.6.0",
    ],
)