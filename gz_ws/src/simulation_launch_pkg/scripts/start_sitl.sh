#!/bin/bash
LAT=$1
LON=$2
ALT=$3
HDG=$4

gnome-terminal -- bash -c '
cd ~Autonomous-Surface-Vessel-ASV-/gz_ws
source install/setup.bash
export GZ_VERSION=harmonic
export GZ_IP=127.0.0.1

sim_vehicle.py -v Rover -f rover-skid --model JSON --console --map \
  --custom-location=$1,$2,$3,$4

exec bash
' _ "$LAT" "$LON" "$ALT" "$HDG"

sleep 5

echo "[spherical] Waiting for Gazebo world '${WORLD_NAME}'..."
until gz topic -l 2>/dev/null | grep -q "/world/${WORLD_NAME}"; do
  sleep 1
done

gz service -s /world/waves/set_spherical_coordinates \
  --reqtype gz.msgs.SphericalCoordinates \
  --reptype gz.msgs.Boolean \
  --timeout 5000 \
  --req "surface_model: EARTH_WGS84,latitude_deg: ${LAT},longitude_deg: ${LON},elevation: ${ALT},heading_deg: ${HDG}"

echo "Spherical coordinates set to: lat=${LAT}, lon=${LON}, alt=${ALT}, hdg=${HDG}"