#!/bin/bash

gnome-terminal -- bash -c '
cd "$1/Autonomous-Surface-Vessel-ASV-/gz_ws" || exit 1

source install/setup.bash

export GZ_VERSION=harmonic
export GZ_IP=127.0.0.1

export GZ_SIM_SYSTEM_PLUGIN_PATH="$1/Autonomous-Surface-Vessel-ASV-/gz_ws/install/lib:$GZ_SIM_SYSTEM_PLUGIN_PATH"
export GZ_SIM_SYSTEM_PLUGIN_PATH="$1/Autonomous-Surface-Vessel-ASV-/gz_ws/src/ardupilot_gazebo/build:$GZ_SIM_SYSTEM_PLUGIN_PATH"

export GZ_SIM_RESOURCE_PATH="$1/Autonomous-Surface-Vessel-ASV-/gz_ws/src/ardupilot_gazebo/models:$1/Autonomous-Surface-Vessel-ASV-/gz_ws/src/ardupilot_gazebo/worlds:$GZ_SIM_RESOURCE_PATH"

export GZ_GUI_PLUGIN_PATH="$GZ_GUI_PLUGIN_PATH:$1/Autonomous-Surface-Vessel-ASV-/gz_ws/src/asv_wave_sim/gz-waves/src/gui/plugins/waves_control/build"

export GZ_SIM_RESOURCE_PATH="$1/Autonomous-Surface-Vessel-ASV-/gz_ws/src/asv_wave_sim/gz-waves-models/models:\
$1/Autonomous-Surface-Vessel-ASV-/gz_ws/src/asv_wave_sim/gz-waves-models/world_models:\
$1/Autonomous-Surface-Vessel-ASV-/gz_ws/src/asv_wave_sim/gz-waves-models/worlds:\
$1/Autonomous-Surface-Vessel-ASV-/SITL_Models/Gazebo/models:\
$GZ_SIM_RESOURCE_PATH"

gz sim -v4 -r waves.sdf
' _ "$HOME"