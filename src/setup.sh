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
cd /home/pi/NTO_2027/files

echo "[1] mv aruco_map.png model.sdf /home/pi/clover2-dev/src/clover2-sim/clover2_gz_sim/models/aruco_plane"
cp aruco_map.png model.sdf /home/pi/clover2-dev/src/clover2-sim/clover2_gz_sim/models/aruco_plane
check

echo "[2] mv clover2_aruco.sdf /home/pi/clover2-dev/src/clover2-sim/clover2_gz_sim/worlds"
cp clover2_aruco.sdf /home/pi/clover2-dev/src/clover2-sim/clover2_gz_sim/worlds
check

echo "[3] mv simulation.yaml /home/pi/clover2-dev/install/clover2_map/share/clover2_map/map"
cp simulation.yaml /home/pi/clover2-dev/install/clover2_map/share/clover2_map/map
check

#cd /home/pi/NTO_2027/files
#echo "[4] mv launcher_config.yaml /home/pi/clover2-dev/src/clover2/tooling/assets/klever5"
#mv launcher_config.yaml /home/pi/clover2-dev/src/clover2/tooling/assets/klever5
#check

#echo "[5] Building"
#cd ~/clover2-dev
#colcon build --symlink-install
#check


#cd /home/pi/NTO_2027
#rm -rf files

echo "Setup done"
