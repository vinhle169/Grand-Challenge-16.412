#! /usr/bin/env bash

# the following variable will only be set by AWS RoboMaker, when run in AWS RoboMaker
# AWS_ROBOMAKER_WORLDFORGE_WORLD_OVERRIDE
# AWS_ROBOMAKER_WORLDFORGE_SETUP_OVERRIDE

REMOVE_CURRENT_WORLDFORGE_PKG_PATH=$(cat <<EOF
from __future__ import print_function
import os
ros_pkg_path = os.getenv("ROS_PACKAGE_PATH", "")
if  not "@(CMAKE_SOURCE_DIR)".startswith(os.path.abspath(os.getenv("AWS_ROBOMAKER_WORLDFORGE_WORLD_PACKAGE_OVERRIDE"))+os.sep):
    prioritized_pkg_paths = []
    secondary_pkg_paths = []
    for pkg_path in ros_pkg_path.split(":"):
        if not pkg_path.startswith(os.path.abspath("@(CMAKE_INSTALL_PREFIX)")+os.sep):
            prioritized_pkg_paths.append(pkg_path)
        else:
            secondary_pkg_paths.append(pkg_path)
    ros_pkg_path = os.pathsep.join(prioritized_pkg_paths + secondary_pkg_paths)
print(ros_pkg_path)
EOF
)

if [ -n "${AWS_ROBOMAKER_WORLDFORGE_WORLD_PACKAGE_OVERRIDE}" ]; then
    export ROS_PACKAGE_PATH
    ROS_PACKAGE_PATH="`@(PYTHON_EXECUTABLE) -c \"$REMOVE_CURRENT_WORLDFORGE_PKG_PATH\"`"
fi