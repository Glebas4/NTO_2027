#!/bin/sh

CNT=1

check() {
    STATUS=$?

    if [ "$STATUS" -eq 0 ]; then
        echo "Step $CNT done"
    else
        echo "ERROR at step $CNT: code $STATUS"
    fi

    CNT=$((CNT + 1))
}

echo "Setup started"
cd /home/pi/NTO_2027/files/others

echo "[1] cp aruco_map.png model.sdf /home/pi/clover2-dev/src/clover2-sim/clover2_gz_sim/models/aruco_plane"
cp aruco_map.png model.sdf /home/pi/clover2-dev/src/clover2-sim/clover2_gz_sim/models/aruco_plane
check

echo "[2] cp clover2_aruco.sdf /home/pi/clover2-dev/src/clover2-sim/clover2_gz_sim/worlds"
cp clover2_aruco.sdf /home/pi/clover2-dev/src/clover2-sim/clover2_gz_sim/worlds
check

echo "[3] cp simulation.yaml /home/pi/clover2-dev/install/clover2_map/share/clover2_map/map"
cp simulation.yaml /home/pi/clover2-dev/install/clover2_map/share/clover2_map/map
check



cd /home/pi/NTO_2027/files
echo "[4] cp -r lep_model isol_black isol_brown isol_red /home/pi/clover2-dev/src/clover2-sim/clover2_gz_sim/models"
cp -r lep_model isol_black isol_brown isol_red /home/pi/clover2-dev/src/clover2-sim/clover2_gz_sim/models
check


echo "[5] Building"
cd ~/clover2-dev
colcon build --symlink-install
check

cd /home/pi/NTO_2027/files/others
echo '[6] cp gz_simple.launch.py /home/pi/clover2-dev/install/clover2_sim/share/clover2_sim/launch'
cp gz_simple.launch.py /home/pi/clover2-dev/install/clover2_sim/share/clover2_sim/launch
check

echo '[7] cp spawn.launch.py /home/pi/clover2-dev/install/clover2_sim/share/clover2_sim/launch'
cp spawn.launch.py /home/pi/clover2-dev/install/clover2_sim/share/clover2_sim/launch
check

echo "Setup done"
