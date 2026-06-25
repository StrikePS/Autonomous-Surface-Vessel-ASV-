# Autonomous Surface Vessel (ASV) Simulation Stack

- **Author:** Pranjal Sinha, IIT Kharagpur
- **Mentor:** Prof. Jagadeesh Kadiyam, IIT Kharagpur
- **Department:** Ocean Engineering and Naval Architecture

---

A complete simulation environment for Autonomous Surface Vessels (ASVs), integrating Gazebo Harmonic wave physics, ArduPilot SITL, ROS 2 Humble, MAVProxy, and a custom 9-state EKF for state estimation. The stack supports both the open-source BlueBoat model and a custom IIT Kharagpur catamaran replica built from physical measurements and CAD.

You can read the entire setup steps in the 'Comprehensive Simulation Setup" document as well.

---

## Table of Contents

- [Overview](#overview)
- [System Requirements](#system-requirements)
- [Repository Structure](#repository-structure)
- [Setup Guide](#setup-guide)
  - [1. OS — Ubuntu 22.04 LTS (Dual Boot)](#1-os--ubuntu-2204-lts-dual-boot)
  - [2. Programming Languages](#2-programming-languages)
  - [3. Git and SSH](#3-git-and-ssh)
  - [4. ROS 2 Humble](#4-ros-2-humble)
  - [5. Gazebo Harmonic](#5-gazebo-harmonic)
  - [6. ArduPilot and SITL](#6-ardupilot-and-sitl)
  - [7. MAVProxy](#7-mavproxy)
  - [8. Clone and Build the Workspace](#8-clone-and-build-the-workspace)
- [Running the Simulation](#running-the-simulation)
- [Workspace Architecture](#workspace-architecture)
- [Models](#models)
- [EKF State Estimation](#ekf-state-estimation)
- [Future Work](#future-work)
- [Credits](#credits)

---

## Overview

This stack simulates an ASV operating in a wave environment. The key components are:

| Component | Role |
|-----------|------|
| **Gazebo Harmonic (gz sim 8)** | 3D simulation world with wave physics (FFT + CGAL) |
| **asv_wave_sim** | Ocean surface rendering and hydrodynamics |
| **ArduPilot SITL (JSON mode)** | Vehicle firmware running as a native desktop process |
| **MAVProxy** | Ground control station and telemetry routing over UDP |
| **ROS 2 Humble** | Package build system, node orchestration, and inter-process communication |
| **GzSim_StateEstimate** | Custom 9-state EKF for ASV localization |
| **Custom ROS-GZ Bridge** | Version-safe bridge between Gazebo topics and ROS 2 |

---

## System Requirements

- **OS:** Ubuntu 22.04 LTS (Jammy Jellyfish) — native dual boot strongly preferred
- **Storage:** Minimum 90 GB allocated to the Linux partition
- **RAM:** 8 GB minimum, 16 GB recommended
- **CPU:** Multi-core (build uses `--parallel-workers 2`)
- **GPU:** Any — Gazebo uses OgreNext for rendering

> **Why Ubuntu 22.04 specifically?** Gazebo Harmonic, ROS 2 Humble, and all plugin dependencies are pinned to this distro. Using any other version will produce build errors.

---

## Repository Structure

```
Autonomous-Surface-Vessel-ASV-/
├── gz_ws/                          # Main Gazebo + ROS 2 workspace
│   └── src/
│       ├── asv_wave_sim/           # Ocean wave simulation (FFT/CGAL)
│       │   └── gz-waves-models/
│       │       ├── worlds/         # waves.sdf world file
│       │       └── world_models/   # waves, regular_waves, ocean_waves
│       ├── ardupilot_gazebo/       # ArduPilot Gazebo plugin (cloned during setup)
│       ├── wave_sim_bridgeup/      # Custom ROS-GZ bridge
│       │   └── src/custom_bridge.cpp
│       ├── simulation_launch_pkg/  # Launch files and startup scripts
│       │   ├── launch/boat_simulation_launch.py
│       │   └── scripts/
│       │       ├── start_gazebo_wave_sim.sh
│       │       └── start_sitl.sh
│       └── asv_localization/       # EKF state estimator
│           └── asv_localization/GzSim_StateEstimate.py
├── SITL_Models/
│   └── Gazebo/
|       └── models/
│           ├── /blueboat           # BlueBoat base model (.sdf, .dae, .stl)
│           └── /newmodel           # IIT KGP catamaran (.sdf, .dae, .stl)
└── ASV_CAD/
    └── Catamaran_v1/               # Fusion360 CAD files (bare hull + joined hull)
```

---

## Setup Guide

### 1. OS — Ubuntu 22.04 LTS (Dual Boot)

**Partition your drive (Windows):**

```
Win + R → diskmgmt.msc → Right-click D: drive → Shrink Volume → 91000 MB
```

**Create a bootable USB:**

1. Download the Ubuntu 22.04 Desktop ISO from [releases.ubuntu.com/jammy](https://releases.ubuntu.com/jammy/)
2. Install [Rufus](https://rufus.ie/en/) (match your CPU architecture: x64, x86, or ARM64)
3. Flash the ISO to a 16 GB+ USB drive via Rufus

Boot into the USB from BIOS, install Ubuntu alongside Windows, and select the unallocated partition created above.

> If Ubuntu 22.04 has driver issues on your hardware, try WSL2 (Windows Subsystem for Linux) as a fallback — a WSL setup guide may be added to this documentation in the future.

---

### 2. Programming Languages

```bash
# C++ compiler
sudo apt install build-essential
g++ --version

# Python 3
sudo apt install python3-pip python3-venv
python3 --version
```

---

### 3. Git and SSH

```bash
sudo apt update && sudo apt install git
git --version
```

Create a GitHub account at [github.com](https://github.com), then set up SSH key authentication by following the official guide: [Connecting to GitHub with SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

Verify the connection:

```bash
ssh -T git@github.com
# Expected: Hi <username>! You've successfully authenticated...
```

> **Note:** Turn off any VPN before using Git. VPNs interfere with SSH network protocols.

---

### 4. ROS 2 Humble

Follow the official installation guide: [ROS 2 Humble — Ubuntu Install](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)

Key resources:
- [ROS 2 Humble Tutorials](https://docs.ros.org/en/humble/Tutorials.html)
- [ROS 2 Humble Concepts](https://docs.ros.org/en/humble/Concepts.html)

---

### 5. Gazebo Harmonic

First, remove any existing Gazebo installations to prevent version conflicts:

```bash
dpkg -l | grep -i gazebo
dpkg -l | grep -i ignition
dpkg -l | grep -i gz-

sudo apt remove --purge '.*gazebo.*'
sudo apt autoremove
sudo apt remove --purge '.*ignition.*'
sudo apt remove --purge 'gz-*'
sudo apt autoremove
sudo apt remove --purge ros-humble-gazebo-ros-pkgs ros-humble-gazebo-ros
sudo apt autoremove
sudo apt clean
```

Install Gazebo Harmonic:

```bash
sudo apt-get install gz-harmonic
gz sim --version
# Expected: Gazebo Sim, version 8.x.x
```

---

### 6. ArduPilot and SITL

```bash
# Clone ArduPilot
git clone --recurse-submodules https://github.com/ArduPilot/ardupilot.git
cd ardupilot

# Install dependencies
Tools/environment_install/install-prereqs-ubuntu.sh -y

# Reload profile
. ~/.profile

# Test the build
cd ~/ardupilot/ArduCopter
sim_vehicle.py -w
```

Install ArduPilot Gazebo plugin dependencies (the plugin itself is built from this repo):

```bash
sudo apt update
sudo apt install libgz-sim8-dev rapidjson-dev
sudo apt install libopencv-dev gstreamer1.0-dev \
  libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-bad \
  gstreamer1.0-libav gstreamer1.0-gl
```

---

### 7. MAVProxy

```bash
pip3 install MAVProxy
mavproxy.py --version
```

---

### 8. Clone and Build the Workspace

```bash
cd ~/
git clone git@github.com:StrikePS/Autonomous-Surface-Vessel-ASV-.git
```

**A. Build the ArduPilot Gazebo Plugin:**

```bash
cd ~/Autonomous-Surface-Vessel-ASV-/gz_ws/src
git clone https://github.com/ArduPilot/ardupilot_gazebo
export GZ_VERSION=harmonic

cd ~/Autonomous-Surface-Vessel-ASV-/gz_ws/src/ardupilot_gazebo
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo
make -j4

# Verify the plugin .so file was built
find / -name "libArduPilotPlugin.so" 2>/dev/null
```

**B. Build the Wave Simulation Workspace:**

```bash
source /opt/ros/humble/setup.bash

cd ~/Autonomous-Surface-Vessel-ASV-/gz_ws
export GZ_VERSION=harmonic
colcon build --merge-install --cmake-args \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DBUILD_TESTING=ON \
  -DCMAKE_CXX_STANDARD=17 \
  --event-handlers console_direct+ \
  --executor sequential --parallel-workers 2
source ./install/setup.bash

# Build the waves control GUI plugin
cd ~/Autonomous-Surface-Vessel-ASV-/gz_ws/src/asv_wave_sim/gz-waves/src/gui/plugins/waves_control
mkdir build && cd build
cmake -Wno-dev .. && make
```

> **Expected warnings (harmless):** A `CMAKE_CXX_STANDARD` warning from the pure-Python launch package, and a `CGAL_DATA_DIR` warning from gz-waves — neither affects the build.

---

## Running the Simulation

```bash
# Source ROS 2 and the workspace
source /opt/ros/humble/setup.bash
cd ~/Autonomous-Surface-Vessel-ASV-/gz_ws
source install/setup.bash

# Launch everything
ros2 launch simulation_launch_pkg boat_simulation_launch.py
```

This single launch command starts:
- Gazebo Harmonic with the wave world
- ArduPilot SITL (JSON mode, Rover/skid-steer frame)
- MAVProxy console and map
- The custom ROS-GZ bridge
- The EKF state estimator node

**After making any code changes, always rebuild before running:**

```bash
cd ~/Autonomous-Surface-Vessel-ASV-/gz_ws
colcon build --merge-install
source install/setup.bash
ros2 launch simulation_launch_pkg boat_simulation_launch.py
```

---

## Workspace Architecture

### `waves.sdf` — World File

Located at `gz_ws/src/asv_wave_sim/gz-waves-models/worlds/waves.sdf`

Key plugins loaded:

| Plugin | Purpose |
|--------|---------|
| `gz-sim-physics-system` | FFT-based force, damping, and collision calculation |
| `gz-sim-scene-broadcaster-system` | CGAL + FFT wave surface rendering |
| `gz-sim-imu-system` / `gz-sim-navsat-system` | Sensor data relay as Gazebo topics |

The world includes the `waves` surface model and the vessel model (BlueBoat or catamaran) via `<include><uri>` tags. Model directories must be exported via `GZ_SIM_RESOURCE_PATH` in `start_gazebo_wave_sim.sh`.

### `start_gazebo_wave_sim.sh`

Sets all required environment exports:

```bash
export GZ_VERSION=harmonic
export GZ_IP=127.0.0.1   # Must match ArduPilot SITL ↔ MAVProxy UDP IP
export GZ_SIM_RESOURCE_PATH="<path>/gz-waves-models/models:\
<path>/gz-waves-models/world_models:\
<path>/gz-waves-models/worlds:\
<path>/SITL_Models/Gazebo/models:$GZ_SIM_RESOURCE_PATH"
```

### `start_sitl.sh`

Starts MAVProxy at the configured GPS coordinates and injects spherical coordinates into the Gazebo world so that sensor GPS data is aligned with the map view:

```bash
sim_vehicle.py -v Rover -f rover-skid --model JSON --console --map \
  --custom-location=$LAT,$LON,$ALT,$HDG

gz service -s /world/waves/set_spherical_coordinates ...
```

### `boat_simulation_launch.py`

Orchestrates all nodes and scripts in the correct order. Default spawn coordinates (IIT Kharagpur):

```python
lat_arg = DeclareLaunchArgument('lat', default_value='22.317677')
lon_arg = DeclareLaunchArgument('lon', default_value='87.301955')
alt_arg = DeclareLaunchArgument('alt', default_value='0.0')
hdg_arg = DeclareLaunchArgument('hdg', default_value='0')
```

---

## Models

### BlueBoat

Located at `SITL_Models/Gazebo/models/blueboat/`

An open-source model from [ArduPilot/SITL_Models](https://github.com/ArduPilot/SITL_Models), modified for this stack. Includes hydrodynamic plugin parameters, IMU and GPS sensor links with Gaussian noise, and dual thruster definitions for skid-steer control.

### IIT KGP Catamaran

Located at `Custom_Models/Gazebo/models/newmodel/`

A custom model built from physical measurements of the catamaran at the Department of Ocean Engineering and Naval Architecture, IIT Kharagpur. Workflow: physical measurements → Fusion360 CAD → `.stl` export → Blender 3.0 `.dae` conversion → `model.sdf` authored using BlueBoat as a base. CAD files (bare hull and joined hull) are in `ASV_CAD/Catamaran_v1/`.

---

## EKF State Estimation

A 9-state Extended Kalman Filter is implemented in:

```
gz_ws/src/asv_localization/asv_localization/GzSim_StateEstimate.py
```

The EKF fuses IMU and GPS data from Gazebo sensor topics and outputs a relative Cartesian pose from the initial spawn position.

To monitor the EKF output in a new terminal:

```bash
cd ~/Autonomous-Surface-Vessel-ASV-/gz_ws
source install/setup.bash
ros2 run asv_localization echo_state_estimate
```

---

## Future Work

- WSL2 setup guide for users unable to dual boot
- BIOS configuration and Ubuntu installer walkthrough (to complete the installation section)
- Wave parameter tuning guide (`waves/`, `regular_waves/`, `ocean_waves/` world models)
- Wave-making render and hydrodynamic interaction for accurate seakeeping response
- Navigation stack integration (path planning, waypoint following)
- QGroundControl (QGC) integration as an alternative to MAVProxy `--map`
- Custom control algorithms on top of ArduPilot SITL

---

## Credits

- **[asv_wave_sim](https://github.com/srmainwaring/asv_wave_sim)** by srmainwaring — ocean wave world, FFT/CGAL hydrodynamics
- **[SITL_Models](https://github.com/ArduPilot/SITL_Models)** by ArduPilot — BlueBoat base model and SITL plugin configuration
- **[ardupilot_gazebo](https://github.com/ArduPilot/ardupilot_gazebo)** by ArduPilot — Gazebo plugin for ArduPilot SITL integration
- **Department of Ocean Engineering and Naval Architecture, IIT Kharagpur** — physical catamaran model and CAD
